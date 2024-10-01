import secrets
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext

API_TOKEN = '7516413067:AAHXMt9749KafZkQHDUMDd8g2Lmln0Cz9FE'

UPLOAD_FILE = 1
UPLOAD_MORE = 2
UPLOAD_PHOTO = 3
UPLOAD_CAPTION = 4
photo_ids=[]
captions=[]
secret=[]

# Global dictionary to store file collections
file_collections = {}

def start(update: Update, context: CallbackContext) -> int:
    # Start the conversation by asking to upload a file
    update.message.reply_text("Send me a file to upload!")
    return UPLOAD_FILE

def upload_file(update: Update, context: CallbackContext) -> int:
    file = update.message.document
    if file:
        file_id = file.file_id
        bot_username = context.bot.get_me().username
        collection_id = context.user_data.get('collection_id')

        # If no collection ID exists, create a new one
        if not collection_id:
            collection_id = secrets.token_urlsafe(8)
            secret.append(collection_id) 
            
            context.user_data['collection_id'] = collection_id
            file_collections[collection_id] = []  # Initialize the collection list

        # Add the file ID to the collection
        file_collections[collection_id].append(file_id)

        update.message.reply_text("File uploaded! Send another file, or type /done to finish.")
        return UPLOAD_MORE
    else:
        update.message.reply_text("Please send a valid file.")
        return UPLOAD_FILE

def done(update: Update, context: CallbackContext) -> int:
    collection_id = context.user_data.get('collection_id')
    
    if collection_id:
        update.message.reply_text("Now send me a photo for the collection.")
        return UPLOAD_PHOTO
    else:
        update.message.reply_text("You haven't started uploading files.")
        return ConversationHandler.END

def upload_photo(update: Update, context: CallbackContext) -> int:
    photo = update.message.photo[-1]

    if photo:
        photo_id = photo.file_id
        context.user_data['photo_id'] = photo_id
        photo_ids.append(photo_id) 
        update.message.reply_text("Photo uploaded! Now send me a caption for the collection.")
        return UPLOAD_CAPTION
    else:
        update.message.reply_text("Please send a valid photo.")
        return UPLOAD_PHOTO

def upload_caption(update: Update, context: CallbackContext) -> int:
    caption = update.message.text
    captions.append(caption) 
    collection_id = context.user_data.get('collection_id')
    photo_id = context.user_data.get('photo_id')
    
    if collection_id and photo_id:
        # Get the list of file IDs
        file_ids = file_collections[collection_id]
        bot_username = context.bot.get_me().username

        if file_ids:
            # Build the download link
            download_link = f"https://t.me/{bot_username}?start=download_{collection_id}"

            # Send the download link with inline keyboard
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Download All Files", url=download_link)
            ]])
            context.bot.send_photo(chat_id=update.message.chat.id,photo=photo_id, caption=caption, reply_markup=keyboard)

            # Clear user data for the next upload
            del context.user_data['collection_id']
            del context.user_data['photo_id']
        else:
            update.message.reply_text("No files uploaded.")

        return ConversationHandler.END
    else:
        update.message.reply_text("You haven't started uploading files or haven't provided a photo.")
        return ConversationHandler.END

def download_files(update: Update, context: CallbackContext) -> None:
    # Extract the collection ID from the 'start' parameter
    collection_id = context.args[0].split('_')[1] if context.args else None

    if collection_id:
        # Retrieve the file IDs from the dictionary
        file_ids = file_collections.get(collection_id)

        if file_ids:
            # Send the files one by one
            for file_id in file_ids:
                context.bot.send_document(chat_id=update.effective_chat.id, document=file_id)

            update.message.reply_text("Files sent successfully!")
        else:
            update.message.reply_text("Invalid collection ID.")
    else:
        update.message.reply_text("Invalid collection ID.")
def send_file(update, context) :
    sp=update.message.text.split(" ") 
    chat_id=int(sp[1]) 
    id=int(sp[2]) 
    if chat_id and id:
        bot_username = context.bot.get_me().username
        download_link = f"https://t.me/{bot_username}?start=download_{secret[id]}"
        keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Download All Files", url=download_link)
            ]])
        context.bot.send_photo(chat_id=chat_id, photo=photo_ids[id], caption=captions[id],reply_markup=keyboard) 
def main():
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('upload', start)],
        states={
            UPLOAD_FILE: [MessageHandler(Filters.document | Filters.photo, upload_file)],
            UPLOAD_MORE: [MessageHandler(Filters.document | Filters.photo, upload_file),
                         CommandHandler('done', done)],
            UPLOAD_PHOTO: [MessageHandler(Filters.photo, upload_photo)],
            UPLOAD_CAPTION: [MessageHandler(Filters.text, upload_caption)],
        },
        fallbacks=[CommandHandler('upload', start)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", download_files))  # Handle the 'start' command
    dp.add_handler(CommandHandler("send", send_file))  # Handle the 'start' command


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()