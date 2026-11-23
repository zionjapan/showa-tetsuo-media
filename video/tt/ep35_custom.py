# #35 作り直し（11/23）：蹴り→ダウン（カウント）→8で立つ→タックル（拳をためる）→白い光＋「昭和ゲンコツ！！」→KO後（拳を突き上げる）・3人抜き
import sys, random
sys.path.insert(0, '/tmp/claude-0/-home-claude/9d5ec005-9cc8-52f5-9eca-474a40bf5cb4/scratchpad')
import tt2
from tt2 import *
from PIL import Image, ImageDraw, ImageFont
P = '/home/claude/showa-tetsuo-media/posts/'
n = 35
tt2.TITLES[n] = '残り10秒、昭和ゲンコツ'
# 時間は実際の秒どおり：カウントは1秒に1つ、試合時計は立ち上がって再開してから1秒に1つ減り、KOの瞬間に止まる
# (画像, 秒, 字幕, 'count'/'tatsu'/'clock'/'ko'/None, 揺れ)
SHOTS = [
    ('ep35/35-0_kick.png', 4.0, ['データ通りの', 'ハイキック'], 'kick', False),
    ('ep35/35-1_hiza.png', 7.0, ['ダウン', 'データ通り、もう立てない'], 'count', False),
    ('ep35/35-1b_tatsu.png', 5.0, ['……立った!?', 'データにない', '残りの1.3%、それが昭和だ'], 'tatsu', False),
    ('ep35/35-2a_tackle.png', 4.0, ['とどめのタックル', '……顔ががら空きだ'], 'clock', False),
    ('ep35/35-2c_ko.png', 4.0, ['KO！！', '3人抜き、達成'], 'ko', True),
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
    lab = 'カウント'; d.text((CX - d.textlength(lab, font=f_clab) / 2, 470), lab, font=f_clab, fill=(255, 200, 60), stroke_width=5, stroke_fill='black')
    t = str(c); w = d.textlength(t, font=f_cnt)
    d.text((CX - w / 2, 510), t, font=f_cnt, fill=(255, 60, 60) if c >= 8 else 'white', stroke_width=10, stroke_fill='black')
out = fname(n); p = pipe(OUT + out)
fr = None
random.seed(1)
for si, (f, sec, lines, clk, shake) in enumerate(SHOTS):
    src = Image.open(P + f).convert('RGB'); nfr = int(sec * FPS)
    if si == 4:  # 当たる瞬間の白い光
        wht = Image.new('RGB', (W, H), 'white').tobytes()
        for _ in range(4): p.stdin.write(wht)
        card = Image.new('RGB', (W, H), (0, 0, 0)); dc = ImageDraw.Draw(card)
        for k, (t_, sz_, c_) in enumerate([('昭和', 170, 'white'), ('ゲンコツ！！', 190, (255, 60, 60))]):
            ff = ImageFont.truetype(F, sz_); ww = dc.textlength(t_, font=ff)
            while ww > 1000: sz_ -= 10; ff = ImageFont.truetype(F, sz_); ww = dc.textlength(t_, font=ff)
            dc.text(((W - ww) / 2, 700 + k * 240), t_, font=ff, fill=c_, stroke_width=10, stroke_fill='black')
        for j in range(21):
            a_ = int(24 * (1 - j / 21)); sh = card.transform((W, H), Image.AFFINE, (1, 0, random.randint(-a_, a_), 0, 1, random.randint(-a_, a_)))
            p.stdin.write(sh.tobytes())
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
        t = i / FPS
        # 試合の時計は止まらずに1秒ずつ減り続ける。ダウン中も進み、立った時がちょうど残り10秒、KOの0:02で止まる
        if clk == 'kick':
            if si != 0 or i >= int(1.5 * FPS): clock(fr, 22 - int(t))
        elif clk == 'count':
            clock(fr, 18 - int(t)); count(fr, min(7, 1 + int(t)))
        elif clk == 'tatsu':
            clock(fr, 11 - int(t))
            if t < 1: count(fr, 8)
        elif clk == 'clock':
            clock(fr, 6 - int(t))
        elif clk == 'ko':
            clock(fr, 2)
        shown = lines[:1 + min(len(lines) - 1, int(i / (nfr / len(lines))))]
        subs(d, lines, shown)
        p.stdin.write(fr.tobytes())
endcard(fr, p)
p.stdin.close(); p.wait(); print('done', out)
