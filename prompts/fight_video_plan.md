# 試合動画プラン（Seedance 2.0 image2video）

設定：9:16 / 720p / 5秒 / 音あり（観客の歓声）/ mode normal
料金：5秒＝400クレジット（10秒＝800）。全14本＝5,600、作り直し込み約8,000
共通の末尾（全プロンプトに付ける）：
Realistic live sports broadcast footage of a professional MMA event, handheld camera behind the cage fence, natural motion, consistent faces and bodies, no extra limbs, no blood, no text overlay.

TikTokルール：各話の最初の画面は殴る絵にしない（にらみ合い・入場から始める）

## まず試す1本（テスト：400）
- T1: 29-1_faceoff → 29-2_ko（startFrame=29-1, endFrame=29-2）
  The referee steps back and signals fight. The silver-haired fighter rushes forward throwing wild punches; the punch-perm fighter calmly slips one punch and lands a single straight right. The silver-haired fighter falls backward stiff onto the canvas, the referee dives in waving his arms, the crowd erupts.

## #22 鬼塚戦 入場・1R
- 22A: start=22-1_nyujo_a｜He walks slowly down the aisle through thick smoke and lasers, robe swaying, chin up, fans reaching out with phones, camera tracking backward in front of him.
- 22B: start=22-2_faceoff｜Tense staredown. The referee gives final words, then pulls his arms apart and steps back. The giant cracks his neck; the skinny fighter does not blink.
- 22C: start=22-3_r1_miss｜The giant throws a huge right hook; the skinny fighter ducks under it at the last instant, the glove whooshing over his hair, and he spins away along the fence.

## #23 鬼塚戦 2R・3R・判定
- 23A: start=23-1_r2_down｜The giant drops to one knee in shock, the referee pushes the skinny fighter back and starts counting with his fingers, the crowd jumps up screaming.
- 23B: start=23-2_r3_boroboro｜Exhausted, swaying, breathing hard through his mouth, he raises his shaky guard again and takes one step forward, refusing to fall. Slow push-in on his face.
- 23C: start=23-3_hantei｜The referee raises the giant's arm. The skinny fighter keeps his head down, biting his lip, then slowly looks up at the giant. Camera flashes.

## #29 バズ斗戦
- 29A: T1（テストの1本をそのまま使う）
- 29B: start=29-2_ko｜The referee waves it off over the fallen fighter. The punch-perm fighter slowly lowers his fist and turns away calmly as the crowd goes wild.

## #32 山嵐戦
- 32A: start=32-1_kawasu｜The 200kg giant charges like a freight train; the lean fighter sidesteps like a matador and the giant crashes into the cage fence, which shakes violently.
- 32B: start=32-2_ketchaku｜The giant crashes face-first onto the canvas, the floor shakes, sweat sprays; the lean fighter raises his fist and roars, the referee waves it off.
- 32C: start=32-3_te｜He pulls the smiling giant up by the hand, they embrace and pat each other's backs, the crowd applauds.

## #35 氷室戦
- 35A: start=35-1_hiza｜Dazed on one knee, he shakes his head, the referee counts; at eight he pushes himself up and raises his guard, eyes burning.
- 35B: start=35-2_gyakuten_ko｜Slow motion: his overhand right lands, the young fighter falls backward stiff, the referee dives in, outside the cage the champion slowly rises from his seat.
- 35C: start=35-3_kanaami_onizuka｜The champion and the punch-perm fighter stand face to face in silence; the fighter presses his fist against the champion's chest; flashes and roaring crowd, slow orbit around them.

## 追加：ブレイキングダウン風の中継パッケージ（ボス要望 2026-10-27）
各試合に「入場 → ゴング → ドローン俯瞰」を入れる。入場の名前テロップと「鉄檻」ロゴはClaudeが後で重ねる（AIに文字は書かせない）
- E（入場）: start=各試合のにらみ合い or 入場の絵｜He walks out of a dark tunnel into a blinding white spotlight, thick smoke, red strobe lights, the camera walking backward in front of him, the crowd screaming, BreakingDown-style entrance.
- G（ゴング）: start=にらみ合いの絵｜Close-up of a referee's hand chopping down between two fighters, a bell rings, both fighters explode toward each other, quick handheld shot through the cage.
- D（ドローン）: start=試合中の絵｜Top-down drone shot directly above the octagon cage, slowly descending and rotating, two tiny fighters circling each other on the canvas, packed arena around them, spotlights sweeping.
- 追加本数：鬼塚戦 G・D（入場は22Aあり）／バズ斗・山嵐・氷室戦 E・G・D ＝ 11本 ＝ 4,400クレジット

## 合計
- 基本14本＋中継11本＝25本＝10,000クレジット、作り直し込みで約15,000
- 予算が足りなければ、鬼塚戦（#22・#23）と氷室戦（#35）を優先

## 使い方
- 生成した5秒動画は、各話の動画の中に静止画と組み合わせて入れる（Claudeが編集）
- 課金後：残高を確認 → T1を作る → ボス確認 → 残り13本

