"""python3 gen-icons.py  →  icons/ にPNG生成（pip3 install pillow）"""
from PIL import Image, ImageDraw, ImageFilter
import os, math

os.makedirs('icons', exist_ok=True)

def draw_icon(size):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ── 角丸マスク（iOS標準: 約22.5%）
    r = int(size * 0.225)

    # ── 背景グラデーション（左上 明るいティール → 右下 深いティール）
    for y in range(size):
        for x in range(size):
            t = (x + y) / (size * 2)
            rc = int(120 + (8   - 120) * t)   # 120 → 8
            gc = int(218 + (143 - 218) * t)   # 218 → 143
            bc = int(220 + (163 - 220) * t)   # 220 → 163
            img.putpixel((x, y), (rc, gc, bc, 255))

    # ── 左上からの白いシーン（光の当たり）
    shine = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shine)
    sd.ellipse([-size//3, -size//3, int(size*0.9), int(size*0.9)],
               fill=(255, 255, 255, 38))
    img = Image.alpha_composite(img, shine)

    # ── 角丸マスク適用
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, size-1, size-1], radius=r, fill=255)
    img.putalpha(mask)

    draw = ImageDraw.Draw(img)

    # ── チェックマーク座標
    pts = [
        (size * 0.22, size * 0.52),
        (size * 0.42, size * 0.70),
        (size * 0.78, size * 0.30),
    ]
    lw = max(int(size * 0.092), 5)

    # ドロップシャドウ（薄く）
    shadow_pts = [(x + size*0.018, y + size*0.022) for x, y in pts]
    draw.line(shadow_pts, fill=(0, 60, 80, 55), width=lw)

    # 白チェックマーク（端を丸く）
    draw.line(pts, fill=(255, 255, 255, 255), width=lw, joint='curve')

    return img

for s in [192, 512]:
    draw_icon(s).save(f'icons/icon-{s}.png')
    print(f'icons/icon-{s}.png 生成完了')
