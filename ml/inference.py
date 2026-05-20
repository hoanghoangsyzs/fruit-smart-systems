"""Inference helpers for backend integration."""

from __future__ import annotations

import json
from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torchvision import models, transforms

_transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ]
)

_models: dict[str, tuple[nn.Module, list[str]]] = {}


def _build_model(num_classes: int) -> nn.Module:
    model = models.efficientnet_b0(weights=None)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    return model


def _load_task(task: str, artifacts_dir: Path) -> tuple[nn.Module, list[str]]:
    if task in _models:
        return _models[task]
    ckpt_path = artifacts_dir / f"{task}_best.pt"
    if not ckpt_path.exists():
        raise FileNotFoundError(f"Missing checkpoint: {ckpt_path}")
    ckpt = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    classes: list[str] = ckpt["classes"]
    model = _build_model(len(classes))
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    _models[task] = (model, classes)
    return model, classes


def predict_single(image_path: Path, task: str, artifacts_dir: Path) -> dict:
    model, classes = _load_task(task, artifacts_dir)
    img = Image.open(image_path).convert("RGB")
    tensor = _transform(img).unsqueeze(0)
    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)[0]
        idx = int(probs.argmax().item())
    return {"label": classes[idx], "confidence": float(probs[idx].item())}


def predict_dual(image_path: Path, artifacts_dir: Path | str) -> dict:
    artifacts_dir = Path(artifacts_dir)
    return {
        "disease": predict_single(image_path, "disease", artifacts_dir),
        "ripeness": predict_single(image_path, "ripeness", artifacts_dir),
    }


def load_labels(artifacts_dir: Path) -> dict:
    out = {}
    for task in ("disease", "ripeness"):
        p = artifacts_dir / f"{task}_labels.json"
        if p.exists():
            out[task] = json.loads(p.read_text(encoding="utf-8"))
    return out
