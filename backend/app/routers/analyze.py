import json
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.config import settings
from app.database import get_db
from app.models import Orchard, Prediction, User
from app.schemas import AnalyzeResponse, HotspotRegion, LabelResult, Recommendation
from app.services.inference import LABEL_VI, analyze_image

router = APIRouter(prefix="/api/v1", tags=["analyze"])

ALLOWED = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 10 * 1024 * 1024


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    file: UploadFile = File(...),
    orchard_id: int | None = Form(None),
    note: str | None = Form(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if file.content_type not in ALLOWED:
        raise HTTPException(status_code=400, detail={"detail": "Invalid image", "code": "INVALID_IMAGE"})

    if orchard_id is not None:
        orchard = db.query(Orchard).filter(Orchard.id == orchard_id, Orchard.user_id == user.id).first()
        if not orchard:
            raise HTTPException(status_code=404, detail="Orchard not found")

    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="File too large")

    settings.upload_path.mkdir(parents=True, exist_ok=True)
    ext = Path(file.filename or "img.jpg").suffix or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    dest = settings.upload_path / filename
    dest.write_bytes(data)

    result = analyze_image(dest)
    recs_json = json.dumps(result["recommendations"], ensure_ascii=False)

    pred = Prediction(
        user_id=user.id,
        orchard_id=orchard_id,
        image_path=filename,
        disease_label=result["disease"]["label"],
        disease_confidence=result["disease"]["confidence"],
        ripeness_label=result["ripeness"]["label"],
        ripeness_confidence=result["ripeness"]["confidence"],
        quality_score=result["quality_score"],
        quality_grade=result["quality_grade"],
        recommendations_json=recs_json,
        note=note,
    )
    db.add(pred)
    db.commit()
    db.refresh(pred)

    recommendations = [Recommendation(**r) for r in result["recommendations"]]
    hotspots = [HotspotRegion(**h) for h in result.get("hotspots", [])]

    return AnalyzeResponse(
        prediction_id=pred.id,
        disease=LabelResult(
            label=result["disease"]["label"],
            label_vi=LABEL_VI.get(result["disease"]["label"], result["disease"]["label"]),
            confidence=result["disease"]["confidence"],
        ),
        ripeness=LabelResult(
            label=result["ripeness"]["label"],
            label_vi=LABEL_VI.get(result["ripeness"]["label"], result["ripeness"]["label"]),
            confidence=result["ripeness"]["confidence"],
        ),
        quality_score=result["quality_score"],
        quality_grade=result["quality_grade"],
        severity=result.get("severity", "none"),
        hotspots=hotspots,
        recommendations=recommendations,
        image_url=f"/uploads/{filename}",
        created_at=pred.created_at or datetime.utcnow(),
    )
