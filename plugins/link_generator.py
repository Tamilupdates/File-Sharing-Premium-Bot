from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import *
from helper_func import encode, get_message_id
import aiohttp

async def get_short_link(link):
    url = "https://cleanuri.com/api/v1/shorten"
    data = {'url': link}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status == 200:
                data = await response.json()
                # Extract the shortened URL from the 'result_url' field
                return data.get("result_url")
            else:
                raise Exception(f"HTTP error: {response.status}")

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "Forward The First Message From DB Channel (With Quotes)..\n\nOr Send The DB Channel Post Link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nThis Forwarded Post Is Not From My DB Channel Or This Link Is Not Taken From DB Channel", quote = True)
            continue

    while True:
        try:
            second_message = await client.ask(text = "Forward The Last Message From DB Channel (With Quotes)..\n\nOr Send The DB Channel Post Link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nThis Forwarded Post Is Not From My DB Channel Or This Link Is Not Taken From DB Channel", quote = True)
            continue
    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    #link = f"https://t.me/{client.username}?start={base64_string}"
    
    try:
        if FINAL_URL is not None:
            link = f"https://{FINAL_URL}?start={base64_string}"
    except:
        link = f"https://telegram.me/{client.username}?start={base64_string}"

    short_link = await get_short_link(link)

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>Here is Link :\n<code>{link}</code></b>", quote=True, reply_markup=reply_markup)
    #await second_message.reply_text(f"<b>Here is Link :\n<code>{short_link}</code></b>", quote=True, reply_markup=reply_markup)
@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "Forward Message From The DB Channel (With Quotes)..\n\nOr Send The DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nThis Forwarded Post Is Not From My DB Channel Or This Link Is Not Taken From DB Channel", quote = True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    #link = f"https://t.me/{client.username}?start={base64_string}"
    try:
        if FINAL_URL is not None:
            link = f"https://{FINAL_URL}?start={base64_string}"
    except:
        link = f"https://telegram.me/{client.username}?start={base64_string}"

    short_link = await get_short_link(link)

    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>Here is Link :\n<code>{link}</code></b>", quote=True, reply_markup=reply_markup)
    #await channel_message.reply_text(f"<b>Here is Link :\n<code>{short_link}</code></b>", quote=True, reply_markup=reply_markup)

