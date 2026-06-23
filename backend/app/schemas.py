from datetime import datetime

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    email: str
    password: str = Field(min_length=6)
    full_name: str = ""


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OrchardCreate(BaseModel):
    name: str
    crop_type: str = "durian"
    location: str | None = None
    area_ha: float | None = None


class OrchardOut(BaseModel):
    id: int
    name: str
    crop_type: str
    location: str | None
    area_ha: float | None
    created_at: datetime

    model_config = {"from_attributes": True}


class LabelResult(BaseModel):
    label: str
    label_vi: str
    confidence: float


class Recommendation(BaseModel):
    priority: str
    title: str
    detail: str


class HotspotRegion(BaseModel):
    x: float
    y: float
    width: float
    height: float
    severity: str
    color: str
    label: str
    label_vi: str
    confidence: float


class AnalyzeResponse(BaseModel):
    prediction_id: int
    fruit: LabelResult
    disease: LabelResult
    ripeness: LabelResult
    quality_score: int
    quality_grade: str
    severity: str
    hotspots: list[HotspotRegion]
    recommendations: list[Recommendation]
    image_url: str
    created_at: datetime


class PredictionOut(BaseModel):
    id: int
    orchard_id: int | None
    disease_label: str
    ripeness_label: str
    quality_score: int
    quality_grade: str
    image_url: str
    created_at: datetime

    model_config = {"from_attributes": True}


class DistributionItem(BaseModel):
    label: str
    count: int


class TimelineItem(BaseModel):
    date: str
    scans: int
    avg_quality: float


class DashboardSummary(BaseModel):
    total_scans: int
    disease_distribution: list[DistributionItem]
    ripeness_distribution: list[DistributionItem]
    timeline: list[TimelineItem]


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    history: list[ChatMessage] = Field(default_factory=list, max_length=12)


class ChatResponse(BaseModel):
    reply: str
    suggestions: list[str] = Field(default_factory=list)
