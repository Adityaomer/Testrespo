
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
        sticker_width = 256  # Fixed width as per Telegram sticker requirements
        sticker_height = 256 # Fixed height as per Telegram sticker requirements
        image_width = cols * sticker_width
        image_height = rows * sticker_height

        # Create a new transparent image
        img = Image.new('RGBA', (image_width, image_height), (0, 0, 0, 0))

        for i, sticker_bytes in enumerate(sticker_bytes_list):
            sticker = Image.open(sticker_bytes).convert("RGBA")
            current_width, current_height = sticker.size
            # Resize the sticker if it's not 256x256
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

            # Adjust the spacing factor to increase distance between stickers
            spacing_factor_x = 4.5  # Increased horizontal space
            spacing_factor_y = 3 #Keep this value
            x = (image_width / spacing_factor_x) * (col + 1) - (sticker_width // 2)
            y = (image_height // spacing_factor_y) * (row + 1) - (sticker_height // 2)

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
    await event.respond("Welcome! Send me eight stickers first. Then, send a photo or type 'NO PHOTO' to combine them without a background.")
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
                        await event.respond("Great! Now send me a photo or type 'NO PHOTO'.")
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
        elif event.message.message.upper() == "NO PHOTO":  # Check for "NO PHOTO" text
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
            user_data[user_id] = {'stickers': [], 'photo': None}
        else:
            await event.respond("Please send a photo or type 'NO PHOTO'.")

if __name__ == '__main__':
    client.run_until_disconnected()
