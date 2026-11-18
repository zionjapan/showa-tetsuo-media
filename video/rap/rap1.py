# 権藤鉄男 ラップデビュー「昭和から来た男」（Suno・全編55秒）
import subprocess
from PIL import Image, ImageDraw, ImageFont
R='/home/claude/showa-tetsuo-media/'; P=R+'posts/'; W,H,FPS=1080,1920,30
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
AUD=R+'video/rap/rap1_full.mp3'; OUT=R+'video/rap/rap1_debut.mp4'
SHOTS=['2026-10-22/sento.png','2026-10-22/shibuya.png','2026-10-22/conbini.png','2026-10-23/tapioca.png',
 'ep22/22-1_nyujo_b.png','ep22/22-2_faceoff.png','ep23/23-3_hantei.png','ep23/23-4_hikaeshitsu.png',
 'ep24/24-1_sento_haru.png','ep25/25-1_tire_run.png','ep25/25-2_ishidan.png','ep26/26-0_sandbag.png',
 'ep26/26-1_mirror.png','ep29/29-2_ko.png','ep30/30-1_chanko.png','ep26/26-3_neon_walk.png']
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',AUD],capture_output=True,text=True).stdout)
total=int(dur*FPS); per=total//len(SHOTS)
band=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(band)
d.rectangle((0,150,W,330),fill=(0,0,0,215))
f1=ImageFont.truetype(F,46); f2=ImageFont.truetype(F,80)
for t,y,f,c in [('権藤鉄男 ラップデビュー',165,f1,(255,210,60)),('「昭和から来た男」',225,f2,'white')]:
    d.text(((W-d.textlength(t,font=f))/2,y),t,font=f,fill=c)
p=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',AUD,
  '-map','0:v','-map','1:a','-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',OUT],stdin=subprocess.PIPE)
for k,f in enumerate(SHOTS):
    src=Image.open(P+f).convert('RGB'); n=per if k<len(SHOTS)-1 else total-per*k
    for i in range(n):
        z=1.0+0.08*i/n; cs=max(W/src.width,H/src.height)*z
        im=src.resize((int(src.width*cs),int(src.height*cs)),Image.BILINEAR)
        cx=(im.width-W)//2; cy=int((im.height-H)*0.2)
        fr=im.crop((cx,cy,cx+W,cy+H)).convert('RGBA'); fr.alpha_composite(band)
        p.stdin.write(fr.convert('RGB').tobytes())
p.stdin.close(); p.wait(); print('done',OUT)
