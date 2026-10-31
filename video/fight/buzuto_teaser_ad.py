# バズ斗戦 予告（昭和VS令和の型：1秒目に大文字→ポスター→にらみ合い→殴る直前で止める）
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bd_fx import *
from PIL import Image, ImageDraw, ImageEnhance
TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bzt'); os.makedirs(TMP, exist_ok=True)
V = R + 'video/fight/'
FACE = V + 'buzuto_faceoff_720.mp4'; KO = V + 'buzuto_ko_1080_v1.mp4'
OUT = V + 'buzuto_teaser_ad.mp4'
ENC = ['-r', '30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '44100', '-ac', '2']
def run(c): subprocess.run(c, check=True)
src = Image.open(R + 'posts/ep29/29-1_faceoff.png').convert('RGB')
fr = aori_frames(src, [('昭和 VS 令和', 'ガリガリがバズを喰う'), ('登録者100万人が', '素人のジジイに挑む')], sec_each=1.4)
pos = Image.open(R + 'posts/ep28/vs_buzuto.png').convert('RGB').resize((W, H))
fr += [pos] * int(1.8 * FPS)
for f in os.listdir(TMP): os.remove(os.path.join(TMP, f))
for i, f in enumerate(fr): f.save(f'{TMP}/{i:04d}.jpg', quality=92)
run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{TMP}/%04d.jpg', '-ss', '0', '-i', FACE,
     '-map', '0:v', '-map', '1:a', '-af', 'volume=0.8', '-shortest'] + ENC + [V + '_t1.mp4'])
lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
d.rectangle((40, 215, 300, 275), fill=(170, 20, 20)); d.text((60, 221), '鉄檻 TEKKAN', font=F(GB, 34), fill='white')
d.rectangle((300, 215, 420, 275), fill=(0, 0, 0)); d.text((318, 221), 'LIVE', font=F(GB, 34), fill=(255, 60, 60))
d.rectangle((0, 1700, W, 1780), fill=(0, 0, 0, 200)); t = '挑戦者決定戦　権藤鉄男 vs バズ斗'
d.text(((W - d.textlength(t, font=F(GB, 44))) / 2, 1714), t, font=F(GB, 44), fill='white'); lay.save(V + '_live.png')
run(['ffmpeg', '-v', 'error', '-y', '-t', '6', '-i', FACE, '-i', V + '_live.png', '-filter_complex',
     '[0:v]scale=1080:1920,setsar=1[a];[a][1:v]overlay=0:0'] + ENC + [V + '_t2.mp4'])
_skip=(['ffmpeg', '-v', 'error', '-y', '-t', '4.7', '-i', KO, '-i', V + '_live.png', '-filter_complex',
     "[0:v]setsar=1,crop=iw-80:ih-142:40:71,scale=1080:1920[a];[a][1:v]overlay=0:0"] + ENC + [V + '_t3.mp4'])
run(['ffmpeg', '-v', 'error', '-y', '-ss', '5.8', '-i', FACE, '-frames:v', '1', V + '_stop.png'])
e = ImageEnhance.Brightness(Image.open(V + '_stop.png').convert('RGB').resize((W, H))).enhance(0.4); d = ImageDraw.Draw(e)
ctext(d, '決着は', 720, F(SB, 120), 'white', 10)
ctext(d, '本編で', 870, F(SB, 170), RED, 12, 'white')
ctext(d, 'フォローして待っとけ', 1150, F(GB, 70), (255, 206, 60), 8)
e.save(V + '_end.png')
run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', '2.5', '-i', V + '_end.png', '-ss', '6', '-t', '2.5', '-i', FACE,
     '-map', '0:v', '-map', '1:a', '-af', 'afade=t=out:st=1.6:d=0.9', '-shortest'] + ENC + [V + '_t4.mp4'])
with open(V + '_l.txt', 'w') as f:
    for p in ['_t1', '_t2', '_t4']: f.write(f"file '{V}{p}.mp4'\n")
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', V + '_l.txt'] + ENC + ['-crf', '18', '-movflags', '+faststart', OUT])
for p in ['_t1.mp4', '_t2.mp4', '_t4.mp4', '_live.png', '_stop.png', '_end.png', '_l.txt']: os.remove(V + p)
print('done', OUT)
