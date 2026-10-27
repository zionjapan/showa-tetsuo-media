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

## 使い方
- 生成した5秒動画は、各話の動画の中に静止画と組み合わせて入れる（Claudeが編集）
- 課金後：残高を確認 → T1を作る → ボス確認 → 残り13本
