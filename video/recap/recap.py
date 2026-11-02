# 「30秒でわかる 権藤鉄男」あらすじ動画（既存の静止画だけで作る・無料）
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import subprocess, os, math, sys
R = '/home/claude/showa-tetsuo-media/'
P = R + 'posts/'
OUT = R + 'video/recap/'
W, H, FPS = 1080, 1920, 30
F = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
Y = (255, 210, 60)

# (画像, 横位置, 上の小見出し, セリフ2行, 秒)
SHOTS = [
    ('2026-10-22/shibuya.png', 0.35, '1979年', ['昭和の男が', '令和の渋谷に落ちてきた'], 3.2),
    ('2026-10-23/scout2.png', 0.35, 'ゲンコツ一発', ['チンピラ瞬殺', 'まさかの格闘技スカウト'], 3.0),
    ('2026-10-23/audition.png', 0.3, '1分間最強を決める大会', ['オーディションに', 'ジジイ顔が乱入'], 3.2),
    ('2026-10-25/sparring_v2.png', 0.55, 'プロとのスパー', ['拳を全部よけて', '試合出場が決定'], 3.0),
    ('2026-10-25/press.png', 0.45, '記者会見', ['金髪ファイターと', '因縁勃発'], 2.8),
    ('2026-10-27/f_faceoff.png', 0.4, '鉄檻デビュー', ['相手は', '狂犬ZERO'], 2.6),
    ('2026-10-27/f_down.png', 0.25, 'まさかの', ['ダウン……', '「昼寝してただけだ」'], 2.8),
    ('2026-10-27/ko.png', 0.45, '残り10秒', ['昭和ゲンコツ一発', '58秒KO'], 2.8),
    ('2026-10-26/haru_photo.png', 0.3, '銭湯のハルさん', ['47年前に', '交わした約束'], 2.8),
    ('2026-10-28/ryuji.png', 0.4, 'そして', ['47年前の宿敵が', '目の前に現れた'], 3.0),
]
END = 2.5

def font(s): return ImageFont.truetype(F, s)
def fit(d, t, s, maxw=980):
    f = font(s)
    while d.textlength(t, font=f) > maxw: s -= 4; f = font(s)
    return f

def frame_of(src, ax, t, dur):
    # 最初0.3秒でドンと寄る→ゆっくり寄り続ける
    z = 1.22 - 0.14 * min(t / 0.3, 1) ** 0.5 + 0.05 * t / dur
    sh = int(14 * math.sin(t * 70) * max(0, 1 - t / 0.3))
    cs = max(W / src.width, H / src.height) * z
    im = src.resize((int(src.width * cs), int(src.height * cs)), Image.BILINEAR)
    cx = int((im.width - W) * ax) + sh; cy = int((im.height - H) * 0.2)
    cx = max(0, min(cx, im.width - W))
    return im.crop((cx, cy, cx + W, cy + H)).convert('RGBA')

def overlay(label, lines, t, idx):
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    # 上：シリーズ名
    d.rectangle((0, 150, W, 290), fill=(0, 0, 0, 170))
    f = font(62); tx = '30秒でわかる 権藤鉄男'
    d.text(((W - d.textlength(tx, font=f)) / 2, 180), tx, font=f, fill=Y, stroke_width=4, stroke_fill='black')
    # 下：小見出し＋2行
    d.rectangle((0, 1240, W, 1640), fill=(0, 0, 0, 150))
    f = fit(d, label, 64)
    d.text(((W - d.textlength(label, font=f)) / 2, 1270), label, font=f, fill=Y, stroke_width=6, stroke_fill='black')
    y = 1370
    for k, L in enumerate(lines):
        f = fit(d, L, 96 if k == 1 else 84)
        if idx == 0 or t > 0.12 + 0.15 * k:
            d.text(((W - d.textlength(L, font=f)) / 2, y), L, font=f, fill='white' if k == 0 else (255, 236, 120), stroke_width=9, stroke_fill='black')
        y += 120
    # 進み具合のバー
    d.rectangle((0, H - 18, int(W * (idx + min(t, 1)) / len(SHOTS)), H), fill=Y + (230,))
    d.text((W - 330, 1830), '@showa_tetsuo', font=font(40), fill=(255, 255, 255, 200), stroke_width=2, stroke_fill='black')
    return ov

