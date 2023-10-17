import hashlib
import openai
import os

import requests
from dotenv import load_dotenv


def generate(prompt: str) -> str:
    # 環境変数の設定
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    # 画像生成
    print('Genarating image...')

    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']

    # 画像をダウンロード
    response = requests.get(image_url, stream=True)
    response.raise_for_status()

    # 画像のバイナリデータをハッシュ値でファイル名を生成
    content = response.content
    hash_value = hashlib.md5(content).hexdigest()  # 32文字のユニークなハッシュ値を生成
    path = f"images/{hash_value}.png"

    # 画像をファイルとして保存
    with open(path, "wb") as file:
        file.write(content)

    print('Image saved successfly.')

    return path
