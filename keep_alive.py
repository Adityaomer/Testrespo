
from telethon import TelegramClient, events, types
from telethon.tl.types import InputStickerSetID
from telethon.tl.functions.messages import GetStickerSetRequest
from PIL import Image
import io
import asyncio
import os



API_ID = int("23599783")
API_HASH = "62c4987db06716e25c4d68dcdcdc1ea5"
BOT_TOKEN = "7541028256:AAHwPTJw7SltuagihXg2hDErXJiZdKZL2zE"
api_id = API_ID
api_hash = API_HASH
bot_token = BOT_TOKEN

session_name = 'sticker_combiner_bot'


user_sticker_counts = {}  # Store sticker counts per user

client = TelegramClient(session_name, api_id, api_hash)

async def combine_stickers(image_paths):
    """Combines a list of image paths into a single image side-by-side."""

    images = [Image.open(path) for path in image_paths]
    widths, heights = zip(*(i.size for i in images))

    # Find maximum height to align the stickers vertically
    max_height = max(heights)
    new_width = sum(widths)
    new_img = Image.new('RGBA', (new_width, max_height), (0, 0, 0, 0))  # Use RGBA for transparency

    x_offset = 0
    for img in images:
        # Paste the image onto the new image, padding the top if necessary
        padding = (max_height - img.size[1]) // 2
        new_img.paste(img, (x_offset, padding))
        x_offset += img.size[0]

    # Save the combined image to a BytesIO object
    combined_image_bytes = io.BytesIO()
    new_img.save(combined_image_bytes, format='PNG')
    combined_image_bytes.seek(0)  # Reset the buffer to the beginning
    return combined_image_bytes

async def download_sticker(client, sticker_document, file_name):
    """Downloads a sticker from its document."""
    sticker_file = await client.download_media(sticker_document, file=file_name)
    return sticker_file



@client.on(events.NewMessage(pattern='/combine'))
async def combine_command_handler(event):
    """Handles the /combine command to start collecting stickers."""
    user_id = event.sender_id
    received_stickers.clear()  # Clear stickers for this user
    user_sticker_counts[user_id] = 0  # Initialize count for this user

    await event.respond("Okay, send me 8 stickers and I'll combine them!")


@client.on(events.NewMessage)
async def sticker_handler(event):
    """Handles incoming stickers."""
    user_id = event.sender_id
    if user_id not in user_sticker_counts:
        return  # Ignore stickers if the user hasn't started the command

    if event.sticker:
        user_sticker_counts[user_id] += 1
        sticker_document = event.message.document

        # Check if it is a sticker using attributes
        is_sticker = False
        for attr in sticker_document.attributes:
            if isinstance(attr, types.DocumentAttributeSticker):
                is_sticker = True
                sticker_set_input = attr.stickerset
                break

        if not is_sticker:
            await event.respond("That was not recognized as a sticker. Please send valid stickers.")
            user_sticker_counts[user_id] -= 1 # Decrement sticker count, as this message wasn't a sticker
            return

        file_ext = '.png'  # Default to PNG
        if sticker_document.mime_type == 'image/webp':  # Webp is also acceptable
            file_ext = '.webp'

        sticker_file_name = f"sticker_{user_sticker_counts[user_id]}_{user_id}{file_ext}" # Unique file name
        try:
            file_path = await download_sticker(client, sticker_document, sticker_file_name)  # Download the sticker
            received_stickers.append(file_path) # Append the downloaded file path

            await event.respond(f"Sticker {user_sticker_counts[user_id]}/8 received.")


            if user_sticker_counts[user_id] == 8:
                try:
                    await event.respond("Combining your stickers...")
                    combined_image = await combine_stickers(received_stickers)
                    await client.send_file(event.chat_id, file=combined_image, caption="Here's your combined sticker!")

                except Exception as e:
                    print(f"Error combining or sending stickers: {e}")
                    await event.respond("Sorry, there was an error combining the stickers.")
                finally:
                    # Clean up sticker files
                    for sticker_file in received_stickers:
                        try:
                            os.remove(sticker_file)  # Delete the temporary sticker file
                        except Exception as e:
                            print(f"Error deleting sticker file: {e}")
                    received_stickers.clear()  # Clear list
                    user_sticker_counts[user_id] = 0 # Reset count

        except Exception as e:
            print(f"Error downloading sticker: {e}")
            await event.respond("Sorry, there was an error downloading the sticker.")
            user_sticker_counts[user_id] -= 1  # Decrement count after download error
            try:
                os.remove(sticker_file_name)
            except FileNotFoundError:
                pass  # File may not have been downloaded
            except Exception as e2:
                print(f"Could not delete sticker due to {e2}")



    

if __name__ == '__main__':
    await client.start(bot_token=bot_token)
    print("Bot started. Listening for messages...")
    await client.run_until_disconnected()
