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

async def create_sticker_pack(sticker_bytes_list):
    try:
        num_stickers = len(sticker_bytes_list)
        # Calculate the required dimensions for the image
        # We'll arrange stickers in two rows, with maximum 4 stickers per row
        rows = 2
        cols = min(num_stickers, 4)  # Number of columns depends on how many stickers we have

        # Calculate the dimensions of the image
        sticker_width = 512  # Increased sticker width
        sticker_height = 512 # Increased sticker height
        image_width = cols * sticker_width
        image_height = rows * sticker_height

        # Create a new transparent image
        img = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))

        for i, sticker_bytes in enumerate(sticker_bytes_list):
            sticker = Image.open(sticker_bytes).convert("RGBA")
            current_width, current_height = sticker.size
            # Resize the sticker if it's not 512x512
            if current_width != sticker_width or current_height != sticker_height:
                sticker = sticker.resize((sticker_width, sticker_height), Image.LANCZOS)

            row = i // 4
            col = i % 4

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
    await event.respond("Welcome! Send me eight stickers. I will create a sticker pack for you.")
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
                        await event.respond("Creating sticker pack...")

                        sticker_pack_image = await create_sticker_pack(user_data[user_id]['stickers'])
                        if sticker_pack_image:
                            try:
                                image_path = f"sticker_pack_{user_id}.png"
                                with open(image_path, "wb") as f:
                                    f.write(sticker_pack_image.getvalue())
                                # Convert PNG to WebP using Pillow
                                img = Image.open(image_path)
                                webp_path = f"sticker_pack_{user_id}.webp"
                                img.save(webp_path, "WEBP", lossless=True)

                                await client.send_file(event.chat_id, webp_path, caption="Here's your sticker pack!")
                                os.remove(image_path)  # Remove the temporary PNG file
                                os.remove(webp_path)   # Remove the temporary WebP file

                            except Exception as e:
                                await event.respond(f"Error sending sticker pack: {e}")
                        else:
                            await event.respond("Failed to create sticker pack.")
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