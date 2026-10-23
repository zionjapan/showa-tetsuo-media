# TikTok本編 v2レイアウト：フック帯を上部、字幕をTikTokのUIにかからない位置へ
import re, sys, subprocess, random
from PIL import Image, ImageFilter, ImageDraw, ImageFont
S='/tmp/claude-0/-home-claude/9d5ec005-9cc8-52f5-9eca-474a40bf5cb4/scratchpad/'
OUT='/home/claude/showa-tetsuo-media/video/tt/'
W,H,FPS=1080,1920,30
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
CX=505          # 右のアイコン列を避けて少し左寄せ
MAXW=860
BOTTOM=1430     # ここより下はTikTokの名前・説明文エリア
OLD={3:'格闘技オーディションに乱入',4:'金髪ファイターと因縁勃発',5:'プロの拳を全部よける男',6:'銭湯のおばあちゃんが泣いた理由',
 7:'ガリガリ男、58秒でKO',8:'KOした翌日、宿敵が動いた',9:'最強の男、80歳に完敗',10:'会長の正体は47年前の宿敵',
 11:'47年前の約束、相手はハルさん',12:'47年、雨の中で待っていた人',13:'昭和の男、令和のジムで吹っ飛ぶ',
 14:'昭和の男、ネカフェで力尽きる',15:'ハルさんの指に、あの日の指輪'}
TITLES={2:'令和のコンビニで大事件',3:'チンピラ瞬殺、まさかのスカウト'}
TITLES.update({k+1:v for k,v in OLD.items() if k<7})
TITLES.update({k+3:v for k,v in OLD.items() if k>=8})
TITLES.update({8:'ZERO戦 前半、まさかのダウン',9:'ZERO戦 中盤、昼寝からの逆襲',10:'ZERO戦 決着、58秒の昭和ゲンコツ'})
import datetime
def fname(n,suffix=''):
    d=datetime.date(2026,10,20)+datetime.timedelta(days=n)
    return f'{d.isoformat()}_tiktok{n}{suffix}.mp4'
f_small=ImageFont.truetype(F,40); f_title=ImageFont.truetype(F,58)
def fit(d,t,size):
    while True:
        f=ImageFont.truetype(F,size)
        if d.textlength(t,font=f)<=MAXW or size<40: return f
        size-=4
band_cache={}
def band(n):
    if n in band_cache: return band_cache[n]
    b=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(b)
    d.rectangle((0,955,W,1105),fill=(0,0,0,150))
    t1=f'昭和から来た男 #{n}'; d.text(((W-d.textlength(t1,font=f_small))/2,965),t1,font=f_small,fill=(255,200,60))
    t2=TITLES[n]; ft=fit(d,t2,58)
    d.text(((W-d.textlength(t2,font=ft))/2,1021),t2,font=ft,fill='white')
    band_cache[n]=b; return b
def subs(d,lines,shown,size=74,lh=106):
    y=1120
    for k,L in enumerate(shown):
        f=fit(d,L,size); tw=d.textlength(L,font=f)
        last=(k==len(lines)-1 and len(shown)==len(lines) and len(lines)>1)
        d.text((CX-tw/2,y),L,font=f,fill=(255,236,150) if last else 'white',stroke_width=8,stroke_fill='black')
        y+=lh
def endcard(last,p):
    im=last.filter(ImageFilter.GaussianBlur(14))
    from PIL import ImageEnhance
    im=ImageEnhance.Brightness(im).enhance(0.4); d=ImageDraw.Draw(im)
    for t,y,sz,c in [('続きは',1000,96,'white'),('フォローして',1120,110,(255,200,60)),('待っとけ',1260,110,'white')]:
        f=ImageFont.truetype(F,sz);w=d.textlength(t,font=f)
        d.text((CX-w/2,y),t,font=f,fill=c,stroke_width=9,stroke_fill='black')
    b=im.tobytes()
    for _ in range(2*FPS): p.stdin.write(b)
def pipe(out):
    return subprocess.Popen(['ffmpeg','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',out],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)