## 準備状況（2026-10-27）
- プロンプト：全25本ぶん完成（このファイル）
- 開始画像：元の2:3の絵をそのまま使う（aspectRatio=adaptive）。9:16に切った版は video/seedance_in/ にある（予備）
- 設定確認済み：Seedance 2.0 image2video は startFrame/endFrame 対応、4〜15秒、9:16可、5秒=400・10秒=800
- 通信：ボスが許可済み（2026-10-27）。開始画像14枚はOpenArtにアップロード済み → prompts/openart_refs.json

## 目標の形（ボス共有 2026-10-27：UFC Reimagined「Seamus O'Grady vs King Charles II」2分40秒）
- 入場：国旗ガウン＋大きな異名テロップ（THE GLORIOUS）→ 名前テロップ
- 試合：中継の引きアングル中心、画面下に中継風スコアバー（名前・R1・タイマー）
- 実況の一言テロップ（白・黄色）：the stare. / IT'S TIME. / wait for it... / BOOM / UH OH. / SEAMUS IS HURT / TAKEDOWN / LONG LIVE THE KING
- 最後：勝者テロップ「WINS BY SUBMISSION」＋「REMATCH? COMMENT BELOW」でコメントを集める
- 鉄男版：日本語の一言（にらみ合い。／ゴング。／効いてない。／昭和ゲンコツ!!／ジジイ、立つ。など）、スコアバー「権藤 R1 鬼塚」、最後「再戦見たい？コメントで」
- 2分40秒＝5秒×約30本＝約12,000クレジット/1試合（720p）。まず鬼塚戦1本をこの長さで作り、YouTube横長＋TikTok縦で出す案

## UFC Reimagined のショート（ボス共有 2026-10-27 2本目）
- 98万・53万再生。全部「AI」表示つき
- 型1 会見の悪口合戦：1単語ずつ大きく出るカラオケ字幕（ピンク・緑の太字）、上に固定の釣り文「THE PRESS CONFERENCE GOT CRAZY😂」
- 型2 ベルト泥棒・乱闘未遂：「dana holding him back like a dad」など、下に一言ツッコミ
- 型3 カメラに向かってしゃべる：キャラが口を動かして挑発、下に字幕
- 冒頭は「HOW IT STARTED👇」で試合へつなぐ
- 注意：実在の選手・社長（Strickland、Dana White）が出てくるが、鉄男では実在の人は使わない
- 鉄男版：会見で鉄男が鬼塚・バズ斗を煽る（「ヒヨッコが」「ナウくねぇな」）を1単語ずつ字幕、上に「会見が荒れた😂」

## ダンス動画（ボス共有 2026-10-27：Phil Jean「トクトクソング＆ダンス」16秒、AI表示つき）
- 型：キャラが部屋で全身を映して流行りのダンスを踊るだけ。1カット、カメラ固定、最後に顔のアップ
- 鉄男版：昭和の部屋（ちゃぶ台・黒電話・ブラウン管）で花柄シャツ＋フレアパンツの鉄男が真顔で踊る
- 作り方：ChatGPTで全身の開始画像（無料）→ Seedance 2.0 image2video 9:16 720p 15秒＝1,200クレジット。曲はボスがTikTokで流行りの音源を付ける
- 動きの指示：energetic modern TikTok dance, footwork shuffle, body rolls, arm waves, deadpan serious face the whole time, ends by walking up to the camera and staring into it

## 金曜（10/30）課金予定・その日の順番（ボス 2026-10-28）
1. ダンス3本（Seedance 2.0 Mini 10秒×3 ≒1,200）：昭和の部屋／銭湯の脱衣所／河原
2. 反応を見て、試合のテスト（バズ斗戦 にらみ合い→KO 5秒 400）
参考：Peter Griffin（@theycallmepeety）10/15開始で5.7万フォロワー。1人・同じ服・部屋で流行りの曲に合わせて踊るだけ・文字なし・毎日

## 決定（2026-10-30 ボス「めちゃいいじゃん、たまに出したい」）
- 型：煽り＋ポスター（タダ）→ にらみ合い 720p 10秒（800）→ KO 1080p 10秒（BD実映像をお手本、2,000）→ KOテロップ＋結果（タダ）＝約28秒・約2,800クレジット
- 作成済み：video/fight/buzuto_fight_30s.mp4（scratchpad/buzuto_fight.py で組み立て）
- 出す頻度：週1本、週末。残り：山嵐戦・氷室戦・鬼塚戦（再戦含む）
- バズ斗戦は作り直さない（ボス 2026-10-30「もったいない」）。編集版（光＋揺れ＋スローリプレイ）で完成
- 次の試合から：お手本は「一発で崩れ落ちる強烈なKO」を選び、指示に「顔がゆがむほどの強打、汗が飛び散る、頭が跳ね上がる」を入れる

## マウスピースのルール（ボス指摘 2026-10-30）
- にらみ合い・試合中・試合直後は必ずマウスピースあり（入場・計量・会見はなし）
- 鉄男は出っ歯なので、AIはマウスピースの上に歯を描いてしまう。黒い板＋歯の二重になって不自然
- 対策1：先にChatGPTで「マウスピースを噛んだ顔」の画像を作り、それを動画の参考画像（または開始画像）にする
- 対策2：口を開けて叫ばせない。lips closed over the mouthguard, breathing through the nose
- 対策3：赤いマウスピース（日の丸カラー）で出っ歯ごと覆う形にする
