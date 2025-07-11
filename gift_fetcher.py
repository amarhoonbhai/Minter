# gift_fetcher.py

import requests
from bot_config import GIFT_LIST_URL, GIFT_INFO_URL, GIFT_IMAGE_URL

def fetch_all_gifts():
    return requests.get(GIFT_LIST_URL).json()

def fetch_gift_info(gift_name):
    return requests.get(GIFT_INFO_URL.format(gift_name)).json()

def get_gift_image(gift_id):
    return GIFT_IMAGE_URL.format(gift_id)
