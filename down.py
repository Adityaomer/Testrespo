
API_TOKEN='7516413067:AAHXMt9749KafZkQHDUMDd8g2Lmln0Cz9FE'
import secrets
import sqlite3
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext

API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

UPLOAD_FILE = 1
UPLOAD_MORE = 2
UPLOAD_PHOTO = 3
UPLOAD_CAPTION = 4

class DatabaseContext:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Send me a file to upload!")
    return UPLOAD_FILE

def upload_file(update: Update, context: CallbackContext) -> int:
    # Get the database context from the bot
    db_context = context.bot.conversation_data.get('db_context')

    file = update.message.document or update.message.photo[-1]
    
    if file:
        file_id = file.file_id
        bot_username = context.bot.get_me().username
        collection_id = context.user_data.get('collection_id')

        # If no collection ID exists, create a new one
        if not collection_id:
            collection_id = secrets.token_urlsafe(8)
            context.user_data['collection_id'] = collection_id

        # Add the file ID to the collection in the database
        db_context.cursor.execute("INSERT OR IGNORE INTO collections (collection_id, file_ids) VALUES (?, ?)", (collection_id, file_id))
        db_context.conn.commit()

        update.message.reply_text("File uploaded! Send another file, or type /done to finish.")
        return UPLOAD_MORE
    else:
        update.message.reply_text("Please send a valid file.")
        return UPLOAD_FILE

def done(update: Update, context: CallbackContext) -> int:
    # Get the database context from the bot
    db_context = context.bot.conversation_data.get('db_context')

    collection_id = context.user_data.get('collection_id')
    
    if collection_id:
        update.message.reply_text("Now send me a photo for the collection.")
        return UPLOAD_PHOTO
    else:
        update.message.reply_text("You haven't started uploading files.")
        return ConversationHandler.END

def upload_photo(update: Update, context: CallbackContext) -> int:
    # Get the database context from the bot
    db_context = context.bot.conversation_data.get('db_context')

    photo = update.message.photo[-1]

    if photo:
        photo_id = photo.file_id
        collection_id = context.user_data['collection_id']
        # Update the collection with the photo ID
        db_context.cursor.execute("UPDATE collections SET photo_id = ? WHERE collection_id = ?", (photo_id, collection_id))
        db_context.conn.commit()

        update.message.reply_text("Photo uploaded! Now send me a caption for the collection.")
        return UPLOAD_CAPTION
    else:
        update.message.reply_text("Please send a valid photo.")
        return UPLOAD_PHOTO

def upload_caption(update: Update, context: CallbackContext) -> int:
    # Get the database context from the bot
    db_context = context.bot.conversation_data.get('db_context')

    caption = update.message.text
    collection_id = context.user_data['collection_id']

    # Update the collection with the caption
    db_context.cursor.execute("UPDATE collections SET caption = ? WHERE collection_id = ?", (caption, collection_id))
    db_context.conn.commit()

    # Build the download link
    bot_username = context.bot.get_me().username
    download_link = f"https://t.me/{bot_username}?start=download_{collection_id}"

    # Send the download link with inline keyboard
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Download All Files", url=download_link)
    ]])
    update.message.reply_text("Files uploaded! Click the link below to download:", reply_markup=keyboard)

    # Clear user data for the next upload
    del context.user_data['collection_id']

    return ConversationHandler.END

def download_files(update: Update, context: CallbackContext) -> None:
    # Get the database context from the bot
    db_context = context.bot.conversation_data.get('db_context')

    # Extract the collection ID from the 'start' parameter
    collection_id = context.args[0].split('_')[1] if context.args else None

    if collection_id:
        # Retrieve the data from the database
        db_context.cursor.execute("SELECT file_ids, photo_id, caption FROM collections WHERE collection_id = ?", (collection_id,))
        result = db_context.cursor.fetchone()

        if result:
            file_ids = result[0].split(',')
            photo_id = result[1]
            caption = result[2]

            # Send the files one by one
            for file_id in file_ids:
                context.bot.send_document(chat_id=update.effective_chat.id, document=file_id)

            # Send the photo with the caption
            if photo_id:
                context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo_id, caption=caption)

            update.message.reply_text("Files sent successfully!")
        else:
            update.message.reply_text("Invalid collection ID.")
    else:
        update.message.reply_text("Invalid collection ID.")

def main():
    global conn, cursor
    conn = sqlite3.connect('file_collections.db')  # Create connection in main
    cursor = conn.cursor()

    db_context = DatabaseContext(conn, cursor)

    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Pass the database context to the ConversationHandler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('upload', start)],
        states={
            UPLOAD_FILE: [MessageHandler(Filters.document | Filters.photo, lambda update, context: upload_file(update, context, db_context))],
            UPLOAD_MORE: [MessageHandler(Filters.document | Filters.photo, lambda update, context: upload_file(update, context, db_context)),
                         CommandHandler('done', lambda update, context: done(update, context, db_context))],
            UPLOAD_PHOTO: [MessageHandler(Filters.photo, lambda update, context: upload_photo(update, context, db_context))],
            UPLOAD_CAPTION: [MessageHandler(Filters.text, lambda update, context:upload_caption(update, context, db_context))],
        },
            fallbacks=[CommandHandler('upload', start)],
        persistent=True,
        per_user=True,
        allow_reentry=True,
        conversation_timeout=300
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", lambda update, context: download_files(update, context, db_context)))  # Handle the 'start' command

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()