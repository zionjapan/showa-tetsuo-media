# バズ斗戦 30秒：煽り→ポスター→にらみ合い動画→KO動画（テロップ）→勝ち名乗り
import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bd_fx import *
from PIL import Image, ImageDraw
TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bz'); os.makedirs(TMP, exist_ok=True)
V = R + 'video/fight/'
FACE = V + 'buzuto_faceoff_720.mp4'; KO = V + 'buzuto_ko_1080_v1.mp4'
OUT = V + 'buzuto_fight_30s.mp4'

def run(c): subprocess.run(c, check=True)
# 1) 煽り＋ポスター（無音）
src = Image.open(R + 'posts/ep29/29-1_faceoff.png').convert('RGB')
fr = aori_frames(src, [('令和のバズか', '昭和のゲンコツか'), ('登録者100万人が', '素人のジジイに挑む')], sec_each=1.4)
pos = Image.open(R + 'posts/ep28/vs_buzuto.png').convert('RGB').resize((W, H))
fr += [pos] * int(2.2 * FPS)
for f in os.listdir(TMP): os.remove(os.path.join(TMP, f))
for i, f in enumerate(fr): f.save(f'{TMP}/{i:04d}.jpg', quality=92)
run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', f'{TMP}/%04d.jpg', '-ss', '0', '-i', FACE,
     '-map', '0:v', '-map', '1:a', '-af', 'volume=0.8,afade=t=in:d=0.8', '-shortest', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'aac', '-ar', '44100', '-ac', '2', V + '_p1.mp4'])
# 2) にらみ合い（ロゴとLIVE表示を重ねる）
lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
d.rectangle((40, 215, 300, 275), fill=(170, 20, 20)); d.text((60, 221), '鉄檻 TEKKAN', font=F(GB, 34), fill='white')
d.rectangle((300, 215, 420, 275), fill=(0, 0, 0)); d.text((318, 221), 'LIVE', font=F(GB, 34), fill=(255, 60, 60))
d.rectangle((0, 1700, W, 1780), fill=(0, 0, 0, 200)); t = '挑戦者決定戦　権藤鉄男 vs バズ斗'
d.text(((W - d.textlength(t, font=F(GB, 44))) / 2, 1714), t, font=F(GB, 44), fill='white')
lay.save(V + '_live.png')
run(['ffmpeg', '-v', 'error', '-y', '-i', FACE, '-i', V + '_live.png', '-filter_complex',
     '[0:v]scale=1080:1920,setsar=1[a];[a][1:v]overlay=0:0', '-r', '30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '44100', '-ac', '2', V + '_p2.mp4'])
# 3) KO（5.5秒以降にKOテロップ）
ko = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ko_telop(ko, '権藤鉄男', '（鉄檻2）', y=1380); ko.save(V + '_ko.png')
run(['ffmpeg', '-v', 'error', '-y', '-i', KO, '-i', V + '_live.png', '-i', V + '_ko.png', '-filter_complex',
     "[0:v]setsar=1,crop=iw-80:ih-142:'40+if(between(t,4.82,5.2),34*sin(90*t),0)':'71+if(between(t,4.82,5.2),34*cos(70*t),0)',scale=1080:1920,"
     "drawbox=0:0:iw:ih:white:t=fill:enable='between(t,4.84,4.92)'[a];[a][1:v]overlay=0:0[b];[b][2:v]overlay=0:0:enable='gte(t,5.5)'",
     '-af', "volume='if(between(t,4.8,5.3),2.2,1)':eval=frame",
     '-r', '30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '44100', '-ac', '2', V + '_p3.mp4'])
# 3b) スローリプレイ（インパクトを0.3倍速でアップ）
rp = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(rp)
d.rectangle((40, 215, 330, 285), fill=(214, 28, 28)); d.text((62, 222), 'REPLAY', font=F(GB, 46), fill='white')
rp.save(V + '_rp.png')
run(['ffmpeg', '-v', 'error', '-y', '-ss', '4.3', '-t', '1.3', '-i', KO, '-i', V + '_rp.png', '-filter_complex',
     "[0:v]setpts=3.3*PTS,crop=860:1529:110:60,scale=1080:1920,setsar=1,drawbox=0:0:iw:ih:white:t=fill:enable='between(t,1.75,1.95)'[a];[a][1:v]overlay=0:0",
     '-af', 'atempo=0.5,atempo=0.606,volume=1.8', '-r', '30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '44100', '-ac', '2', V + '_p3b.mp4'])
# 4) 勝ち名乗り（最後のコマを止めて結果）
run(['ffmpeg', '-v', 'error', '-y', '-sseof', '-0.1', '-i', KO, '-frames:v', '1', V + '_last.png'])
last = Image.open(V + '_last.png').convert('RGB').resize((W, H))
from PIL import ImageEnhance
e = ImageEnhance.Brightness(last).enhance(0.55); d = ImageDraw.Draw(e)
ctext(d, '1R 0:41', 700, F(GB, 90), 'white', 8)
ctext(d, 'KO勝ち', 820, F(SB, 190), RED, 12, 'white')
ctext(d, '権藤鉄男', 1060, F(SB, 130), 'white', 10)
ctext(d, '次の相手は、元力士・山嵐', 1300, F(GB, 60), (255, 206, 60), 6)
e.save(V + '_end.png')
run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', '3', '-i', V + '_end.png', '-ss', '6.5', '-t', '3', '-i', KO,
     '-map', '0:v', '-map', '1:a', '-af', 'afade=t=out:st=2.2:d=0.8', '-shortest', '-r', '30', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-ar', '44100', '-ac', '2', V + '_p4.mp4'])
with open(V + '_list.txt', 'w') as f:
    for p in ['_p1', '_p2', '_p3', '_p3b', '_p4']: f.write(f"file '{V}{p}.mp4'\n")
run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', V + '_list.txt', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-c:a', 'aac', '-movflags', '+faststart', OUT])
for p in ['_p1.mp4', '_p2.mp4', '_p3.mp4', '_p3b.mp4', '_rp.png', '_p4.mp4', '_live.png', '_ko.png', '_last.png', '_end.png', '_list.txt']: os.remove(V + p)
print('done', OUT)
