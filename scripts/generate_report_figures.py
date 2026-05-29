"""
Generate reference PNGs for report figures 2.8.5.1–2.8.5.4 (code + dataset tree).
Replace with real Cursor/browser screenshots when preparing final Word document.

Usage:
  python scripts/generate_report_figures.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "figures" / "2.8.5"
FONT = ImageFont.load_default()
LINE_H = 16
PAD = 12
MAX_W = 1100


def _font(size: int = 14):
    try:
        return ImageFont.truetype("consola.ttf", size)
    except OSError:
        try:
            return ImageFont.truetype("C:/Windows/Fonts/consola.ttf", size)
        except OSError:
            return ImageFont.load_default()


def render_text_image(title: str, lines: list[str], out: Path) -> None:
    font = _font(13)
    title_font = _font(15)
    w = MAX_W
    h = PAD * 2 + 24 + len(lines) * LINE_H + 8
    img = Image.new("RGB", (w, h), "#1e1e1e")
    draw = ImageDraw.Draw(img)
    draw.text((PAD, PAD), title, fill="#4ec9b0", font=title_font)
    y = PAD + 28
    for line in lines:
        draw.text((PAD, y), line, fill="#d4d4d4", font=font)
        y += LINE_H
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    print(f"Wrote {out}")


def snippet_file(path: Path, start: int, end: int, title: str, out_name: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    body = []
    for i in range(start - 1, min(end, len(lines))):
        body.append(f"{i + 1:4}  {lines[i]}")
    render_text_image(title, body, OUT / out_name)


def dataset_tree() -> None:
    tree = [
        "dataset/",
        "├── disease/",
        "│   ├── train/",
        "│   │   ├── healthy/      (ảnh mẫu: sample_001.jpg)",
        "│   │   ├── leaf_spot/",
        "│   │   └── anthracnose/",
        "│   ├── val/",
        "│   └── test/",
        "├── ripeness/",
        "│   ├── train/",
        "│   │   ├── unripe/",
        "│   │   ├── half_ripe/",
        "│   │   └── ripe/",
        "│   └── val/",
        "├── DATASET.md",
        "└── metadata.csv",
    ]
    render_text_image("Hinh 2.8.5.1 — Cau truc dataset", tree, OUT / "Hinh_2_8_5_1_dataset.png")


def main() -> None:
    dataset_tree()
    snippet_file(
        ROOT / "ml" / "train.py",
        21,
        52,
        "Hinh 2.8.5.2 — ml/train.py (build_model, DataLoader)",
        "Hinh_2_8_5_2_train.png",
    )
    snippet_file(
        ROOT / "ml" / "train.py",
        104,
        126,
        "Hinh 2.8.5.2 — ml/train.py (luu checkpoint)",
        "Hinh_2_8_5_2_train_epoch.png",
    )
    snippet_file(
        ROOT / "ml" / "inference.py",
        31,
        62,
        "Hinh 2.8.5.3 — ml/inference.py (predict)",
        "Hinh_2_8_5_3_inference.png",
    )
    snippet_file(
        ROOT / "backend" / "app" / "services" / "inference.py",
        78,
        102,
        "Hinh 2.8.5.3 — backend/services/inference.py",
        "Hinh_2_8_5_3_inference_service.png",
    )
    snippet_file(
        ROOT / "backend" / "app" / "main.py",
        22,
        50,
        "Hinh 2.8.5.4 — backend/app/main.py",
        "Hinh_2_8_5_4_fastapi_main.png",
    )
    snippet_file(
        ROOT / "backend" / "app" / "routers" / "analyze.py",
        22,
        50,
        "Hinh 2.8.5.4 — routers/analyze.py",
        "Hinh_2_8_5_4_fastapi_analyze.png",
    )
    web_guide_5 = [
        "Hinh 2.8.5.5 — Test Web (truoc phan tich)",
        "",
        "1. Mo http://localhost:5173/analyze",
        "2. Dang nhap tai /login",
        "3. Chon anh — thay preview",
        "4. Chup man hinh TRUOC khi bam 'Chay phan tich AI'",
        "",
        "Thay file nay bang screenshot that khi nop bao cao.",
    ]
    web_guide_6 = [
        "Hinh 2.8.5.6 — Test Web (sau phan tich)",
        "",
        "1. Bam 'Chay phan tich AI'",
        "2. Thay anh + vung mau xanh/cam/do",
        "3. Thay chi so va khuyen nghi",
        "",
        "Backend phai chay: uvicorn port 8000",
    ]
    render_text_image("Web GUI", web_guide_5, OUT / "Hinh_2_8_5_5_web_gui_PLACEHOLDER.png")
    render_text_image("Web ket qua", web_guide_6, OUT / "Hinh_2_8_5_6_web_ket_qua_PLACEHOLDER.png")
    print("Done. Replace PLACEHOLDER web PNGs with real screenshots from /analyze")


if __name__ == "__main__":
    main()
