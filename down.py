import secrets
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext
import logging
import time

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)  # Use __name__ to get the module name

API_TOKEN = '7831748189:AAEHcnOH7ozusV_5hieBTxQQXY_VaYqMIJQ'

UPLOAD_FILE = 1
UPLOAD_MORE = 2
UPLOAD_PHOTO = 3
UPLOAD_CAPTION = 4
photo_ids=[]
captions=[]
secret=[]
approved_users=[]
name=[]
redeploy=1
# Global dictionary to store file collections
file_collections = {}
SOURCE_CHAT_ID = -1002316663794
OWNER_CHAT_ID = 7048431897
OWNER = 7048431897


# Define states for the ConversationHandler
CHECKING, STOPPED = range(2)

def back(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in approved_users:
        # Allow the message if user is approved
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
    chat_id = update.effective_chat.id
    context.user_data[chat_id] = CHECKING  # Set user data to indicate checking has started
    update.message.reply_text("Bot started! I'll check all messages for 'hi'. Use /stop to stop.")
    return CHECKING

def stop(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in approved_users:
        # Allow the message if user is approved
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
    chat_id = update.effective_chat.id
    if chat_id in context.user_data and context.user_data[chat_id] == CHECKING:
        del context.user_data[chat_id]  # Remove this chat from active checks
        update.message.reply_text("Bot stopped! You can restart it with /back.")
        return ConversationHandler.END
    else:
        update.message.reply_text("Bot is not running. Use /back to begin.")
        return ConversationHandler.END
def approve(update,context):
    user_id = update.message.from_user.id
    if user_id == OWNER:
        # Allow the message if user is approved
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not the owner")
        return
    command_parts = update.message.text.split(" ") 
    if len(command_parts) >= 2:  # You need at least 3 parts: command + word1 + word2
        u_to_ap = int(command_parts[1])
        approved_users.append(u_to_ap)
        context.bot.send_message(chat_id=update.message.chat.id, text=f"user <blockquote><a href='tg://user?id={u_to_ap}'>{u_to_ap} 🍁</a></blockquote> approved", parse_mode="html")
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="OWNER SAMA!! please provide user id to approve 🥶")

def check_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id in approved_users:
        # Allow the message if user is approved
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
    chat_id = update.effective_chat.id
    message=update.message.text
    if "$" in message:
        sp=message.split("$")
        sec=sp[0]
        ph=sp[2]
        secret.append(sec)
        photo_ids.append(ph)
        captions.append("This is a back up file")
        datas=sp[1].split(" ") 
        if sec not in file_collections:
            file_collections[sec]=[]
        for data in datas:
            file_collections[sec].append(data) 
        
        update.message.reply_text("the backup file uploaded!")

def start(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    if user_id in approved_users:
        # Allow the message if user is approved
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
    # Start the conversation by asking to upload a file
    update.message.reply_text("Send me a file to upload!")
    return UPLOAD_FILE

def upload_file(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    if user_id in approved_users:
        # Allow the message if user is approved
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
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
    user_id = update.message.from_user.id
    if user_id in approved_users:
        # Allow the message if user is approved
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
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
        update.message.reply_text(f"Photo uploaded!")
        return UPLOAD_CAPTION
    else:
        update.message.reply_text("Please send a valid photo.")
        return UPLOAD_PHOTO

def upload_caption(update: Update, context: CallbackContext) -> int:
    user_id = update.message.from_user.id
    if user_id in approved_users:
        # Allow the message if user is approved
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
    caption = update.message.text
    na=caption.split("\n") 
    name.append(na[0]) 
    captions.append(caption) 
    collection_id = context.user_data.get('collection_id')
    photo_id = context.user_data.get('photo_id')
    
    if collection_id and photo_id:
        # Get the list of file IDs
        file_ids = file_collections[collection_id]
        files="no"
        for file_id in file_ids:
            if files == "no":
                files=f" {collection_id}${file_id}"
            else:
                files=f"{files} {file_id}"
        context.bot.send_message(chat_id=-1002316663794,text=f"{files}:{photo_id}")
        bot_username = context.bot.get_me().username

        if file_ids:
            # Build the download link
            download_link = f"https://t.me/{bot_username}?start={collection_id}"

            # Send the download link with inline keyboard
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Download All Files", url=download_link)
            ]])
            context.bot.send_photo(chat_id=update.message.chat.id,photo=photo_id, caption=f"<code><b>{caption}</b></code>", reply_markup=keyboard, parse_mode="html")

            # Clear user data for the next upload
            del context.user_data['collection_id']
            del context.user_data['photo_id']
            context. bot.send_message(chat_id=update.message.chat.id,text=f"file id of this batch is “<code>{len(secret)-1}</code>”",parse_mode="html")
        else:
            update.message.reply_text("No files uploaded.")
        
        return ConversationHandler.END
    else:
        update.message.reply_text("You haven't started uploading files or haven't provided a photo.")
        return ConversationHandler.END
    
