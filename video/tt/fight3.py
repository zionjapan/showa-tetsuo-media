# ZERO戦 3話（TikTok字幕版 / YouTube漫画版）
import sys; sys.path.insert(0,'/tmp/claude-0/-home-claude/9d5ec005-9cc8-52f5-9eca-474a40bf5cb4/scratchpad')
import tt2, manga, bd_fx
from manga import bubble, caption, sfx, speedlines, frame_of
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
W,H,FPS=1080,1920,30
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
P='/home/claude/showa-tetsuo-media/posts/2026-10-27/'
sm=ImageFont.truetype(F,34); clk=ImageFont.truetype(F,40)
def B(t,l,xy,tail,size=52,until=99,kind='round'): return ('b',t,until,l,xy,tail,size,kind)
def SH(t,l,xy,tail,size=54,until=99): return B(t,l,xy,tail,size,until,'shout')
def CAP(t,l,xy,size=46,until=99): return ('c',t,until,l,xy,size)
def SF(t,txt,xy,size=150,ang=-12,until=99): return ('s',t,until,txt,xy,size,ang)
# panel: img, ax, sec, subtitles(TikTok), manga events, clock(start,end) or 'KO' or None, speedline center
EP={
8:[(P+'entrance.png',0.45,5,['預かっとけ、ユウト','ここから先は','素顔で行く'],[B(0.3,['預かっとけ','ユウト'],(830,260),(460,300),52,2.6),B(2.6,['ここから先は','素顔で行く'],(830,260),(460,300),52)],None,None),
   (P+'f_faceoff.png',0.3,5,['「ジジイみてぇな顔しやがって！」','……よく吠える犬だねぇ'],[CAP(0.1,['試合開始'],(70,820),48),SH(0.6,['ジジイみてぇな','顔しやがって！'],(870,1080),(690,590),46),B(2.8,['……よく吠える','犬だねぇ'],(520,190),(380,430),44)],(60,56),None),
   (P+'f_hit.png',0.3,5,['ZEROの右ストレートが','顔面に直撃！'],[SF(0.1,'ドガッ',(560,230),170,-14)],(56,51),(330,430)),
   (P+'f_down.png',0.3,5,['ダウン！！','鉄檻ルール：10カウント','立てるのか、鉄男！？'],[SF(0.1,'ダウン！！',(330,950),140,-8),CAP(1.2,['鉄檻ルール','ダウンは','10カウント'],(130,330),46),CAP(3.0,['次回','立てるのか鉄男！？'],(880,1350),46)],(51,51),None)],
9:[(P+'f_yuto.png',0.3,5,['「鉄男さぁぁん！！」','カウント……7……8……'],[SH(0.3,['鉄男','さぁぁん！！'],(200,260),(352,1040),56),CAP(2.4,['カウント','7……8……'],(900,1200),46)],(51,51),None),
   (P+'f_getup.png',0.3,6,['……ふぁ～あ','昼寝してただけだ','効いてねぇよ'],[B(0.5,['……ふぁ～あ'],(560,190),(690,630),50,2.6),B(2.6,['昼寝して','ただけだ'],(560,200),(690,630),52)],(51,42),None),
   (P+'f_tackle.png',0.3,4,['怒ったZEROがタックル！','……甘ぇな'],[SF(0.1,'ダダッ',(300,210),150,-10),B(1.6,['……甘ぇな'],(880,260),(620,430),54)],(42,38),None),
   (P+'f_throw.png',0.3,6,['突っ込んできたZEROを','ちゃぶ台返し！！','残り10秒、次回決着'],[SH(0.4,['ちゃぶ台','返し！！'],(220,210),(340,560),54),SF(0.2,'ドッシャーン',(760,1250),130,-10),CAP(4.0,['残り10秒','次回、決着'],(150,1250),46)],(38,10),(600,500))],
10:[(P+'ko.png',0.95,6,['昭和ゲンコツ','一発！！'],[SF(0.15,'ドゴォッ',(700,250),150,-14),SH(0.8,['昭和ゲンコツ','一発！'],(560,200),(300,340),54)],(10,2),(800,500)),
    (P+'victory.png',0.4,7,['1R 0:58 KO勝ち','令和のヒヨッコども','見たか'],[CAP(0.3,['1R 0:58','KO勝ち'],(160,1150),50),B(1.5,['令和の','ヒヨッコども','見たか'],(860,300),(480,480),50)],'KO',None),
    (P+'f_glasses.png',0.3,7,['ユウト、グラサン','……ナウいねぇ'],[B(0.4,['ユウト','グラサン'],(830,230),(400,420),52,3.0),SH(3.0,['ナウいねぇ'],(830,240),(400,420),60)],'KO',None)],
}
def hud(fr,clock,t,sec):
    d=ImageDraw.Draw(fr)
    d.rectangle((40,215,300,275),fill=(170,20,20)); d.text((60,221),'鉄檻 TEKKAN',font=sm,fill='white')
    if clock is None:
        d.rectangle((300,215,420,275),fill=(0,0,0)); d.text((318,221),'LIVE',font=sm,fill=(255,60,60)); return
    if clock=='KO':
        d.rectangle((300,215,560,275),fill=(0,0,0)); d.text((318,219),'1R 0:58 KO',font=clk,fill=(255,200,60)); return
    a,b=clock; rem=a+(b-a)*min(1,t/sec); s=max(0,int(round(rem)))
    d.rectangle((300,215,470,275),fill=(0,0,0)); d.text((318,219),f'残り0:{s:02d}',font=ImageFont.truetype(F,34),fill='white')
