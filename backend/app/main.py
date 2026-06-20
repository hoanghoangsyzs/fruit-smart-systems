from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routers import analyze, auth, chat, dashboard, orchards, predictions
from app.services.inference import models_loaded


@asynccontextmanager
async def lifespan(app: FastAPI):
    Path("data").mkdir(exist_ok=True)
    settings.upload_path.mkdir(parents=True, exist_ok=True)
    init_db()
    yield


app = FastAPI(
    title="Durian Smart System API",
    description="Hệ thống thông minh nhận diện trái/cây sầu riêng - SDC",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(orchards.router)
app.include_router(analyze.router)
app.include_router(predictions.router)
app.include_router(dashboard.router)
app.include_router(chat.router)

settings.upload_path.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=str(settings.upload_path)), name="uploads")


@app.get("/health")
def health():
    loaded = models_loaded()
    return {"status": "ok", "models_loaded": loaded}
