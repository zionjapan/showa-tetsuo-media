import sys, os, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bd_fx import *
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
V='/home/claude/showa-tetsuo-media/video/future/'; G=V+'gfx/'; T=V+'_t/'; os.makedirs(T,exist_ok=True)
OUT=V+'future_ufc_full_v2.mp4'
ENC=['-r','30','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-c:a','aac','-ar','44100','-ac','2']
def run(c): subprocess.run(c, check=True)
segs=[]
def seg(src, ss, t, overlays=(), name=None, fadein=False):
    # overlays: [(png, start, end)]
    o=T+f'{len(segs):02d}.mp4'; cmd=['ffmpeg','-v','error','-y','-ss',str(ss),'-t',str(t),'-i',src]
    for p,_,_ in overlays: cmd+=['-loop','1','-t',str(t),'-i',p]
    fc='[0:v]scale=1080:1920,setsar=1,fps=30'+(',fade=t=in:d=0.3' if fadein else '')+'[v0]'
    last='v0'
    for i,(p,s,e) in enumerate(overlays):
        fc+=f';[{i+1}:v]format=rgba,fade=t=in:st={s}:d=0.3:alpha=1[g{i}];[{last}][g{i}]overlay=0:0:enable=\'between(t,{s},{e})\'[v{i+1}]'; last=f'v{i+1}'
    cmd+=['-filter_complex',fc,'-map',f'[{last}]','-map','0:a','-af','afade=t=in:d=0.15']+ENC+[o]
    run(cmd); segs.append(o)
def still(img, t, audio_src, ass):
    o=T+f'{len(segs):02d}.mp4'; img.save(T+'s.png')
    run(['ffmpeg','-v','error','-y','-loop','1','-t',str(t),'-i',T+'s.png','-ss',str(ass),'-t',str(t),'-i',audio_src,'-map','0:v','-map','1:a',
         '-vf','fade=t=in:d=0.4','-af','volume=0.7,afade=t=in:d=0.3'+(',afade=t=out:st=%.1f:d=1'%(t-1.2))]+ENC+[o]); segs.append(o)
FU=V+'future_ufc_v1.mp4'
# オープニング
op=Image.new('RGBA',(W,H),(0,0,0,0)); d=ImageDraw.Draw(op); d.rectangle((0,1440,W,1640),fill=(0,0,0,150))
ctext(d,'20XX年',1455,F(SB,110),'white',8); ctext(d,'ZION FC 1　世界王座戦',1575,F(GB,46),(255,206,60),5); op.save(T+'op.png')
seg(FU,0,3.15,[(T+'op.png',0.2,3.15)])
seg(V+'b_walk_champ.mp4',0,6,[(G+'lt_champ.png',1.2,6)])
seg(V+'a_walk_tetsuo.mp4',0,8,[(G+'lt_tetsuo.png',1.5,8)])
seg(V+'c_cage.mp4',0,9.5)
# 身長体重比較：上からの絵をぼかして背景に
run(['ffmpeg','-v','error','-y','-ss','2.0','-i',FU,'-frames:v','1',T+'bg.png'])
bg=Image.open(T+'bg.png').convert('RGB').resize((W,H)).filter(ImageFilter.GaussianBlur(14)); bg=ImageEnhance.Brightness(bg).enhance(0.6).convert('RGBA')
tl=Image.open(G+'tale.png'); bg.alpha_composite(tl); still(bg.convert('RGB'),3.5,FU,0)
seg(V+'d_announce.mp4',0,5.0)
seg(V+'f_faceoff_mg.mp4',0,9.0,[(G+'scorebar.png',0,9.0)])
seg(V+'e_gloves_mg.mp4',0,5.0,[(G+'scorebar.png',0,5.0)])
# 締め
run(['ffmpeg','-v','error','-y','-sseof','-0.1','-i',V+'e_gloves_mg.mp4','-frames:v','1',T+'last.png'])
e=ImageEnhance.Brightness(Image.open(T+'last.png').convert('RGB').resize((W,H))).enhance(0.35); d=ImageDraw.Draw(e)
ctext(d,'これは、',760,F(SB,80),'white',8); ctext(d,'昭和から来た男の',870,F(SB,96),'white',8)
ctext(d,'未来かもしれない',990,F(SB,96),(255,206,60),8); ctext(d,'権藤鉄男　毎日19時更新',1300,F(GB,50),'white',6)
still(e,4.0,V+'e_gloves_mg.mp4',1.0)
open(T+'l.txt','w').write(''.join(f"file '{s}'\n" for s in segs))
run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',T+'l.txt']+ENC+['-movflags','+faststart',OUT])
print('done')
