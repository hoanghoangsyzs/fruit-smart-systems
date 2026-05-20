from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Prediction, User
from app.schemas import PredictionOut

router = APIRouter(prefix="/api/v1/predictions", tags=["predictions"])


@router.get("", response_model=list[PredictionOut])
def list_predictions(
    orchard_id: int | None = Query(None),
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Prediction).filter(Prediction.user_id == user.id)
    if orchard_id is not None:
        q = q.filter(Prediction.orchard_id == orchard_id)
    rows = q.order_by(Prediction.created_at.desc()).offset(offset).limit(limit).all()
    return [
        PredictionOut(
            id=p.id,
            orchard_id=p.orchard_id,
            disease_label=p.disease_label,
            ripeness_label=p.ripeness_label,
            quality_score=p.quality_score,
            quality_grade=p.quality_grade,
            image_url=f"/uploads/{p.image_path.split('/')[-1]}",
            created_at=p.created_at,
        )
        for p in rows
    ]
