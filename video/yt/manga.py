# YouTubeショート用 漫画調（縦書きフキダシ・効果音・集中線）
import math, random, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
W,H,FPS=1080,1920,30
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
FB='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def vtext_size(lines,f,gap=14):
    d=ImageDraw.Draw(Image.new('L',(10,10)))
    hs=[d.textbbox((0,0),L,font=f,direction='ttb',features=['vert'])[3] for L in lines]
    cw=f.size+gap
    return cw*len(lines), max(hs)

def bubble(img, lines, box_xy, tail, kind='round', size=60, sfx=False):
    """lines: columns right->left. box_xy: center of bubble. tail: (x,y) point."""
    f=ImageFont.truetype(F if kind=='shout' else FB,size)
    tw,th=vtext_size(lines,f)
    cx,cy=box_xy
    pw,ph=tw*0.62+50, th*0.62+60
    lay=Image.new('RGBA',img.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    if kind=='shout':
        pts=[]; n=26
        for i in range(n):
            a=2*math.pi*i/n; r=1.0 if i%2==0 else 0.78
            pts.append((cx+math.cos(a)*pw*r*1.25, cy+math.sin(a)*ph*r*1.18))
        # tail
        d.polygon([(cx-pw*0.25,cy+ph*0.5),(tail[0],tail[1]),(cx+pw*0.1,cy+ph*0.6)],fill='white',outline='black')
        d.polygon(pts,fill='white',outline='black',width=7)
    else:
        bx=(cx-pw,cy-ph,cx+pw,cy+ph)
        # tail first (outline), then ellipse covers base
        ang=math.atan2(tail[1]-cy,tail[0]-cx); px,py=-math.sin(ang),math.cos(ang)
        bxp,byp=cx+math.cos(ang)*pw*0.8,cy+math.sin(ang)*ph*0.8
        tri=[(bxp+px*28,byp+py*28),(tail[0],tail[1]),(bxp-px*28,byp-py*28)]
        d.polygon(tri,fill='black');
        tri2=[(bxp+px*20,byp+py*20),(tail[0]-math.cos(ang)*10,tail[1]-math.sin(ang)*10),(bxp-px*20,byp-py*20)]
        d.ellipse((bx[0]-6,bx[1]-6,bx[2]+6,bx[3]+6),fill='black')
        d.ellipse(bx,fill='white'); d.polygon(tri2,fill='white')
    # text columns right -> left
    cw=f.size+14
    x0=cx+tw/2-cw
    for i,L in enumerate(lines):
        bb=d.textbbox((0,0),L,font=f,direction='ttb',features=['vert'])
        d.text((x0-i*cw, cy-bb[3]/2),L,font=f,fill='black',direction='ttb',features=['vert'])
    img.alpha_composite(lay)

def sfx(img,text,xy,size=170,angle=-12,color=(255,230,40)):
    f=ImageFont.truetype(F,size)
    d0=ImageDraw.Draw(Image.new('L',(10,10)))
    bb=d0.textbbox((0,0),text,font=f,stroke_width=14)
    t=Image.new('RGBA',(bb[2]+40,bb[3]+40),(0,0,0,0)); d=ImageDraw.Draw(t)
    d.text((20,20),text,font=f,fill=color,stroke_width=14,stroke_fill='black')
    t=t.rotate(angle,expand=True,resample=Image.BICUBIC)
    img.alpha_composite(t,(int(xy[0]-t.width/2),int(xy[1]-t.height/2)))

def speedlines(img,center,n=90,inner=330,seed=1):
    rnd=random.Random(seed)
    lay=Image.new('RGBA',img.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    cx,cy=center; R=2400
    for i in range(n):
        a=rnd.uniform(0,2*math.pi); w=rnd.uniform(0.004,0.012); r0=inner+rnd.uniform(0,220)
        p1=(cx+math.cos(a-w)*R,cy+math.sin(a-w)*R); p2=(cx+math.cos(a+w)*R,cy+math.sin(a+w)*R)
        p0=(cx+math.cos(a)*r0,cy+math.sin(a)*r0)
        d.polygon([p0,p1,p2],fill=(0,0,0,150))
    img.alpha_composite(lay)

def frame_of(src,ax,z):
    cs=max(W/src.width,H/src.height)*z
    im=src.resize((int(src.width*cs),int(src.height*cs)),Image.BILINEAR)
    cx=int((im.width-W)*ax); cy=int((im.height-H)*0.15)
    return im.crop((cx,cy,cx+W,cy+H)).convert('RGBA')

def render(shots,out,title_band=None,SEC=6):
    p=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',out],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
    for sh in shots:
        src=Image.open(sh['img']).convert('RGB'); n=SEC*FPS
        # manga tone: a bit more contrast
        for i in range(n):
            t=i/FPS
            z=1.0+0.06*i/n
            fr=frame_of(src,sh['ax'],z)
            fr=ImageEnhance.Contrast(fr.convert('RGB')).enhance(1.12).convert('RGBA')
            if sh.get('lines_fx') and t>=sh['lines_fx']: speedlines(fr,sh['fx_center'])
            if title_band: fr.alpha_composite(title_band)
            for ev in sh['events']:
                if t>=ev['t']:
                    if ev['type']=='bubble':
                        k=min(1,(t-ev['t'])*6)  # pop-in
                        bubble(fr,ev['lines'],ev['xy'],ev['tail'],ev.get('kind','round'),int(ev.get('size',60)*(0.7+0.3*k)))
                    elif ev['type']=='sfx':
                        k=min(1,(t-ev['t'])*8)
                        sfx(fr,ev['text'],ev['xy'],int(ev.get('size',170)*(1.4-0.4*k)),ev.get('angle',-12))
            p.stdin.write(fr.convert('RGB').tobytes())
    p.stdin.close(); p.wait()
