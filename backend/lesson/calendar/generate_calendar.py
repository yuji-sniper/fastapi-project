import calendar
import os

from PIL import Image, ImageDraw, ImageFont


def generate(year: int, month: int) -> str:
    print('Generating calendar...')
    
    path = f"calendars/calendar_{year}_{month}.png"
    if os.path.exists(path):
        print('Calendar already exists.')
        return path
    
    # 画像のサイズ
    width, height = 512, 288

    # カレンダーの日付データを取得
    cal = calendar.monthcalendar(year, month)

    # 新しい画像を作成
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  

    # タイトルを描画
    title = f"{calendar.month_name[month]} {year}"
    title_font = ImageFont.truetype(font_path, 40)
    _, _, title_w, _ = draw.textbbox((0, 0), title, font=title_font)
    draw.text(((width - title_w) / 2, 0), title, fill="black", font=title_font)

    # 曜日の名前を描画
    days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    day_font = ImageFont.truetype(font_path, 25)
    day_spacing = width / 7
    for i, day in enumerate(days):
        draw.text((i * day_spacing + 10, 50), day, fill="black", font=day_font)

    # 日付を描画
    date_font = ImageFont.truetype(font_path, 18)
    for i, week in enumerate(cal):
        for j, day in enumerate(week):
            if day != 0:
                # print(100 + i * 40)
                draw.text((j * day_spacing + 25, 80 + i * 40), str(day), fill="black", font=date_font)

    # 画像を保存
    img.save(path)
    print('Carendar saved successfly.')
    
    return path
