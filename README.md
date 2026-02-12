# 静止画MADメーカー (Simple Video Maker)

画像ファイルと音声ファイルを組み合わせて、MP4動画を簡単に作成できるWindows用GUIツールです。
「音声はあるけど動画編集ソフトを開くのは面倒」という時に便利です。

## ✨ 特徴

- シンプルな操作画面
- ドラッグ＆ドロップ感覚でファイル選択（参照ボタン）
- 処理はバックグラウンドで行われるためフリーズしない

## 📦 使い方 (配布版)

1. `SimpleVideoMaker.exe` を同じフォルダに `ffmpeg.exe` がある状態で起動します。
2. **音声ファイル** (mp3, wavなど) を選択します。
3. **画像ファイル** (jpg, pngなど) を選択します。
4. **「動画を作成する」** ボタンをクリック！
5. 音声ファイルと同じ場所に動画ファイル (`_video.mp4`) が生成されます。

## 🛠️ 開発者向け情報

### 必要要件
- Python 3.x
- ffmpeg (PATHまたは同階層)

### セットアップ
```bash
git clone https://github.com/naerecnegi-spec/nandemoeeai.git
cd nandemoeeai/静止画MADメーカー
```

### 実行
```bash
python video_maker.py
```

### ビルド (exe化)
PyInstallerを使用します。
```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name "SimpleVideoMaker" video_maker.py
```

## 📜 ライセンス
MIT License (またはお好きなライセンス)
