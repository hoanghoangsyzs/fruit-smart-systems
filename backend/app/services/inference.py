"""Bridge to ML inference — mock mode for week 1, real models week 2+."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from app.config import settings

# Allow importing ml package from repo root
ML_ROOT = Path(__file__).resolve().parents[3] / "ml"
if str(ML_ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ML_ROOT.parent))

LABEL_VI = {
    "healthy": "Khỏe mạnh",
    "leaf_spot": "Đốm lá",
    "anthracnose": "Thán thư",
    "unripe": "Chưa chín",
    "half_ripe": "Gần chín",
    "ripe": "Chín",
}


def _attach_visual_analysis(result: dict, image_path: Path | None) -> dict:
    from app.services.hotspots import generate_hotspots, overall_severity

    disease = result["disease"]["label"]
    conf = result["disease"]["confidence"]
    result["hotspots"] = generate_hotspots(disease, image_path)
    result["severity"] = overall_severity(disease, conf)
    return result


def _mock_result(image_path: Path | None = None) -> dict:
    base = {
        "disease": {"label": "leaf_spot", "confidence": 0.87},
        "ripeness": {"label": "half_ripe", "confidence": 0.84},
        "quality_score": 72,
        "quality_grade": "B",
        "recommendations": [],
    }
    base["recommendations"] = _load_recommendations(
        base["disease"]["label"], base["ripeness"]["label"]
    )
    return _attach_visual_analysis(base, image_path)


def _load_recommendations(disease: str, ripeness: str) -> list[dict]:
    rules_path = ML_ROOT / "config" / "recommendations.yaml"
    if not rules_path.exists():
        return []
    try:
        import yaml

        with open(rules_path, encoding="utf-8") as f:
            rules = yaml.safe_load(f) or {}
    except Exception:
        return []

    out: list[dict] = []
    for key in (f"disease.{disease}", f"ripeness.{ripeness}"):
        if key in rules:
            out.extend(rules[key])
    return out


def _compute_quality(disease: str, ripeness: str, d_conf: float, r_conf: float) -> tuple[int, str]:
    score = 70.0
    if disease == "healthy":
        score += 15
    elif disease == "leaf_spot":
        score -= 10
    else:
        score -= 20
    if ripeness == "ripe":
        score += 10
    elif ripeness == "unripe":
        score -= 5
    score = min(100, max(0, int(score * (d_conf + r_conf) / 2)))
    grade = "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "D"
    return score, grade


def analyze_image(image_path: Path) -> dict:
    if settings.mock_inference:
        return _mock_result(image_path)

    try:
        from ml.inference import predict_dual

        raw = predict_dual(image_path, artifacts_dir=settings.artifacts_path)
    except Exception:
        return _mock_result(image_path)

    disease = raw["disease"]["label"]
    ripeness = raw["ripeness"]["label"]
    d_conf = raw["disease"]["confidence"]
    r_conf = raw["ripeness"]["confidence"]
    quality_score, quality_grade = _compute_quality(disease, ripeness, d_conf, r_conf)
    recommendations = _load_recommendations(disease, ripeness)

    return _attach_visual_analysis(
        {
            "disease": {"label": disease, "confidence": d_conf},
            "ripeness": {"label": ripeness, "confidence": r_conf},
            "quality_score": quality_score,
            "quality_grade": quality_grade,
            "recommendations": recommendations,
        },
        image_path,
    )


def models_loaded() -> dict[str, bool]:
    if settings.mock_inference:
        return {"disease": False, "ripeness": False, "mode": "mock"}
    artifacts = settings.artifacts_path
    return {
        "disease": (artifacts / "disease_best.pt").exists(),
        "ripeness": (artifacts / "ripeness_best.pt").exists(),
        "mode": "live",
    }
