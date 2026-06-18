"""python3 gen-icons.py  →  icons/ にPNG生成（pip3 install pillow）"""
from PIL import Image, ImageDraw
import os, math

os.makedirs('icons', exist_ok=True)

def draw_icon(size):
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    r = int(size * 0.225)

    # ── 背景グラデーション（左上の明るいシアン → 右下の深いティール）
    for y in range(size):
        for x in range(size):
            # 対角方向 t: 0.0(左上) → 1.0(右下)
            t = (x + y) / (size * 2.0)
            rc = int(round(148 * (1-t) + 8   * t))
            gc = int(round(224 * (1-t) + 143 * t))
            bc = int(round(232 * (1-t) + 163 * t))
            img.putpixel((x, y), (rc, gc, bc, 255))

    # ── 角丸マスク
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,size-1,size-1], radius=r, fill=255)
    img.putalpha(mask)

    draw = ImageDraw.Draw(img)

    # ── ガラス光沢レイヤー1: 左上の大きな白い楕円ハイライト
    shine = Image.new('RGBA', (size, size), (0,0,0,0))
    sd = ImageDraw.Draw(shine)
    cx, cy = int(size*.30), int(size*.22)
    for step in range(60):
        prog = step / 60
        alpha = int(52 * (1 - prog)**2)
        rx = int(size * (.55 - prog*.30))
        ry = int(size * (.38 - prog*.22))
        sd.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=(255,255,255,alpha))
    img = Image.alpha_composite(img, shine)

    # ── ガラス光沢レイヤー2: 上部の細い白いハイライト帯
    for y2 in range(int(size*.18)):
        t2 = y2 / (size*.18)
        alpha = int(38 * (1-t2)**2)
        draw2 = ImageDraw.Draw(img)
        draw2.rectangle([0, y2, size, y2], fill=(255,255,255,alpha))

    # ── 角丸マスク再適用（光沢描画後）
    img.putalpha(mask)
    draw = ImageDraw.Draw(img)

    # ── チェックマーク
    pts = [
        (size * 0.215, size * 0.520),
        (size * 0.415, size * 0.705),
        (size * 0.785, size * 0.298),
    ]
    lw = max(int(size * 0.088), 5)

    # ドロップシャドウ
    shd = [(x + size*.020, y + size*.024) for x,y in pts]
    draw.line(shd, fill=(0, 55, 75, 60), width=lw+2)

    # 白チェック本体
    draw.line(pts, fill=(255, 255, 255, 255), width=lw)

    # 白いグロー（重ねて柔らかく）
    draw.line(pts, fill=(255, 255, 255, 90), width=lw+4)
    draw.line(pts, fill=(255, 255, 255, 255), width=lw)

    return img

for s in [192, 512]:
    draw_icon(s).save(f'icons/icon-{s}.png')
    print(f'icons/icon-{s}.png 生成完了')
