import asyncio
import io
from PIL import Image, UnidentifiedImageError
from telethon import TelegramClient, events, types
import os

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

async def add_stickers_to_image(image_bytes, sticker_bytes_list, event):
    try:
        image = Image.open(image_bytes).convert("RGBA")
        image_width, image_height = image.size
        num_stickers = len(sticker_bytes_list)

        for i, sticker_bytes in enumerate(sticker_bytes_list):
            sticker = Image.open(sticker_bytes).convert("RGBA")
            sticker_width, sticker_height = sticker.size

            # Resize the sticker if it's too big
            max_sticker_size = min(image_width // 4, image_height // 4)  # Reduced size
            if sticker_width > max_sticker_size or sticker_height > max_sticker_size:
                ratio = min(max_sticker_size / sticker_width, max_sticker_size / sticker_height)
                sticker = sticker.resize((int(sticker_width * ratio), int(sticker_height * ratio)), Image.LANCZOS)
                sticker_width, sticker_height = sticker.size

            # Calculate position (distribute evenly in two rows)
            row = i // 4  # Determine row (0 or 1)
            col = i % 4   # Determine column (0 to 3)

            x = (image_width // 5) * (col + 1) - (sticker_width // 2)
            y = (image_height // 3) * (row + 1) - (sticker_height // 2)

            image.paste(sticker, (int(x), int(y)), sticker)

        output = io.BytesIO()
        image.save(output, format="PNG")
        output.seek(0)
        return output
    except UnidentifiedImageError as e:
        await event.respond(f"Error processing image (likely invalid format): {e}")
        return None
    except Exception as e:
        await event.respond(f"Error adding stickers: {e}")
        return None
@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond("Welcome! Send me eight stickers first, then a photo. I will combine them!")
    user_id = event.sender_id
    user_data[user_id] = {'stickers': [], 'photo': None}

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
                        await event.respond("Great! Now send me a photo.")
                else:
                     await event.respond("Failed to download sticker. Please try again.")

            except Exception as e:
                await event.respond(f"Error processing sticker: {e}")
        else:
            await event.respond("Please send a sticker.")

    elif user_data[user_id]['photo'] is None:
        if event.photo or (event.media and isinstance(event.media, types.MessageMediaDocument) and event.media.mime_type.startswith('image')):
            try:
                photo_bytes = await download_media(event)
                if photo_bytes:
                    user_data[user_id]['photo'] = photo_bytes
                    await event.respond("Photo received. Processing...")

                    combined_image = await add_stickers_to_image(user_data[user_id]['photo'], user_data[user_id]['stickers'], event)

                    if combined_image:
                        try:
                            image_path = f"temp_image_{user_id}.png"
                            with open(image_path, "wb") as f:
                                f.write(combined_image.getvalue())

                            await client.send_file(event.chat_id, image_path, caption="Here's your image with stickers!")
                            os.remove(image_path)

                        except Exception as e:
                             await event.respond(f"Error sending file: {e}")

                    else:
                        await event.respond("Failed to combine stickers with the image.  Make sure the image is in a valid format (PNG, JPG, etc.)")

                    user_data[user_id] = {'stickers': [], 'photo': None}
                else:
                    await event.respond("Failed to download the photo. Please try again.")

            except Exception as e:
                await event.respond(f"Error processing photo: {e}")
        else:
            await event.respond("Please send a photo.")

if __name__ == '__main__':
    client.run_until_disconnected()