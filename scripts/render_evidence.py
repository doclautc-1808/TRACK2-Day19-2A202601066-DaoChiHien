"""Render executed notebook outputs into compact PNG submission evidence."""
from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK_DIR = ROOT / "notebooks"
OUTPUT_DIR = ROOT / "submission" / "screenshots"
ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def output_text(notebook: Path) -> str:
    data = json.loads(notebook.read_text(encoding="utf-8"))
    chunks: list[str] = []
    for cell in data["cells"]:
        for output in cell.get("outputs", []):
            if output.get("output_type") == "stream":
                text = output.get("text", "")
            else:
                text = output.get("data", {}).get("text/plain", "")
            if isinstance(text, list):
                text = "".join(text)
            if text:
                chunks.append(ANSI.sub("", text).strip())
    return "\n\n".join(chunks)


def compact_lines(text: str, limit: int = 78) -> list[str]:
    raw = [line.rstrip() for line in text.splitlines()]
    if len(raw) > limit:
        raw = raw[:28] + ["... (output shortened; full output is in the .ipynb) ..."] + raw[-49:]
    wrapped: list[str] = []
    for line in raw:
        wrapped.extend(textwrap.wrap(line, width=108, replace_whitespace=False) or [""])
    return wrapped


def render(notebook: Path) -> Path:
    lines = compact_lines(output_text(notebook))
    title_font = ImageFont.truetype(FONT_PATH, 25)
    body_font = ImageFont.truetype(FONT_PATH, 16)
    line_height = 24
    width = 1900
    height = max(420, 105 + line_height * len(lines))
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, 72), fill="#17324d")
    draw.text((32, 20), f"Day 19 evidence — {notebook.name}", font=title_font, fill="white")
    draw.text((32, 84), "Executed notebook output", font=body_font, fill="#36566f")
    y = 116
    for line in lines:
        draw.text((32, y), line, font=body_font, fill="#17212b")
        y += line_height
    out = OUTPUT_DIR / f"{notebook.stem}_evidence.png"
    image.save(out, optimize=True)
    return out


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    notebooks = sorted(NOTEBOOK_DIR.glob("[0-9][0-9]_*.ipynb"))
    if len(notebooks) != 8:
        raise RuntimeError(f"expected 8 notebooks, found {len(notebooks)}")
    for notebook in notebooks:
        out = render(notebook)
        print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
