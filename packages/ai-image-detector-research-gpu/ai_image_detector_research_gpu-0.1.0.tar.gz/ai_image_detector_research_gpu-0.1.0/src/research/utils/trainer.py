import torch
import os
from typing import NamedTuple
from numpy import ndarray
from torch import nn, optim
from torch.utils.data import DataLoader
from .dataset import MergeDataset
from sklearn.metrics import confusion_matrix
from tqdm import tqdm


EpochResult = NamedTuple(
    "EpochResult",
    [
        ("train_loss", float),
        ("train_accuracy", float),
        ("train_cm", ndarray),
        ("val_loss", float),
        ("val_accuracy", float),
        ("val_cm", ndarray),
    ],
)


class Trainer:
    def __init__(
        self,
        model: nn.Module,
        dataset: MergeDataset,
        checkpoint_dir: str,
        optimizer: optim.Optimizer | None = None,
        lr: float = 0.001,
        epochs: int = 10,
        batch_size: int = 32,
        criterion: nn.Module = nn.BCEWithLogitsLoss(),
        device: str = "cpu",
        weight_decay: float = 0.0,
    ):
        """Инициализация тренера для обучения модели на заданном датасете.

        Args:
            model (nn.Module): Модель для обучения.
            dataset (MergeDataset): Датасет, содержащий train и val наборы данных.
            optimizer (optim.Optimizer | None, optional): Оптимизатор для обучения модели. Если не указан, используется Adam с lr. Defaults to None.
            lr (float, optional): Начальная скорость обучения. Defaults to 0.001.
            epochs (int, optional): Количество эпох для обучения. Defaults to 10.
            batch_size (int, optional): Размер батча для загрузки данных. Defaults to 32.
            criterion (nn.Module, optional): Функция потерь для обучения модели. Defaults to nn.CrossEntropyLoss().
            device (str, optional): Устройство для обучения модели (например, "cpu" или "cuda"). Defaults to "cpu".
        """
        self.model = model.to(device)
        self.train_loader = DataLoader(
            dataset.train_dataset, batch_size=batch_size, shuffle=True
        )
        self.val_loader = DataLoader(
            dataset.val_dataset, batch_size=batch_size, shuffle=False
        )

        self.optimizer = optimizer or optim.Adam(
            self.model.parameters(), lr=lr, weight_decay=weight_decay
        )
        self.criterion = criterion
        self.epochs = epochs
        self.device = device
        self.checkpoint_dir = checkpoint_dir
        self.result: list[EpochResult] = []
        self.current_epoch = 0
        self.load_checkpoint()

    def __call__(self) -> list[EpochResult]:
        """Запуск обучения модели на заданном датасете.

        Returns:
            list[EpochResult]: Список результатов по эпохам, содержащий потери, точность и матрицу ошибок
                на train и val наборах данных.
        """

        for self.current_epoch in range(self.current_epoch, self.epochs):
            train_loss, train_accuracy, train_cm = self._run_epoch(False)
            val_loss, val_accuracy, val_cm = self._run_epoch(True)

            self.result.append(
                EpochResult(
                    train_loss=train_loss,
                    train_accuracy=train_accuracy,
                    train_cm=train_cm,
                    val_loss=val_loss,
                    val_accuracy=val_accuracy,
                    val_cm=val_cm,
                )
            )

            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

            print(
                f"Epoch {self.current_epoch + 1}/{self.epochs} - "
                f"Train Loss: {train_loss:.4f}, "
                f"Train Accuracy: {train_accuracy:.4f}, "
                f"Val Loss: {val_loss:.4f}, "
                f"Val Accuracy: {val_accuracy:.4f}"
            )

            self.create_checkpoint()

        return self.result

    def _run_epoch(self, validate: bool) -> tuple[float, float, ndarray]:
        """Выполнение одной эпохи обучения или валидации модели.

        Args:
            validate (bool): Если True, выполняется валидация модели, иначе обучение.

        Returns:
            tuple[float, float]: Кортеж, содержащий среднюю потерю, точность модели на текущей эпохе и матрицу ошибок (confusion matrix)
        """
        if validate:
            self.model.eval()
        else:
            self.model.train()

        total_loss = 0.0
        correct = 0.0
        total = 0

        data_loader = self.val_loader if validate else self.train_loader

        all_preds: list[ndarray] = []
        all_targets: list[ndarray] = []

        for batch_x, batch_y in tqdm(data_loader):
            inputs: torch.Tensor = batch_x.to(self.device)
            targets: torch.Tensor = batch_y.to(self.device).view(-1, 1).float()

            if validate:
                with torch.no_grad():
                    logits: torch.Tensor = self.model(inputs)
                    loss: torch.Tensor = self.criterion(logits, targets)
            else:
                self.optimizer.zero_grad()
                logits = self.model(inputs)
                loss = self.criterion(logits, targets)
                loss.backward()
                self.optimizer.step()

            total_loss += loss.item()
            pred = (logits > 0).int()
            correct += pred.eq(targets.view_as(pred)).sum().item()
            total += targets.size(0)

            all_preds.extend(pred.cpu().numpy())
            all_targets.extend(targets.cpu().numpy())

        return (
            total_loss / len(data_loader),
            correct / total,
            confusion_matrix(all_targets, all_preds),
        )

    def create_checkpoint(self) -> None:
        """Сохранение текущего состояния модели и оптимизатора."""
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        model_path = os.path.join(self.checkpoint_dir, "checkpoint.pth")
        torch.save(
            {
                "model_state_dict": self.model.state_dict(),
                "optimizer_state_dict": self.optimizer.state_dict(),
                "result": self.result,
                "epochs": self.current_epoch,
            },
            model_path,
        )
        print(f"Model checkpoint saved to {model_path}")

    def load_checkpoint(self) -> None:
        """Загрузка модели из сохраненного состояния."""
        model_path = os.path.join(self.checkpoint_dir, "checkpoint.pth")
        if os.path.exists(model_path):
            checkpoint = torch.load(
                model_path, map_location=self.device, weights_only=False
            )
            self.model.load_state_dict(checkpoint["model_state_dict"])
            self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
            self.result = checkpoint["result"]
            self.current_epoch = checkpoint["epochs"]
            print(f"Model loaded from {model_path}")
        else:
            print(f"No saved model found at {model_path}")
