from collections import defaultdict
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Prediction, User
from app.schemas import DashboardSummary, DistributionItem, TimelineItem

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(
    orchard_id: int | None = Query(None),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Prediction).filter(Prediction.user_id == user.id)
    if orchard_id is not None:
        q = q.filter(Prediction.orchard_id == orchard_id)
    rows = q.order_by(Prediction.created_at.desc()).limit(500).all()

    disease_counts: dict[str, int] = defaultdict(int)
    ripeness_counts: dict[str, int] = defaultdict(int)
    timeline: dict[str, list] = defaultdict(lambda: {"scans": 0, "quality_sum": 0})

    for p in rows:
        disease_counts[p.disease_label] += 1
        ripeness_counts[p.ripeness_label] += 1
        day = (p.created_at or datetime.utcnow()).strftime("%Y-%m-%d")
        timeline[day]["scans"] += 1
        timeline[day]["quality_sum"] += p.quality_score

    timeline_list = sorted(timeline.items())[-14:]
    return DashboardSummary(
        total_scans=len(rows),
        disease_distribution=[
            DistributionItem(label=k, count=v) for k, v in sorted(disease_counts.items(), key=lambda x: -x[1])
        ],
        ripeness_distribution=[
            DistributionItem(label=k, count=v) for k, v in sorted(ripeness_counts.items(), key=lambda x: -x[1])
        ],
        timeline=[
            TimelineItem(
                date=day,
                scans=info["scans"],
                avg_quality=round(info["quality_sum"] / info["scans"], 1) if info["scans"] else 0,
            )
            for day, info in timeline_list
        ],
    )
