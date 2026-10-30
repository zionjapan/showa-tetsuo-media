import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bd_fx import *
from PIL import Image, ImageDraw, ImageEnhance
V='/home/claude/showa-tetsuo-media/video/future/'; SRC=V+'future_ufc_v1.mp4'; OUT=V+'future_ufc.mp4'
def run(c): subprocess.run(c, check=True)
# 冒頭テロップ
op=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(op)
d.rectangle((0,1440,W,1640),fill=(0,0,0,150))
ctext(d,'20XX年',1455,F(SB,110),'white',8)
ctext(d,'世界王座戦',1575,F(GB,46),(255,206,60),5)
op.save(V+'_op.png')
run(['ffmpeg','-v','error','-y','-i',SRC,'-loop','1','-t','3.2','-i',V+'_op.png','-filter_complex',
 "[1:v]format=rgba,fade=t=in:st=0.3:d=0.4:alpha=1,fade=t=out:st=2.6:d=0.4:alpha=1[o];[0:v][o]overlay=0:0:eof_action=pass",
 '-c:v','libx264','-pix_fmt','yuv420p','-r','30','-c:a','aac','-ar','44100','-ac','2',V+'_a.mp4'])
# 締め：最後のコマを止めて一言
run(['ffmpeg','-v','error','-y','-sseof','-0.1','-i',SRC,'-frames:v','1',V+'_last.png'])
e=ImageEnhance.Brightness(Image.open(V+'_last.png').convert('RGB').resize((W,H))).enhance(0.4); d=ImageDraw.Draw(e)
ctext(d,'これは、',760,F(SB,80),'white',8)
ctext(d,'昭和から来た男の',870,F(SB,96),'white',8)
ctext(d,'未来かもしれない',990,F(SB,96),(255,206,60),8)
ctext(d,'権藤鉄男　毎日19時更新',1300,F(GB,50),'white',6)
e.save(V+'_end.png')
run(['ffmpeg','-v','error','-y','-loop','1','-t','3.5','-i',V+'_end.png','-sseof','-3.5','-i',SRC,'-map','0:v','-map','1:a',
 '-vf','fade=t=in:d=0.5','-af','volume=0.6,afade=t=out:st=2.5:d=1','-shortest','-r','30','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac','-ar','44100','-ac','2',V+'_b.mp4'])
open(V+'_l.txt','w').write(f"file '{V}_a.mp4'\nfile '{V}_b.mp4'\n")
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',V+'_l.txt','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-c:a','aac','-movflags','+faststart',OUT])
for p in ['_op.png','_a.mp4','_last.png','_end.png','_b.mp4','_l.txt']: os.remove(V+p)
print('done')
