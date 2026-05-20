"""
Huấn luyện mô hình phân loại — disease hoặc ripeness.

Usage:
  python train.py --task disease --data-dir ../dataset/disease
  python train.py --task ripeness --data-dir ../dataset/ripeness --epochs 15
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


def build_model(num_classes: int) -> nn.Module:
    weights = models.EfficientNet_B0_Weights.IMAGENET1K_V1
    model = models.efficientnet_b0(weights=weights)
    in_features = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_features, num_classes)
    return model


def get_loaders(data_dir: Path, batch_size: int = 16):
    train_tf = transforms.Compose(
        [
            transforms.Resize((256, 256)),
            transforms.RandomResizedCrop(224),
            transforms.RandomHorizontalFlip(),
            transforms.ColorJitter(0.2, 0.2, 0.2),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    eval_tf = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    train_ds = datasets.ImageFolder(data_dir / "train", transform=train_tf)
    val_ds = datasets.ImageFolder(data_dir / "val", transform=eval_tf)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=0)
    return train_loader, val_loader, train_ds.classes


def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total, correct, loss_sum = 0, 0, 0.0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        out = model(x)
        loss = criterion(out, y)
        loss.backward()
        optimizer.step()
        loss_sum += loss.item() * x.size(0)
        correct += (out.argmax(1) == y).sum().item()
        total += x.size(0)
    return loss_sum / total, correct / total


@torch.no_grad()
def eval_epoch(model, loader, criterion, device):
    model.eval()
    total, correct, loss_sum = 0, 0, 0.0
    for x, y in loader:
        x, y = x.to(device), y.to(device)
        out = model(x)
        loss = criterion(out, y)
        loss_sum += loss.item() * x.size(0)
        correct += (out.argmax(1) == y).sum().item()
        total += x.size(0)
    return loss_sum / total, correct / total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True, choices=["disease", "ripeness"])
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts"))
    args = parser.parse_args()

    if not (args.data_dir / "train").exists():
        raise SystemExit(
            f"Missing {args.data_dir / 'train'}. See dataset/DATASET.md for folder layout."
        )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    train_loader, val_loader, classes = get_loaders(args.data_dir)
    model = build_model(len(classes)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    best_acc = 0.0
    ckpt_name = f"{args.task}_best.pt"

    for epoch in range(1, args.epochs + 1):
        tr_loss, tr_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        va_loss, va_acc = eval_epoch(model, val_loader, criterion, device)
        print(f"Epoch {epoch}/{args.epochs} train_acc={tr_acc:.3f} val_acc={va_acc:.3f}")
        if va_acc > best_acc:
            best_acc = va_acc
            torch.save(
                {
                    "model_state": model.state_dict(),
                    "classes": classes,
                    "task": args.task,
                    "val_acc": va_acc,
                },
                args.output_dir / ckpt_name,
            )

    labels_path = args.output_dir / f"{args.task}_labels.json"
    labels_path.write_text(json.dumps(classes, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Saved {args.output_dir / ckpt_name} (best val_acc={best_acc:.3f})")


if __name__ == "__main__":
    main()
