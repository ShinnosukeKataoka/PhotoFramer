# PhotoFramer

PhotoFramer は、写真に余白と額縁風のフレームを付与し、Exif 情報 (メーカー名・機種・ISO・シャッタースピード・絞り値) をキャプションとして描画する Python スクリプトです。`input/` ディレクトリ内の JPEG/PNG をまとめて処理し、`output/` ディレクトリに 7,000px 四方の正方形キャンバスとして書き出します。

## 主な機能
- JPEG / PNG の一括処理 (Exif キャプションは JPEG のみ)
- 白・黒の額縁風フレームと余白の追加
- 任意フォント (Noto Sans CJK など) によるキャプション描画
- Exif 情報が取得できない場合はそのまま出力

## 必要要件
- Python 3.10 以上を想定
- 依存ライブラリ: [Pillow](https://python-pillow.org/) / [ExifRead](https://pypi.org/project/ExifRead/)
- 日本語フォントファイル (例: `NotoSansCJKjp-Regular.otf`) — `autoflame.py` の `font_path` を編集することで任意のフォントを利用可能

### 仮想環境の例
```bash
python -m venv venv
source venv/bin/activate  # Windows の場合は venv\Scripts\activate
pip install Pillow ExifRead
```

## 使い方
1. `input/` に処理したい JPEG / PNG ファイルを配置します。
2. キャプションに使いたいフォントファイルをリポジトリ直下に置くか、`autoflame.py` 内の `font_path` をフォントファイルのパスに変更します。
3. 以下のコマンドでスクリプトを実行します。
   ```bash
   python autoflame.py
   ```
4. 処理結果が `output/` に `framed_<元ファイル名>` というファイル名で保存されます。Exif を保持できた JPEG はオリジナルの Exif も再付与されます。

## デモ
リポジトリにはサンプル画像 `input/sample.jpg` が含まれています。上記コマンドを実行すると、`output/framed_sample.jpg` が生成され、白いマットと黒枠を持つ正方形画像に変換されます。Exif 情報 (例: `Canon EOS R6 / ISO 100 / 1/200s / F2.8`) が画像下部にセンタリングされて描画されます。

## カスタマイズのヒント
- 出力サイズや余白の幅は `autoflame.py` 冒頭の定数 (`OUTPUT_SIZE` や `white_border_thin` など) を変更することで調整できます。
- JPEG 以外にもキャプションを付与したい場合は `process_image` 関数内の `is_jpeg` 判定を調整してください。

## ライセンスと免責事項
- このコードの実行により生じた不利益について一切の責任を負いません。
- コードの一部またはすべては、出典を明記することで再利用可能です。
