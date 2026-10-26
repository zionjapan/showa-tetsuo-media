import sys; sys.path.insert(0,'/tmp/claude-0/-home-claude/9d5ec005-9cc8-52f5-9eca-474a40bf5cb4/scratchpad')
import tt2, re
from PIL import Image, ImageDraw
SHADE=Image.open('/tmp/claude-0/-home-claude/9d5ec005-9cc8-52f5-9eca-474a40bf5cb4/scratchpad/shade.png')
W,H,FPS=1080,1920,30
CROP={'sparring.png':(0.3,0.35,0.4),'press.png':(0.5,0.35,0.65),'oden.png':(0.45,0.4,0.7),
'weighin.png':(0.3,0.155,0.3),'mitt.png':(0.5,0.4,0.7),'haru_photo.png':(0.4,0.4,0.7)}
def crop_frame(src,fx,fy,vh,z):
    bh=src.height*vh/z; bw=bh*W/H
    cx=min(max(fx*src.width,bw/2),src.width-bw/2); cy=min(max(fy*src.height,bh/2),src.height-bh/2)
    return src.crop((int(cx-bw/2),int(cy-bh/2),int(cx+bw/2),int(cy+bh/2))).resize((W,H),Image.BICUBIC)
def run(n,script):
    s=open(tt2.S+script).read(); P=re.search(r"P='([^']+)'",s).group(1)
    shots=eval(re.search(r"shots=(\[.*?\])\n",s,re.S).group(1),{'P':P})
    p=tt2.pipe(tt2.OUT+tt2.fname(n,'_safe')); SEC=6
    for f,ax,lines in shots:
        src=Image.open(f).convert('RGB'); fx,fy,vh=CROP[f.split('/')[-1]]; nf=SEC*FPS
        for i in range(nf):
            fr=crop_frame(src,fx,fy,vh,1.0+0.08*i/nf).convert('RGBA'); fr.alpha_composite(SHADE); fr.alpha_composite(tt2.band(n)); fr=fr.convert('RGB')
            d=ImageDraw.Draw(fr); shown=lines[:1+min(len(lines)-1,int(i/(nf/len(lines))))]; tt2.subs(d,lines,shown)
            p.stdin.write(fr.tobytes())
    tt2.endcard(fr,p); p.stdin.close(); p.wait(); print('done',n)
run(6,'reel5.py'); run(7,'reel6.py')
