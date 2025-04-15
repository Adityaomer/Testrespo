from telethon import TelegramClient, events, Button
from telethon.tl.types import ReplyKeyboardMarkup, KeyboardButton
from telethon.tl.custom import Message
from config import api_id,api_hash,bot_token
from telethon.tl.functions.messages import SendMediaRequest
import random


@app.on(events.NewMessage)
async def checke(event):
    if not event.message.video:
        return
    message = event.message.video
    await send_unforward(app, event.sender_id,message, "This is a cool video!")


async def send_unforward(bot, chat_id, media, caption="", random_id=None):

    try:
        if random_id is None:
            random_id = generate_random_long()

        await bot(
            SendMediaRequest(
                peer=chat_id,
                media=media,
                message=caption,
                random_id=random_id,
                noforwards=True
            )
        )

    except Exception as e:
        print(f"Error sending unforwardable media: {e}")


def generate_random_long():
    return random.getrandbits(63) 
@app.on(events.NewMessage(pattern="/delete"))