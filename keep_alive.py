import asyncio
import io
from PIL import Image, UnidentifiedImageError
from telethon import TelegramClient, events, types
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetID


API_ID = int("23599783")
API_HASH = "62c4987db06716e25c4d68dcdcdc1ea5"
BOT_TOKEN = "7541028256:AAHwPTJw7SltuagihXg2hDErXJiZdKZL2zE"
api_id = API_ID
api_hash = API_HASH
bot_token = BOT_TOKEN


client = TelegramClient('sticker_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


# Store the stickers and photo for each user
user_data = {}  # Dict to store user-specific data (stickers and photo)


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

        for sticker_bytes in sticker_bytes_list:
            sticker = Image.open(sticker_bytes).convert("RGBA")
            sticker_width, sticker_height = sticker.size

            # Resize the sticker if it's too big (optional, adjust as needed)
            max_sticker_size = min(image_width // 3, image_height // 3) # relative to image
            if sticker_width > max_sticker_size or sticker_height > max_sticker_size:
                ratio = min(max_sticker_size / sticker_width, max_sticker_size / sticker_height)
                sticker = sticker.resize((int(sticker_width * ratio), int(sticker_height * ratio)), Image.LANCZOS)
                sticker_width, sticker_height = sticker.size

            # Calculate position (example: bottom right corner, adjust as needed)
            x = image_width - sticker_width - 10  # 10 pixels from the right
            y = image_height - sticker_height - 10 # 10 pixels from the bottom

            # Paste the sticker onto the image
            image.paste(sticker, (x, y), sticker) # 'sticker' is the mask
        output.jpg = io.BytesIO()
        image.save(output.jpg, format="PNG")
        output.jpg.seek(0)
        return output
    except UnidentifiedImageError as e:
        await event.respond(f"Error processing image (likely invalid format): {e}")
        return None
    except Exception as e:
        await event.respond(f"Error adding stickers: {e}")
        return None


@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.respond("Welcome! Send me four stickers first, then a photo. I will combine them!")
    user_id = event.sender_id
    user_data[user_id] = {'stickers': [], 'photo': None} # initializes the user's data

@client.on(events.NewMessage)
async def message_handler(event):
    user_id = event.sender_id
    if user_id not in user_data: # if user starts sending media without /start
        await event.respond("Please send /start first.")
        return

    if len(user_data[user_id]['stickers']) < 4: # collecting stickers
        if event.sticker:  # Check if the message is a sticker
            try:
                sticker_bytes = await download_media(event)
                if sticker_bytes:
                    user_data[user_id]['stickers'].append(sticker_bytes)

                    await event.respond(f"Sticker {len(user_data[user_id]['stickers'])}/4 received.")

                    if len(user_data[user_id]['stickers']) == 4:
                        await event.respond("Great! Now send me a photo.")
                else:
                     await event.respond("Failed to download sticker. Please try again.")

            except Exception as e:
                await event.respond(f"Error processing sticker: {e}")

        else:
            await event.respond("Please send a sticker.")


    elif user_data[user_id]['photo'] is None: # collects the photo

        if event.photo or (event.media and isinstance(event.media, types.MessageMediaDocument) and event.media.mime_type.startswith('image')): # Check if the message is a photo (photo or document of type image)
            try:

                photo_bytes = await download_media(event)

                if photo_bytes:
                    user_data[user_id]['photo'] = photo_bytes
                    await event.respond("Photo received. Processing...")

                    # Combine stickers and photo
                    combined_image = await add_stickers_to_image(user_data[user_id]['photo'], user_data[user_id]['stickers'],event)

                    if combined_image:
                        try:
                            await client.send_file(event.chat_id, combined_image, caption="Here's your image with stickers!")

                        except Exception as e:
                             await event.respond(f"Error sending file: {e}")

                    else:
                        await event.respond("Failed to combine stickers with the image.  Make sure the image is in a valid format (PNG, JPG, etc.)")


                    # Reset user data
                    user_data[user_id] = {'stickers': [], 'photo': None}
                else:
                    await event.respond("Failed to download the photo. Please try again.")


            except Exception as e:
                await event.respond(f"Error processing photo: {e}")
        else:
            await event.respond("Please send a photo.")







if __name__ == '__main__':
    client.run_until_disconnected()