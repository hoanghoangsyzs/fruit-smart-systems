"""Bridge to ML inference with Roboflow, local-model, and mock fallbacks."""

from __future__ import annotations

import base64
import re
import sys
from pathlib import Path
from typing import Any

from app.config import settings

ML_ROOT = Path(__file__).resolve().parents[3] / "ml"
if str(ML_ROOT.parent) not in sys.path:
    sys.path.insert(0, str(ML_ROOT.parent))

FRUIT_CLASSES = {
    "durian",
    "sầu_riêng",
    "sầu riêng",
    "sau_rieng",
    "saurieng",
    "durian_smart_system",
}
RIPENESS_CLASSES = {
    "unripe": "unripe",
    "chua_chin": "unripe",
    "chưa_chín": "unripe",
    "half_ripe": "half_ripe",
    "gan_chin": "half_ripe",
    "gần_chín": "half_ripe",
    "ripe": "ripe",
    "chin": "ripe",
    "chín": "ripe",
}
HEALTHY_CLASSES = {"healthy", "khoe_manh", "khỏe_mạnh", "normal", "no_disease"}

LABEL_VI = {
    "durian": "Sầu riêng",
    "disease_detected": "Có dấu hiệu sâu bệnh",
    "healthy": "Không phát hiện sâu bệnh",
    "leaf_spot": "Đốm lá",
    "anthracnose": "Thán thư",
    "phytophthora": "Phytophthora / xì mủ",
    "fruit_rot": "Thối trái",
    "root_rot": "Thối rễ",
    "stem_canker": "Nứt thân / xì mủ thân",
    "leaf_blight": "Cháy lá",
    "unknown": "Chưa xác định",
    "unripe": "Chưa chín",
    "half_ripe": "Gần chín",
    "ripe": "Chín",
}


def _normalize_label(label: str) -> str:
    value = label.strip().lower()
    value = value.replace("-", "_").replace(" ", "_")
    value = re.sub(r"[^0-9a-zA-Z_à-ỹÀ-Ỹ]", "", value)
    return value


def _attach_visual_analysis(result: dict, image_path: Path | None) -> dict:
    from app.services.hotspots import generate_hotspots, overall_severity

    disease = result["disease"]["label"]
    conf = result["disease"]["confidence"]
    if "hotspots" not in result:
        result["hotspots"] = generate_hotspots(disease, image_path)
    result["severity"] = overall_severity(disease, conf)
    return result


