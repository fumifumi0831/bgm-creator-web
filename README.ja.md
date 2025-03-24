# BGM Creator Web

YouTube作業BGM動画を簡単に作成するWebアプリケーション。ループ再生や周波数調整機能を備えています。

## 機能

- オーディオファイルのアップロードとループBGM動画への変換
- 音声の周波数（Hz）調整
- フェードイン・フェードアウト効果の追加
- 静止画またはGIFアニメーションの追加
- 静止画に動きエフェクトを追加
- カスタム長の動画作成（最大30分）
- カジュアルなクリエイター向けのシンプルで直感的なユーザーインターフェース

## 技術スタック

- フロントエンド: Next.js（TypeScript、Tailwind CSS）
- バックエンド: Python（FastAPI）
- 音声・動画処理: FFmpeg
- デプロイ: Dockerコンテナ

## プロジェクト構成

```
/
├── frontend/          # Next.jsフロントエンドアプリケーション
│   ├── components/    # 再利用可能なUIコンポーネント
│   ├── pages/         # アプリケーションページ
│   └── styles/        # グローバルスタイル
├── backend/           # Python FastAPIバックエンド
│   ├── app/           # メインアプリケーションコード
│   ├── processors/    # 音声・動画処理モジュール
│   └── assets/        # デフォルトリソース
└── docs/              # ドキュメント
```

## 始め方

### 必要条件

- Node.js 18以上
- Python 3.9以上
- FFmpeg
- Docker と Docker Compose（コンテナ化セットアップ用、オプション）

### 開発環境のセットアップ

#### オプション1: ローカル開発

1. **リポジトリのクローン**

```bash
git clone https://github.com/fumifumi0831/bgm-creator-web.git
cd bgm-creator-web
```

2. **フロントエンドのセットアップ**

```bash
cd frontend
npm install
npm run dev
```

3. **バックエンドのセットアップ**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. **バックエンドサーバーの実行**

```bash
uvicorn app.main:app --reload
```

5. **アプリケーションにアクセス**

ウェブブラウザで [http://localhost:3000](http://localhost:3000) を開きます。

#### オプション2: Dockerセットアップ

1. **リポジトリのクローン**

```bash
git clone https://github.com/fumifumi0831/bgm-creator-web.git
cd bgm-creator-web
```

2. **Docker Composeでビルドと実行**

```bash
docker-compose up -d
```

3. **アプリケーションにアクセス**

ウェブブラウザで [http://localhost:3000](http://localhost:3000) を開きます。

## 使い方

1. **BGM動画の作成**
   - オーディオファイル（MP3、WAVなど）をアップロード
   - 必要に応じて画像またはGIFをアップロード
   - 希望する動画の長さを設定
   - 追加オプション（周波数調整、フェード効果、モーション）を設定
   - 「BGM動画を作成」をクリック

2. **動画のダウンロード**
   - 処理が完了したら、動画をダウンロード
   - YouTubeにアップロードするか、必要に応じて使用

### 詳細設定

#### オーディオプロファイル

以下のプリセットプロファイルから選択できます：

- **デフォルト**: 標準的な音質バランス
- **作業用**: 低音を強調し、集中しやすい音質に調整
- **リラックス用**: よりリラックスできる周波数バランス
- **集中用**: 集中力を高める周波数設定

#### 周波数最適化

この機能を有効にすると、選択したプロファイルに基づいて以下の処理が行われます：

- 低周波数帯域の強調（より豊かな低音）
- 耳障りな周波数帯域の抑制
- 全体的な音量の最適化

#### 動きエフェクト

静止画に動きエフェクトを追加すると、以下のような効果が得られます：

- ゆっくりとしたズームイン/ズームアウト
- パン効果（画像がゆっくり動く）

## デプロイ

### サーバー要件

- 最小2 CPUコア（処理速度向上のため4コア以上推奨）
- 最小4GB RAM（8GB以上推奨）
- FFmpegがインストールされていること
- Docker と Docker Compose（コンテナ化デプロイ用）

### 本番環境へのデプロイ

1. **サーバー上でリポジトリをクローン**

```bash
git clone https://github.com/fumifumi0831/bgm-creator-web.git
cd bgm-creator-web
```

2. **環境変数の設定**

ルートディレクトリに `.env` ファイルを作成：

```
NEXT_PUBLIC_API_URL=https://あなたのAPIドメイン.com
```

3. **Docker Composeでデプロイ**

```bash
docker-compose up -d
```

4. **リバースプロキシの設定**

Nginx などのリバースプロキシを設定して、リクエストを適切なコンテナに転送します。

## ライセンス

MIT

## 謝辞

- 音声・動画処理のためのFFmpeg
- アプリケーションフレームワークのNext.jsとFastAPI
- このプロジェクトのすべての貢献者とユーザー