def draw_manga(fr,evs,t):
    for e in evs:
        if not(e[1]<=t<e[2]): continue
        k=min(1,(t-e[1])*6)
        if e[0]=='b': bubble(fr,e[3],e[4],e[5],e[7],int(e[6]*(0.7+0.3*k)))
        elif e[0]=='c': caption(fr,e[3],e[4],e[5])
        elif e[0]=='s': sfx(fr,e[3],e[4],int(e[5]*(1.4-0.4*min(1,(t-e[1])*8))),e[6])
def render(n,mode):
    out=(tt2.OUT+tt2.fname(n)) if mode=='tt' else ('/home/claude/showa-tetsuo-media/video/yt/'+tt2.fname(n).replace('tiktok','yt'))
    p=tt2.pipe(out); last=None
    if n==8:
        src0=Image.open(P+'f_faceoff.png').convert('RGB')
        for fr in bd_fx.aori_frames(src0,[('昭和 VS 令和','ガリガリが金髪を喰う'),('素人のジジイ顔が','鉄檻の狂犬に挑む')]):
            p.stdin.write(fr.tobytes())
        post=Image.open(P+'vs_zero.png').convert('RGB')
        for i in range(int(2.5*FPS)):
            z=1.0+0.04*i/(2.5*FPS); im=post.resize((int(W*z),int(H*z))); x=(im.width-W)//2; y=(im.height-H)//2
            p.stdin.write(im.crop((x,y,x+W,y+H)).tobytes())
    for img,ax,sec,subl,evs,clock,fx in EP[n]:
        src=Image.open(img).convert('RGB'); nf=sec*FPS
        for i in range(nf):
            t=i/FPS
            fr=frame_of(src,ax,1.0+(0.08 if mode=='tt' else 0.05)*i/nf)
            if fx:
                if mode=='yt' or t<1.2: speedlines(fr,fx)
            if mode=='tt':
                fr.alpha_composite(tt2.band(n))
            else:
                fr=ImageEnhance.Contrast(fr.convert('RGB')).enhance(1.12).convert('RGBA')
            hud(fr,clock,t,sec)
            if mode=='tt':
                d=ImageDraw.Draw(fr)
                shown=subl[:1+min(len(subl)-1,int(i/(nf/len(subl))))]
                tt2.subs(d,subl,shown)
                for e in evs:
                    if e[0]=='s' and e[1]<=t: sfx(fr,e[3],(e[4][0],e[4][1] if e[4][1]<900 else 640),int(e[5]*0.8),e[6])
            else:
                draw_manga(fr,evs,t)
            if n==10 and img.endswith('ko.png') and t>=1.0:
                bd_fx.ko_telop(fr,'権藤鉄男','（鉄檻1）',y=(700 if mode=='tt' else 1480))
            last=fr.convert('RGB'); p.stdin.write(last.tobytes())
    if mode=='tt': tt2.endcard(last,p)
    p.stdin.close(); p.wait(); print('done',mode,n)
if __name__=='__main__':
    for a in sys.argv[2:]: render(int(a),sys.argv[1])
