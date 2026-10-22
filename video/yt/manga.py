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

FW=str.maketrans('0123456789','０１２３４５６７８９')
def split_cols(lines,maxc=8):
    lines=[L.translate(FW) for L in lines]
    out=[]
    for L in lines:
        while len(L)>maxc and len(L)-maxc>2:
            cut=maxc
            for sep in '、。！？…':
                i=L.rfind(sep,2,maxc+1)
                if i>0: cut=i+1; break
            out.append(L[:cut]); L=L[cut:]
        if L: out.append(L)
    return out
def bubble(img, lines, box_xy, tail, kind='round', size=60, sfx=False):
    """lines: columns right->left. box_xy: center of bubble. tail: (x,y) point."""
    lines=split_cols(lines)
    f=ImageFont.truetype(F if kind=='shout' else FB,size)
    tw,th=vtext_size(lines,f)
    cx,cy=box_xy
    pw,ph=tw*0.62+50, th*0.62+60
    if kind=='shout': mx,my=pw*1.25+12,ph*1.18+12
    else: mx,my=pw+12,ph+12
    cx=min(max(cx,mx+8),W-mx-8); cy=min(max(cy,my+8),1500-my)
    lay=Image.new('RGBA',img.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    if kind=='shout':
        pts=[]; n=26
        for i in range(n):
            a=2*math.pi*i/n; r=1.0 if i%2==0 else 0.78
            pts.append((cx+math.cos(a)*pw*r*1.25, cy+math.sin(a)*ph*r*1.18))
        ang=math.atan2(tail[1]-cy,tail[0]-cx)
        ex,ey=cx+math.cos(ang)*pw*1.1,cy+math.sin(ang)*ph*1.05
        L=math.hypot(tail[0]-ex,tail[1]-ey); cap=110
        if L>cap: tail=(ex+(tail[0]-ex)*cap/L, ey+(tail[1]-ey)*cap/L)
        px,py=-math.sin(ang),math.cos(ang)
        bx0,by0=cx+math.cos(ang)*pw*0.7,cy+math.sin(ang)*ph*0.7
        d.polygon([(bx0+px*30,by0+py*30),tail,(bx0-px*30,by0-py*30)],fill='white',outline='black',width=6)
        d.polygon(pts,fill='white',outline='black',width=7)
    else:
        bx=(cx-pw,cy-ph,cx+pw,cy+ph)
        # tail first (outline), then ellipse covers base
        ang=math.atan2(tail[1]-cy,tail[0]-cx); px,py=-math.sin(ang),math.cos(ang)
        ex,ey=cx+math.cos(ang)*pw,cy+math.sin(ang)*ph
        L=math.hypot(tail[0]-ex,tail[1]-ey); cap=110
        if L>cap: tail=(ex+(tail[0]-ex)*cap/L, ey+(tail[1]-ey)*cap/L)
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

def caption(img,lines,xy,size=50):
    lines=split_cols(lines,8)
    f=ImageFont.truetype(FB,size); tw,th=vtext_size(lines,f)
    bw,bh=tw+40,th+50
    x0=min(max(xy[0]-bw/2,14),W-bw-14); y0=min(max(xy[1]-bh/2,14),1500-bh)
    lay=Image.new('RGBA',img.size,(0,0,0,0)); d=ImageDraw.Draw(lay)
    d.rectangle((x0,y0,x0+bw,y0+bh),fill=(255,255,250),outline='black',width=6)
    cw=f.size+14; xr=x0+bw-20-cw
    for i,L in enumerate(lines):
        d.text((xr-i*cw+7,y0+25),L,font=f,fill='black',direction='ttb',features=['vert'])
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

def render(shots,out,title_band=None,SEC=6,secs=None):
    p=subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',out],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
    for sh in shots:
        src=Image.open(sh['img']).convert('RGB'); n=sh.get('sec',SEC)*FPS
        # manga tone: a bit more contrast
        for i in range(n):
            t=i/FPS
            z=1.0+0.06*i/n
            fr=frame_of(src,sh['ax'],z)
            fr=ImageEnhance.Contrast(fr.convert('RGB')).enhance(1.12).convert('RGBA')
            if sh.get('lines_fx') and t>=sh['lines_fx']: speedlines(fr,sh['fx_center'])
            if title_band: fr.alpha_composite(title_band)
            for ev in sh['events']:
                if t>=ev['t'] and t<ev.get('until',99):
                    if ev['type']=='bubble':
                        k=min(1,(t-ev['t'])*6)  # pop-in
                        bubble(fr,ev['lines'],ev['xy'],ev['tail'],ev.get('kind','round'),int(ev.get('size',60)*(0.7+0.3*k)))
                    elif ev['type']=='cap':
                        caption(fr,ev['lines'],ev['xy'],ev.get('size',50))
                    elif ev['type']=='sfx':
                        k=min(1,(t-ev['t'])*8)
                        sfx(fr,ev['text'],ev['xy'],int(ev.get('size',170)*(1.4-0.4*k)),ev.get('angle',-12))
            p.stdin.write(fr.convert('RGB').tobytes())
    p.stdin.close(); p.wait()
