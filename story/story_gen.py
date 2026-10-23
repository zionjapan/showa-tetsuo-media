import sys, re, datetime
sys.path.insert(0,'/tmp/claude-0/-home-claude/9d5ec005-9cc8-52f5-9eca-474a40bf5cb4/scratchpad')
import tt2
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
F='/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; W,H=1080,1920; Y=(255,210,60)
R='/home/claude/showa-tetsuo-media/'; ST=R+'posts/stock/'; OUT=R+'story/'
def make(src,out,lines,ax=0.4,band=None):
    im=Image.open(src).convert('RGB'); s=max(W/im.width,H/im.height)
    im=im.resize((int(im.width*s),int(im.height*s))); x=int((im.width-W)*ax); y=int((im.height-H)*0.2); im=im.crop((x,y,x+W,y+H))
    im=ImageEnhance.Brightness(im).enhance(0.9).convert('RGBA')
    if band: ov=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(ov).rectangle((0,band[0],W,band[1]),fill=(0,0,0,140)); im.alpha_composite(ov)
    im=im.convert('RGB'); d=ImageDraw.Draw(im)
    for t,yy,sz,c in lines:
        f=ImageFont.truetype(F,sz)
        while d.textlength(t,font=f)>960: sz-=4; f=ImageFont.truetype(F,sz)
        d.text(((W-d.textlength(t,font=f))/2,yy),t,font=f,fill=c,stroke_width=8,stroke_fill='black')
    im.save(out,quality=90)
# morning: stock + one-liner (top area)
AM={24:('k10_sauna.png','朝サウナ','……ととのった'),25:('k09_nunchaku.png','ユウトの板っきれ','ヌンチャクに丁度いい'),
26:('k03_autodoor.png','自動ドアが','オレを無視しやがる'),27:('k25_geta_bike.png','朝練は下駄','自転車より速ぇ'),
28:('k24_raw_eggs.png','試合当日の朝飯','生卵10個'),29:('k21_tire_stairs.png','ダウンした翌朝も','石段ダッシュだ'),
30:('k27_haru_watch.png','夜の河原','……誰か見てた気がする'),31:('k11_scramble.png','ハロウィンの渋谷','流される……！'),
1:('k06_100yen.png','全部100円だと！？','令和は天国か'),2:('k14_kotatsu.png','こたつとみかん','これだけは昭和と同じだ'),
3:('k17_lecture.png','ユウトの大学に','潜り込んでみた'),4:('k05_karaoke.png','演歌は','魂で歌うもんだ'),
5:('k08_protein.png','ぷろていん','……砂の味がする'),6:('k20_catcafe.png','猫にまで','無視される男'),7:('k28_waterfall.png','真冬の滝行','根性は裏切らねぇ')}
def ep_img(n):
    if n in (8,9,10):
        P=R+'posts/2026-10-27/'; return {8:P+'f_faceoff.png',9:P+'f_getup.png',10:P+'victory.png'}[n]
    script='reel%d.py'%(n-1 if n<=7 else n-3)
    s=open(tt2.S+script).read(); P=re.search(r"P='([^']+)'",s).group(1)
    return eval(re.search(r'shots=(\[.*?\])\n',s,re.S).group(1),{'P':P})[0][0]
for n in range(4,19):
    d=datetime.date(2026,10,20)+datetime.timedelta(days=n); key=d.day
    img,a,b=AM[key]
    make(ST+img,OUT+f'{d.isoformat()}_story_am.jpg',[(a,200,92,'white'),(b,320,100,Y)],band=(170,450))
    make(ep_img(n),OUT+f'{d.isoformat()}_story_pm.jpg',[('今夜19時',1200,110,Y),(tt2.TITLES[n],1350,76,'white'),(f'昭和から来た男 #{n}',1480,64,Y)],band=(1170,1580))
    print(d, n)
