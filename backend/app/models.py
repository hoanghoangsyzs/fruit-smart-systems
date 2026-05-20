from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    orchards: Mapped[list["Orchard"]] = relationship(back_populates="owner")
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="user")


class Orchard(Base):
    __tablename__ = "orchards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(255))
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    area_ha: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    owner: Mapped["User"] = relationship(back_populates="orchards")
    predictions: Mapped[list["Prediction"]] = relationship(back_populates="orchard")


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    orchard_id: Mapped[int | None] = mapped_column(ForeignKey("orchards.id"), nullable=True, index=True)
    image_path: Mapped[str] = mapped_column(String(512))
    disease_label: Mapped[str] = mapped_column(String(64))
    disease_confidence: Mapped[float] = mapped_column(Float)
    ripeness_label: Mapped[str] = mapped_column(String(64))
    ripeness_confidence: Mapped[float] = mapped_column(Float)
    quality_score: Mapped[int] = mapped_column(Integer)
    quality_grade: Mapped[str] = mapped_column(String(2))
    recommendations_json: Mapped[str] = mapped_column(Text, default="[]")
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    user: Mapped["User"] = relationship(back_populates="predictions")
    orchard: Mapped["Orchard | None"] = relationship(back_populates="predictions")
