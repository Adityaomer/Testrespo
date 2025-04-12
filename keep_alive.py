
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
        if message.media:  # Check if media exists
            data = await client.download_media(message.media)
            return data
        else:
            return None
    except Exception as e:
        await message.respond(f"Error downloading media: {e}")
        return None

async def add_stickers_to_image(image_bytes, sticker_bytes_list, event):
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")  # Open from bytes directly
        image_width, image_height = image.size
        num_stickers = len(sticker_bytes_list)

        # Calculate sticker size
        max_sticker_size = min(image_width // 4, image_height // 4)
        resized = False  # Track if resizing happened

        sticker_images = []
        for sticker_bytes in sticker_bytes_list:
            sticker = Image.open(io.BytesIO(sticker_bytes)).convert("RGBA")  # Open from bytes directly
            sticker_width, sticker_height = sticker.size
            if sticker_width > max_sticker_size or sticker_height > max_sticker_size:
                ratio = min(max_sticker_size / sticker_width, max_sticker_size / sticker_height)
                sticker = sticker.resize((int(sticker_width * ratio), int(sticker_height * ratio)), Image.LANCZOS)
                sticker_width, sticker_height = sticker.size
                resized = True
            sticker_images.append(sticker)

        # Positioning logic
        row1_count = min(4, num_stickers)
        row2_count = max(0, num_stickers - 4)
        y_offset_row1 = image_height // 4 - sticker_images[0].height // 2 if sticker_images else 0 # Place row 1 stickers at the top quarter
        y_offset_row2 = 3 * image_height // 4 - (sticker_images[0].height // 2) if sticker_images else 0  # Place row 2 at bottom

        # Place stickers in row 1
        if row1_count > 0:
            x_start_row1 = (image_width - (sum(sticker.width for sticker in sticker_images[:row1_count]))) // (row1_count + 1)

            x_pos = x_start_row1
            for i in range(row1_count):
                image.paste(sticker_images[i], (int(x_pos), int(y_offset_row1)), sticker_images[i])
                x_pos += sticker_images[i].width + x_start_row1

        # Place stickers in row 2
        if row2_count > 0:
            x_start_row2 = (image_width - (sum(sticker.width for sticker in sticker_images[4:]))) // (row2_count + 1)

            x_pos = x_start_row2
            for i in range(4, num_stickers):
                image.paste(sticker_images[i], (int(x_pos), int(y_offset_row2)), sticker_images[i])
                x_pos += sticker_images[i].width + x_start_row2



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
    user_id = event.sender_id
    user_data[user_id] = {'stickers': [], 'photo': None}
    await event.respond("Welcome! Send me stickers (up to 8). Send /stop when you're done, then send the photo.")


@client.on(events.NewMessage(pattern='/stop'))
async def stop_handler(event):
    user_id = event.sender_id
    if user_id in user_data:
        await event.respond("Sticker collection stopped. Now send me the photo.")
    else:
        await event.respond("Please send /start first.")

@client.on(events.NewMessage)
async def message_handler(event):
    user_id = event.sender_id

    if user_id not in user_data:
        if event.text != '/start':  # Only allow /start if no user data
            await event.respond("Please send /start first.")
            return
        else: # Handles /start when user is not in user_data
            await start_handler(event)
            return
    if event.text == '/stop':
            return # ignores

    if len(user_data[user_id]['stickers']) < 8 and user_data[user_id].get('photo') is None:
        if event.sticker:
            try:
                sticker_bytes = await download_media(event)
                if sticker_bytes:
                    user_data[user_id]['stickers'].append(sticker_bytes)
                    await event.respond(f"Sticker {len(user_data[user_id]['stickers'])}/8 received.")
                else:
                     await event.respond("Failed to download sticker. Please try again.")

            except Exception as e:
                await event.respond(f"Error processing sticker: {e}")
        elif event.photo or (event.media and isinstance(event.media, types.MessageMediaDocument) and event.media.mime_type.startswith('image')): # Catch stray photo send before /stop
            await event.respond("Please send /stop first before sending a photo.")
        else:
            await event.respond("Please send a sticker or /stop.")


    elif user_data[user_id].get('photo') is None:
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

                    del user_data[user_id]  # Reset by deleting the user data

                else:
                    await event.respond("Failed to download the photo. Please try again.")

            except Exception as e:
                await event.respond(f"Error processing photo: {e}")
        else:
            await event.respond("Please send a photo.")


if __name__ == '__main__':
    client.run_until_disconnected()
