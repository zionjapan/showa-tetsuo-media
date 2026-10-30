# YouTube用 v3：オチを1秒目から出す・ドンと寄る・効果音つき・約7秒
from PIL import Image, ImageDraw, ImageFont
import subprocess, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'render.py')).read().split('def run')[0]
_ns={}; exec(_src,_ns); C=_ns['C']; R=_ns['R']
W, H, FPS = 1080, 1920, 30
F = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
OUT = R + 'video/yt_v3/'; os.makedirs(OUT, exist_ok=True)
SFX = OUT + '_sfx.wav'
if not os.path.exists(SFX):
    # ドン（低音＋ノイズ）→ 余韻。全部 ffmpeg で合成（無料）
    subprocess.run(['ffmpeg', '-v', 'error', '-y',
        '-f', 'lavfi', '-i', 'sine=f=55:d=0.9', '-f', 'lavfi', '-i', 'anoisesrc=d=0.25:c=brown:a=0.9',
        '-f', 'lavfi', '-i', 'sine=f=880:d=0.15', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=stereo',
        '-filter_complex',
        '[0]volume=2.2,afade=t=out:st=0.05:d=0.85[a];[1]afade=t=out:st=0:d=0.25,volume=0.8[b];'
        '[2]volume=0.15,adelay=4300|4300[c];[3]atrim=0:8[s];'
        '[a][b]amix=2:normalize=0[ab];[s][ab][c]amix=3:normalize=0,atrim=0:8',
        '-ar', '44100', '-ac', '2', SFX], check=True)

def font(s): return ImageFont.truetype(F, s)

def fit(d, t, s, maxw=1000):
    f = font(s)
    while d.textlength(t, font=f) > maxw: s -= 4; f = font(s)
    return f

def run(c):
    num, name, img, ax, hook, lines = c
    src = Image.open(R + 'posts/stock/' + img).convert('RGB')
    tmp = OUT + f'_{name}.mp4'; out = OUT + f'{name}.mp4'
    MAIN, END = 6.0, 1.3
    p = subprocess.Popen(['ffmpeg', '-nostdin', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', tmp], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    n = int(MAIN * FPS); clean = None
    for i in range(n):
        t = i / FPS
        # 0〜0.35秒でドンと寄る（1.28→1.06）、その後ゆっくり寄り続ける
        z = 1.28 - 0.22 * min(t / 0.35, 1) ** 0.5 + 0.06 * t / MAIN
        sh = int(18 * math.sin(t * 70) * max(0, 1 - t / 0.4))  # 揺れ
        cs = max(W / src.width, H / src.height) * z
        im = src.resize((int(src.width * cs), int(src.height * cs)), Image.BILINEAR)
        cx = int((im.width - W) * ax) + sh; cy = int((im.height - H) * 0.15)
        cx = max(0, min(cx, im.width - W))
        fr = im.crop((cx, cy, cx + W, cy + H)).convert('RGBA'); clean = fr
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        # 上：お題（最初から出す）
        d.rectangle((0, 170, W, 330), fill=(0, 0, 0, 170))
        f = fit(d, hook, 64); tw = d.textlength(hook, font=f)
        d.text(((W - tw) / 2, 205), hook, font=f, fill=(255, 210, 74), stroke_width=4, stroke_fill='black')
        # 下：セリフ（オチ）を最初から全部出す。最後の行だけ黄色で大きく
        y = 1300
        for k, L in enumerate(lines):
            last = k == len(lines) - 1
            f = fit(d, L, 104 if last else 86)
            pop = 1.0 if t > 0.2 else 0.0
            if pop:
                tw = d.textlength(L, font=f)
                d.text(((W - tw) / 2, y), L, font=f, fill=(255, 236, 120) if last else 'white', stroke_width=10, stroke_fill='black')
            y += 140 if not last else 150
        d.text((W - 330, 1840), '@showa_tetsuo', font=font(40), fill=(255, 255, 255, 200), stroke_width=2, stroke_fill='black')
        fr = Image.alpha_composite(fr, ov)
        if t < 0.08:  # 一瞬白く光る
            fr = Image.blend(fr, Image.new('RGBA', (W, H), (255, 255, 255, 255)), 0.6)
        p.stdin.write(fr.convert('RGB').tobytes())
    e = clean.copy(); band = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(band).rectangle((0, 820, W, 1180), fill=(0, 0, 0, 170)); e = Image.alpha_composite(e, band).convert('RGB'); d = ImageDraw.Draw(e)
    for tx, y, sz, col in [('続きはフォローで', 860, 96, (255, 200, 60)), ('毎日、令和に殴り込み', 1010, 72, 'white')]:
        f = font(sz); w = d.textlength(tx, font=f); d.text(((W - w) / 2, y), tx, font=f, fill=col, stroke_width=9, stroke_fill='black')
    b = e.tobytes()
    for _ in range(int(END * FPS)): p.stdin.write(b)
    p.stdin.close(); p.wait()
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', SFX, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac',
                    '-shortest', '-movflags', '+faststart', out], check=True)
    os.remove(tmp); print('done', out)

ONLY = [int(a) for a in sys.argv[1:]]
for c in C:
    if not ONLY or c[0] in ONLY: run(c)
