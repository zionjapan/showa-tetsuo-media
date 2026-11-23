# #35 作り直し（11/23）：蹴り→ダウン（カウント）→8で立つ→タックルに上から→白い光→ゲンコツ（揺れ）・3人抜き
import sys, random
sys.path.insert(0, '/tmp/claude-0/-home-claude/9d5ec005-9cc8-52f5-9eca-474a40bf5cb4/scratchpad')
import tt2
from tt2 import *
from PIL import Image, ImageDraw, ImageFont
P = '/home/claude/showa-tetsuo-media/posts/'
n = 35
tt2.TITLES[n] = '残り10秒、昭和ゲンコツ'
# (画像, 秒, 字幕, 残り秒の表示(始,終) or None, 揺れ)
# (画像, 秒, 字幕, ('clock',始,終) or ('count',始,終) or None, 揺れ)
SHOTS = [
    ('ep35/35-0_kick.png', 5.0, ['データ通りの', 'ハイキック'], None, False),
    ('ep35/35-1_hiza.png', 5.0, ['ダウン', 'データ通り、もう立てない'], ('count', 1, 7), False),
    ('ep35/35-1b_tatsu.png', 5.5, ['……立った!?', 'データにない', '残りの1.3%、それが昭和だ'], ('count', 8, 8), False),
    ('ep35/35-2a_tackle.png', 3.5, ['とどめのタックル', '……上ががら空きだ'], ('clock', 10, 2), False),
    ('ep35/35-2b_genkotsu.png', 5.0, ['昭和ゲンコツ！！', '3人抜き、達成'], ('clock', 1, 1), True),
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
f_cnt = ImageFont.truetype(F, 200)
def count(fr, c):
    d = ImageDraw.Draw(fr)
    lab = 'カウント'; d.text((CX - d.textlength(lab, font=f_clab) / 2, 250), lab, font=f_clab, fill=(255, 200, 60), stroke_width=5, stroke_fill='black')
    t = str(c); w = d.textlength(t, font=f_cnt)
    d.text((CX - w / 2, 290), t, font=f_cnt, fill=(255, 60, 60) if c >= 8 else 'white', stroke_width=10, stroke_fill='black')
out = fname(n); p = pipe(OUT + out)
fr = None
random.seed(1)
for si, (f, sec, lines, clk, shake) in enumerate(SHOTS):
    src = Image.open(P + f).convert('RGB'); nfr = int(sec * FPS)
    if si == 4:  # 当たる瞬間の白い光
        wht = Image.new('RGB', (W, H), 'white').tobytes()
        for _ in range(5): p.stdin.write(wht)
    for i in range(nfr):
        z = 1.0 + (0.18 if si == 3 else 0.10) * i / nfr
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
            kind, s0, s1 = clk
            if kind == 'clock':
                s = s0 - int((s0 - s1 + 1) * i / nfr) if s0 != s1 else s0
                clock(fr, max(s1, s))
            else:
                c = s0 + int((s1 - s0 + 1) * i / nfr) if s0 != s1 else s0
                count(fr, min(s1, c))
        shown = lines[:1 + min(len(lines) - 1, int(i / (nfr / len(lines))))]
        subs(d, lines, shown)
        p.stdin.write(fr.tobytes())
endcard(fr, p)
p.stdin.close(); p.wait(); print('done', out)
