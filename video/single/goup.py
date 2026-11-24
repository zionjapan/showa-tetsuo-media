# 単発：We could stay here or we could go up（11/24）既存の画像で無料。音はTikTokで元ネタの音を付ける
import sys
sys.path.insert(0, '/home/claude/showa-tetsuo-media/video/tt')
from tt2 import W, H, FPS, F, CX, fit, pipe
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
P = '/home/claude/showa-tetsuo-media/posts/'
OUT = '/home/claude/showa-tetsuo-media/video/single/goup.mp4'
SHOTS = [  # 画像, 秒, 字幕, 暗さ
    ('ep23/23-2_r3_boroboro.png', 2.6, ['負けた。', 'ここにいるか、'], 0.55),
    ('ep23/23-2_r3_boroboro.png', 1.6, ['上に行くか。'], 0.55),
    ('ep25/25-0_dawn_start.png', 1.3, [], 1.0),
    ('ep25/25-1_tire_run.png', 1.3, [], 1.0),
    ('ep26/26-0_sandbag.png', 1.3, [], 1.0),
    ('ep25/25-2_ishidan.png', 1.3, [], 1.0),
    ('ep26/26-1_mirror.png', 1.3, [], 1.0),
    ('ep25/25-3_ishidan_top.png', 3.2, ['上に行く。', '昭和の男だからな'], 1.0),
]
p = pipe(OUT)
for k, (f, sec, lines, br) in enumerate(SHOTS):
    src = Image.open(P + f).convert('RGB'); n = int(sec * FPS)
    for i in range(n):
        z = 1.0 + (0.12 if lines else 0.18) * i / n
        cs = max(W / src.width, H / src.height) * z
        im = src.resize((int(src.width * cs), int(src.height * cs)), Image.BILINEAR)
        cx = (im.width - W) // 2; cy = int((im.height - H) * 0.2)
        fr = im.crop((cx, cy, cx + W, cy + H))
        if br != 1.0: fr = ImageEnhance.Brightness(fr).enhance(br)
        d = ImageDraw.Draw(fr)
        shown = lines[:1 + min(len(lines) - 1, int(i / (n / max(1, len(lines)))))] if lines else []
        y = 1050
        for j, L in enumerate(shown):
            ft = fit(d, L, 96); tw = d.textlength(L, font=ft)
            col = (255, 214, 51) if (k == len(SHOTS) - 1 and j == 0) or k == 1 else 'white'
            d.text((CX - tw / 2, y), L, font=ft, fill=col, stroke_width=9, stroke_fill='black'); y += 130
        p.stdin.write(fr.tobytes())
p.stdin.close(); p.wait(); print('done', OUT)