def _mock_result(image_path: Path | None = None) -> dict:
    base = {
        "fruit": {"label": "durian", "confidence": 0.93},
        "disease": {"label": "anthracnose", "confidence": 0.87},
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


def _fallback_recommendations(disease: str, ripeness: str, d_conf: float) -> list[dict]:
    if disease == "disease_detected":
        if d_conf >= 0.75:
            return [
                {
                    "priority": "high",
                    "title": "Ưu tiên kiểm tra vùng nghi nhiễm",
                    "detail": "AI phát hiện dấu hiệu sâu bệnh với độ tin cậy cao. Hãy kiểm tra trực tiếp vùng được đánh dấu, cách ly trái/cành nghi nhiễm nếu cần và cân nhắc hỏi kỹ sư nông nghiệp trước khi xử lý thuốc.",
                }
            ]
        return [
            {
                "priority": "medium",
                "title": "Cần chụp và kiểm tra bổ sung",
                "detail": "AI phát hiện dấu hiệu sâu bệnh ở mức chưa thật chắc chắn. Hãy chụp thêm ảnh rõ hơn ở vùng nghi ngờ, đủ sáng và gần hơn để xác nhận trước khi đưa ra biện pháp xử lý.",
            }
        ]

    if disease == "healthy" and d_conf >= 0.7:
        return [
            {
                "priority": "low",
                "title": "Chưa phát hiện dấu hiệu sâu bệnh rõ ràng",
                "detail": "Tiếp tục theo dõi định kỳ, giữ vườn thông thoáng và duy trì lịch chăm sóc phù hợp. Nên quét lại nếu xuất hiện đốm, xì mủ, thối trái hoặc lá vàng bất thường.",
            }
        ]

    if disease == "unknown":
        return [
            {
                "priority": "medium",
                "title": "Chưa đủ cơ sở kết luận sâu bệnh",
                "detail": "Ảnh hiện tại chưa cho kết quả sâu bệnh đủ rõ. Hãy chụp thêm ảnh cận cảnh vùng nghi ngờ như vỏ trái, cuống, thân, lá hoặc vùng xì mủ để AI đánh giá chính xác hơn.",
            }
        ]

    return []


def _build_recommendations(disease: str, ripeness: str, d_conf: float) -> list[dict]:
    rules = _load_recommendations(disease, ripeness)
    return rules or _fallback_recommendations(disease, ripeness, d_conf)


def _compute_quality(disease: str, ripeness: str, d_conf: float, r_conf: float) -> tuple[int, str]:
    score = 72.0
    serious_diseases = {"phytophthora", "fruit_rot", "root_rot", "stem_canker"}
    medium_diseases = {"anthracnose", "leaf_blight", "leaf_spot"}

    if disease == "healthy":
        score += 15
    elif disease in medium_diseases:
        score -= 12
    elif disease in serious_diseases:
        score -= 24
    elif disease != "unknown":
        score -= 16

    if ripeness == "ripe":
        score += 8
    elif ripeness == "unripe":
        score -= 5

    score = min(100, max(0, int(score * max(0.45, (d_conf + r_conf) / 2))))
    grade = "A" if score >= 85 else "B" if score >= 70 else "C" if score >= 55 else "D"
    return score, grade


def _prediction_confidence(pred: dict[str, Any]) -> float:
    raw = float(pred.get("confidence", 0) or 0)
    return raw / 100 if raw > 1 else raw


def _prediction_label(pred: dict[str, Any]) -> str:
    return str(pred.get("class") or pred.get("class_name") or pred.get("label") or "unknown")


def _class_group(label: str) -> tuple[str, str]:
    normalized = _normalize_label(label)
    if normalized in FRUIT_CLASSES:
        return "fruit", "durian"
    if normalized in RIPENESS_CLASSES:
        return "ripeness", RIPENESS_CLASSES[normalized]
    if normalized in HEALTHY_CLASSES:
        return "disease", "healthy"
    if normalized in {"disease", "benh", "bệnh", "sau_benh", "sâu_bệnh"}:
        return "disease", "disease_detected"
    return "disease", normalized


def _best_by_group(predictions: list[dict[str, Any]]) -> tuple[dict, dict, dict]:
    fruit = {"label": "unknown", "confidence": 0.0}
    disease = {"label": "unknown", "confidence": 0.0}
    ripeness = {"label": "unknown", "confidence": 0.0}

    for pred in predictions:
        group, label = _class_group(_prediction_label(pred))
        conf = _prediction_confidence(pred)
        target = {"label": label, "confidence": conf}
        if group == "fruit" and conf >= fruit["confidence"]:
            fruit = target
        elif group == "disease" and conf >= disease["confidence"]:
            disease = target
        elif group == "ripeness" and conf >= ripeness["confidence"]:
            ripeness = target

    if predictions and disease["label"] == "unknown" and disease["confidence"] == 0.0:
        disease = {"label": "unknown", "confidence": 0.5}

    return fruit, disease, ripeness


def _roboflow_hotspots(predictions: list[dict[str, Any]]) -> list[dict]:
    hotspots: list[dict] = []
    for pred in predictions[:8]:
        group, label = _class_group(_prediction_label(pred))
        if group == "fruit":
            continue

        width = float(pred.get("width", 0) or 0)
        height = float(pred.get("height", 0) or 0)
        x_center = float(pred.get("x", 0) or 0)
        y_center = float(pred.get("y", 0) or 0)
        if width <= 0 or height <= 0:
            continue

        conf = _prediction_confidence(pred)
        severity = "high" if conf >= 0.75 else "medium" if conf >= 0.5 else "low"
        color = "#e53935" if severity == "high" else "#fb8c00" if severity == "medium" else "#43a047"
        hotspots.append(
            {
                "x": max(0, x_center - width / 2),
                "y": max(0, y_center - height / 2),
                "width": width,
                "height": height,
                "severity": severity,
                "color": color,
                "label": label,
                "label_vi": LABEL_VI.get(label, label),
                "confidence": conf,
            }
        )
    return hotspots


def _roboflow_result(image_path: Path) -> dict:
    import requests

    url = f"https://detect.roboflow.com/{settings.roboflow_model_id}/{settings.roboflow_model_version}"
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    response = requests.post(
        url,
        params={
            "api_key": settings.roboflow_api_key,
            "confidence": settings.roboflow_confidence,
        },
        data=image_b64,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    response.raise_for_status()
    predictions = response.json().get("predictions") or []

    fruit, disease, ripeness = _best_by_group(predictions)
    if fruit["label"] == "unknown" and predictions:
        fruit = {"label": "durian", "confidence": 0.5}

    quality_score, quality_grade = _compute_quality(
        disease["label"],
        ripeness["label"],
        disease["confidence"],
        ripeness["confidence"] or 0.5,
    )

    return _attach_visual_analysis(
        {
            "fruit": fruit,
            "disease": disease,
            "ripeness": ripeness,
            "quality_score": quality_score,
            "quality_grade": quality_grade,
            "recommendations": _build_recommendations(
                disease["label"],
                ripeness["label"],
                disease["confidence"],
            ),
            "hotspots": _roboflow_hotspots(predictions),
        },
        image_path,
    )


def _local_model_result(image_path: Path) -> dict:
    from ml.inference import predict_dual

    raw = predict_dual(image_path, artifacts_dir=settings.artifacts_path)
    disease = raw["disease"]["label"]
    ripeness = raw["ripeness"]["label"]
    d_conf = raw["disease"]["confidence"]
    r_conf = raw["ripeness"]["confidence"]
    quality_score, quality_grade = _compute_quality(disease, ripeness, d_conf, r_conf)

    return _attach_visual_analysis(
        {
            "fruit": {"label": "durian", "confidence": 1.0},
            "disease": {"label": disease, "confidence": d_conf},
            "ripeness": {"label": ripeness, "confidence": r_conf},
            "quality_score": quality_score,
            "quality_grade": quality_grade,
            "recommendations": _load_recommendations(disease, ripeness),
        },
        image_path,
    )


def analyze_image(image_path: Path) -> dict:
    if settings.mock_inference:
        return _mock_result(image_path)

    if settings.roboflow_api_key and settings.roboflow_model_id:
        try:
            return _roboflow_result(image_path)
        except Exception:
            return _mock_result(image_path)

    try:
        return _local_model_result(image_path)
    except Exception:
        return _mock_result(image_path)


def models_loaded() -> dict[str, bool | str]:
    if settings.mock_inference:
        return {"fruit": False, "disease": False, "ripeness": False, "mode": "mock"}

    if settings.roboflow_api_key and settings.roboflow_model_id:
        return {
            "fruit": True,
            "disease": True,
            "ripeness": True,
            "mode": "roboflow",
            "model": f"{settings.roboflow_model_id}/{settings.roboflow_model_version}",
        }

    artifacts = settings.artifacts_path
    return {
        "fruit": True,
        "disease": (artifacts / "disease_best.pt").exists(),
        "ripeness": (artifacts / "ripeness_best.pt").exists(),
        "mode": "local",
    }