def run():
    os.makedirs(OUT, exist_ok=True)
    tmp = OUT + '_recap_v.mp4'
    p = subprocess.Popen(['ffmpeg', '-nostdin', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', tmp], stdin=subprocess.PIPE, stderr=subprocess.DEVNULL)
    hits = []; T = 0.0; last = None
    for idx, (img, ax, label, lines, dur) in enumerate(SHOTS):
        src = Image.open(P + img).convert('RGB')
        hits.append(T)
        for i in range(int(dur * FPS)):
            t = i / FPS
            fr = frame_of(src, ax, t, dur); last = fr
            fr = Image.alpha_composite(fr, overlay(label, lines, t, idx))
            if t < 0.07 and idx > 0: fr = Image.blend(fr, Image.new('RGBA', (W, H), (255, 255, 255, 255)), 0.55)
            p.stdin.write(fr.convert('RGB').tobytes())
        T += dur
    # 締め：暗くして「続きは毎日19時」
    e = ImageEnhance.Brightness(last.convert('RGB')).enhance(0.35); d = ImageDraw.Draw(e)
    for tx, y, sz, col in [('この続きは', 700, 90, 'white'), ('毎日19時', 830, 150, Y), ('本編で', 1020, 110, 'white'), ('フォローして待っとけ', 1220, 76, Y)]:
        f = font(sz); d.text(((W - d.textlength(tx, font=f)) / 2, y), tx, font=f, fill=col, stroke_width=9, stroke_fill='black')
    hits.append(T)
    b = e.tobytes()
    for _ in range(int(END * FPS)): p.stdin.write(b)
    T += END
    p.stdin.close(); p.wait()
    # 音：熱血BGM（30秒版）＋カットごとのドン
    bgm = OUT + 'bgm_nekketsu30.wav'
    if not os.path.exists(bgm):
        sys.path.insert(0, R + 'video/yt_v3'); import importlib.util
        spec = importlib.util.spec_from_file_location('bs', R + 'video/yt_v3/bgm_synth.py')
        src = open(R + 'video/yt_v3/bgm_synth.py').read().split('# 演歌風')[0]
        ns = {'__file__': R + 'video/yt_v3/bgm_synth.py'}; exec(src, ns); ns['OUT'] = OUT
        E_, F_, A_, C_ = 7, 8, 0, 3
        ns['song']('nekketsu30', 150, [(0, E_, 0.5), (0.5, E_, 0.5), (1, F_, 0.5), (1.5, E_, 0.5), (2, C_, 1), (3, E_, 1), (4, A_ + 12, 1.5), (5.5, F_, 0.5), (6, E_, 2)],
                   [(0, A_, 0.5), (0.5, A_, 0.5), (1, A_, 0.5), (1.5, A_, 0.5), (2, F_ - 12, 1), (3, F_ - 12, 1), (4, E_ - 12, 1), (5, E_ - 12, 1), (6, A_, 2)], lead='sq', secs=T)
    boom = OUT + '_boom.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'sine=f=55:d=0.6', '-f', 'lavfi', '-i', 'anoisesrc=d=0.2:c=brown:a=0.8',
                    '-filter_complex', '[0]volume=2,afade=t=out:st=0.05:d=0.55[a];[1]afade=t=out:st=0:d=0.2,volume=0.7[b];[a][b]amix=2:normalize=0', '-ar', '44100', '-ac', '2', boom], check=True)
    inputs = ['-i', tmp, '-i', bgm]; fc = '[1]volume=0.45[bg];'; mix = '[bg]'
    for k, h in enumerate(hits):
        inputs += ['-i', boom]; ms = int(h * 1000)
        fc += f'[{k+2}]adelay={ms}|{ms},volume={1.6 if k == 7 else 0.9}[h{k}];'; mix += f'[h{k}]'
    fc += f'{mix}amix={len(hits)+1}:normalize=0,atrim=0:{T}[a]'
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + inputs + ['-filter_complex', fc, '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac',
                    '-movflags', '+faststart', OUT + 'recap30.mp4'], check=True)
    os.remove(tmp); print('done', T)

run()
