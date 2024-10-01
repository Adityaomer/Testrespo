from telegram.ext import ConversationHandler
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import re
import time
from telegram.ext.dispatcher import run_async
from telegram import User, PhotoSize, ParseMode
import telegram
from urllib.parse import quote_plus
import secrets

API_TOKEN = '7516413067:AAHXMt9749KafZkQHDUMDd8g2Lmln0Cz9FE'
UPLOAD_FILE = 1  # State for waiting for a file

def upload(update, context):
    update.message.reply_text('Send me a file to upload!')
    return UPLOAD_FILE

def upload_file(update: Update, context: CallbackContext) -> int:
    file = update.message.document or update.message.photo[-1]  # Handle both documents and photos

    if file:
        file_id = file.file_id
        bot_username = context.bot.get_me().username  # Get the bot's username

        # Generate a short unique identifier
        short_id = secrets.token_urlsafe(8)  # Adjust length as needed

        # Store the file ID in the global dictionary
        file_storage[short_id] = file_id

        # Build the inline keyboard
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Get Your File",
                url=f"https://t.me/{bot_username}?start={short_id}"
            )
        ]])

        update.message.reply_text("Here is your file ID:", reply_markup=keyboard)
        return ConversationHandler.END
    else:
        update.message.reply_text("Please send a valid file.")
        return UPLOAD_FILE

def get_file(update: Update, context: CallbackContext) -> None:
    # Extract the short ID from the 'start' parameter
    short_id = context.args[0] if context.args else None

    if short_id:
        # Retrieve the full file ID from the global dictionary
        file_id = file_storage.get(short_id)

        if file_id:
            # Send the file
            context.bot.send_document(chat_id=update.effective_chat.id, document=file_id)
            update.message.reply_text("File sent successfully!")
        else:
            update.message.reply_text("Invalid file ID.")
    else:
        update.message.reply_text("Invalid file ID.")

def main():
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('upload', upload)],
        states={
            UPLOAD_FILE: [MessageHandler(Filters.document | Filters.photo, upload_file)],
        },
        fallbacks=[CommandHandler('upload', upload)]
    )

    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", get_file))  # Handle the 'start' command

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()