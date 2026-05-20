from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models import Orchard, User
from app.schemas import OrchardCreate, OrchardOut

router = APIRouter(prefix="/api/v1/orchards", tags=["orchards"])


@router.get("", response_model=list[OrchardOut])
def list_orchards(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Orchard).filter(Orchard.user_id == user.id).order_by(Orchard.id.desc()).all()


@router.post("", response_model=OrchardOut, status_code=201)
def create_orchard(
    body: OrchardCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    orchard = Orchard(user_id=user.id, name=body.name, location=body.location, area_ha=body.area_ha)
    db.add(orchard)
    db.commit()
    db.refresh(orchard)
    return orchard


@router.get("/{orchard_id}", response_model=OrchardOut)
def get_orchard(orchard_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orchard = db.query(Orchard).filter(Orchard.id == orchard_id, Orchard.user_id == user.id).first()
    if not orchard:
        raise HTTPException(status_code=404, detail="Orchard not found")
    return orchard


@router.delete("/{orchard_id}", status_code=204)
def delete_orchard(orchard_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    orchard = db.query(Orchard).filter(Orchard.id == orchard_id, Orchard.user_id == user.id).first()
    if not orchard:
        raise HTTPException(status_code=404, detail="Orchard not found")
    db.delete(orchard)
    db.commit()
