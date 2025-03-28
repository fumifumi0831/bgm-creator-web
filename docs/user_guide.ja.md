# BGM Creator Web ユーザーガイド

このガイドでは、BGM Creator Webの使い方と各機能について詳しく説明します。

## 目次

1. [はじめに](#はじめに)
2. [基本的な使い方](#基本的な使い方)
3. [詳細設定](#詳細設定)
4. [よくある質問](#よくある質問)
5. [トラブルシューティング](#トラブルシューティング)

## はじめに

BGM Creator Webは、YouTube用の作業BGM動画を簡単に作成するためのツールです。オーディオファイルをアップロードし、必要に応じて画像を追加し、設定を調整するだけで、高品質なBGM動画を作成できます。

### 主な機能

- オーディオファイルのループ再生（指定した長さまで自動延長）
- 音声の周波数調整（高音・低音のバランス調整）
- フェードイン・フェードアウト効果
- 静止画像またはGIFアニメーションとの統合
- 静止画像に動きエフェクトを追加
- 音質最適化プロファイル

## 基本的な使い方

### ステップ1: ファイルのアップロード

1. ホームページにアクセスします。
2. 「オーディオファイル」欄で、使用したいBGM音源（MP3、WAV形式など）を選択します。
3. 必要に応じて「画像ファイル」欄で、動画に表示する画像（JPG、PNG、GIF形式など）を選択します。
   - 画像をアップロードしない場合は、デフォルトの背景が使用されます。

### ステップ2: 基本設定

1. 「動画の長さ」スライダーを使って、作成する動画の長さを設定します（1〜30分）。
2. 「サウンドプロファイル」ドロップダウンから、音質の最適化プロファイルを選択します：
   - **デフォルト**: 標準的な音質バランス
   - **作業用**: 低音を強調し、集中しやすい音質に調整
   - **リラックス用**: よりリラックスできる周波数バランス
   - **集中用**: 集中力を高める周波数設定

### ステップ3: 動画の作成とダウンロード

1. 「BGM動画を作成」ボタンをクリックします。
2. 処理状況がプログレスバーに表示されます。処理時間は動画の長さによって異なります。
3. 処理が完了すると、「BGM動画をダウンロード」ボタンが表示されます。
4. ボタンをクリックして、作成された動画をダウンロードします。

## 詳細設定

### フェード効果

- **フェードイン**: 曲の始まりをフェードインする時間（秒）を設定します。0〜10秒の範囲で設定可能です。
- **フェードアウト**: 曲の終わりをフェードアウトする時間（秒）を設定します。0〜10秒の範囲で設定可能です。

これらの設定により、動画の始まりと終わりが滑らかになります。特に長時間のループ再生では、突然の音量変化を防ぐために有効です。

### 動きエフェクト

「静止画に動きエフェクトを追加する」チェックボックスをオンにすると、静止画像にゆっくりとしたズームやパン効果が追加されます。これにより、単調な静止画像でも視覚的な変化が生まれ、視聴者の注意を引きつけます。

GIF画像をアップロードした場合、このオプションは無視され、GIFのアニメーションがそのまま使用されます。

### 音声最適化

「音声を最適化する」チェックボックスをオンにすると、選択したプロファイルに基づいて以下の処理が行われます：

- 低周波数帯域の強調または抑制
- 人間の耳に不快に感じられる特定の周波数帯域の調整
- 全体的な音量の正規化

これにより、長時間の視聴でも疲れにくい音質になります。

## よくある質問

### Q: どんな種類の音楽ファイルが使えますか？

A: MP3、WAV、OGG、AACなど、一般的な音声フォーマットをサポートしています。最良の結果を得るには、MP3形式（192kbps以上）またはWAV形式をお勧めします。

### Q: 作成できる動画の最大長は？

A: 30分までの動画を作成できます。無料プランでは10分までに制限されています。

### Q: アップロードした音楽の著作権について注意すべきことは？

A: アップロードする音楽の著作権は必ずご確認ください。著作権で保護された音楽を使用する場合は、適切な権利をお持ちであることを確認してください。商用利用の場合は特に注意が必要です。

### Q: 画像はどのようなサイズがベストですか？

A: 16:9のアスペクト比（例：1920x1080ピクセル）が最適です。他のサイズでも動作しますが、黒い帯が表示される場合があります。

### Q: 作成した動画をYouTubeにアップロードする方法は？

A: 作成した動画をダウンロードした後、通常のYouTubeアップロードプロセスに従ってください。タイトル、説明、タグなどを設定し、アップロードします。

## トラブルシューティング

### 動画の処理が完了しない

- **原因**: ファイルサイズが大きすぎる、またはサーバーが混雑している可能性があります。
- **解決策**: より小さいファイルを使用するか、時間をおいて再試行してください。

### 音質が期待どおりでない

- **原因**: 入力ファイルの品質が低い、または不適切なプロファイルを選択している可能性があります。
- **解決策**: より高品質の音源を使用するか、別のプロファイルを試してください。

### 動画のダウンロードができない

- **原因**: ブラウザの設定、ネットワーク問題、またはファイルの破損の可能性があります。
- **解決策**: 別のブラウザを試す、またはプロセスをやり直してください。

### フェード効果が適用されていない

- **原因**: 音声ファイルが短すぎる場合、フェード効果が目立たないことがあります。
- **解決策**: より長いフェード時間を設定するか、より長い音源を使用してください。

---

問題が解決しない場合は、サポートにお問い合わせください。より良いサービスを提供するために、フィードバックもお待ちしています。
