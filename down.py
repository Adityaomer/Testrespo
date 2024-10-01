from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, CallbackContext
from telegram.ext.filters import Filters 
API_TOKEN = '7516413067:AAHXMt9749KafZkQHDUMDd8g2Lmln0Cz9FE'

UPLOAD_FILE = 1  # State for waiting for a file

def start(update: Update, context: CallbackContext) -> None:
    file_id = context.args[0] if context.args else None

    if file_id:
        # Send the file with the provided file ID
        context.bot.send_document(chat_id=update.effective_chat.id, document=file_id)
        update.message.reply_text("File sent successfully!")
    else:
        update.message.reply_text("Invalid file ID.")

def upload(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Send me a file to upload!')
    return UPLOAD_FILE

def upload_file(update: Update, context: CallbackContext) -> int:
    file = update.message.document or update.message.photo[-1]  # Handle both documents and photos

    if file:
        file_id = file.file_id
        bot_username = context.bot.get_me().username  # Get the bot's username

        # Build the inline keyboard
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "Your File ID",
                url=f"https://t.me/{bot_username}?start={file_id}"  # URL for starting a PM with the file ID
            )
        ]])

        update.message.reply_text("Here is your file ID:", reply_markup=keyboard)
        return ConversationHandler.END
    else:
        update.message.reply_text("Please send a valid file.")
        return UPLOAD_FILE

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
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()