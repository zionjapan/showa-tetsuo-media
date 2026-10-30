# 昭和っぽいBGMをプログラムで作る（著作権フリー・自作）
import numpy as np, wave, os
SR = 44100
OUT = os.path.dirname(os.path.abspath(__file__)) + '/'

def note(n):  # n: A4=0 からの半音
    return 440.0 * 2 ** (n / 12)

def pluck(f, dur, vol=0.5):  # 三味線・ギター風（Karplus-Strong）
    N = int(SR / f); buf = np.random.uniform(-1, 1, N); out = np.zeros(int(SR * dur))
    for i in range(len(out)):
        out[i] = buf[i % N]; buf[i % N] = 0.996 * 0.5 * (buf[i % N] + buf[(i + 1) % N])
    return out * vol

def tone(f, dur, vol=0.3, kind='sq'):
    t = np.arange(int(SR * dur)) / SR
    w = np.sign(np.sin(2 * np.pi * f * t)) * 0.5 + np.sin(2 * np.pi * f * t) * 0.5 if kind == 'sq' else np.sin(2 * np.pi * f * t)
    env = np.minimum(1, t * 40) * np.exp(-t * 3)
    return w * env * vol

def kick(dur=0.25):
    t = np.arange(int(SR * dur)) / SR
    return np.sin(2 * np.pi * (120 * np.exp(-t * 18) + 40) * t) * np.exp(-t * 14) * 0.9

def snare(dur=0.18):
    t = np.arange(int(SR * dur)) / SR
    return np.random.uniform(-1, 1, len(t)) * np.exp(-t * 22) * 0.35

def place(track, s, at):
    i = int(at * SR); e = min(len(track), i + len(s)); track[i:e] += s[:e - i]

def song(name, bpm, mel, bass, swing=False, lead='pluck', secs=8.0):
    tr = np.zeros(int(SR * secs)); beat = 60 / bpm
    # メロディ：(拍位置, 半音, 長さ拍)
    loop = max(b + l for b, _, l in mel)
    k = 0
    while k * loop * beat < secs:
        for b, n, l in mel:
            at = (k * loop + b) * beat
            if at >= secs: continue
            s = pluck(note(n), l * beat + 0.3, 0.45) if lead == 'pluck' else tone(note(n), l * beat + 0.2, 0.22)
            place(tr, s, at)
        for b, n, l in bass:
            at = (k * loop + b) * beat
            if at < secs: place(tr, tone(note(n - 24), l * beat, 0.35, 'sin'), at)
        k += 1
    nb = int(secs / beat)
    for i in range(nb):
        at = i * beat + (0.04 if swing and i % 2 else 0)
        place(tr, kick() if i % 2 == 0 else snare(), at)
    tr = tr / max(1e-9, np.abs(tr).max()) * 0.8
    fade = int(SR * 0.6); tr[-fade:] *= np.linspace(1, 0, fade)
    st = np.stack([tr, tr], 1)
    with wave.open(OUT + f'bgm_{name}.wav', 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())
    print('bgm', name)

# 演歌風（ヨナ抜き短音階：ラ シ ド ミ ファ）
A, B, C, E, F = 0, 2, 3, 7, 8
song('enka', 84, [(0, E, 1), (1, F, 0.5), (1.5, E, 0.5), (2, C, 1), (3, B, 1), (4, A, 1.5), (5.5, B, 0.5), (6, C, 1), (7, E, 1)],
     [(0, A, 2), (2, F - 12, 2), (4, E - 12, 2), (6, A, 2)])
# コミカル（昭和のバラエティ風・長調ヨナ抜き）
c, d, e, g, a = 3, 5, 7, 10, 12
song('comic', 132, [(0, g, 0.5), (0.5, e, 0.5), (1, g, 0.5), (1.5, a, 0.5), (2, g, 1), (3, e, 0.5), (3.5, d, 0.5), (4, c, 0.5), (4.5, d, 0.5), (5, e, 1), (6, g, 1), (7, c + 12, 1)],
     [(0, c, 1), (1, g - 12, 1), (2, c, 1), (3, g - 12, 1), (4, a - 12, 1), (5, e - 12, 1), (6, g - 12, 1), (7, c, 1)], swing=True, lead='sq')
# 熱血（特訓・格闘）
song('nekketsu', 150, [(0, E, 0.5), (0.5, E, 0.5), (1, F, 0.5), (1.5, E, 0.5), (2, C, 1), (3, E, 1), (4, A + 12, 1.5), (5.5, F, 0.5), (6, E, 2)],
     [(0, A, 0.5), (0.5, A, 0.5), (1, A, 0.5), (1.5, A, 0.5), (2, F - 12, 1), (3, F - 12, 1), (4, E - 12, 1), (5, E - 12, 1), (6, A, 2)], lead='sq')
