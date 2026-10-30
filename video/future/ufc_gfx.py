import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bd_fx import *
from PIL import Image, ImageDraw
O='/home/claude/showa-tetsuo-media/video/future/gfx/'; os.makedirs(O,exist_ok=True)
GOLD=(212,175,55)
def lower(name_jp, nick, flag, rec, fn, col):
    im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
    y=1420
    d.rectangle((40,y,W-40,y+70),fill=col+(235,))
    d.text((70,y+10),nick,font=F(GB,40),fill='white')
    d.rectangle((40,y+70,W-40,y+200),fill=(10,10,10,235))
    d.text((70,y+82),name_jp,font=F(GB,80),fill='white')
    d.text((W-70-d.textlength(flag,font=F(GB,40)),y+110),flag,font=F(GB,40),fill=GOLD)
    d.rectangle((40,y+200,W-40,y+260),fill=(30,30,30,235))
    d.text((70,y+208),rec,font=F(GB,36),fill=(220,220,220))
    im.save(O+fn)
lower('権藤 鉄男','“THE SHOWA MAN”','JAPAN','23勝1敗　ヘビー級 1位','lt_tetsuo.png',(200,16,46))
lower('ヴァイ・トゥポウ','“THE TONGAN WALL”','TONGA','31勝1敗　ヘビー級 王者','lt_champ.png',(20,60,160))
# 身長体重比較
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
d.rectangle((40,520,W-40,1400),fill=(8,8,12,230))
d.rectangle((40,520,W-40,620),fill=GOLD+(255,))
t='世界ヘビー級タイトルマッチ'; d.text(((W-d.textlength(t,font=F(GB,52)))/2,540),t,font=F(GB,52),fill='black')
d.text((90,650),'権藤',font=F(GB,70),fill=(255,80,80)); t='トゥポウ'; d.text((W-90-d.textlength(t,font=F(GB,70)),650),t,font=F(GB,70),fill=(110,160,255))
rows=[('23-1-0','戦績','31-1-0'),('181cm','身長','198cm'),('118kg','体重','131kg'),('193cm','リーチ','206cm'),('23','KO勝ち','27'),('昭和','出身','トンガ')]
for i,(a,k,b) in enumerate(rows):
    y=790+i*96
    d.line((90,y-12,W-90,y-12),fill=(70,70,70),width=2)
    d.text((90,y),a,font=F(GB,52),fill='white')
    d.text(((W-d.textlength(k,font=F(GB,40)))/2,y+8),k,font=F(GB,40),fill=GOLD)
    d.text((W-90-d.textlength(b,font=F(GB,52)),y),b,font=F(GB,52),fill='white')
im.save(O+'tale.png')
# スコアバー
im=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(im)
y=1760; d.rectangle((40,y,W-40,y+80),fill=(10,10,10,230))
d.rectangle((40,y,60,y+80),fill=(200,16,46)); d.rectangle((W-60,y,W-40,y+80),fill=(20,60,160))
d.text((80,y+14),'権藤',font=F(GB,46),fill='white'); t='トゥポウ'; d.text((W-80-d.textlength(t,font=F(GB,46)),y+14),t,font=F(GB,46),fill='white')
t='R1  5:00'; d.text(((W-d.textlength(t,font=F(GB,46)))/2,y+14),t,font=F(GB,46),fill=GOLD)
d.rectangle((40,200,330,262),fill=(200,16,46,235)); d.text((60,206),'ZION FC 1',font=F(GB,40),fill='white')
d.rectangle((330,200,450,262),fill=(0,0,0,235)); d.text((350,206),'LIVE',font=F(GB,40),fill=(255,60,60))
im.save(O+'scorebar.png')
print('ok')
