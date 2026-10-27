"""Preprocessing pipelines, identical to the training notebook and the demo app."""
from __future__ import annotations

from torchvision import transforms

MEAN: tuple[float, float, float] = (0.485, 0.456, 0.406)
STD: tuple[float, float, float] = (0.229, 0.224, 0.225)


def eval_transforms() -> transforms.Compose:
    """Inference/validation pipeline: Resize(224) -> ToTensor -> Normalize(ImageNet)."""
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=list(MEAN), std=list(STD)),
    ])


def train_transforms() -> transforms.Compose:
    """Training pipeline: same as evaluation plus light augmentation (train split only)."""
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2),
        transforms.ToTensor(),
        transforms.Normalize(mean=list(MEAN), std=list(STD)),
    ])


if __name__ == "__main__":
    print(eval_transforms())
