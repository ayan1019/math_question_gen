# src/image_utils.py
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for scripts
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def draw_packed_balls(rows: int, cols: int, radius_cm: float, out_path: str, scale_px_per_cm: int = 30):
    """
    Draws a top-view of equally sized circles packed in rows x cols.
    radius_cm: radius in centimeters (keeps math clear)
    scale_px_per_cm: scaling to convert cm to pixels (visual size)
    """
    r_px = radius_cm * scale_px_per_cm
    width_px = int(cols * 2 * r_px)
    height_px = int(rows * 2 * r_px)
    fig, ax = plt.subplots(figsize=(width_px/100, height_px/100), dpi=100)
    ax.set_xlim(0, width_px)
    ax.set_ylim(0, height_px)
    ax.set_aspect("equal")
    ax.axis("off")
    # draw circles
    for row in range(rows):
        for col in range(cols):
            cx = col * 2 * r_px + r_px
            # invert row so top row appears at top of image
            cy = (rows - 1 - row) * 2 * r_px + r_px
            circ = plt.Circle((cx, cy), r_px, fill=False, linewidth=1)
            ax.add_artist(circ)
    # border
    rect = plt.Rectangle((0,0), width_px, height_px, fill=False, linewidth=1)
    ax.add_artist(rect)
    plt.tight_layout(pad=0)
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_path, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)

def draw_uniform_table(shirt_colors, pant_colors, out_path: str):
    """
    Creates a simple image showing a table of shirt/pant choices. Useful for Q1-like visuals.
    """
    # simple canvas
    font_size = 16
    padding = 12
    col_width = 180
    rows = max(len(shirt_colors), len(pant_colors)) + 1
    width = col_width * 2 + padding * 2
    height = rows * (font_size + 14) + padding * 2
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("Arial.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()

    # header
    draw.text((padding + 10, padding), "Shirt Color", fill="black", font=font)
    draw.text((padding + col_width + 10, padding), "Pants Color", fill="black", font=font)
    y = padding + font_size + 8
    for i in range(max(len(shirt_colors), len(pant_colors))):
        s = shirt_colors[i] if i < len(shirt_colors) else ""
        p = pant_colors[i] if i < len(pant_colors) else ""
        draw.text((padding + 10, y), s, fill="black", font=font)
        draw.text((padding + col_width + 10, y), p, fill="black", font=font)
        y += font_size + 8
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path)
