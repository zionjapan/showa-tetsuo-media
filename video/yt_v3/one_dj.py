import sys, runpy
sys.argv = ['render_v3.py', '-1']  # 既存リストは描かない
ns = runpy.run_path('video/igreel/v2/render_v3.py')
ns['run']((99, 'o_dj', 'n07_dj_beach.png', 0.5, '昭和の男、夕日のビーチでDJ', ['回すのは', 'レコードと', '昭和の魂だ']))
