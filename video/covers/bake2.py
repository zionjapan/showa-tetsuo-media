# 表紙対策その2（11/6）：最初の1秒差し込みはTikTokに拾われなかった（#16・#17）。
# 動画の最初の3秒間ずっと「昭和から来た男 #番号」の帯を重ねる。TikTokが最初の数秒のどのコマを選んでも表紙になる。
# 出力：video/tt/<日付>_tiktok<番号>_cover.mp4（上書き）
import subprocess, sys, glob
from PIL import Image, ImageDraw, ImageFont
R = '/home/claude/showa-tetsuo-media/'; W, H = 1080, 1920
F = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; Y = (255, 210, 60)
sys.path.insert(0, R + 'video/covers'); from bake import TITLES
SECS = 3.0

def band(n, out):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rectangle((0, 840, W, 1700), fill=(0, 0, 0, 255))
    def t(txt, y, sz, col):
        f = ImageFont.truetype(F, sz)
        while d.textlength(txt, font=f) > 1010: sz -= 4; f = ImageFont.truetype(F, sz)
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=col, stroke_width=12, stroke_fill='black')
    t('昭和から来た男', 900, 130, 'white'); t(f'#{n}', 1050, 260, Y); t(TITLES.get(n, ''), 1380, 80, 'white')
    im.save(out)

def run(n):
    src = [p for p in glob.glob(R + f'video/tt/*_tiktok{n}.mp4')][0]
    png = R + f'video/covers/band_{n}.png'; band(n, png)
    out = src.replace('.mp4', '_cover.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-i', png, '-filter_complex',
                    f"[0:v]scale={W}:{H},setsar=1[v];[v][1:v]overlay=0:0:enable='lt(t,{SECS})'[o]",
                    '-map', '[o]', '-map', '0:a?', '-c:v', 'libx264', '-crf', '20', '-c:a', 'copy', '-movflags', '+faststart', out], check=True)
    print('done', out)

for n in [int(a) for a in sys.argv[1:]]: run(n)
