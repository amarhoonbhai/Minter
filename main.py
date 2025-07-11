# main.py

import os, json, time, schedule
from PIL import Image
from io import BytesIO
import requests

from bot_config import *
from sticker_manager import add_sticker_to_set, create_sticker_set
from gift_fetcher import fetch_all_gifts, fetch_gift_info, get_gift_image
from poster import client, post_sticker_with_caption, post_gift_details

STICKER_DIR = 'stickers'
CACHE_FILE = 'seen_gifts.json'

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'r') as f:
        seen = set(json.load(f))
else:
    seen = set()

os.makedirs(STICKER_DIR, exist_ok=True)

async def process_new_gifts():
    print("🔍 Checking for new gifts...")
    all_gifts = fetch_all_gifts()

    for gift_id, gift_name in all_gifts.items():
        if gift_id in seen:
            continue

        print(f"🎁 New gift: {gift_name} ({gift_id})")

        image_url = get_gift_image(gift_id)
        img_data = requests.get(image_url).content
        img = Image.open(BytesIO(img_data))
        img.thumbnail((512, 512))
        image_path = os.path.join(STICKER_DIR, f"{gift_id}.webp")
        img.save(image_path, 'WEBP')

        if not os.path.exists(f"{STICKER_DIR}/.pack_created"):
            create_sticker_set(gift_id, '🎁', image_path)
            open(f"{STICKER_DIR}/.pack_created", 'w').close()
        else:
            add_sticker_to_set(image_path, '🎁')

        gift_info = fetch_gift_info(gift_name)
        await post_sticker_with_caption(image_path, gift_name)
        await post_gift_details(gift_info)

        seen.add(gift_id)
        with open(CACHE_FILE, 'w') as f:
            json.dump(list(seen), f)

def run_scheduler():
    schedule.every(10).minutes.do(lambda: client.loop.create_task(process_new_gifts()))
    print("🚀 Gift bot started. Watching for new NFTs...")
    while True:
        schedule.run_pending()
        time.sleep(1)

with client:
    client.start(phone=PHONE_NUMBER)
    run_scheduler()
