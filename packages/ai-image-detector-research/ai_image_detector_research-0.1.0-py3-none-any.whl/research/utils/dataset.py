from torchvision.datasets import VisionDataset
from torchvision.transforms import transforms
import kagglehub
import os
import pandas as pd
from PIL import Image
from .config import Config
import kagglehub.config
from typing import NamedTuple


MergeDataset = NamedTuple(
    "MergeDataset",
    [
        ("train_dataset", VisionDataset),
        ("val_dataset", VisionDataset),
    ],
)


class ArtiFactDataset(VisionDataset):
    """Класс для работы с датасетом ArtiFact (awsaf49/artifact-dataset),
    содержащим реальные и сгенерированные изображения."""

    @classmethod
    def get_merged_dataset(
        cls, size: int = 100_000, images_ratio: float = 0.5, ratio: float = 0.5
    ) -> MergeDataset:
        """Получает датасет для обучения и валидации, состоящий из реальных и сгенерированных изображений.

        Args:
            size (int, optional): Суммарное количество изображений в датасете. Defaults to 100_000.
            images_ratio (float, optional): Распределение реальных и сгенерированных изображений в датасете.
                Если images_ratio = 0.5, то в датасете будет 50% реальных и 50% сгенерированных изображений.
                Если images_ratio = 0.7, то в датасете будет 70% реальных и 30% сгенерированных изображений.
                Defaults to 0.5.
            ratio (float, optional): Соотношение между train и val датасетами.
                Если ratio = 0.5, то в train и val датасетах будет по 50% изображений.
                Если ratio = 0.7, то в train датасете будет 70% изображений, а в val - 30%.
                Defaults to 0.5.

        Returns:
            MergeDataset: Кортеж из train и val датасетов, содержащих изображения и их метки.
        """
        train_size = int(size * ratio)
        val_size = size - train_size

        train_dataset = cls(
            transform=transforms.Compose(
                [
                    transforms.Resize((256, 256)),
                    transforms.ToTensor(),
                    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                ]
            ),
            images_count=train_size,
            ratio=images_ratio,
            start_index=0,
        )
        val_dataset = cls(
            transform=transforms.Compose(
                [
                    transforms.Resize((256, 256)),
                    transforms.ToTensor(),
                    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
                ]
            ),
            images_count=val_size,
            ratio=images_ratio,
            start_index=train_size,
        )

        return MergeDataset(train_dataset, val_dataset)

    def __init__(
        self,
        transform=None,
        images_count: int = 100_000,
        ratio: float = 0.5,
        start_index: int = 0,
    ) -> None:
        """_summary_

        Args:
            transform (_type_, optional): Трансформации, применяемые к изображениям. Defaults to None.
            images_count (int, optional): Количество изображений в датасете (максимум 2 496 738). Defaults to 100_000.
            ratio (float, optional): Соотношение между реальными и сгенерированными изображениями.
                Если ratio = 0.5, то в датасете будет 50% реальных и 50% сгенерированных изображений.
                Если ratio = 0.7, то в датасете будет 70% реальных и 30% сгенерированных изображений.
                Defaults to 0.5.
            start_index (int, optional): Индекс, с которого начинать выборку изображений.
                Нужно для разделения датасета на test/train. Например test.start_index = 50 000 (будут индексы [50 000 - 150 000)). Defaults to 0.
        """
        kagglehub.config.set_kaggle_credentials(
            Config.KAGGLE_USERNAME, Config.KAGGLE_KEY
        )

        root = kagglehub.dataset_download("awsaf49/artifact-dataset")
        super().__init__(root, transform=transform)
        metadata = self.get_metadata()

        metadata = metadata.iloc[start_index:]

        real_needed = int(images_count * ratio)
        generated_needed = images_count - real_needed

        generated = metadata[metadata["target"] == 1]
        real = metadata[metadata["target"] == 0]

        if len(generated) < generated_needed or len(real) < real_needed:
            raise ValueError(
                "Недостаточно данных после start_index для соблюдения ratio и images_count"
            )

        self.data = (
            pd.concat([generated.iloc[:generated_needed], real[:real_needed]])
            .sample(frac=1, random_state=42)
            .reset_index(drop=True)
        )

    def get_metadata(self) -> pd.DataFrame:
        """Получает метаданные из всех папок в корневом каталоге и объединяет их в один DataFrame.

        Returns:
            pd.DataFrame: Объединенный DataFrame с метаданными изображений.
        Если файл full_metadata.csv уже существует, то он будет загружен из него.
        Если нет, то будет создан новый DataFrame из всех папок в корневом каталоге.
        """
        metadata_list: list[pd.DataFrame] = []
        full_metadata_path = os.path.join(self.root, "full_metadata.csv")

        if os.path.exists(full_metadata_path):
            return pd.read_csv(full_metadata_path)

        for folder, _, files in os.walk(self.root):
            for file in files:
                if file != "metadata.csv":
                    continue
                metadata_file = os.path.join(folder, file)
                file_dir = os.path.dirname(metadata_file)

                metadata = pd.read_csv(metadata_file)

                metadata["path"] = metadata.apply(
                    lambda row: os.path.join(file_dir, row["image_path"]), axis=1
                ).astype(str)
                metadata.drop(
                    columns=["image_path", "filename", "category"], inplace=True
                )
                metadata["target"] = (
                    metadata["target"].replace({i: 1 for i in range(2, 7)}).astype(int)
                )
                metadata_list.append(metadata)
        metadata = (
            pd.concat(metadata_list, ignore_index=True)
            .sample(frac=1, random_state=42)
            .reset_index(drop=True)
        )
        metadata.to_csv(full_metadata_path, index=False)
        return metadata

    def __getitem__(self, index: int) -> tuple[Image.Image, int]:
        row = self.data.iloc[index]
        image = Image.open(row["path"]).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, row["target"]

    def __len__(self) -> int:
        return len(self.data)
