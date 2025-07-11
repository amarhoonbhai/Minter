# sticker_manager.py

import requests
from bot_config import BOT_TOKEN, STICKER_SET_NAME, STICKER_SET_TITLE, TELEGRAM_USER_ID

def create_sticker_set(gift_id, emoji, file_path):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/createNewStickerSet'
    with open(file_path, 'rb') as f:
        files = {'png_sticker': f}
        data = {
            'user_id': TELEGRAM_USER_ID,
            'name': STICKER_SET_NAME,
            'title': STICKER_SET_TITLE,
            'emojis': emoji
        }
        return requests.post(url, data=data, files=files).json()

def add_sticker_to_set(file_path, emoji):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/addStickerToSet'
    with open(file_path, 'rb') as f:
        files = {'png_sticker': f}
        data = {
            'user_id': TELEGRAM_USER_ID,
            'name': STICKER_SET_NAME,
            'emojis': emoji
        }
        return requests.post(url, data=data, files=files).json()
