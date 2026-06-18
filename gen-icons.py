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

    # ── 背景グラデーション（上：明るいシアン → 下：深いティール）
    draw = ImageDraw.Draw(img)
    for y in range(size):
        t = y / size
        rc = int(round(100 * (1-t) + 6   * t))
        gc = int(round(210 * (1-t) + 138 * t))
        bc = int(round(225 * (1-t) + 160 * t))
        draw.rectangle([0, y, size, y], fill=(rc, gc, bc, 255))
    img.putalpha(mask)

    # ── 波レイヤー（角丸マスクを考慮して別画像で作りcomposite）
    wave_layer = Image.new('RGBA', (size, size), (0,0,0,0))
    wd = ImageDraw.Draw(wave_layer)
    steps = size * 2
    wave_y_base = size * 0.72
    amp = size * 0.042

    # 波1（手前・濃い目）
    pts1 = []
    for i in range(steps + 1):
        x = i * size / steps
        y = (wave_y_base
             + amp * math.sin(2*math.pi * x/size * 1.7)
             + amp * 0.38 * math.sin(2*math.pi * x/size * 3.2 + 1.1))
        pts1.append((x, y))
    poly1 = list(pts1) + [(size, size), (0, size)]
    wd.polygon(poly1, fill=(255, 255, 255, 55))

    # 波2（奥・薄め）
    pts2 = []
    for i in range(steps + 1):
        x = i * size / steps
        y = (wave_y_base - size*0.065
             + amp * math.sin(2*math.pi * x/size * 1.6 + 0.85)
             + amp * 0.32 * math.sin(2*math.pi * x/size * 2.9 + 0.4))
        pts2.append((x, y))
    poly2 = list(pts2) + [(size, size), (0, size)]
    wd.polygon(poly2, fill=(255, 255, 255, 28))

    # 波の輝線
    lw_wave = max(2, size // 85)
    wd.line(pts1, fill=(255, 255, 255, 150), width=lw_wave)
    wd.line(pts2, fill=(255, 255, 255,  85), width=max(1, lw_wave-1))

    # 波レイヤーをマスクで切り抜いてcomposite
    r_ch, g_ch, b_ch, a_ch = wave_layer.split()
    new_a = Image.new('L', (size, size), 0)
    new_a.paste(a_ch, mask=mask)
    wave_layer.putalpha(new_a)
    img = Image.alpha_composite(img, wave_layer)

    # ── 上部ガラス光沢
    shine = Image.new('RGBA', (size, size), (0,0,0,0))
    sd = ImageDraw.Draw(shine)
    cx, cy = int(size*.27), int(size*.19)
    for step in range(55):
        prog = step / 55
        alpha = int(46 * (1 - prog)**2.3)
        rx = int(size * (.50 - prog*.30))
        ry = int(size * (.34 - prog*.20))
        if rx > 0 and ry > 0:
            sd.ellipse([cx-rx, cy-ry, cx+rx, cy+ry], fill=(255,255,255,alpha))
    img = Image.alpha_composite(img, shine)
    img.putalpha(mask)

    # ── チェックマーク（波より上のエリアに）
    draw = ImageDraw.Draw(img)
    pts = [
        (size * 0.210, size * 0.460),
        (size * 0.400, size * 0.635),
        (size * 0.788, size * 0.252),
    ]
    lw = max(int(size * 0.082), 4)
    shd = [(x + size*.018, y + size*.022) for x, y in pts]
    draw.line(shd, fill=(0, 55, 75, 55), width=lw+2)
    draw.line(pts, fill=(255, 255, 255, 75), width=lw+7)
    draw.line(pts, fill=(255, 255, 255, 255), width=lw)

    return img

for s in [192, 512]:
    draw_icon(s).save(f'icons/icon-{s}.png')
    print(f'icons/icon-{s}.png 生成完了')
