from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.models import User
from app.schemas import ChatRequest, ChatResponse
from app.services.chatbot import build_chat_reply

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def chat(body: ChatRequest, user: User = Depends(get_current_user)):
    reply, suggestions = build_chat_reply(body.message, body.history)
    return ChatResponse(reply=reply, suggestions=suggestions)
