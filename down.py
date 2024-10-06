import secrets
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackContext
import logging
import time

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)  # Use __name__ to get the module name

API_TOKEN = '7643255671:AAFDUAy9VWeYP-EeGIhv8CUuRBSy4ZzVvxk'

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
user_list=[]
BROADCAST_MESSAGE = 1
FORWARD_MESSAGE=1
CHECKING, STOPPED = range(2)
def send_long_message(bot, chat_id, text):
    max_length = 4096 # Telegram's max message length
    parts = [text[i:i + max_length] for i in range(0, len(text), max_length)]

    for part in parts:
        bot.send_message(chat_id=chat_id, text=part, parse_mode="html")

def users(update, context):
    user_id = update.message.from_user.id
    if user_id in approved_users:
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
      
    users=[]
    for user in user_list:
        users.append(f"{user}")
    usersl = ",".join(users) 
    users.clear()
  

  # Check if the message is long and send it accordingly
    if len(usersl) > 4096:
        send_long_message(context.bot, update.message.chat.id, usersl)
    else:
    
        context.bot.send_message(chat_id=update.message.chat.id, text=usersl)

def broadcast(update, context):
    user_id = update.message.from_user.id
    if user_id in approved_users:
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter the message you want to broadcast:")
    return BROADCAST_MESSAGE