def delete_messages(context: CallbackContext):
    job = context.job
    context.bot.delete_message(chat_id=job.context['chat_id'], message_id=job.context['message_id'])

def download_files(update: Update, context: CallbackContext) -> None:
    # Extract the collection ID from the 'start' parameter
    collection_id = context.args[0] if context.args else None
    bot_username = context.bot.get_me().username
    if collection_id:
        # Retrieve the file IDs from the dictionary
        file_ids = file_collections.get(collection_id)
        
        if file_ids:
            for file_id in file_ids:
                message = context.bot.send_document(chat_id=update.effective_chat.id, document=file_id)

                # Schedule a job to delete this message after 5 minutes (300 seconds)
                context.job_queue.run_once(delete_messages, 300, context={'chat_id': update.effective_chat.id, 'message_id': message.message_id})

            update.message.reply_text("Files sent successfully!\save these files they will be automatically deletedafter 5 minutes!")
        else:
            update.message.reply_text("Invalid collection ID.")
    else:
        download_link = f"https://t.me/{bot_username}"

            # Send the download link with inline keyboard
        keyboard = InlineKeyboardMarkup([[
             InlineKeyboardButton("Download All Files", url=download_link)
            ]])
        context.bot.send_video(chat_id=update.message.chat.id,video="BAACAgUAAxkBAAMSZv7WQUHD7Jh0QB7_dgbhV9i-FDMAAo8UAAJX1PFX0MSOUfJ50g82BA",caption="""ʟᴏᴠᴇ ᴀɴɪᴍᴇ? ɪ ᴀᴍ ᴍᴀᴅᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴡᴀᴛᴄʜ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ʟᴏᴏᴋɪɴɢ ꜰᴏʀ. 

ᴄʜᴇᴄᴋ ᴏᴜᴛ ᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ ʙᴇʟᴏᴡ ꜰᴏʀ ᴍᴏʀᴇ!👇
<blockquote>𝘾𝙧𝙚𝙖𝙩𝙤𝙧 :</blockquote> @l0_Mr_unknown_0l""",reply_markup=keyboard, parse_mode="html")

def send_file(update, context) :
    user_id = update.message.from_user.id
    if user_id in approved_users:
        # Allow the message if user is approved
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
    sp=update.message.text.split(" ") 
    chat_id=int(sp[1]) 
    id=int(sp[2]) 
    try:
        bot_username = context.bot.get_me().username
        download_link = f"https://t.me/{bot_username}?start={secret[id]}"
        keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Download All Files", url=download_link)
            ]])
        context.bot.send_photo(chat_id=chat_id, photo=photo_ids[id], caption=f"<b>{captions[id]}</b>",reply_markup=keyboard,parse_mode="html") 
    except:
        update.message.reply_text(f"No files id saved as {id}")

        
def send_files(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in approved_users:
        # Allow the message if user is approved
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
    user_id = update.effective_user.id
    if str(user_id) != str(user_id) :  # Assuming user_id is a string, adjust if necessary
        update.message.reply_text("You are not authorized to access these files.")
        return

    all_file_contents = []  # List to hold contents of all files

    # Iterate through each secret
    for sec in secret:
        if sec in file_collections:
            # Iterate through each file associated with the current secret
            file_ids=file_collections[sec]
            for file_id in file_ids:
                try:
                    context.bot.send_document(chat_id=update.effective_chat.id, document=file_id)
                except Exception as e:
                    update.message.reply_text(f"Failed to read {files}: {str(e)}")
                if files == "no":
                    files=file_id
                else:
                    files=f"{files}\n\n{file_id}"
            update.message.reply_text(f"{files}")
            all_file_contents.append(files)  # Append content to the list
                
def all_files(update, context):
    if not secret:  # Check if the secret list is empty
        update.message.reply_text("No Data stored yet.")
    else:
        response = "\n".join(f"<code>{index}</code> : {item}\n{name[index]}" for index, item in enumerate(secret))
        context.bot.send_message(chat_id=update.message.chat.id,text=response,parse_mode="html")


    
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
        fallbacks=[CommandHandler('start', download_files)]
    )
    c_hand=ConversationHandler(
        entry_points=[CommandHandler('back_up', back)],
        states={
            CHECKING: [
                MessageHandler(Filters.text & ~Filters.command, check_message),
                CommandHandler('stop', stop),
            ],
        },
        fallbacks=[CommandHandler('start', download_files)],
    )
    dp.add_handler(conv_handler)
    dp.add_handler(c_hand)
    dp.add_handler(CommandHandler("start", download_files))  # Handle the 'start' command
    dp.add_handler(CommandHandler("send_all", send_files))
    dp.add_handler(CommandHandler("approve", approve)) 
    dp.add_handler(CommandHandler("all_files", all_files))
    
    dp.add_handler(CommandHandler("send", send_file))  # Handle the 'start' command


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()