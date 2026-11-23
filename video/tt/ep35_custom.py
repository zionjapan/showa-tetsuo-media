# #35 作り直し（11/23）：蹴り→膝（残り10秒のカウント）→振り上げ→白い光→ゲンコツ（揺れ）→鬼塚
import sys, random
sys.path.insert(0, '/tmp/claude-0/-home-claude/9d5ec005-9cc8-52f5-9eca-474a40bf5cb4/scratchpad')
import tt2
from tt2 import *
from PIL import Image, ImageDraw, ImageFont
P = '/home/claude/showa-tetsuo-media/posts/'
n = 35
tt2.TITLES[n] = '残り10秒、昭和ゲンコツ'
# (画像, 秒, 字幕, 残り秒の表示(始,終) or None, 揺れ)
SHOTS = [
    ('ep35/35-0_kick.png', 5.0, ['データ通りの', 'ハイキック'], None, False),
    ('ep35/35-1_hiza.png', 6.0, ['データ通り、もう立てない', '……昭和を', 'なめんな'], (10, 5), False),
    ('ep35/35-2a_furiage.png', 3.0, ['とどめに飛び込む天才', '……待ってたぜ'], (4, 2), False),
    ('ep35/35-2b_genkotsu.png', 4.0, ['ゲンコツ！！'], (1, 1), True),
    ('ep35/35-3_kanaami_onizuka.png', 6.0, ['待ってろ、鬼塚', '次は、てめぇだ'], None, False),
]
f_clock = ImageFont.truetype(F, 120); f_clab = ImageFont.truetype(F, 44)
def clock(fr, sec):
    d = ImageDraw.Draw(fr)
    t = f'0:{sec:02d}'
    w = d.textlength(t, font=f_clock)
    d.rounded_rectangle((CX - w / 2 - 40, 250, CX + w / 2 + 40, 440), 24, fill=(0, 0, 0))
    lab = '残り'
    d.text((CX - d.textlength(lab, font=f_clab) / 2, 258), lab, font=f_clab, fill=(255, 200, 60))
    d.text((CX - w / 2, 300), t, font=f_clock, fill=(255, 60, 60) if sec <= 5 else 'white')
out = fname(n); p = pipe(OUT + out)
fr = None
random.seed(1)
for si, (f, sec, lines, clk, shake) in enumerate(SHOTS):
    src = Image.open(P + f).convert('RGB'); nfr = int(sec * FPS)
    if si == 3:  # 当たる瞬間の白い光
        wht = Image.new('RGB', (W, H), 'white').tobytes()
        for _ in range(5): p.stdin.write(wht)
    for i in range(nfr):
        z = 1.0 + (0.18 if si == 2 else 0.10) * i / nfr
        cs = max(W / src.width, H / src.height) * z
        im = src.resize((int(src.width * cs), int(src.height * cs)), Image.BILINEAR)
        cx = (im.width - W) // 2; cy = int((im.height - H) * 0.15)
        if shake and i < 18:
            a = int(30 * (1 - i / 18)); cx = max(0, min(im.width - W, cx + random.randint(-a, a))); cy = max(0, min(im.height - H, cy + random.randint(-a, a)))
        fr = im.crop((cx, cy, cx + W, cy + H)).convert('RGBA')
        if si == 0 and i < int(1.5 * FPS):
            big_title(fr, n); p.stdin.write(fr.convert('RGB').tobytes()); continue
        fr.alpha_composite(band(n)); fr = fr.convert('RGB')
        d = ImageDraw.Draw(fr)
        if clk:
            s0, s1 = clk; s = s0 - int((s0 - s1 + 1) * i / nfr) if s0 != s1 else s0
            clock(fr, max(s1, s))
        if si == 3:
            subs(d, lines, lines, size=120, lh=150)
        else:
            shown = lines[:1 + min(len(lines) - 1, int(i / (nfr / len(lines))))]
            subs(d, lines, shown)
        p.stdin.write(fr.tobytes())
endcard(fr, p)
p.stdin.close(); p.wait(); print('done', out)
