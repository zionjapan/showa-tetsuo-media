# 自作テクノBGM（著作権フリー）：4つ打ち＋ハイハット＋ベース＋シンセ、15秒
import numpy as np, wave
SR=44100; BPM=128; beat=60/BPM; secs=15.05
tr=np.zeros(int(SR*secs))
def place(s,at):
    i=int(at*SR); e=min(len(tr),i+len(s)); 
    if i<len(tr): tr[i:e]+=s[:e-i]
def kick():
    t=np.arange(int(SR*0.35))/SR
    return np.sin(2*np.pi*(150*np.exp(-t*25)+45)*t)*np.exp(-t*9)*1.0
def hat(o=False):
    t=np.arange(int(SR*(0.12 if o else 0.04)))/SR
    n=np.random.uniform(-1,1,len(t)); n=np.diff(n,prepend=0)
    return n*np.exp(-t*(25 if o else 90))*0.18
def clap():
    t=np.arange(int(SR*0.2))/SR
    return np.random.uniform(-1,1,len(t))*np.exp(-t*20)*0.3
def saw(f,d,v):
    t=np.arange(int(SR*d))/SR
    w=sum(np.sin(2*np.pi*f*k*t)/k for k in range(1,12))
    return w*np.minimum(1,t*200)*np.exp(-t*6)*v
bass=[45,45,48,43]  # A1系の進行（Hz近似は下で計算）
def hz(n): return 440*2**(n/12)
nb=int(secs/beat)
for i in range(nb):
    at=i*beat; bar=i//4
    build = i>=8   # 2小節目からハット等が入る
    place(kick(),at)
    if build:
        place(hat(True),at+beat/2)
        place(hat(),at+beat/4); place(hat(),at+3*beat/4)
    if i%4 in (1,3) and i>=16: place(clap(),at)
    # ベース（裏拍）
    root=[-36,-36,-33,-38][bar%4]
    place(saw(hz(root),beat/2.2,0.35),at+beat/2)
    # シンセのリフ（4小節目以降）
    if i>=16:
        riff=[0,7,12,7][i%4]
        place(saw(hz(root+24+riff),beat/3,0.10),at)
        place(saw(hz(root+24+riff+3),beat/3,0.07),at+beat/2)
tr=np.tanh(tr*1.2); tr=tr/np.abs(tr).max()*0.85
f=int(SR*0.8); tr[-f:]*=np.linspace(1,0,f)
st=np.stack([tr,tr],1)
with wave.open('bgm_techno.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype(np.int16).tobytes())
