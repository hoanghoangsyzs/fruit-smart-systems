from __future__ import annotations

import re

from app.config import settings
from app.schemas import ChatMessage


DEFAULT_SUGGESTIONS = [
    "Những bệnh thường gặp ở sầu riêng?",
    "Cách chụp ảnh sầu riêng để phân tích chính xác?",
    "Điểm chất lượng được tính như thế nào?",
]

SYSTEM_PROMPT = """
Bạn là trợ lý AI trong website Durian Smart System. Website này hỗ trợ phân tích
ảnh trái/cây sầu riêng, nhận diện sâu bệnh, đánh giá độ chín, điểm chất lượng,
quản lý vườn và xem dashboard.

Phong cách trả lời:
- Trả lời bằng tiếng Việt tự nhiên, thân thiện, hữu ích, giống một chatbot AI thông thường.
- Ưu tiên kiến thức về sầu riêng: sâu bệnh, độ chín, chất lượng trái, chăm sóc vườn,
  chụp ảnh để phân tích và cách dùng hệ thống.
- Nếu người dùng hỏi kiến thức nông nghiệp chung như xoài, mít, cà phê, phân bón,
  thời tiết, kỹ thuật chăm sóc..., hãy trả lời trực tiếp theo kiến thức tổng quát.
- Chỉ nhắc rằng hệ thống chuyên về sầu riêng khi người dùng hỏi về phạm vi tính năng,
  yêu cầu phân tích ảnh bằng hệ thống, hoặc hỏi dữ liệu mà hệ thống thực sự chưa có.
- Nếu người dùng hỏi lỗi kỹ thuật của dự án, hướng dẫn theo backend chạy ở
  127.0.0.1:8001 và frontend chạy ở 127.0.0.1:5174.
- Không bịa chẩn đoán chắc chắn khi không có ảnh, mẫu bệnh hoặc dữ liệu thực tế.
  Với bệnh cây trồng, hãy nói đây là dấu hiệu thường gặp và khuyên kiểm tra thực địa
  hoặc hỏi kỹ sư nông nghiệp khi cần.
""".strip()


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _format_history(history: list[ChatMessage]) -> str:
    lines: list[str] = []
    for item in history[-8:]:
        role = "Người dùng" if item.role == "user" else "Trợ lý"
        content = item.content.strip()
        if content:
            lines.append(f"{role}: {content}")
    return "\n".join(lines)


def _gemini_reply(message: str, history: list[ChatMessage]) -> str | None:
    if not settings.gemini_api_key:
        return None

    try:
        from google import genai
    except ImportError:
        return None

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Lịch sử gần đây:\n{_format_history(history) or '(chưa có)'}\n\n"
        f"Câu hỏi hiện tại:\n{message}"
    )

    try:
        client = genai.Client(api_key=settings.gemini_api_key)
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )
    except Exception:
        return None

    text = getattr(response, "text", None)
    if not text:
        return None
    return text.strip()


def _fallback_reply(message: str, history: list[ChatMessage]) -> tuple[str, list[str]]:
    text = _normalize(message)

    if any(keyword in text for keyword in ["sầu riêng", "sau rieng", "bệnh", "xì mủ", "thối rễ"]):
        return (
            "Một số bệnh thường gặp ở sầu riêng gồm: thối rễ, xì mủ thân do nấm Phytophthora, cháy lá, thán thư, nứt thân chảy nhựa, thối trái và bệnh do tuyến trùng làm cây suy yếu. Bạn nên quan sát vị trí bệnh: rễ, thân, lá hay trái; kiểm tra độ ẩm đất, vết chảy nhựa, lá vàng rụng và vùng trái bị thối để khoanh nguyên nhân. Nếu bệnh lan nhanh, nên nhờ kỹ sư nông nghiệp kiểm tra trực tiếp trước khi dùng thuốc.",
            [
                "Dấu hiệu xì mủ trên sầu riêng là gì?",
                "Cách phòng thối rễ sầu riêng?",
                "Phân biệt thán thư và cháy lá thế nào?",
            ],
        )

    if any(keyword in text for keyword in ["chào", "hello", "hi", "xin chao", "xin chào"]):
        return (
            "Chào bạn, mình là trợ lý Durian Smart. Mình có thể hỗ trợ về sâu bệnh, độ chín, chất lượng trái sầu riêng, cách chụp ảnh phân tích và cách dùng website.",
            DEFAULT_SUGGESTIONS,
        )

    if any(keyword in text for keyword in ["chụp", "ảnh", "camera", "scan"]):
        return (
            "Để phân tích sầu riêng tốt hơn, bạn nên chụp trong điều kiện đủ sáng, giữ camera ổn định, để trái hoặc bộ phận cây nằm rõ trong khung hình. Nếu kiểm tra bệnh, hãy chụp cận cảnh vùng có dấu hiệu như xì mủ, đốm lá, cháy mép, thối trái hoặc nứt thân.",
            [
                "Nên chụp bao nhiêu ảnh?",
                "Ảnh bị mờ có phân tích được không?",
                "Làm sao kiểm tra lại kết quả?",
            ],
        )

    if any(keyword in text for keyword in ["api", "backend", "frontend", "lỗi", "không chạy", "server"]):
        return (
            "Nếu website không gọi được API, hãy kiểm tra backend đã chạy ở 127.0.0.1:8001 chưa, frontend đang chạy ở 127.0.0.1:5174 chưa, và token đăng nhập còn hợp lệ không.",
            [
                "Cách đổi backend sang port 8001?",
                "Vì sao frontend không gọi được API?",
                "Làm sao kiểm tra backend còn chạy?",
            ],
        )

    recent_context = ""
    if history:
        recent_context = " Mình cũng đã ghi nhận ngữ cảnh câu hỏi trước đó của bạn."

    return (
        "Mình có thể hỗ trợ câu hỏi về sầu riêng, nông nghiệp chung hoặc cách dùng Durian Smart. Bạn có thể nói rõ triệu chứng, vị trí bệnh và điều kiện vườn để mình gợi ý sát hơn."
        + recent_context,
        DEFAULT_SUGGESTIONS,
    )


def build_chat_reply(message: str, history: list[ChatMessage] | None = None) -> tuple[str, list[str]]:
    history = history or []

    gemini_text = _gemini_reply(message, history)
    if gemini_text:
        return gemini_text, DEFAULT_SUGGESTIONS

    return _fallback_reply(message, history)
