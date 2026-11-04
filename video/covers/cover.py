# 本編の表紙（大きい文字・一覧で読める）を作る。あらすじ表紙が伸びたので標準にする（ボス 11/4）
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import sys
R='/home/claude/showa-tetsuo-media/'; W,H=1080,1920; F='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; Y=(255,210,60)
# 1行は7文字くらいまでに区切る（一覧の小さい表紙でも読めるように）
EP={
 15:('posts/2026-11-01/sushi.png',0.4,['47年、','雨の中で','待っていた人']),
 16:('posts/2026-11-02/treadmill.png',0.4,['昭和の男、','令和のジムで','吹っ飛ぶ']),
 17:('posts/2026-11-03/shichigosan.png',0.45,['昭和の男、','ネカフェで','力尽きる']),
 18:('posts/2026-11-04/revolving.png',0.4,['ハルさんの指に','あの日の指輪']),
}
def make(n,img,ax,lines):
    im=Image.open(R+img).convert('RGB'); s=max(W/im.width,H/im.height); im=im.resize((int(im.width*s),int(im.height*s)))
    x=int((im.width-W)*ax); y=int((im.height-H)*0.15); im=im.crop((x,y,x+W,y+H)); im=ImageEnhance.Brightness(im).enhance(0.85).convert('RGBA')
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(ov).rectangle((0,1060,W,1760),fill=(0,0,0,175)); im=Image.alpha_composite(im,ov).convert('RGB'); d=ImageDraw.Draw(im)
    def t(txt,y,sz,col):
        f=ImageFont.truetype(F,sz)
        while d.textlength(txt,font=f)>1010: sz-=4; f=ImageFont.truetype(F,sz)
        d.text(((W-d.textlength(txt,font=f))/2,y),txt,font=f,fill=col,stroke_width=12,stroke_fill='black')
    if STYLE=='series':  # シリーズ名と番号を主役に、題名は小さく
        t('昭和から来た男',1090,130,'white'); t(f'#{n}',1240,260,Y); t(''.join(lines),1560,80,'white')
    else:
        t(f'昭和から来た男 #{n}',1085,64,Y)
        y=1180 if len(lines)==3 else 1250
        for k,L in enumerate(lines):
            t(L,y,175,Y if k==len(lines)-1 else 'white'); y+=190
    out=R+f'video/covers/cover_{n}'+('_series' if STYLE=='series' else '')+'.jpg'; im.save(out,quality=92); print(out)
args=sys.argv[1:]; STYLE='series' if 'series' in args else 'title'
for n in ([int(a) for a in args if a.isdigit()] or EP):
    make(n,*EP[n])
