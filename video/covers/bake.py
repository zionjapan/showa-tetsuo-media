# 本編の動画の「最初の1秒」を「昭和から来た男 #番号」の大きい表紙にした版を作る（ボス 11/4）
# そのまま投稿すれば表紙になる。出力：video/tt/<日付>_tiktok<番号>_cover.mp4
import subprocess, sys, glob, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
R = '/home/claude/showa-tetsuo-media/'; W, H = 1080, 1920
F = '/usr/share/fonts/opentype/noto/NotoSansCJK-Black.ttc'; Y = (255, 210, 60)
TITLES = {15: '47年、雨の中で待っていた人', 16: '昭和の男、令和のジムで吹っ飛ぶ', 17: '昭和の男、ネカフェで力尽きる', 18: 'ハルさんの指に、あの日の指輪',
          19: '会長から届いた挑戦状', 20: '無敗の王者、鬼塚現る', 21: '王者の特訓が異次元', 22: '王座戦ゴング、王者の豪腕', 23: '昭和の男、初めての黒星',
          24: '負けた夜、ハルさんの一言', 25: '地獄の昭和特訓', 26: '修行の成果がすごすぎた', 27: 'YouTuber格闘家が煽ってきた', 28: '会見で配信者を一喝',
          29: '配信者との決着は一撃', 30: '元力士と大食い対決', 31: '体重差130kgの計量', 32: '200kgの巨体が倒れた', 33: '鬼塚ジムの無敗の天才',
          34: '天才がデータで丸裸に', 35: '残り10秒、昭和ゲンコツ'}
HOLD = 1.0  # 表紙を出す秒数（0.3秒だと表紙に拾われなかった）

def cover(n, src, out):
    # 動画の2秒目のコマを背景にして、下半分を黒帯で覆って文字を入れる
    tmp = out + '.bg.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '2.0', '-i', src, '-frames:v', '1', '-vf', f'scale={W}:{H}', tmp], check=True)
    im = ImageEnhance.Brightness(Image.open(tmp).convert('RGB')).enhance(0.85).convert('RGBA'); os.remove(tmp)
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle((0, 840, W, 1700), fill=(0, 0, 0, 255))
    im = Image.alpha_composite(im, ov).convert('RGB'); d = ImageDraw.Draw(im)
    def t(txt, y, sz, col):
        f = ImageFont.truetype(F, sz)
        while d.textlength(txt, font=f) > 1010: sz -= 4; f = ImageFont.truetype(F, sz)
        d.text(((W - d.textlength(txt, font=f)) / 2, y), txt, font=f, fill=col, stroke_width=12, stroke_fill='black')
    t('昭和から来た男', 900, 130, 'white'); t(f'#{n}', 1050, 260, Y); t(TITLES.get(n, ''), 1380, 80, 'white')  # 一覧の再生数の表示にかぶらないよう上寄せ
    im.save(out, quality=92)

def bake(n):
    src = glob.glob(R + f'video/tt/*_tiktok{n}.mp4')[0]
    jpg = R + f'video/covers/cover_{n}_series.jpg'; cover(n, src, jpg)
    out = src.replace('.mp4', '_cover.mp4')
    has_a = 'audio' in subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout
    fc = f'[0:v]scale={W}:{H},setsar=1,fps=30,format=yuv420p[c];[1:v]scale={W}:{H},setsar=1,fps=30,format=yuv420p[v];'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-t', str(HOLD), '-i', jpg, '-i', src]
    if has_a:
        cmd += ['-f', 'lavfi', '-t', str(HOLD), '-i', 'anullsrc=r=44100:cl=stereo']
        fc += '[c][2:a][v][1:a]concat=n=2:v=1:a=1[ov][oa]'; maps = ['-map', '[ov]', '-map', '[oa]', '-c:a', 'aac']
    else:
        fc += '[c][v]concat=n=2:v=1:a=0[ov]'; maps = ['-map', '[ov]']
    subprocess.run(cmd + ['-filter_complex', fc] + maps + ['-c:v', 'libx264', '-crf', '20', '-movflags', '+faststart', out], check=True)
    print('done', out)

for n in [int(a) for a in sys.argv[1:]]: bake(n)
