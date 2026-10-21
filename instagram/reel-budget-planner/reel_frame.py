"""Place images on a 1080x1920 Instagram Reel canvas with a glowing orange frame.

Usage: python3 reel_frame.py OUT_DIR IMG1 [IMG2 ...]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

W, H = 1080, 1920
# Instagram Reel UI overlays: top bar, bottom caption/audio area, right-side buttons.
SAFE_TOP, SAFE_BOTTOM, SAFE_SIDE = 250, 420, 130
BG_TOP, BG_BOTTOM = (18, 14, 12), (6, 5, 5)
ORANGE = (255, 140, 26)        # bright brand-like orange for the frame
GLOW = (255, 120, 0)
STROKE, RADIUS, PAD = 8, 44, 10  # frame thickness, corner radius, gap image↔frame


def background():
    bg = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOTTOM)))
    # soft orange ambient glow behind the frame
    halo = Image.new("L", (W, H), 0)
    ImageDraw.Draw(halo).ellipse((W * 0.1, H * 0.25, W * 0.9, H * 0.7), fill=70)
    halo = halo.filter(ImageFilter.GaussianBlur(160))
    return Image.composite(Image.new("RGB", (W, H), GLOW), bg, halo)


def rounded_mask(size, r):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255)
    return m


def frame(src):
    img = Image.open(src).convert("RGB")
    max_w = W - 2 * SAFE_SIDE - 2 * (PAD + STROKE)
    max_h = H - SAFE_TOP - SAFE_BOTTOM - 2 * (PAD + STROKE)
    s = min(max_w / img.width, max_h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)

    x0 = (W - img.width) // 2
    y0 = SAFE_TOP + PAD + STROKE + (max_h - img.height) // 2
    box = (x0 - PAD - STROKE, y0 - PAD - STROKE, x0 + img.width + PAD + STROKE, y0 + img.height + PAD + STROKE)

    canvas = background()

    # neon glow: stacked blurred strokes, wide & faint -> tight & bright
    for blur, width, alpha in ((60, 40, 150), (28, 22, 200), (10, 12, 255)):
        layer = Image.new("L", (W, H), 0)
        ImageDraw.Draw(layer).rounded_rectangle(box, RADIUS + PAD, outline=alpha, width=width)
        layer = layer.filter(ImageFilter.GaussianBlur(blur))
        canvas = Image.composite(Image.new("RGB", (W, H), GLOW), canvas, layer)

    # dark plate inside the frame, then the image with rounded corners
    ImageDraw.Draw(canvas).rounded_rectangle(box, RADIUS + PAD, fill=(10, 8, 8))
    canvas.paste(img, (x0, y0), rounded_mask(img.size, RADIUS))

    # crisp stroke + thin hot-white core for the "lit" look
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle(box, RADIUS + PAD, outline=ORANGE, width=STROKE)
    inset = STROKE // 2 - 1
    d.rounded_rectangle((box[0] + inset, box[1] + inset, box[2] - inset, box[3] - inset),
                        RADIUS + PAD - inset, outline=(255, 214, 160), width=2)
    return canvas


if __name__ == "__main__":
    out_dir, srcs = sys.argv[1], sys.argv[2:]
    os.makedirs(out_dir, exist_ok=True)
    for i, src in enumerate(srcs, 1):
        out = os.path.join(out_dir, f"reel_{i:02d}.png")
        frame(src).save(out, optimize=True)
        print(out)
