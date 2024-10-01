import secrets
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext

API_TOKEN ='7516413067:AAHXMt9749KafZkQHDUMDd8g2Lmln0Cz9FE'

UPLOAD_FILE = 1
UPLOAD_MORE = 2 
FRONT_PAGE = 3 # State for asking to upload more files

# Global dictionary to store file collections
file_collections = {}

def start(update: Update, context: CallbackContext) -> int:
    # Start the conversation by asking to upload a file
    update.message.reply_text("Send me a file to upload!")
    return UPLOAD_FILE

def upload_file(update: Update, context: CallbackContext) -> int:
    file = update.message.document or update.message.photo[-1]
    
    if file:
        file_id = file.file_id
        bot_username = context.bot.get_me().username
        collection_id = context.user_data.get('collection_id')

        # If no collection ID exists, create a new one
        if not collection_id:
            collection_id = secrets.token_urlsafe(8)
            context.user_data['collection_id'] = collection_id
            file_collections[collection_id] = []  # Initialize the collection list

        # Add the file ID to the collection
        file_collections[collection_id].append(file_id)

        update.message.reply_text("File uploaded! Send another file, or type /done to finish.")
        return UPLOAD_MORE
    else:
        update.message.reply_text("Please send a valid file.")
        return FRONT_PAGE
def front_page(update, context):
    user = update.effective_user
    user_id = user.id

    item_name = context.user_data.get("collection_id")                     
                   photo = update.message.photo[-1]  # Get the largest photo size
                   context.user_data["picture"] = photo.file_id
                   context.user_data["caption"] = update. message. caption
                   
   return UPLOAD_FILE

def done(update: Update, context: CallbackContext) -> int:
    collection_id = context.user_data.get('collection_id')
    photo=context.user_data.get("picture") 
    caption=context.user_data.get("caption") 
    
    if collection_id:
        # Get the list of file IDs
        file_ids = file_collections[collection_id]
        bo = context.bot.get_me().username

        if file_ids:
            # Build the download link
            download_link = f"https://t.me/{bo}?start=download_{collection_id}"

            # Send the download link
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Download All Files", url=download_link)
            ]])
            context. bot.send_photo(photo=photo,caption=caption, reply_markup=keyboard)
            
            # Clear user data for the next upload
            del context.user_data['collection_id']
        else:
            update.message.reply_text("No files uploaded.")
        
        return ConversationHandler.END
    else:
        update.message.reply_text("You haven't started uploading files.")
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

def main():
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('upload', start)],
        states={
            UPLOAD_FILE: [MessageHandler(Filters.document | Filters.photo, upload_file)],
            UPLOAD_MORE: [MessageHandler(Filters.document | Filters.photo, upload_file),
            FRONT_PAGE: [MessageHandler(Filters.document | Filters.photo, front_page),
                         CommandHandler('done', done)]
        },
        fallbacks=[CommandHandler('upload', start)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", download_files))  # Handle the 'start' command

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()