from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import subprocess, sys
R='/home/claude/showa-tetsuo-media/'
W,H,FPS,SEC=1080,1920,30,8
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'
fh=ImageFont.truetype(F,62);fs=ImageFont.truetype(F,40);fb=ImageFont.truetype(F,80);fl=ImageFont.truetype(F,40)
C=[ # num, name, img, ax, hook, lines
(7,'s_phone','k16_phonebooth.png',0.6,'令和で公衆電話を見つけた男',['会いたかったぜ','……相棒']),
(8,'e_street','e03.png',0.5,'昭和の男、渋谷の路上で演歌を熱唱',['令和のヒヨッコども','聴いていきな']),
(9,'j_meoshi','s01.png',0.6,'昭和の男、獣王に座る',['目押しは','昭和の必修科目だ']),
(10,'s_salon','k07_salon.png',0.4,'昭和の男、美容院に行く',['毛先を','整えてくんな']),
(11,'e_snack','e01.png',0.4,'昭和の男、スナックで熱唱',['ママ、','次は銀恋だ']),
(12,'j_atari','s02.png',0.5,'昭和の男、獣王で大当たり',['サバンナが','オレを呼んでる！']),
(13,'s_matchapp','k02_matchapp.png',0.6,'マッチングアプリの写真を撮る男',['これで令和の娘も','イチコロだ']),
(14,'e_kobushi','e02.png',0.3,'昭和の男、こぶし講座',['腹から出せ','これが昭和のこぶしだ']),
(15,'s_vr','k12_vr.png',0.5,'昭和の男、VRで戦う',['敵はどこだ！','……あ、電気が']),
(16,'e_sunset','e04.png',0.5,'昭和の男、夕日に向かって熱唱',['泣くんじゃねぇ','……オレもだ']),
(17,'s_vintage','k15_vintage.png',0.3,'古着屋で自分の服を見つけた男',['オレの普段着が','この値段！？']),
(18,'g_shinbun','g01.png',0.4,'昭和の男、競馬新聞で予想',['この馬は','目が死んでねぇ']),
(19,'s_ticket','k18_ticket.png',0.6,'ラーメン屋の券売機に挑む男',['大将はどこだ','注文させろ']),
(20,'g_zekkyo','g02.png',0.4,'昭和の男、ゴール前で絶叫',['差せ！','差せぇぇぇ！！']),
(21,'s_pushup','k22_pushup_zero.png',0.6,'弟子を背中に乗せて腕立て',['ZERO、重てぇ','……あと100回']),
(22,'g_kamifubuki','g03.png',0.4,'昭和の男、馬券が紙吹雪',['……','これが昭和の散り際だ']),
(23,'s_mitt','k26_mitt_zero.png',0.3,'ヒョロヒョロ師匠のミット打ち',['構えとけって','言っただろ']),
(24,'g_keirin','g04.png',0.4,'昭和の男、競輪場で絶叫',['まくれ！','まくれぇぇぇ！！']),
(25,'g_kanpai','g05.png',0.4,'20歳、競輪場で乾杯',['オレ、20歳だ','……誰も信じねぇ']),
(26,'s_tire','k23_tire_punch.png',0.3,'高架下の夜練',['次の試合まで','あと少しだ']),
]
def run(c):
    num,name,img,ax,hook,lines=c
    src=Image.open(R+'posts/stock/'+img).convert('RGB'); n=SEC*FPS
    out=R+f'video/igreel/v2/{name}.mp4'
    p=subprocess.Popen(['ffmpeg','-nostdin','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','20','-movflags','+faststart',out],stdin=subprocess.PIPE,stderr=subprocess.DEVNULL)
    label=f'昭和の男、令和に挑戦 #{num}'
    for i in range(n):
        z=1.0+0.10*i/n; cs=max(W/src.width,H/src.height)*z
        im=src.resize((int(src.width*cs),int(src.height*cs)),Image.BILINEAR)
        cx=int((im.width-W)*ax); cy=int((im.height-H)*0.15)
        fr=im.crop((cx,cy,cx+W,cy+H)).convert('RGBA')
        ov=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
        d.rectangle((0,1010,W,1200),fill=(0,0,0,150))
        tw=d.textlength(label,font=fl); d.text(((W-tw)/2,1022),label,font=fl,fill=(255,255,255))
        f=fh; s=62
        while d.textlength(hook,font=f)>1000: s-=4; f=ImageFont.truetype(F,s)
        tw=d.textlength(hook,font=f); d.text(((W-tw)/2,1090),hook,font=f,fill=(255,210,74),stroke_width=3,stroke_fill='black')
        if i>=int(FPS*1.8):
            y=1300
            for k,L in enumerate(lines):
                if i>=int(FPS*(1.8+1.2*k)):
                    tw=d.textlength(L,font=fb); d.text(((W-tw)/2,y),L,font=fb,fill='white' if k<len(lines)-1 else (255,236,150),stroke_width=8,stroke_fill='black')
                y+=120
        d.text((W-330,1840),'@showa_tetsuo',font=fs,fill=(255,255,255,200),stroke_width=2,stroke_fill='black')
        fr=Image.alpha_composite(fr,ov).convert('RGB'); p.stdin.write(fr.tobytes())
    e=ImageEnhance.Brightness(fr.filter(ImageFilter.GaussianBlur(14))).enhance(0.4); d=ImageDraw.Draw(e)
    for t,y,sz,c in [('フォローしとけ',900,110,(255,200,60)),('明日も令和に',1060,84,'white'),('殴り込むぜ',1170,84,'white')]:
        f=ImageFont.truetype(F,sz); w=d.textlength(t,font=f); d.text(((W-w)/2,y),t,font=f,fill=c,stroke_width=9,stroke_fill='black')
    b=e.tobytes()
    for _ in range(int(1.5*FPS)): p.stdin.write(b)
    p.stdin.close(); p.wait()
import os; os.makedirs(R+'video/igreel/v2',exist_ok=True)
for c in C: run(c)
print('done')
