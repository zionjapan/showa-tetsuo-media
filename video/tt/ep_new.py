# 本編 #19〜#35（初黒星編〜挑戦者決定戦編）TikTok縦版
import sys
sys.path.insert(0, '/tmp/claude-0/-home-claude/9d5ec005-9cc8-52f5-9eca-474a40bf5cb4/scratchpad')
import tt2
from tt2 import *
P = '/home/claude/showa-tetsuo-media/posts/'
POSTER = 'poster'
EP = {
 19: ('会長から/届いた挑戦状', [
   ('ep19/19-1_kaichoshitsu.png', 0.5, ['呼び出しとは', '偉くなったな、龍二']),
   ('ep19/19-2_keiyakusho.png', 0.5, ['鉄檻の王者、鬼塚と戦え', '……上等だ']),
   ('ep19/19-3_kaerimichi.png', 0.5, ['相手は無敗の王者ですよ!?', '知らねぇな', '強ぇ奴ほど燃えるだろ'])]),
 20: ('無敗の王者、/鬼塚現る', [
   ('ep20/20-3_kaiken.png', 0.5, ['見上げてやるよ', '首は疲れるけどな']),
   ('ep20/20-1_onizuka.png', 0.5, ['王者・鬼塚', '24戦24勝、全部KO']),
   ('ep20/20-2_kawara_zero.png', 0.5, ['師匠、あいつはヤバい！', '耳くそのほうがヤバい'])]),
 21: ('王者の特訓が/異次元', [
   ('ep21/21-3_onizuka_tire.png', 0.5, ['300kgのタイヤを', 'ひとりで']),
   ('ep21/21-4_kawara_mitt.png', 0.5, ['昭和の特訓は', '気合いでやるんだよ']),
   ('ep21/vs_onizuka.png', POSTER, [])]),
 22: ('王座戦ゴング、/王者の豪腕', [
   ('ep22/22-2_faceoff.png', 0.5, ['ジジイ、立ってられるか', 'てめぇこそな']),
   ('ep22/22-1_nyujo_b.png', 0.5, ['入場曲は演歌', '47年遅れの挑戦者']),
   ('ep22/22-3_r1_miss.png', 0.5, ['1R', '当たれば終わる豪腕'])]),
 23: ('昭和の男、/初めての黒星', [
   ('ep23/23-1_r2_down.png', 0.5, ['2R', '王者が初めて膝をついた']),
   ('ep23/23-2_r3_boroboro.png', 0.5, ['3R', '倒れねぇ……', 'オレは倒れねぇ']),
   ('ep23/23-3_hantei.png', 0.5, ['判定', '勝者、鬼塚']),
   ('ep23/23-4_hikaeshitsu.png', 0.5, ['……', 'すまねぇ、ハルさん'])]),
 24: ('負けた夜、/ハルさんの一言', [
   ('ep24/24-1_sento_haru.png', 0.5, ['お疲れさま、鉄ちゃん', '……負けちまった', '負けた人の顔じゃないね']),
   ('ep24/24-2_yatai_ryuji.png', 0.5, ['強くなりたきゃ', 'もう一回、昭和に戻れ'])]),
 25: ('地獄の/昭和特訓', [
   ('ep25/25-1_tire_run.png', 0.5, ['夜明け前', 'タイヤ引き10km']),
   ('ep25/25-2_ishidan.png', 0.5, ['石段300段', 'ZEROを背負って'])]),
 26: ('修行の成果が/すごすぎた', [
   ('ep26/26-1_mirror.png', 0.5, ['……誰だ、こいつ', 'オレだ']),
   ('ep26/26-2_mitsu.png', 0.5, ['鬼塚に再挑戦したいなら', 'この3人に勝て'])]),
 27: ('YouTuber格闘家が/煽ってきた', [
   ('ep27/27-1_buzuto_haishin.png', 0.5, ['見てこれ', '鬼塚にボコられたジジイ']),
   ('ep27/27-2_kawara_ranyu.png', 0.5, ['本人来ちゃいました〜', '……失せろ'])]),
 28: ('会見で/配信者を一喝', [
   ('ep28/28-1_kaiken.png', 0.5, ['ジジイ、目線ちょうだい', '板っきれ越しじゃ', '目も合わせられねぇのか']),
   ('ep28/vs_buzuto.png', POSTER, [])]),
 29: ('配信者との決着は/一撃', [
   ('ep29/29-1_faceoff.png', 0.5, ['配信中で〜す！', '……黙ってろ']),
   ('ep29/29-2_ko.png', 0.5, ['一撃', '令和のバズより', '昭和のゲンコツ'])]),
 30: ('元力士と/大食い対決', [
   ('ep30/30-1_chanko.png', 0.5, ['おかわり！', '負けるか！']),
   ('ep30/30-2_teppo_b.png', 0.5, ['2人目の相手', '体重200kgの元力士'])]),
 31: ('体重差150kgの/計量', [
   ('ep31/31-1_keiryo.png', 0.5, ['体重差150kg', '見ろ、この力こぶ']),
   ('ep31/vs_yamaarashi.png', POSTER, [])]),
 32: ('200kgの巨体が/倒れた', [
   ('ep32/32-1_kawasu.png', 0.5, ['闘牛かよ', 'オーレ']),
   ('ep32/32-2_ketchaku.png', 0.5, ['200kgが', '倒れた']),
   ('ep32/32-3_te.png', 0.5, ['いい相撲だった', 'ちゃんこ、また食わせろよ'])]),
 33: ('鬼塚ジムの/無敗の天才', [
   ('ep33/33-1_himuro_shadow.png', 0.5, ['3人目', '鬼塚ジムの天才、氷室']),
   ('ep33/33-2_teisatsu.png', 0.5, ['……データ通りだ', '見てんじゃねぇよ'])]),
 34: ('天才がデータで/丸裸に', [
   ('ep34/34-1_kaiken_tablet.png', 0.5, ['勝率98.7%', 'あなたは昭和の遺物です', '……ナウくねぇな']),
   ('ep34/vs_himuro.png', POSTER, [])]),
 35: ('残り10秒、/昭和ゲンコツ', [
   ('ep35/35-1_hiza.png', 0.5, ['データ通り、もう立てない', '……昭和を', 'なめんな']),
   ('ep35/35-2_gyakuten_ko.png', 0.5, ['残り10秒', '昭和ゲンコツ！！']),
   ('ep35/35-3_kanaami_onizuka.png', 0.5, ['待ってろ、鬼塚', '次は、てめぇだ'])]),
}