def broadcast_message(update, context):
  message = update.message
  message_id = message.message_id

  for user_id in user_list:
    try:
      # Check message type and forward accordingly
      if message.photo: # If photo
        context.bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id,caption=message.caption)
      elif message.text: # If text
        context.bot.send_message(chat_id=user_id, text=message.text)
      elif message.video or message.audio: # If video or audio
        if message.video:
          context.bot.send_video(chat_id=user_id, video=message.video.file_id,caption=message.caption)
        else: # If audio
          context.bot.send_audio(chat_id=user_id, audio=message.audio.file_id)
      else:
        print(f"Unsupported message type for user {user_id}")

    except Exception as e:
      print(f"Error sending message to {user_id}: {e}")

  context.bot.send_message(chat_id=update.effective_chat.id, text="Broadcast complete!")
  return ConversationHandler.END
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
    elif user_id == 1381668733:
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
        if sec not in secret:
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
        update.message.reply_text(f"Photo uploaded! Now sendCaption")
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
                if len(files) <= 2000:
                    files=f"{files} {file_id}"
                else:
                     context.bot.send_message(chat_id=-1002316663794,text=f"{files}${photo_id}")
                     files="no"
        context.bot.send_message(chat_id=-1002316663794,text=f"{files}${photo_id}")
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
    user_id=update.message.from_user.id 
    if user_id != update.message.chat.id:
        context.bot.send_message(chat_id=update.message.chat.id,text="𝑇ℎ𝑖𝑠 𝑐𝑜𝑚𝑚𝑎𝑛𝑑 𝑐𝑎𝑛 𝑜𝑛𝑙𝑦 𝑏𝑒 𝑢𝑠𝑒𝑑 𝑖𝑛 𝑑𝑚")
        return ConversationHandler.END
    if user_id not in user_list:
        user_list.append(user_id)
    user=update.message.from_user
    channels = ['@Asia_Anime_community','@Anime_Asia_Community']
    for channel_username in channels:
        try:
    # Get the chat object for the channel
            chat = context.bot.get_chat(channel_username)

    # Check if the user is a member of the channel
            member = context.bot.get_chat_member(chat_id=chat.id, user_id=user.id)

    # If the user is not a member, exit the function
            if member.status not in ['member', 'creator', 'administrator']:
                download_link = f"https://t.me/Anime_Asia_Community"
                download_linker = f"https://t.me/Asia_Anime_Community"

            # Send the download link with inline keyboard
                keyboard = InlineKeyboardMarkup([[
                     InlineKeyboardButton("Channel link", url=download_link), InlineKeyboardButton("Group link", url=download_linker)
            ]])
                context.bot.send_video(chat_id=update.message.chat.id,video="BAACAgUAAxkBAAMSZwABG5xVX1zbpEEBMwtXSF8QlLzfAAKPFAACV9TxV2Uiq1_IcQbqNgQ",caption="""ɪ Aᴍ Hᴇʀᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴡᴀᴛᴄʜ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ʟᴏᴏᴋɪɴɢ ꜰᴏʀ.∆ 

Bᴜᴛ Yᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ʏᴇᴛ sᴏ
JOIN OUR CHANNEL FIRST
<blockquote>𝘾𝙧𝙚𝙖𝙩𝙤𝙧 :</blockquote> @l0_Mr_unknown_0l""",reply_markup=keyboard, parse_mode="html")
                return

        except Exception as e:
            update.message.reply_text(f"Error checking channel membership: {e}")
            return
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
        download_link = f"https://t.me/Anime_Asia_Community"

            # Send the download link with inline keyboard
        keyboard = InlineKeyboardMarkup([[
             InlineKeyboardButton("Channel link", url=download_link)
            ]])
        context.bot.send_video(chat_id=update.message.chat.id,video="BAACAgUAAxkBAAMSZwABG5xVX1zbpEEBMwtXSF8QlLzfAAKPFAACV9TxV2Uiq1_IcQbqNgQ",caption="""ʟᴏᴠᴇ ᴀɴɪᴍᴇ? ɪ ᴀᴍ ᴍᴀᴅᴇ ᴛᴏ ʜᴇʟᴘ ʏᴏᴜ ᴡᴀᴛᴄʜ ᴡʜᴀᴛ ʏᴏᴜ'ʀᴇ ʟᴏᴏᴋɪɴɢ ꜰᴏʀ. 

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
    if not context.args:  # Check if no arguments are provided
        update.message.reply_text("Please provide an argument. Example: /send <chat_id> <file_id>")
        return
    try:
        sp=update.message.text.split(" ") 
        chat_id=int(sp[1])
    except:
        update.message.reply_text("The above provided argument <chat_id> is not valid")
        return
    try:
        id=int(sp[2]) 
    except:
        update.message.reply_text("The above provided argument <file_id> is not valid")
        return
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
    user_id = update.message.from_user.id
    if user_id == OWNER:
        # Allow the message if user is approved
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not the owner")
        return
    if not secret:  # Check if the secret list is empty
        update.message.reply_text("No Data stored yet.")
    else:
        response = "\n".join(
    f"<code>{index}</code> : {item}\n{name[index] if index < len(name) else 'User'}" for index, item in enumerate(secret) )
    if len(response) > 4096:
        send_long_message(context.bot, update.message.chat.id, response)
    else:
        context.bot.send_message(chat_id=update.message.chat.id,text=response,parse_mode="html")
def forward(update, context):
    user_id = update.message.from_user.id
    if user_id in approved_users:
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter the message you want to broadcast:")
    return BROADCAST_MESSAGE
def add_users(update,context):
   
    user_id = update.message.from_user.id
    if user_id in approved_users:
        # Allow the message if user is approved
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return 
    message_text=update.message.text
    data=message_text.split(" ")
    usersp=data[1]
    usersq=usersp.split(",")
    for user in usersq:
        user_list.append(int(user))

def forward_message(update, context):
    message = update.message
    message_id=message.message_id
    for user_id in user_list:
        try:
            context.bot.forward_message(chat_id=user_id,from_chat_id=update.message.chat_id,message_id=message_id)
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Broadcast complete!")
    return ConversationHandler.END
    
def add_caption(update, context):
    user_id = update.message.from_user.id
    if user_id in approved_users:
        # Allow the message if user is approved
        pass
    else:
        update.message.reply_text("Not a admin get the f**k off")
        return 

    message = update.message
    text = message.text
    if ":" not in text:
        update.message.reply_text("Wrong format \n format: /add_caption:<caption>:<file_id>")
        return
    sp = text.split(":")
    if len(sp) < 3:
        update.message.reply_text("Not enough argument \n format: /add_caption:<caption>:<file_id>")
        return
    cap = sp[1]
    try:
        id = int(sp[2])
        captions[id]= cap
        context.bot.send_message(chat_id=update.message.chat.id, text=f"File ID: {id}\nCaption: {cap}")
    except Exception as e:
        update.message.reply_text(f"file_id invalid: {sp[2]} \n {e}")

     
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
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("broadcast", broadcast)],
        states={
            BROADCAST_MESSAGE: [
                MessageHandler(Filters.text & ~Filters.command, broadcast_message), # Handle text separately
                MessageHandler(Filters.photo, broadcast_message),
                MessageHandler(Filters.video, broadcast_message),
                MessageHandler(Filters.audio, broadcast_message),
               ],
           },
           fallbacks=[CommandHandler("cancel", download_files)],
     )

    conn = ConversationHandler(
        entry_points=[CommandHandler("forward", forward)],
        states={
            FORWARD_MESSAGE: [
                MessageHandler(Filters.text & ~Filters.command, forward_message), # Handle text separately
                MessageHandler(Filters.photo, forward_message),
                MessageHandler(Filters.video, forward_message),
                MessageHandler(Filters.audio, forward_message),
               ],
           },
           fallbacks=[CommandHandler("cancel", download_files)],
     ) 
    dp.add_handler(conversation_handler)
    dp.add_handler(conn)
    dp.add_handler(conv_handler)
    dp.add_handler(c_hand)
    dp.add_handler(CommandHandler("start", download_files))  # Handle the 'start' command
    dp.add_handler(CommandHandler("send_all", send_files))
    dp.add_handler(CommandHandler("approve", approve)) 
    dp.add_handler(CommandHandler("all_files", all_files))
    
    dp.add_handler(CommandHandler("users", users))

    dp.add_handler(CommandHandler("add_users", add_users))
    dp.add_handler(CommandHandler("add_caption", add_caption))
    dp.add_handler(CommandHandler("send", send_file))  # Handle the 'start' command


    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()