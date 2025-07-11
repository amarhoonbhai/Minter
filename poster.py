# poster.py

from telethon import TelegramClient
from telethon.tl.functions.messages import SendMessageRequest
from bot_config import API_ID, API_HASH, PHONE_NUMBER, CHANNEL_USERNAME

client = TelegramClient('gift_session', API_ID, API_HASH)

async def post_sticker_with_caption(image_path, gift_name):
    await client.send_file(
        entity=CHANNEL_USERNAME,
        file=image_path,
        caption=f"🎁 *{gift_name}* | {CHANNEL_USERNAME}",
        parse_mode='markdown'
    )

async def post_gift_details(gift_info):
    text = (
        "🎉 *A new gift has been added!*

"
        f"Released by: @{gift_info.get('releasedBy', 'unknown')}
"
        f"Price: {gift_info.get('price', 'unknown')} ⭐
"
        f"Limit: {gift_info.get('limit', 'unknown')}
"
        f"Upgrade: {gift_info.get('upgrade', 'unavailable')}"
    )
    await client(SendMessageRequest(
        peer=CHANNEL_USERNAME,
        message=text,
        parse_mode='markdown'
    ))