def render(n):
    title, shots = EP[n]
    tt2.TITLES[n] = title.replace('/', '')
    _sp = tt2.split2
    tt2.split2 = lambda t: title.split('/') if '/' in title else _sp(t)
    globals()['split2'] = tt2.split2
    out = fname(n); p = pipe(OUT + out); SEC = 6
    fr = None
    for si, (f, ax, lines) in enumerate(shots):
        src = Image.open(P + f).convert('RGB')
        if ax == POSTER:
            img = src.resize((W, H)); b = img.tobytes()
            for _ in range(3 * FPS): p.stdin.write(b)
            fr = img; continue
        nfr = SEC * FPS
        for i in range(nfr):
            z = 1.0 + 0.10 * i / nfr
            cs = max(W / src.width, H / src.height) * z
            im = src.resize((int(src.width * cs), int(src.height * cs)), Image.BILINEAR)
            cx = int((im.width - W) * ax); cy = int((im.height - H) * 0.15)
            fr = im.crop((cx, cy, cx + W, cy + H)).convert('RGBA')
            if si == 0 and i < int(1.5 * FPS):
                big_title(fr, n); p.stdin.write(fr.convert('RGB').tobytes()); continue
            fr.alpha_composite(band(n)); fr = fr.convert('RGB')
            d = ImageDraw.Draw(fr)
            shown = lines[:1 + min(len(lines) - 1, int(i / (nfr / len(lines))))]
            subs(d, lines, shown)
            p.stdin.write(fr.tobytes())
    endcard(fr, p)
    p.stdin.close(); p.wait(); print('done', out)

if __name__ == '__main__':
    for a in sys.argv[1:]: render(int(a))
