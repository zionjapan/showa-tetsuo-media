from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import subprocess
U='/mnt/user-data/uploads/'
W,H,FPS=1080,1920,30
P='/home/claude/showa-tetsuo-media/posts/2026-11-01/'
shots=[(P+'sushi.png',0.3,['皿が止まらねぇ！','誰だ頼んだのは！']),
       (P+'kissaten.png',0.3,['ハルさんと','クリームソーダ','……照れるじゃねぇか']),
       (P+'haru_rain.png',0.35,['1979年の秋','あの子は','雨の中ずっと待ってた'])]
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc',76,index=0)
SEC=6
p=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart','/home/claude/showa-tetsuo-media/video/2026-11-01_tiktok12.mp4'],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
for f,ax,lines in shots:
    src=Image.open(f).convert('RGB')
    s=max(W/src.width,H/src.height)
    bg=src.resize((int(src.width*s),int(src.height*s))).crop((0,0,W,H)).filter(ImageFilter.GaussianBlur(30))
    bg=ImageEnhance.Brightness(bg).enhance(0.4)
    n=SEC*FPS
    for i in range(n):
        z=1.0+0.10*i/n
        cs=max(W/src.width,H/src.height)*z
        im=src.resize((int(src.width*cs),int(src.height*cs)),Image.BILINEAR)
        cx=int((im.width-W)*ax); cy=int((im.height-H)*0.15)
        fr=im.crop((cx,cy,cx+W,cy+H))
        d=ImageDraw.Draw(fr)
        shown=lines[:1+min(len(lines)-1,int(i/(n/len(lines))))]
        y=1440 if len(lines)<4 else 1330
        for L in shown:
            tw=d.textlength(L,font=font)
            d.text(((W-tw)/2,y),L,font=font,fill=(255,236,150) if L==lines[-1] and len(lines)>1 and L in shown[-1:] and len(shown)==len(lines) else 'white',stroke_width=8,stroke_fill='black')
            y+=112
        p.stdin.write(fr.tobytes())
p.stdin.close();p.wait()
