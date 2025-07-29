import torch
import torch.nn as nn


class Model(nn.Module):
    def __init__(
        self,
        conv_blocks_number: int = 4,
        dropout_probability: float = 0.3,
        base_channels: int = 64,
        classifier_layers_count: int = 2,
    ):
        """Инициализация модели.

        Args:
            conv_blocks_number (int, optional): Количество сверточных блоков. Defaults to 4.
            dropout_probability (float, optional): Вероятность дропаут слоя. Defaults to 0.3.
            base_channels (int, optional): Количество базовых каналов. Defaults to 64.
            classifier_layers_count (int, optional): Количество слоев классификатора. Defaults to 2.

        Raises:
            ValueError: conv_blocks_number must be at least 1
            ValueError: dropout_probability must be between 0 and 1
            ValueError: base_channels must be at least 1
            ValueError: classifier_layers_count must be at least 1
        """
        super().__init__()
        if conv_blocks_number < 1:
            raise ValueError("conv_blocks_number must be at least 1")
        if dropout_probability < 0 or dropout_probability > 1:
            raise ValueError("dropout_probability must be between 0 and 1")
        if base_channels < 1:
            raise ValueError("base_channels must be at least 1")
        if classifier_layers_count < 1:
            raise ValueError("classifier_layers must be at least 1")

        conv_blocks: list[nn.Sequential] = [
            self.get_conv_block(3, base_channels, dropout_probability)
        ]

        in_channels = base_channels
        for _ in range(conv_blocks_number - 1):
            conv_blocks.append(
                self.get_conv_block(in_channels, in_channels * 2, dropout_probability)
            )
            in_channels *= 2
        self.features = nn.Sequential(*conv_blocks)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))

        classifier_layers: list[nn.Module] = [nn.Flatten()]
        for _ in range(classifier_layers_count):
            classifier_layers.extend(
                [
                    nn.Linear(in_channels, in_channels),
                    nn.ReLU(),
                    nn.Dropout(p=dropout_probability),
                ]
            )
        classifier_layers.append(nn.Linear(in_channels, 1))
        self.classifier = nn.Sequential(*classifier_layers)

    def get_conv_block(
        self, in_channels: int, out_channels: int, dropout_probability: float
    ) -> nn.Sequential:
        """Создание сверточного блока.

        Args:
            in_channels (int): Количество входных каналов
            out_channels (int): Количество выходных каналов
            dropout_probability (float): Вероятность дропаут слоя

        Returns:
            nn.Sequential: Сверточный блок
        """
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(p=dropout_probability),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.features(x)
        x = self.avgpool(x)
        x = self.classifier(x)
        return x


if __name__ == "__main__":
    model = Model()
    print(model)
    x = torch.randn(1, 3, 256, 256)
    output: torch.Tensor = model(x)
    assert output.shape == (1, 1), "Output shape should be (1, 1)"
