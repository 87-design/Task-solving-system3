"""
python3 gen-icons.py  →  icons/ フォルダにPNGを生成
依存: pip3 install pillow
"""
from PIL import Image, ImageDraw
import os, math

os.makedirs('icons', exist_ok=True)

def draw_icon(size):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    r = int(size * 0.22)

    # 背景グラデーション（薄いミントグリーン）
    # Pillowに線形グラデはないので縦方向に1行ずつ描く
    top_col    = (183, 238, 230)  # #B7EEE6
    bottom_col = (157, 214, 221)  # #9FD6DD
    for y in range(size):
        t = y / size
        rc = int(top_col[0] + (bottom_col[0] - top_col[0]) * t)
        gc = int(top_col[1] + (bottom_col[1] - top_col[1]) * t)
        bc = int(top_col[2] + (bottom_col[2] - top_col[2]) * t)
        draw.rectangle([0, y, size - 1, y], fill=(rc, gc, bc, 255))

    # 角丸マスクをかける
    mask = Image.new('L', (size, size), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=255)
    img.putalpha(mask)

    # チェックマーク（黄色）
    # 座標: 左下から右上へ
    lw = max(int(size * 0.085), 4)
    pts = [
        (size * 0.22, size * 0.52),
        (size * 0.42, size * 0.70),
        (size * 0.78, size * 0.30),
    ]
    yellow = (255, 213, 50, 255)  # #FFD532

    # アンチエイリアス的に太さを出すために少しずつずらして重ね描き
    for offset in [(-1, -1), (1, -1), (-1, 1), (1, 1), (0, 0)]:
        shifted = [(x + offset[0], y + offset[1]) for x, y in pts]
        draw.line(shifted, fill=yellow, width=lw, joint='curve')

    return img

for s in [192, 512]:
    img = draw_icon(s)
    img.save(f'icons/icon-{s}.png')
    print(f'icons/icon-{s}.png 生成完了')
