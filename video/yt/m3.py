import sys; sys.path.insert(0,'.')
from manga import *
P='/home/claude/showa-tetsuo-media/posts/2026-10-23/'
shots=[
 {'img':P+'scout1.png','ax':0.3,'events':[
   {'t':0.5,'type':'bubble','lines':['肩ぶつけといて','詫びもねぇのかい'],'xy':(135,330),'tail':(470,390),'size':56}]},
 {'img':P+'scout2.png','ax':0.25,'lines_fx':0.0,'fx_center':(880,410),'events':[
   {'t':0.2,'type':'sfx','text':'バキィッ','xy':(730,215),'size':160,'angle':-14},
   {'t':0.8,'type':'bubble','kind':'shout','lines':['昭和','ゲンコツ'],'xy':(110,205),'tail':(380,390),'size':58},
   {'t':3.5,'type':'bubble','lines':['……軽ぃなぁ'],'xy':(130,860),'tail':(330,560),'size':54}]},
 {'img':P+'scout3.png','ax':0.3,'events':[
   {'t':0.4,'type':'bubble','lines':['なんだい','この紙切れ'],'xy':(160,240),'tail':(470,380),'size':56},
   {'t':2.0,'type':'bubble','lines':['鉄檻の','スカウトです！'],'xy':(930,260),'tail':(860,330),'size':54},
   {'t':4.0,'type':'bubble','lines':['オーディション','……？'],'xy':(470,760),'tail':(500,420),'size':56}]},
]
if sys.argv[1:]==['still']:
    for k,sh in enumerate(shots):
        src=Image.open(sh['img']).convert('RGB'); fr=frame_of(src,sh['ax'],1.03)
        fr=ImageEnhance.Contrast(fr.convert('RGB')).enhance(1.12).convert('RGBA')
        if sh.get('lines_fx') is not None: speedlines(fr,sh['fx_center'])
        for ev in sh['events']:
            if ev['type']=='bubble': bubble(fr,ev['lines'],ev['xy'],ev['tail'],ev.get('kind','round'),ev.get('size',60))
            else: sfx(fr,ev['text'],ev['xy'],ev.get('size',170),ev.get('angle',-12))
        fr.convert('RGB').resize((360,640)).save(f'mg{k}.png')
else:
    render(shots,'/home/claude/showa-tetsuo-media/video/yt/2026-10-23_yt3.mp4')