def reel(n,script):
    src_code=open(S+script).read()
    P=re.search(r"P='([^']+)'",src_code).group(1)
    shots=eval(re.search(r"shots=(\[.*?\])\n",src_code,re.S).group(1),{'P':P})
    out=fname(n)
    p=pipe(OUT+out); SEC=6
    for f,ax,lines in shots:
        src=Image.open(f).convert('RGB'); nfr=SEC*FPS
        for i in range(nfr):
            z=1.0+0.10*i/nfr
            cs=max(W/src.width,H/src.height)*z
            im=src.resize((int(src.width*cs),int(src.height*cs)),Image.BILINEAR)
            cx=int((im.width-W)*ax); cy=int((im.height-H)*0.15)
            fr=im.crop((cx,cy,cx+W,cy+H)).convert('RGBA')
            fr.alpha_composite(band(n)); fr=fr.convert('RGB')
            d=ImageDraw.Draw(fr)
            shown=lines[:1+min(len(lines)-1,int(i/(nfr/len(lines))))]
            subs(d,lines,shown)
            p.stdin.write(fr.tobytes())
    if n>=3: endcard(fr,p)
    p.stdin.close(); p.wait(); print('done',out)

def fight():
    P='/home/claude/showa-tetsuo-media/posts/2026-10-27/'
    mid=ImageFont.truetype(F,48); sm=ImageFont.truetype(F,34)
    shots=[(P+'entrance.png',0.45,6,['預かっとけ、ユウト','ここから先は','素顔で行く'],'entrance'),
           (P+'ko.png',0.95,6,['昭和ゲンコツ','一発！'],'ko'),
           (P+'victory.png',0.4,7,['令和のヒヨッコども','見たか','ナウいねぇ'],'win')]
    p=pipe(OUT+fname(8,'_fight'))
    for f,ax,sec,lines,kind in shots:
        src=Image.open(f).convert('RGB'); nfr=sec*FPS
        for i in range(nfr):
            z=1.0+(0.03 if kind=='ko' else 0.08)*i/nfr
            cs=max(W/src.width,H/src.height)*z
            im=src.resize((int(src.width*cs),int(src.height*cs)),Image.BILINEAR)
            cx=int((im.width-W)*ax); cy=int((im.height-H)*0.15)
            if kind=='ko' and i<12:
                cx+=random.randint(-18,18); cy+=random.randint(-18,18)
                cx=max(0,min(cx,im.width-W)); cy=max(0,min(cy,im.height-H))
            fr=im.crop((cx,cy,cx+W,cy+H))
            if kind=='ko' and i<5: fr=Image.blend(fr,Image.new('RGB',(W,H),'white'),1-i/5)
            fr=fr.convert('RGBA'); fr.alpha_composite(band(8)); fr=fr.convert('RGB')
            d=ImageDraw.Draw(fr)
            d.rectangle((40,215,300,275),fill=(170,20,20)); d.text((60,221),'鉄檻 TEKKAN',font=sm,fill='white')
            d.rectangle((300,215,420,275),fill=(0,0,0)); d.text((318,221),'LIVE',font=sm,fill=(255,60,60))
            top=-999
            if False:
                d.rectangle((0,top,W,top+70),fill=(0,0,0))
                d.text((60,top+10),'権藤鉄男',font=mid,fill='white'); d.text((440,top+10),'VS',font=mid,fill=(222,184,92)); d.text((580,top+10),'ZERO',font=mid,fill='white')
            else:
                d.rectangle((0,top-10,W,top+80),fill=(170,20,20))
                t='1R 0:58 KO勝ち 権藤鉄男'; tw=d.textlength(t,font=mid); d.text((CX-tw/2,top+8),t,font=mid,fill='white')
            shown=lines[:1+min(len(lines)-1,int(i/(nfr/len(lines))))]
            subs(d,lines,shown)
            p.stdin.write(fr.tobytes())
    endcard(fr,p)
    p.stdin.close(); p.wait(); print('done fight')

if __name__=='__main__':
    for a in sys.argv[1:]:
        n=int(a)
        if n==3: reel(3,'reel_scout.py')
        elif n==2: reel(2,'reel2.py')
        elif n<=7: reel(n,f'reel{n-1}.py')
        elif n>=11: reel(n,f'reel{n-3}.py')
