"""Generate disease hotspot regions for UI overlay (mock/heuristic until segmentation model)."""

from __future__ import annotations

import random
from pathlib import Path

SEVERITY_COLORS = {
    "low": "#43a047",
    "medium": "#fb8c00",
    "high": "#e53935",
}

DISEASE_SEVERITY = {
    "healthy": None,
    "leaf_spot": "medium",
    "anthracnose": "high",
}

DISEASE_HOTSPOT_COUNT = {
    "healthy": 0,
    "leaf_spot": 2,
    "anthracnose": 3,
}


def _stable_seed(path: Path) -> int:
    return sum(path.stat().st_size + ord(c) for c in path.name[:12]) % 10000


def generate_hotspots(disease: str, image_path: Path | None = None) -> list[dict]:
    """Return normalized bounding regions (0–1) with severity for frontend overlay."""
    count = DISEASE_HOTSPOT_COUNT.get(disease, 0)
    if count == 0:
        return []

    base_severity = DISEASE_SEVERITY.get(disease, "medium")
    rng = random.Random(_stable_seed(image_path) if image_path and image_path.exists() else 42)

    presets = [
        (0.18, 0.22, 0.28, 0.24),
        (0.52, 0.35, 0.22, 0.2),
        (0.35, 0.58, 0.25, 0.22),
    ]
    severities = {
        "low": ["low", "low", "medium"],
        "medium": ["low", "medium", "medium"],
        "high": ["medium", "high", "high"],
    }
    levels = severities.get(base_severity or "medium", severities["medium"])

    label_vi = {
        "healthy": "Khỏe mạnh",
        "leaf_spot": "Đốm lá",
        "anthracnose": "Thán thư",
    }.get(disease, disease)
    out: list[dict] = []
    for i in range(count):
        x, y, w, h = presets[i % len(presets)]
        jitter = lambda v: max(0.05, min(0.85, v + rng.uniform(-0.06, 0.06)))
        sev = levels[i % len(levels)]
        out.append(
            {
                "x": jitter(x),
                "y": jitter(y),
                "width": w,
                "height": h,
                "severity": sev,
                "color": SEVERITY_COLORS[sev],
                "label": disease,
                "label_vi": label_vi,
                "confidence": round(rng.uniform(0.72, 0.96), 2),
            }
        )
    return out


def overall_severity(disease: str, confidence: float) -> str:
    if disease == "healthy":
        return "none"
    if disease == "anthracnose" or confidence >= 0.88:
        return "high"
    if disease == "leaf_spot" or confidence >= 0.75:
        return "medium"
    return "low"
