from PIL import Image, ImageDraw, ImageFont, ExifTags
import exifread
import os

INPUT_DIR = "input"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

OUTPUT_SIZE = 7000
white_border_thin = 20
black_border = 60
white_background = 50

# 任意の日本語ゴシック体フォントのパスを指定
font_path = "./NotoSansCJKjp-Regular.otf"
font_size = 130

# EXIF タグ名変換辞書
EXIF_TAGS = {v: k for k, v in ExifTags.TAGS.items()}

def get_exif_info(image_path):
    try:
        with open(image_path, "rb") as f:
            tags = exifread.process_file(f, stop_tag="UNDEF", details=False)

        make = str(tags.get("Image Make", "Unknown")).strip()
        model = str(tags.get("Image Model", "Unknown")).strip()
        iso = str(tags.get("EXIF ISOSpeedRatings", "Unknown"))
        exposure = str(tags.get("EXIF ExposureTime", "Unknown"))
        fnumber = str(tags.get("EXIF FNumber", "Unknown")).replace("/", ".")

        return f"{make} {model} / ISO {iso} / {exposure}s / F{fnumber}"
    except Exception as e:
        print(f"EXIF読み込みエラー: {e}")
        return None

def process_image(image_path):
    img = Image.open(image_path)
    exif_data = img.info.get("exif", None)
    img = Image.open(image_path).convert("RGB")
    is_jpeg = image_path.lower().endswith((".jpg", ".jpeg"))

    # 最大画像サイズ（枠とテキストを除く）
    text_space = 190 if is_jpeg else 0
    max_photo_size = OUTPUT_SIZE - 2 * (white_border_thin + black_border + white_background) - text_space
    img.thumbnail((max_photo_size, max_photo_size), Image.LANCZOS)

    # 写真 → 白細枠
    img_white = Image.new("RGB", (img.width + 2 * white_border_thin, img.height + 2 * white_border_thin), "white")
    img_white.paste(img, (white_border_thin, white_border_thin))

    # → 黒枠
    img_black = Image.new("RGB", (img_white.width + 2 * black_border, img_white.height + 2 * black_border), "black")
    img_black.paste(img_white, (black_border, black_border))

    # テキスト付き画像に変換
    total_height = img_black.height + text_space
    canvas_img = Image.new("RGB", (img_black.width, total_height), "white")
    canvas_img.paste(img_black, (0, 0))

    if is_jpeg:
        text = get_exif_info(image_path)
        if text:
            draw = ImageDraw.Draw(canvas_img)
            try:
                font = ImageFont.truetype(font_path, font_size)
            except OSError:
                print("フォントが見つかりません。標準フォントで描画します。")
                font = ImageFont.load_default(font_size)

            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (canvas_img.width - text_width) // 2
            y = img_black.height + (text_space - text_height) // 2
            draw.text((x, y), text, fill="black", font=font)

    # 背景に最終配置
    final = Image.new("RGB", (OUTPUT_SIZE, OUTPUT_SIZE), "white")
    x = (OUTPUT_SIZE - canvas_img.width) // 2
    y = (OUTPUT_SIZE - canvas_img.height) // 2
    final.paste(canvas_img, (x, y))

    return final, exif_data

def batch_process():
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            img_path = os.path.join(INPUT_DIR, filename)
            result, exif_data = process_image(img_path)
            if exif_data:
                result.save(os.path.join(OUTPUT_DIR, f"framed_{filename}"), exif=exif_data)
            else:
                result.save(os.path.join(OUTPUT_DIR, f"framed_{filename}"))
            print(f"Processed: {filename}")

if __name__ == "__main__":
    batch_process()
    print("All images processed.")
    print(f"Processed images saved in: {OUTPUT_DIR}")
