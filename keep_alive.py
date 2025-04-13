import asyncio
import io
from PIL import Image, UnidentifiedImageError, ImageDraw, ImageFont
from telethon import TelegramClient, events, types
import os
import random

API_ID = int("23599783")
API_HASH = "62c4987db06716e25c4d68dcdcdc1ea5"
BOT_TOKEN = "7541028256:AAHwPTJw7SltuagihXg2hDErXJiZdKZL2zE"
api_id = API_ID
api_hash = API_HASH
bot_token = BOT_TOKEN

client = TelegramClient('sticker_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Store the stickers and photo for each user
user_data = {}

async def download_media(message):
    try:
        media = message.message.media
        if media is None:
            return None
        data = await client.download_media(media)
        return data
    except Exception as e:
        await message.respond(f"Error downloading media: {e}")
        return None

async def create_sticker_grid(sticker_bytes_list):
    try:
        num_stickers = len(sticker_bytes_list)
        # Calculate the required dimensions for the image
        rows = 4  # Fixed to 4 rows
        cols = 2  # Fixed to 2 columns
        if num_stickers != 8:
            raise ValueError("Exactly 8 stickers are required")

        # Calculate the dimensions of the image
        sticker_width = 512
        sticker_height = 512
        image_width = cols * sticker_width
        image_height = rows * sticker_height

        # Create a new transparent image
        img = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))

        for i, sticker_bytes in enumerate(sticker_bytes_list):
            sticker = Image.open(sticker_bytes).convert("RGBA")
            current_width, current_height = sticker.size

            if current_width != sticker_width or current_height != sticker_height:
                sticker = sticker.resize((sticker_width, sticker_height), Image.LANCZOS)

            row = i // 2  # Calculate row based on index
            col = i % 2   # Calculate column based on index

            x = col * sticker_width
            y = row * sticker_height
            img.paste(sticker, (x, y), sticker)

        output = io.BytesIO()
        img.save(output, format="PNG")
        output.seek(0)
        return output
    except Exception as e:
        print(f"Error creating sticker pack: {e}")
        return None

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond("Welcome! Send me eight stickers. I will create a sticker with them in a 4x2 grid (4 rows, 2 columns).")
    user_id = event.sender_id
    user_data[user_id] = {'stickers': []}  # Only store stickers

@client.on(events.NewMessage)
async def message_handler(event):
    user_id = event.sender_id
    if user_id not in user_data:
        await event.respond("Please send /start first.")
        return

    if len(user_data[user_id]['stickers']) < 8:
        if event.sticker:
            try:
                sticker_bytes = await download_media(event)
                if sticker_bytes:
                    user_data[user_id]['stickers'].append(sticker_bytes)
                    await event.respond(f"Sticker {len(user_data[user_id]['stickers'])}/8 received.")
                    if len(user_data[user_id]['stickers']) == 8:
                        await event.respond("Creating sticker...")

                        sticker_grid_image = await create_sticker_grid(user_data[user_id]['stickers'])
                        if sticker_grid_image:
                            try:
                                image_path = f"sticker_grid_{user_id}.png"
                                with open(image_path, "wb") as f:
                                    f.write(sticker_grid_image.getvalue())
                                img = Image.open(image_path)
                                webp_path = f"sticker_grid_{user_id}.webp"
                                img.save(webp_path, "WEBP", lossless=True)

                                await client.send_file(event.chat_id, webp_path, caption="Here's your sticker!")
                                os.remove(image_path)
                                os.remove(webp_path)

                            except Exception as e:
                                await event.respond(f"Error sending sticker: {e}")
                        else:
                            await event.respond("Failed to create sticker.")

                        del user_data[user_id]  # Reset user data

                else:
                     await event.respond("Failed to download sticker. Please try again.")

            except Exception as e:
                await event.respond(f"Error processing sticker: {e}")
        else:
            await event.respond("Please send a sticker.")
    else:
        await event.respond("You already sent eight stickers.  Please send /start to create another sticker pack.")

if __name__ == '__main__':
    client.run_until_disconnected()