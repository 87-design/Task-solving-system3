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

    # 波のベースライン（上から60%）
    wave_y_base = size * 0.60
    amp = size * 0.042
    steps = size * 2

    # 波の輪郭ポイントを先に計算
    pts1 = []
    for i in range(steps + 1):
        x = i * size / steps
        y = (wave_y_base
             + amp * math.sin(2*math.pi * x/size * 1.7)
             + amp * 0.38 * math.sin(2*math.pi * x/size * 3.2 + 1.1))
        pts1.append((x, y))

    pts2 = []
    for i in range(steps + 1):
        x = i * size / steps
        y = (wave_y_base - size*0.065
             + amp * math.sin(2*math.pi * x/size * 1.6 + 0.85)
             + amp * 0.32 * math.sin(2*math.pi * x/size * 2.9 + 0.4))
        pts2.append((x, y))

    # ── 上半分：白
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, size, size], fill=(255, 255, 255, 255))

    # ── 下半分（波より下）：ティールグラデーション
    # 波の最小Y以下を塗る（行ごとに波のYを計算）
    wave_y_at_x = {}
    for i in range(steps + 1):
        x_idx = int(i * size / steps)
        y = (wave_y_base
             + amp * math.sin(2*math.pi * (i/steps) * 1.7)
             + amp * 0.38 * math.sin(2*math.pi * (i/steps) * 3.2 + 1.1))
        wave_y_at_x[x_idx] = y

    # 列ごとにグラデーション
    for x in range(size):
        wy = wave_y_at_x.get(x, wave_y_base)
        for y in range(int(wy), size):
            t = (y - wy) / (size - wy + 1)
            rc = int(round(80  * (1-t) + 6   * t))
            gc = int(round(200 * (1-t) + 138 * t))
            bc = int(round(220 * (1-t) + 160 * t))
            img.putpixel((x, y), (rc, gc, bc, 255))

    img.putalpha(mask)

    # ── 波レイヤー（輝線と奥の波）
    wave_layer = Image.new('RGBA', (size, size), (0,0,0,0))
    wd = ImageDraw.Draw(wave_layer)
    lw_wave = max(2, size // 85)

    # 奥の波（薄い白塗り）
    poly2 = list(pts2) + [(size, size), (0, size)]
    wd.polygon(poly2, fill=(255, 255, 255, 30))
    wd.line(pts2, fill=(255, 255, 255, 100), width=max(1, lw_wave-1))

    # 手前の波輝線
    wd.line(pts1, fill=(255, 255, 255, 180), width=lw_wave)

    r_ch, g_ch, b_ch, a_ch = wave_layer.split()
    new_a = Image.new('L', (size, size), 0)
    new_a.paste(a_ch, mask=mask)
    wave_layer.putalpha(new_a)
    img = Image.alpha_composite(img, wave_layer)

    # ── チェックマーク（白エリア上部に）
    draw = ImageDraw.Draw(img)
    pts = [
        (size * 0.190, size * 0.330),
        (size * 0.385, size * 0.515),
        (size * 0.800, size * 0.115),
    ]
    lw = max(int(size * 0.082), 4)
    shd = [(x + size*.016, y + size*.020) for x, y in pts]
    draw.line(shd, fill=(10, 143, 163, 55), width=lw+2)
    draw.line(pts, fill=(10, 143, 163, 60), width=lw+7)
    draw.line(pts, fill=(10, 143, 163, 255), width=lw)

    img.putalpha(mask)
    return img

for s in [192, 512]:
    draw_icon(s).save(f'icons/icon-{s}.png')
    print(f'icons/icon-{s}.png 生成完了')
