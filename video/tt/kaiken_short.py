# 会見の悪口合戦ショート（UFC Reimagined型：1単語ずつ字幕）
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from bd_fx import *
from PIL import Image, ImageDraw, ImageFont
P = R + 'posts/'
OUT = R + 'video/tt/kaiken_buzuto_v1.mp4'
TMP = os.path.join(os.path.dirname(__file__), 'kk_frames'); os.makedirs(TMP, exist_ok=True)
for f in os.listdir(TMP): os.remove(os.path.join(TMP, f))

EMO = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf', 109)
PINK, GREEN, YEL = (255, 70, 200), (90, 255, 90), (255, 220, 40)

def emoji(ch, size):
    im = Image.new('RGBA', (136, 128), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((0, 0), ch, font=EMO, embedded_color=True)
    return im.resize((int(136 * size / 128), size))

def topbar(fr):
    d = ImageDraw.Draw(fr)
    f = F(GB, 74); t = '会見が荒れた'
    w = d.textlength(t, font=f); x = (W - w - 90) / 2
    d.text((x, 150), t, font=f, fill=YEL, stroke_width=8, stroke_fill='black')
    e = emoji('😂', 80); fr.paste(e, (int(x + w + 10), 155), e)

def word(fr, ws, k, col, y=1120):
    # それまでの単語を残して行を作る。今の単語だけ色つき、前の単語は白
    d = ImageDraw.Draw(fr); f = F(GB, 120); lines = [[]]; 
    for i, t in enumerate(ws[:k + 1]):
        cur = ''.join(x for x, _ in lines[-1]) + t
        if lines[-1] and d.textlength(cur, font=f) > W - 80: lines.append([])
        lines[-1].append((t, i))
    for li, ln in enumerate(lines):
        tw = sum(d.textlength(t, font=f) for t, _ in ln); x = (W - tw) / 2
        for t, i in ln:
            d.text((x, y + li * 150), t, font=f, fill=col if i == k else 'white', stroke_width=12, stroke_fill='black')
            x += d.textlength(t, font=f)

def zoom(src, t, z0, z1, cx, cy):
    z = z0 + (z1 - z0) * t
    w, h = int(src.width / z), int(src.height / z)
    x = int((src.width - w) * cx); y = int((src.height - h) * cy)
    return cover(src.crop((x, y, x + w, y + h)), W, H)

frames = []
def add(img): frames.append(img)

kai = Image.open(P + 'ep28/28-1_kaiken.png').convert('RGB')
lines = [
    # (セリフの単語, 色, ズーム中心x, y)  バズ斗→鉄男
    (['おいジジイ', '100万人の前で', '泣かせて', 'やるよ'], PINK, 1.0, 0.0),
    (['ヒヨッコが', '板っきれ越しじゃ', 'ねぇと', '目も合わせ', 'られねぇのか'], GREEN, 0.0, 0.2),
    (['は？', '老害は', '帰って寝ろ'], PINK, 1.0, 0.0),
    (['47年', '早ぇんだよ'], YEL, 0.0, 0.2),
]
for li, (ws, col, cx, cy) in enumerate(lines):
    per = 24  # 1単語の長さ（フレーム）
    n = per * len(ws) + 30
    for i in range(n):
        z0,z1=(1.0,1.12) if cx>0.5 else (1.25,1.45)
        fr = zoom(kai, i / n, z0, z1, cx, cy); topbar(fr)
        k = min(i // per, len(ws) - 1); word(fr, ws, k, col)
        add(fr)
# 締め：対戦ポスター＋煽り
pos = Image.open(P + 'ep28/vs_buzuto.png').convert('RGB')
for i in range(int(2.2 * FPS)):
    fr = pos.copy(); d = ImageDraw.Draw(fr)
    pass
    add(fr)
for i, fr in enumerate(frames): fr.save(f'{TMP}/{i:04d}.jpg', quality=90)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{TMP}/%04d.jpg',
                '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo', '-shortest',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', OUT], check=True)
print(OUT, len(frames) / FPS)
