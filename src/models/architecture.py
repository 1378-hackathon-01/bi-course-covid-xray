"""Model definition reconstructed from `models/baseline_model.pt` (state_dict keys)."""
from __future__ import annotations

from pathlib import Path

import torch
import torch.nn as nn
from torchvision import models

NUM_CLASSES: int = 2


def build_model(num_classes: int = NUM_CLASSES) -> nn.Module:
    """ResNet-18 with the Dropout(0.5) + Linear(512, 2) head used in training."""
    model = models.resnet18(weights=None)
    in_features = model.fc.in_features
    model.fc = nn.Sequential(nn.Dropout(p=0.5), nn.Linear(in_features, num_classes))
    return model


def load_frozen_model(checkpoint: str | Path, device: str = "cpu") -> nn.Module:
    """Load the frozen baseline checkpoint in eval mode (never retrained)."""
    model = build_model()
    state = torch.load(str(checkpoint), map_location="cpu", weights_only=True)
    model.load_state_dict(state)
    model.to(device)
    model.eval()
    return model


if __name__ == "__main__":
    ckpt = Path(__file__).resolve().parents[2] / "models" / "baseline_model.pt"
    if ckpt.exists():
        net = load_frozen_model(ckpt)
        total = sum(p.numel() for p in net.parameters())
        print("parameters:", f"{total:,}", "| head shape:", tuple(net.fc[1].weight.shape))
    else:
        print("checkpoint not found: run `git lfs pull` (see docs/reproduction_guide.md)")
