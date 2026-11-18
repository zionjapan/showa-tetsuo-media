# TikTok Shop カート付き動画①：鉄男の丸サングラス（Dainty & Trendy）
import sys, subprocess
sys.path.insert(0, '/tmp/claude-0/-home-claude/9d5ec005-9cc8-52f5-9eca-474a40bf5cb4/scratchpad')
from PIL import Image, ImageDraw, ImageFont
from tt2 import W, H, FPS, F, fit, CX
P = '/home/claude/showa-tetsuo-media/posts/shop/sunglasses/'
OUT = '/home/claude/showa-tetsuo-media/video/shop/sunglasses_cart.mp4'
SHOTS = [('s1_girori.png', 3.5, ['このグラサン', 'どこで買えるかって？'], 1380),
         ('s2_miseru.png', 3.5, ['令和でも', '売ってやがった'], 1380),
         ('s3_kime.png', 4.0, ['昭和の男の目元は', 'これで決まりだ'], 1120)]
def subs(d, lines, shown, y):
    for k, L in enumerate(shown):
        f = fit(d, L, 74); tw = d.textlength(L, font=f)
        last = (k == len(lines) - 1 and len(shown) == len(lines))
        d.text((CX - tw / 2, y), L, font=f, fill=(255, 236, 150) if last else 'white', stroke_width=8, stroke_fill='black'); y += 106
f_top = ImageFont.truetype(F, 54)
def top(d):
    t = '昭和の男の愛用品'
    d.rectangle((0, 150, W, 250), fill=(0, 0, 0))
    d.text(((W - d.textlength(t, font=f_top)) / 2, 165), t, font=f_top, fill=(255, 210, 60))
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', OUT], stdin=subprocess.PIPE)
for f, sec, lines, sy in SHOTS:
    src = Image.open(P + f).convert('RGB'); n = int(sec * FPS)
    for i in range(n):
        z = 1.0 + 0.08 * i / n
        cs = max(W / src.width, H / src.height) * z
        im = src.resize((int(src.width * cs), int(src.height * cs)), Image.BILINEAR)
        cx = (im.width - W) // 2; cy = int((im.height - H) * 0.2)
        fr = im.crop((cx, cy, cx + W, cy + H)); d = ImageDraw.Draw(fr)
        top(d)
        shown = lines[:1 + min(len(lines) - 1, int(i / (n / len(lines))))]
        subs(d, lines, shown, sy)
        p.stdin.write(fr.tobytes())
# 最後：本物の商品写真
prod = Image.open(P + 'p1_two.png').convert('RGB')
w, h = prod.size; prod = prod.crop((0, int(h * 0.27), w, int(h * 0.73)))
prod = prod.resize((W, int(prod.height * W / prod.width)))
end = Image.new('RGB', (W, H), (245, 240, 230)); end.paste(prod, (0, (H - prod.height) // 2 - 100))
d = ImageDraw.Draw(end); top(d)
fb = ImageFont.truetype(F, 80); fs = ImageFont.truetype(F, 56)
for t, y, fo, c in [('鉄男と同じ丸グラサン', 1180, fb, (30, 30, 30)), ('黒・茶・シルバー', 1300, fs, (90, 60, 30)), ('下の商品リンクから買えるぜ', 1400, fs, (200, 30, 30))]:
    d.text(((W - d.textlength(t, font=fo)) / 2, y), t, font=fo, fill=c)
for _ in range(int(4.0 * FPS)): p.stdin.write(end.tobytes())
p.stdin.close(); p.wait(); print('done', OUT)
