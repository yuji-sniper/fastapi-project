import hashlib
import time

from PIL import Image


def generate(image_path: str, calendar_path: str):
    print('Combining...')
    
    # 画像を開く
    image = Image.open(image_path)
    calendar = Image.open(calendar_path)

    # 結合した画像のサイズを計算
    width = max(image.width, calendar.width)
    height = image.height + calendar.height

    # 新しい画像を作成
    combined_img = Image.new("RGB", (width, height))

    # 画像を新しい画像にペースト
    combined_img.paste(image, (0, 0))
    combined_img.paste(calendar, (0, image.height))

    # 画像を保存
    data = str(time.time()).encode('utf-8')
    hashed_name = hashlib.md5(data).hexdigest()
    combined_img.save(f"image_calendars/{hashed_name}.png")
    
    print('combined successfly.')
