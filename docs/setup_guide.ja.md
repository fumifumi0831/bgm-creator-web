# BGM Creator Web セットアップガイド

このガイドでは、BGM Creator Webの詳細なセットアップ方法と、よくある問題の解決方法を説明します。

## 目次

1. [必要条件](#必要条件)
2. [ローカル開発環境のセットアップ](#ローカル開発環境のセットアップ)
3. [Docker環境のセットアップ](#Docker環境のセットアップ)
4. [よくある問題と解決方法](#よくある問題と解決方法)
5. [本番環境へのデプロイ](#本番環境へのデプロイ)

## 必要条件

### 最小要件

- **Node.js**: バージョン18.0.0以上
- **Python**: バージョン3.9以上
- **FFmpeg**: 最新安定版
- **ディスク容量**: 少なくとも2GBの空き容量
- **メモリ**: 4GB以上のRAM

### 推奨要件

- **Node.js**: バージョン20.0.0以上
- **Python**: バージョン3.11以上
- **FFmpeg**: 最新安定版（libmp3lame対応）
- **ディスク容量**: 10GB以上の空き容量（処理ファイル用）
- **メモリ**: 8GB以上のRAM
- **CPU**: 4コア以上（並列処理向け）

## ローカル開発環境のセットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/fumifumi0831/bgm-creator-web.git
cd bgm-creator-web
```

### 2. FFmpegのインストール

#### Ubuntu/Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

#### MacOS (Homebrew)

```bash
brew install ffmpeg
```

#### Windows

1. [FFmpeg公式サイト](https://ffmpeg.org/download.html)からWindows用バイナリをダウンロード
2. ダウンロードしたZIPファイルを展開
3. 展開したフォルダをC:\ffmpegなどに配置
4. システム環境変数のPATHにC:\ffmpeg\binを追加

### 3. バックエンドのセットアップ

```bash
cd backend

# 仮想環境の作成
python -m venv venv

# 仮想環境の有効化
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# requirements.txtに不足しているライブラリがある場合は追加でインストール
pip install scipy soundfile numpy
```

### 4. フロントエンドのセットアップ

```bash
cd frontend

# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev
```

### 5. アプリケーションの実行

```bash
# バックエンドの実行（backend ディレクトリ内で）
uvicorn app.main:app --reload

# フロントエンドの実行（別ターミナルで、frontend ディレクトリ内で）
npm run dev
```

ブラウザで http://localhost:3000 にアクセスして、アプリケーションが正常に動作していることを確認してください。

## Docker環境のセットアップ

### 1. Docker と Docker Composeのインストール

[Docker公式ドキュメント](https://docs.docker.com/get-docker/)に従ってDockerをインストールしてください。

### 2. アプリケーションのビルドと実行

```bash
# リポジトリのルートディレクトリで
docker-compose up -d
```

これにより、フロントエンドとバックエンドの両方のコンテナがビルドされ、起動します。

### 3. アプリケーションへのアクセス

ブラウザで http://localhost:3000 にアクセスして、アプリケーションが正常に動作していることを確認してください。

## よくある問題と解決方法

### バックエンドの依存関係エラー

```
ModuleNotFoundError: No module named 'scipy'
```

**解決方法**: 不足しているライブラリをインストールします。

```bash
pip install scipy
```

同様に、`soundfile`や`numpy`などのエラーが出た場合も、対応するライブラリをインストールしてください。

### FFmpegが見つからないエラー

```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

**解決方法**: FFmpegがインストールされており、PATHに含まれていることを確認してください。

```bash
# FFmpegがインストールされているか確認
ffmpeg -version
```

### 一時ファイルのパーミッションエラー

```
PermissionError: [Errno 13] Permission denied: './temp/uploads'
```

**解決方法**: 一時ディレクトリの権限を確認し、必要に応じて変更します。

```bash
# Linux/macOS
chmod -R 755 ./temp

# または新しく作り直す
rm -rf ./temp
mkdir -p ./temp/uploads ./temp/outputs ./temp/jobs
chmod -R 755 ./temp
```

## 本番環境へのデプロイ

### Vercel + サーバーレス関数でのデプロイ

1. フロントエンドはVercelにデプロイできます
2. バックエンドは別途サーバーが必要です（FFmpegの実行環境が必要）

### VPSまたはクラウドサーバーでのデプロイ

1. **サーバーの準備**
   - 最小2 CPUコア、4GB RAM、20GB ディスク容量の環境を用意
   - Ubuntu 20.04 LTS以上を推奨

2. **Dockerを使ったデプロイ**
   ```bash
   git clone https://github.com/fumifumi0831/bgm-creator-web.git
   cd bgm-creator-web
   
   # 環境変数の設定
   cp .env.example .env
   # .envファイルを編集して本番用の設定に変更
   
   # Dockerでビルドと起動
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Nginxなどのリバースプロキシの設定**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
       
       location /api {
           proxy_pass http://localhost:8000;
           proxy_http_version 1.1;
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

4. **SSLの設定（Let's Encryptなど）**
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

これでBGM Creator Webは本番環境で動作するようになります。
