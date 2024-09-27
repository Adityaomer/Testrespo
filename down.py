from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Replace with your actual bot token
TOKEN = "7209661607:AAG9W_N9Yel3IUtJkWYAbaVHYufIdbsfGvA"

# Define bunchify function (or use a library)
def bunchify(obj):
    if isinstance(obj, dict):
        return Bunch(**{key: bunchify(value) for key, value in obj.items()})
    elif isinstance(obj, list):
        return [bunchify(item) for item in obj]
    else:
        return obj

class Bunch(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        rf'Hi {user.mention_markdown_v2()}!',
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")

def handle_message(update: Update, context: CallbackContext) -> None:
    """Handle the message sent by the user."""
    message = update.message

    # Informing the user that the bot is processing their request
    update.message.reply_markdown_v2(
        "⏳ *Please wait...* I'm working on processing your video. This may take a moment depending on the length. Hang tight! 🚀"
    )

    # Notify the user that a video upload is in progress
    context.bot.sendChatAction(chat_id=message.chat.id, action='upload_video')

    # Proceed with the URL handling
    ms = message.text

    # Sanitize the user's input (optional)
    # ... 

    url = f"https://tele-social.vercel.app/down?url={ms}"

    # Retry logic for HTTP requests
    retries = Retry(
        total=5,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=0.3,
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retries)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    try:
        response = bunchify(http.get(url).json())

        if 'data' in response and response['data'].get('status', '').lower() == "success":
            platform = response['platform']
            urls = response['data']['urls']

            # Handle different content types based on the number of URLs
            if len(urls) > 1:  # Check for multiple URLs
                # Handle the specific content type here
                # ...

            else:  # Handle the single URL case
                # ...
        else:
            # Handle case where the status is not success or data is missing
            update.message.reply_markdown_v2(
                "⚠️ *Sorry, I couldn't fetch the content.* Please check the link and try again later."
            )
    except Exception as e:
        # Handle any other errors such as network issues or invalid URLs
        update.message.reply_markdown_v2(
            "⚠️ *Oops! Something went wrong.* Please try again later."
        )

# Create the Updater and dispatcher
updater = Updater(7209661607:AAG9W_N9Yel3IUtJkWYAbaVHYufIdbsfGvA)
dispatcher = updater.dispatcher

# Add handlers
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Start the bot
updater.start_polling()
updater.idle()