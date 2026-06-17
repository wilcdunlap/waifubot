import os
import requests
from random import randint
from io import BytesIO
from PIL import Image
import facebook

def get_env_token():
    token = os.getenv("WAIFU_BOT_PAGE_TOKEN")
    if not token:
        raise ValueError("WAIFU_BOT_PAGE_TOKEN environment variable not set")
    return token

def get_waifu_image():
    waifu_number = randint(1, 100000)
    url = f"https://www.thiswaifudoesnotexist.net/example-{waifu_number}.jpg"
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save("waifu.jpg")
    return "waifu.jpg"

def get_caption():
    text_number = randint(1, 125000)
    url = f"https://www.thiswaifudoesnotexist.net/snippet-{text_number}.txt"
    response = requests.get(url)

    # Decode safely
    text = response.content.decode("utf-8", errors="replace")

    # Clean up ellipses and whitespace
    text = text.replace("...", "…")
    text = text.strip()

    # Remove null bytes or weird characters
    text = text.replace("\x00", "")

    # Ensure it's not empty
    if not text:
        text = "✨ A new waifu appears ✨"

    return text


def post_to_facebook(token, image_path, message):
    graph = facebook.GraphAPI(token)
    post = graph.put_photo(
        image=open(image_path, "rb"),
        message=str(message)
    )
    print("Posted:", post)

def main():
    token = get_env_token()
    image_path = get_waifu_image()
    caption = get_caption()
    print("Caption:", caption)
    post_to_facebook(token, image_path, caption)

if __name__ == "__main__":
    main()

