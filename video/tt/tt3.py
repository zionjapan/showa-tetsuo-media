# TikTok本編 v3：最初の1.6秒は「オチ」をドンと見せる（寄り＋光＋揺れ＋効果音）→ 本編を短めに
import sys, os, re, math, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tt2
from tt2 import W, H, FPS, F, CX, band, subs, endcard, fname, OUT
from PIL import Image, ImageDraw, ImageFont
S = os.path.dirname(os.path.abspath(__file__)) + '/'
# n: (台本ファイル, フックに使う画像の番号, フックの切り抜き(左,上,右,下 比率), フック文字2行)
HOOK = {
 13: ('reel10.py', 1, (0.0, 0.0, 1.0, 1.0), ['47年前の宿敵が', '目の前にいた'], 0.2, 0.0),
}
SEC = 4.5
def font(s): return ImageFont.truetype(F, s)
def boom(path, dur):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=f=55:d=0.9', '-f', 'lavfi', '-i', 'anoisesrc=d=0.25:c=brown:a=0.9',
        '-f', 'lavfi', '-i', f'anullsrc=r=44100:cl=stereo', '-filter_complex',
        f'[0]volume=2.2,afade=t=out:st=0.05:d=0.85[a];[1]afade=t=out:st=0:d=0.25,volume=0.8[b];[2]atrim=0:{dur}[s];[s][a][b]amix=3:normalize=0,atrim=0:{dur}',
        '-ar', '44100', '-ac', '2', path], check=True)
def render(n):
    script, hi, box, hook, hax, hay = HOOK[n]
    code = open(S + script).read()
    P = re.search(r"P='([^']+)'", code).group(1)
    shots = eval(re.search(r"shots=(\[.*?\])\n", code, re.S).group(1), {'P': P})
    tmp = OUT + f'_v3_{n}.mp4'; out = OUT + fname(n)
    p = tt2.pipe(tmp); nf = 0
    # フック
    src = Image.open(shots[hi][0]).convert('RGB')
    l, t, r, b = box; src = src.crop((int(src.width * l), int(src.height * t), int(src.width * r), int(src.height * b)))
    hn = int(1.6 * FPS)
    for i in range(hn):
        tt = i / FPS
        z = 1.30 - 0.20 * min(tt / 0.35, 1) ** 0.5 + 0.05 * tt
        cs = max(W / src.width, H / src.height) * z
        im = src.resize((int(src.width * cs), int(src.height * cs)), Image.BILINEAR)
        sh = int(16 * math.sin(tt * 70) * max(0, 1 - tt / 0.4))
        cx = max(0, min(int((im.width - W) * hax) + sh, im.width - W)); cy = int((im.height - H) * hay)
        fr = im.crop((cx, cy, cx + W, cy + H)).convert('RGBA')
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        d.rectangle((0, 760, W, 1250), fill=(0, 0, 0, 150))
        s1 = f'昭和から来た男 #{n}'; d.text((CX - d.textlength(s1, font=font(52)) / 2, 785), s1, font=font(52), fill=(255, 200, 60), stroke_width=4, stroke_fill='black')
        y = 870
        for k, L in enumerate(hook):
            sz = 130
            while d.textlength(L, font=font(sz)) > 920: sz -= 6
            d.text((CX - d.textlength(L, font=font(sz)) / 2, y), L, font=font(sz), fill=(255, 236, 120) if k == len(hook) - 1 else 'white', stroke_width=10, stroke_fill='black')
            y += sz + 25
        fr.alpha_composite(lay)
        if 0.10 < tt < 0.18: fr = Image.blend(fr, Image.new('RGBA', (W, H), 'white'), 0.6)  # 1コマ目は白くしない（表紙が白くなるため）
        p.stdin.write(fr.convert('RGB').tobytes()); nf += 1
    # 本編
    for f, ax, lines in shots:
        src = Image.open(f).convert('RGB'); nfr = int(SEC * FPS)
        for i in range(nfr):
            z = 1.0 + 0.10 * i / nfr
            cs = max(W / src.width, H / src.height) * z
            im = src.resize((int(src.width * cs), int(src.height * cs)), Image.BILINEAR)
            cx = int((im.width - W) * ax); cy = int((im.height - H) * 0.15)
            fr = im.crop((cx, cy, cx + W, cy + H)).convert('RGBA')
            fr.alpha_composite(band(n)); fr = fr.convert('RGB'); d = ImageDraw.Draw(fr)
            shown = lines[:1 + min(len(lines) - 1, int(i / (nfr / len(lines))))]
            subs(d, lines, shown); p.stdin.write(fr.tobytes()); nf += 1
    endcard(fr, p); nf += 2 * FPS
    p.stdin.close(); p.wait()
    dur = nf / FPS; wav = OUT + f'_boom_{n}.wav'; boom(wav, dur)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-shortest', '-movflags', '+faststart', out], check=True)
    os.remove(tmp); os.remove(wav); print('done', out, round(dur, 1))
if __name__ == '__main__':
    for a in sys.argv[1:]: render(int(a))
