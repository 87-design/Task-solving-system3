"""python3 gen-icons.py  →  icons/ にPNG生成（pip3 install pillow）"""
from PIL import Image, ImageDraw
import os, math

os.makedirs('icons', exist_ok=True)

def draw_icon(size):
    img = Image.new('RGBA', (size, size), (0,0,0,0))
    r = int(size * 0.225)

    # ── 角丸マスク
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,size-1,size-1], radius=r, fill=255)

    # 波のベースライン（上から38% — チェックマーク最上部のすぐ上）
    wave_y_base = size * 0.18
    amp         = size * 0.044
    steps       = size * 2

    # 波の輪郭ポイント（手前の波）
    pts1 = []
    for i in range(steps + 1):
        x = i * size / steps
        y = (wave_y_base
             + amp * math.sin(2*math.pi * x/size * 1.7)
             + amp * 0.38 * math.sin(2*math.pi * x/size * 3.2 + 1.1))
        pts1.append((x, y))

    # 奥の波
    pts2 = []
    for i in range(steps + 1):
        x = i * size / steps
        y = (wave_y_base - size*0.030
             + amp * math.sin(2*math.pi * x/size * 1.6 + 0.85)
             + amp * 0.32 * math.sin(2*math.pi * x/size * 2.9 + 0.4))
        pts2.append((x, y))

    draw = ImageDraw.Draw(img)

    # ── 背景：全体白
    draw.rectangle([0, 0, size, size], fill=(255, 255, 255, 255))

    # ── 波より下：ティールグラデーション（列ごと）
    wave_y_at_x = {}
    for i in range(steps + 1):
        x_idx = min(size-1, int(i * size / steps))
        y = (wave_y_base
             + amp * math.sin(2*math.pi * (i/steps) * 1.7)
             + amp * 0.38 * math.sin(2*math.pi * (i/steps) * 3.2 + 1.1))
        wave_y_at_x[x_idx] = y

    for x in range(size):
        wy = wave_y_at_x.get(x, wave_y_base)
        for y in range(int(wy), size):
            t = (y - wy) / max(1, size - wy)
            rc = int(round(90  * (1-t) + 6   * t))
            gc = int(round(205 * (1-t) + 138 * t))
            bc = int(round(222 * (1-t) + 160 * t))
            img.putpixel((x, y), (rc, gc, bc, 255))

    img.putalpha(mask)

    # ── 波レイヤー
    wave_layer = Image.new('RGBA', (size, size), (0,0,0,0))
    wd = ImageDraw.Draw(wave_layer)
    lw_wave = max(2, size // 85)

    poly2 = list(pts2) + [(size, size), (0, size)]
    wd.polygon(poly2, fill=(255, 255, 255, 32))
    wd.line(pts2, fill=(255, 255, 255, 110), width=max(1, lw_wave-1))
    wd.line(pts1, fill=(255, 255, 255, 190), width=lw_wave)

    r_ch, g_ch, b_ch, a_ch = wave_layer.split()
    new_a = Image.new('L', (size, size), 0)
    new_a.paste(a_ch, mask=mask)
    wave_layer.putalpha(new_a)
    img = Image.alpha_composite(img, wave_layer)

    # ── チェックマーク（アイコン中央、濃いグレー、丸み付き）
    draw = ImageDraw.Draw(img)
    # 重心を(50%, 60%)に配置
    pts = [
        (size * 0.210, size * 0.590),
        (size * 0.415, size * 0.778),
        (size * 0.790, size * 0.402),
    ]
    lw = max(int(size * 0.090), 4)
    col = (65, 65, 65, 255)
    # 丸みを出すため各頂点に円を描画
    r_cap = lw // 2
    draw.line(pts, fill=col, width=lw)
    for px, py in pts:
        draw.ellipse([px-r_cap, py-r_cap, px+r_cap, py+r_cap], fill=col)

    img.putalpha(mask)
    return img

for s in [192, 512]:
    draw_icon(s).save(f'icons/icon-{s}.png')
    print(f'icons/icon-{s}.png 生成完了')
