import sys; sys.path.insert(0,'/tmp/claude-0/-home-claude/9d5ec005-9cc8-52f5-9eca-474a40bf5cb4/scratchpad')
import tt2
from manga import *
from PIL import Image, ImageDraw, ImageEnhance
P='/home/claude/showa-tetsuo-media/posts/stock/'
W,H,FPS=1080,1920,30
tt2.TITLES['M']='昭和の男、メントスコーラに挑む'
def band():
    b=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(b)
    d.rectangle((0,955,W,1105),fill=(0,0,0,150))
    t1='昭和から来た男 日常'; d.text(((W-d.textlength(t1,font=tt2.f_small))/2,965),t1,font=tt2.f_small,fill=(255,200,60))
    t2='昭和の男、メントスコーラに挑む'; f=tt2.fit(d,t2,58); d.text(((W-d.textlength(t2,font=f))/2,1021),t2,font=f,fill='white'); return b
BAND=band()
shots=[(P+'m01_mentos1.png',0.3,['こんな飴で','何が起きるってんだ'],
        [B(0.4,['こんな飴で','何が起きる','ってんだ'],(880,700),(560,340),48)] if False else None),
       ]
def B(t,l,xy,tail,size=52,until=99,kind='round'): return ('b',t,until,l,xy,tail,size,kind)
SPEC=[(P+'m01_mentos1.png',0.25,6,['こんな飴で','何が起きるってんだ'],[B(0.4,['こんな飴で','何が起きる','ってんだ'],(860,760),(560,330),48)],None),
      (P+'m02_mentos2.png',0.3,6,['……覗いてみるか','ブシャアアア！！'],[SFX:=None] and [] ,(330,380)),
      (P+'m03_mentos3.png',0.35,6,['……計算通りだ','ナウいねぇ'],[B(0.6,['……計算','通りだ'],(160,820),(400,420),54,3.2),('b',3.2,99,['ナウいねぇ'],(160,820),(400,420),58,'shout')],None)]
SPEC[1]=(P+'m02_mentos2.png',0.3,6,['……覗いてみるか','ブシャアアア！！'],[('s',0.1,99,'ブシャアア',(720,260),150,-12),('b',2.0,99,['ぶわっ','ぷ！？'],(880,800),(470,420),54,'shout')],(330,380))
def run(mode):
    out='/home/claude/showa-tetsuo-media/video/'+('tt/2026-xx_mentos_tt.mp4' if mode=='tt' else 'yt/2026-xx_mentos_yt.mp4')
    p=tt2.pipe(out); last=None
    for img,ax,sec,subl,evs,fx in SPEC:
        src=Image.open(img).convert('RGB'); nf=sec*FPS
        for i in range(nf):
            t=i/FPS; fr=frame_of(src,ax,1.0+0.07*i/nf)
            if fx and (mode=='yt' or t<1.2): speedlines(fr,fx)
            if mode=='tt':
                fr.alpha_composite(BAND); d=ImageDraw.Draw(fr)
                shown=subl[:1+min(len(subl)-1,int(i/(nf/len(subl))))]; tt2.subs(d,subl,shown)
            else:
                fr=ImageEnhance.Contrast(fr.convert('RGB')).enhance(1.12).convert('RGBA')
                for e in evs:
                    if not(e[1]<=t<e[2]): continue
                    k=min(1,(t-e[1])*6)
                    if e[0]=='b': bubble(fr,e[3],e[4],e[5],e[7],int(e[6]*(0.7+0.3*k)))
                    elif e[0]=='s': sfx(fr,e[3],e[4],int(e[5]*(1.4-0.4*min(1,(t-e[1])*8))),e[6])
            last=fr.convert('RGB'); p.stdin.write(last.tobytes())
    if mode=='tt': tt2.endcard(last,p)
    p.stdin.close(); p.wait(); print('done',mode)
run(sys.argv[1])
