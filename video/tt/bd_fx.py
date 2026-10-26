# ブレイキングダウン風：あおりVTR・VSポスター・KOテロップ
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageFilter, ImageChops
import random
W,H,FPS=1080,1920,30
R='/home/claude/showa-tetsuo-media/'
GB='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
SB='/usr/share/fonts/opentype/noto/NotoSerifCJK-Black.ttc'
RED=(214,28,28)
def F(p,s): return ImageFont.truetype(p,s)
def cover(im,box_w,box_h,cx=0.5,cy=0.4):
    s=max(box_w/im.width,box_h/im.height); im=im.resize((int(im.width*s)+1,int(im.height*s)+1))
    x=int((im.width-box_w)*cx); y=int((im.height-box_h)*cy); return im.crop((x,y,x+box_w,y+box_h))
def grade(im):
    g=ImageOps.grayscale(im).convert('RGB'); g=ImageEnhance.Contrast(g).enhance(1.5)
    return Image.blend(g,im,0.45)
def ctext(d,t,y,font,fill,stroke=8,sf='black',x=None):
    w=d.textlength(t,font=font); d.text(((W-w)/2 if x is None else x,y),t,font=font,fill=fill,stroke_width=stroke,stroke_fill=sf)
def poster(left_img,right_img,l_nick,l_name,r_nick,r_name,match='第1試合　1分1ラウンド'):
    bg=Image.new('RGB',(W,H),(10,8,8)); d=ImageDraw.Draw(bg)
    rnd=random.Random(3)
    for _ in range(26):
        x=rnd.randint(-400,W); w=rnd.randint(8,60); d.polygon([(x,0),(x+w,0),(x+w+700,H),(x+700,H)],fill=(60+rnd.randint(0,50),8,8))
    top=grade(cover(left_img,W,860,0.5,0.25)); bot=grade(cover(right_img,W,860,0.5,0.2))
    mt=Image.new('L',(W,860),0); ImageDraw.Draw(mt).polygon([(0,0),(W,0),(W,700),(0,860)],fill=255)
    mb=Image.new('L',(W,860),0); ImageDraw.Draw(mb).polygon([(0,160),(W,0),(W,860),(0,860)],fill=255)
    bg.paste(top,(0,180),mt); bg.paste(bot,(0,940),mb)
    d=ImageDraw.Draw(bg)
    d.polygon([(0,1040),(W,880),(W,940),(0,1100)],fill=RED)
    d.rectangle((0,0,W,180),fill=(0,0,0)); d.rectangle((60,50,420,130),fill=RED)
    d.text((80,58),'鉄檻 TEKKAN',font=F(GB,52),fill='white')
    d.text((450,66),match,font=F(GB,40),fill=(240,240,240))
    d.text((60,600),l_nick,font=F(GB,56),fill=(255,206,60),stroke_width=6,stroke_fill='black')
    d.text((60,670),l_name,font=F(SB,150),fill='white',stroke_width=10,stroke_fill='black')
    rw=d.textlength(r_nick,font=F(GB,56)); d.text((W-60-rw,1420),r_nick,font=F(GB,56),fill=(255,206,60),stroke_width=6,stroke_fill='black')
    rw=d.textlength(r_name,font=F(SB,150)); d.text((W-60-rw,1490),r_name,font=F(SB,150),fill='white',stroke_width=10,stroke_fill='black')
    vs=F(SB,260); ctext(d,'VS',830,vs,RED,14,'white')
    d.rectangle((0,1740,W,H),fill=(0,0,0)); ctext(d,'昭和の根性か、令和の筋肉か',1780,F(GB,58),'white',4)
    return bg
def glitch(im,amt,rnd):
    r,g,b=im.split(); r=ImageChops.offset(r,amt,0); b=ImageChops.offset(b,-amt,0); out=Image.merge('RGB',(r,g,b))
    d=ImageDraw.Draw(out)
    for _ in range(6):
        y=rnd.randint(0,H-40); h=rnd.randint(6,40); strip=out.crop((0,y,W,y+h)); out.paste(strip,(rnd.randint(-80,80),y))
    return out
def aori_frames(src,cards,sec_each=1.3):
    """cards: [(line_white, line_red)]"""
    base=ImageEnhance.Brightness(grade(cover(src,W,H))).enhance(0.45)
    rnd=random.Random(7); frames=[]
    for wl,rl in cards:
        n=int(sec_each*FPS)
        for i in range(n):
            fr=base.copy(); d=ImageDraw.Draw(fr)
            ctext(d,wl,760,F(SB,120),'white',6)
            if i>=int(n*0.35): ctext(d,rl,940,F(SB,104),RED,6,'white')
            if i<5 or rnd.random()<0.12: fr=glitch(fr,rnd.randint(8,30),rnd)
            frames.append(fr)
    return frames
def ko_telop(fr,name,tag,y=1480):
    lay=Image.new('RGBA',(W,300),(0,0,0,0)); d=ImageDraw.Draw(lay)
    f=F(GB,110); d.text((70,60),name,font=f,fill='white',stroke_width=10,stroke_fill='black')
    x=70+d.textlength(name,font=f)+20; d.text((x,90),tag,font=F(GB,80),fill=RED,stroke_width=8,stroke_fill='black')
    lay=lay.transform(lay.size,Image.AFFINE,(1,0.25,-60,0,1,0),resample=Image.BICUBIC)
    fr.alpha_composite(lay,(0,y)) if fr.mode=='RGBA' else fr.paste(lay,(0,y),lay)
    return fr
if __name__=='__main__':
    T=Image.open(R+'posts/stock/portrait_tetsuo.png').convert('RGB')
    Z=Image.open(R+'posts/2026-10-27/f_faceoff.png').convert('RGB').crop((500,120,1024,900))
    p=poster(T,Z,'昭和から来た男','権藤鉄男','金髪の狂犬','ZERO'); p.save(R+'posts/2026-10-27/vs_zero.png')
    print('ok')
