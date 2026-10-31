import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bd_fx import *
from PIL import Image, ImageDraw
V = R + 'video/training/'; SRC = V + 'cigar_walk.mp4'; OUT = V + 'cigar_walk_jimaku.mp4'
def png(lines, name, top=None, y=1350, col='white'):
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if top:
        d.rectangle((0, 170, W, 270), fill=(0, 0, 0, 160)); ctext(d, top, 185, F(GB, 54), (255, 206, 60), 5)
    for i, (t, c, s) in enumerate(lines):
        ctext(d, t, y + i * 130, F(GB, s), c, 10)
    im.save(V + name); return V + name
a = png([('どけどけ', 'white', 96), ('主役のお通りだ', (255, 206, 60), 96)], '_s1.png', top='ZERO戦KOの翌日')
b = png([('見たか？', 'white', 96), ('昭和ゲンコツ', (255, 206, 60), 104)], '_s2.png', top='ZERO戦KOの翌日')
c = png([('令和のヒヨッコども！', 'white', 84), ('サインは後でな！', (255, 206, 60), 100)], '_s3.png', top='ZERO戦KOの翌日')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-i', a, '-i', b, '-i', c, '-filter_complex',
  "[0:v]scale=1080:1920,setsar=1[v];[v][1:v]overlay=0:0:enable='lt(t,4.3)'[x];[x][2:v]overlay=0:0:enable='between(t,4.3,7.3)'[y];[y][3:v]overlay=0:0:enable='gte(t,7.3)'",
  '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT], check=True)
for f in ['_s1.png', '_s2.png', '_s3.png']: os.remove(V + f)
print('done')
