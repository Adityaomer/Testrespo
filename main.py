import sqlite3
import asyncio 
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CommandHandler, CallbackContext, Application
import re
import time
import os
import shutil
import sqlite3
import asyncio 
from urllib.parse import quote_plus
from sqlalchemy import create_engine, MetaData, Table, select, insert
from sqlalchemy.exc import SQLAlchemyError

API_TOKEN = '7396022246:AAHwQozG_vH7eNjT2iPGPT_3-kW9UgyysTo'
OWNER_ID = 7048431897

WELCOME_PHOTO_URL = "https://wall.alphacoders.com/big.php?i=1351278.jpg"
GROUP_LINK = 'https://t.me/journey_groups_ok'

gym_leaders = {
    7048431897: "Steel",
    7048431897: "Flying",
    7048431897: "Bug",
    7048431897: "Fighting",
    7048431897: "Dragon",
    7048431897: "Fairy",
    7048431897: "Psychic",
    7048431897: "Ghost"
}

badges = {
    "Steel": "🔗",
    "Flying": "🛩",
    "Bug": "🦋",
    "Fighting": "🎖",
    "Dragon": "🐉",
    "Fairy": "🎀",
    "Psychic": "🔮",
    "Ghost": "☠"
}
USERS_PER_PAGE = 10

db_path = 'iota.db'  # Path to your SQLite database
backup_path = 'iota_backup.db'  # Path to save the backup

def backup_database():
    if os.path.exists(db_path):
        shutil.copy(db_path, backup_path)
        print("Database backup successful!")

def restore_database():
    if os.path.exists(backup_path):
        shutil.copy(backup_path, db_path)
        print("Database restoration successful!")
def create_tables():
    conn = sqlite3.connect('iota.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, username TEXT, approved INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS badges
                 (id INTEGER PRIMARY KEY, user_id INTEGER, badge_name TEXT, FOREIGN KEY(user_id) REFERENCES users(user_id))''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS uses (
        user_id INTEGER PRIMARY KEY
    )
''')
    conn.commit()
    conn.close()

def add_user(user_id, first_name, last_name, username):
    conn = sqlite3.connect('iota.db')
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (user_id, first_name, last_name, username) VALUES (?, ?, ?, ?)", (user_id, first_name, last_name, username))
    conn.commit()
    conn.close()

def add_badge(user_id, badge_name):
    conn = sqlite3.connect('iota.db')
    c = conn.cursor()
    c.execute("INSERT INTO badges (user_id, badge_name) VALUES (?, ?)", (user_id, badge_name))
    conn.commit()
    conn.close()
def get_all_users():
    conn = sqlite3.connect('iota.db')
    c = conn.cursor()

    # Ensure we are selecting the correct fields from the users table
    c.execute("SELECT user_id, first_name, username FROM users")
    users = c.fetchall()  # This should return a list of tuples [(user_id, first_name, username), ...]

    conn.close()
    return users
# Constants


async def users_command(update: Update, context: CallbackContext):
    # Only the owner can use this command
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_html("<b>Only the owner can view the list of users.</b>")
        return

    # Get all users from the database
    users = get_all_users()

    if not users:
        await update.message.reply_html("<b>No users found in the database.</b>")
        return

    # Get the current page number from the callback data or default to 1
    query = update.callback_query
    current_page = int(context.args[0]) if context.args else 1

    # Calculate total pages
    total_pages = (len(users) + USERS_PER_PAGE - 1) // USERS_PER_PAGE

    # Paginate the users
    start_idx = (current_page - 1) * USERS_PER_PAGE
    end_idx = start_idx + USERS_PER_PAGE
    paginated_users = users[start_idx:end_idx]

    # Generate the user list text
    user_list_text = "<b><blockquote>📋 List of Users:</blockquote></b>\n\n"
    for user in paginated_users:
        user_id, first_name, username = user
        first_name = first_name or "Unknown"
        if username:
            user_display = f"@{username}"
        else:
            user_display = f"<a href='tg://user?id={user_id}'>{first_name}</a>"
        user_list_text += f"• {user_display} <blockquote>(ID: <code>{user_id}</code>)</blockquote>\n"

    # Build the pagination buttons
    keyboard = []
    if current_page > 1:
        keyboard.append(InlineKeyboardButton("⬅️ Back", callback_data=f"users {current_page - 1}"))
    if current_page < total_pages:
        keyboard.append(InlineKeyboardButton("➡️ Next", callback_data=f"users {current_page + 1}"))

    # Send or update the message with InlineKeyboardMarkup
    reply_markup = InlineKeyboardMarkup([keyboard])

    if query:
        # If it is a callback, edit the original message
        await query.edit_message_text(user_list_text, reply_markup=reply_markup, disable_web_page_preview=True)
    else:
        # If it's the first message, send a new message
        await update.message.reply_html(user_list_text, reply_markup=reply_markup, disable_web_page_preview=True)

# Callback handler for pagination
async def handle_pagination(update: Update, context: CallbackContext):
    query = update.callback_query
    await users_command(update, context)
    await query.answer()
def get_badges(user_id):
    conn = sqlite3.connect('iota.db')
    c = conn.cursor()
    c.execute("SELECT badge_name FROM badges WHERE user_id=?", (user_id,))
    badges_list = c.fetchall()
    conn.close()
    return [badge[0] for badge in badges_list]

def get_user(user_id):
    conn = sqlite3.connect('iota.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user_data = c.fetchone()
    conn.close()
    return user_data

def approve_user(user_id):
    conn = sqlite3.connect('iota.db')
    c = conn.cursor()
    c.execute("UPDATE users SET approved=1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

def unapprove_user(user_id):
    conn = sqlite3.connect('iota.db')
    c = conn.cursor()
    c.execute("UPDATE users SET approved=0 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

create_tables()

async def give_badge(update: Update, context: CallbackContext):
    try:
        badge_name, user_id = context.args[0].capitalize(), int(context.args[1])

        if badge_name not in badges:
            await update.message.reply_html(f"<b>The badge name '{badge_name}' is not valid. Please use one of the following: {', '.join(badges.keys())}.</b>")
            return

        if update.message.from_user.id not in gym_leaders and update.message.from_user.id != OWNER_ID:
            await update.message.reply_html("<b>Only gym leaders or the owner can give badges.</b>")
            return

        if update.message.from_user.id in gym_leaders:
            gym_leader_type = gym_leaders[update.message.from_user.id]
            if badge_name == gym_leader_type:
                await update.message.reply_html(f"<b>You are a {gym_leader_type} type gym leader. You can only give {gym_leader_type} badges.</b>")
                return

        add_badge(user_id, badge_name)
        await update.message.reply_html(f"<b>Badge {badge_name} ({badges[badge_name]}) given to user {user_id}.</b>")

        badges_count = len(get_badges(user_id))
        if badges_count == 8:
            await context.bot.send_message(user_id, "<b>Congratulations! You have collected all 8 badges and are now qualified!</b>")
    except (IndexError, ValueError):
        await update.message.reply_html("<b>Usage: /give &lt;badge_name&gt; &lt;user_id&gt;</b>")

async def remove_badge_command(update: Update, context: CallbackContext):
    try:
        badge_name, user_id = context.args[0], int(context.args[1])
        conn = sqlite3.connect('iota.db')
        c = conn.cursor()
        c.execute("DELETE FROM badges WHERE user_id=? AND badge_name=?", (user_id, badge_name))
        conn.commit()
        conn.close()
        await update.message.reply_html(f"<b>Badge {badge_name} ({badges[badge_name]}) removed from user {user_id}.</b>")
    except (IndexError, ValueError):
        await update.message.reply_html("<b>Usage: /remove &lt;badge_name&gt; &lt;user_id&gt;</b>")

def get_all_user_ids():
    """Retrieve all user IDs from the database."""
    conn = sqlite3.connect('iota.db')
    c = conn.cursor()
    c.execute('SELECT user_id FROM uses')
    user_ids = [row[0] for row in c.fetchall()]
    conn.close()
    return user_ids

async def broadcast_message(update: Update, context: CallbackContext):
    """Broadcast a message to all users."""
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_html("<b>Only the owner can broadcast messages.</b>")
        return

    try:
        broadcast_text = ' '.join(context.args)
        if not broadcast_text:
            await update.message.reply_html("<b>Usage: /broadcast <message></b>")
            return

        user_ids = get_all_user_ids()
        if not user_ids:
            await update.message.reply_html("<b>No users found to broadcast.</b>")
            return

        success_count = 0
        failure_count = 0

        for user_id in user_ids:
            try:
                await context.bot.send_message(chat_id=user_id, text=broadcast_text)
                success_count += 1
                # Optional: Add a delay to handle rate limits
                await asyncio.sleep(0.5)  # Delay in seconds
            except Exception as e:
                await update.message.reply_html(f"Failed to send message to {user_id}: {e}")
                failure_count += 1

        await update.message.reply_html(f"<b>Message broadcasted to {success_count} users. {failure_count} failed.</b>")

    except Exception as e:
        await update.message.reply_html(f"<b>Error: {e}</b>")

async def send_welcome(update: Update, context: CallbackContext):
    if update.message.chat.type == "private":
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Join our Group", url=GROUP_LINK)]])
        await context.bot.send_photo(
            chat_id=update.message.chat_id, 
            photo=WELCOME_PHOTO_URL, 
            caption="<b><i><code>🎭Hello there!</code>\n<blockquote> I am iota gym bot</blockquote> \n<code>Welcome to the adventure!</code>\n \nReady to take on some epic gym challenges and test your skills?\n<blockquote>🎐 Let the games begin!</blockquote></i></b>",reply_to_message_id=update.message.message_id,
            parse_mode="html",
            reply_markup=keyboard
        )
        user_id = update.message.from_user.id
        # Insert the user ID into the database if not already present
        conn = sqlite3.connect('iota.db')
        c = conn.cursor()
        c.execute('INSERT OR IGNORE INTO uses (user_id) VALUES (?)', (user_id,))
        conn.commit()
    else:
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("start me", url="https://t.me/Iota_gym_bot?start=1")]])
        await context.bot.send_message(update.message.chat.id, "Please use this command in a private message.",reply_to_message_id=update.message.message_id,parse_mode="html",reply_markup=keyboard)

async def my_badge(update: Update, context: CallbackContext):
    current_time = time.time()
    message_time = update.message.date.timestamp()

    # Check if the message was sent within the last 60 seconds
    if current_time - message_time >= 60:
        return
    else:
        user_id = update.message.from_user.id
        # Check if the user ID exists in the database
        conn = sqlite3.connect('iota.db', check_same_thread=False)
        cursor = conn.cursor()

        # Create a table to store user IDs
        cursor.execute('SELECT user_id FROM uses WHERE user_id = ?', (user_id,))
        if cursor.fetchone() is None:
            keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("start me", url="https://t.me/Iota_gym_bot?start=1")]])
            await context.bot.send_message(update.message.chat.id, "Please use this command in a private message.",parse_mode="html",reply_to_message_id=update.message.message_id, reply_markup=keyboard)
            return

        user_data = get_user(user_id)
        if not user_data:
            add_user(user_id, update.message.from_user.first_name, update.message.from_user.last_name, update.message.from_user.username)

        badges_list = get_badges(user_id)
        if not badges_list:
            await update.message.reply_text("<blockquote><code>🎐𝘏𝘦𝘳𝘦 𝘪𝘴 𝘺𝘰𝘶𝘳 𝘣𝘢𝘥𝘨𝘦 𝘤𝘢𝘴𝘦🎐\n</code></blockquote><b><code>╔═════════════════╗  \n╠●NO BADGES EARNED YET !!</code></b>\n╚═════════════════╝\n<blockquote>——🔘—— You can do it! </blockquote>",reply_to_message_id=update.message.message_id,parse_mode="html")
        else:
            badge_display = "\n╠●".join([f"{badges[badge]} {badge}" for badge in badges_list])
            await update.message.reply_text(
    reply_to_message_id=update.message.message_id,text=f"<blockquote><code>🎐𝘏𝘦𝘳𝘦 𝘪𝘴 𝘺𝘰𝘶𝘳 𝘣𝘢𝘥𝘨𝘦 𝘤𝘢𝘴𝘦🎐\n</code></blockquote><b><code>╔═════════════════╗  \n╠●{badge_display}</code></b>\n╚═════════════════╝\n<blockquote>——🔘—— You can do it! </blockquote>",parse_mode ="html"
)

async def backup_command(update: Update, context: CallbackContext):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("<b>Only the owner can perform a backup.</b>", parse_mode="html")
        return

    try:
        backup_database()
        await update.message.reply_text("<b>Database backup successful!</b>", parse_mode="html")
    except Exception as e:
        await update.message.reply_text(f"<b>Error during backup: {e}</b>", parse_mode="html")

async def restore_command(update: Update, context: CallbackContext):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("<b>Only the owner can perform a restore.</b>", parse_mode="html")
        return

    try:
        restore_database()
        await update.message.reply_text("<b>Database restored successfully!</b>", parse_mode="html")
    except Exception as e:
        await update.message.reply_text(f"<b>Error during restore: {e}</b>", parse_mode="html")

async def clear_database_command(update: Update, context: CallbackContext):
    if update.message.from_user.id == OWNER_ID:
        clear_database()
        await update.message.reply_html("<b>Database cleared successfully.</b>")
    else:
        await update.message.reply_html("<b>Only the owner can clear the database.</b>")

async def approve_command(update: Update, context: CallbackContext):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text(reply_to_message_id=update.message.message_id,text="<b>Only the owner can approve users.</b>",parse_mode="html")
        return

    try:
        user_id = int(context.args[0])
        if get_user(user_id) is None:
            await update.message.reply_text(reply_to_message_id=update.message.message_id,text="<b>User not found.</b>",parse_mode="html")
            return
        approve_user(user_id)
        await update.message.reply_text(reply_to_message_id=update.message.message_id,text=f"<b>User {user_id} has been approved.</b>",parse_mode="html")
    except (IndexError, ValueError):
        await update.message.reply_text("<b>Usage: /approve &lt;user_id&gt;</b>",reply_to_message_id=update.message.message_id,parse_mode="html")

async def unapprove_command(update: Update, context: CallbackContext):
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text(reply_to_message_id=update.message.message_id,text="<b>Only the owner can unapprove users.</b>",parse_mode="html")
        return

    try:
        user_id = int(context.args[0])
        if get_user(user_id) is None:
            await update.message.reply_text(reply_to_message_id=update.message.message_id,text="<b>User not found.</b>",parse_mode="html")
            return
        unapprove_user(user_id)
        await update.message.reply_text(reply_to_message_id=update.message.message_id,text=f"<b>User {user_id} has been unapproved.</b>")
    except (IndexError, ValueError):
        await update.message.reply_text(reply_to_message_id=update.message.message_id,text="<b>Usage: /unapprove &lt;user_id&gt;</b>",parse_mode="html")

def get_all_users_and_badges():
    conn = sqlite3.connect('iota.db')
    c = conn.cursor()
    c.execute('''
        SELECT u.user_id, u.username, u.first_name, COUNT(b.badge_name) as badge_count
        FROM users u
        LEFT JOIN badges b ON u.user_id = b.user_id
        GROUP BY u.user_id, u.username, u.first_name
        ORDER BY badge_count DESC, u.username ASC, u.first_name ASC
    ''')
    users_badges = c.fetchall()
    conn.close()
    return users_badges
def sanitize_name(name):
    # Replace any non-alphanumeric characters with an empty string
    return re.sub(r'\W+', '', name)
async def backup_command(update: Update, context: CallbackContext):
    OWNER_ID = 7048431897  # Ensure this matches your OWNER_ID
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("<b>Only the owner can perform a backup.</b>", parse_mode="html")
        return

    try:
        # Define CockroachDB connection parameters
        cluster_id = '390aab70-1739-403d-aa1e-c7c19ed76107'
        username = "testing"
        password = "bqWrQ1YIyJvWbt_KtSPdGQ"
        database = "Testgit"

        # Download the SSL root certificate
        cert_path = os.path.expanduser("~/.postgresql/root.crt")
        if not os.path.exists(cert_path):
            os.system(f"curl --create-dirs -o {cert_path} 'https://cockroachlabs.cloud/clusters/{cluster_id}/cert'")

        # Set environment variable for the root certificate path
        os.environ["ROOT_CERT_PATH"] = cert_path

        # Encode the password for the DATABASE_URL
        encoded_password = quote_plus(password)
        DATABASE_URL = f"postgresql://{username}:{encoded_password}@sienna-sphinx-6116.7s5.aws-ap-south-1.cockroachlabs.cloud:26257/{database}?sslmode=verify-full"

        # Create SQLAlchemy engine for CockroachDB
        engine = create_engine(DATABASE_URL)
        metadata = MetaData()

        # Reflect existing tables or define them
        users = Table('users', metadata, autoload_with=engine)
        badges = Table('badges', metadata, autoload_with=engine)
        uses = Table('uses', metadata, autoload_with=engine)

        # Connect to CockroachDB
        with engine.connect() as cockroach_conn:
            trans = cockroach_conn.begin()
            try:
                # Connect to SQLite3
                sqlite_conn = sqlite3.connect('iota.db')
                sqlite_cursor = sqlite_conn.cursor()

                # Backup 'users' table
                sqlite_cursor.execute("SELECT * FROM users")
                users_data = sqlite_cursor.fetchall()
                cockroach_conn.execute(users.delete())  # Clear existing data
                cockroach_conn.execute(users.insert(), [
                    {
                        'user_id': row[0],
                        'first_name': row[1],
                        'last_name': row[2],
                        'username': row[3],
                        'approved': row[4]
                    } for row in users_data
                ])

                # Backup 'badges' table
                sqlite_cursor.execute("SELECT * FROM badges")
                badges_data = sqlite_cursor.fetchall()
                cockroach_conn.execute(badges.delete())  # Clear existing data
                cockroach_conn.execute(badges.insert(), [
                    {
                        'id': row[0],
                        'user_id': row[1],
                        'badge_name': row[2]
                    } for row in badges_data
                ])

                # Backup 'uses' table
                sqlite_cursor.execute("SELECT * FROM uses")
                uses_data = sqlite_cursor.fetchall()
                cockroach_conn.execute(uses.delete())  # Clear existing data
                cockroach_conn.execute(uses.insert(), [
                    {
                        'user_id': row[0]
                    } for row in uses_data
                ])

                # Commit the transaction
                trans.commit()
                sqlite_conn.close()
                await update.message.reply_text("<b>Database backup to CockroachDB successful!</b>", parse_mode="html")
            except Exception as e:
                trans.rollback()
                sqlite_conn.close()
                await update.message.reply_text(f"<b>Error during backup: {e}</b>", parse_mode="html")
            finally:
                engine.dispose()
    except SQLAlchemyError as e:
        await update.message.reply_text(f"<b>Database connection error: {e}</b>", parse_mode="html")
    except Exception as e:
        await update.message.reply_text(f"<b>Unexpected error: {e}</b>", parse_mode="html")

async def restore_command(update: Update, context: CallbackContext):
    OWNER_ID = 7048431897  # Ensure this matches your OWNER_ID
    if update.message.from_user.id != OWNER_ID:
        await update.message.reply_text("<b>Only the owner can perform a restore.</b>", parse_mode="html")
        return

    try:
        # Define CockroachDB connection parameters
        cluster_id = '390aab70-1739-403d-aa1e-c7c19ed76107'
        username = "testing"
        password = "bqWrQ1YIyJvWbt_KtSPdGQ"
        database = "Testgit"

        # Download the SSL root certificate
        cert_path = os.path.expanduser("~/.postgresql/root.crt")
        if not os.path.exists(cert_path):
            os.system(f"curl --create-dirs -o {cert_path} 'https://cockroachlabs.cloud/clusters/{cluster_id}/cert'")

        # Set environment variable for the root certificate path
        os.environ["ROOT_CERT_PATH"] = cert_path

        # Encode the password for the DATABASE_URL
        encoded_password = quote_plus(password)
        DATABASE_URL = f"postgresql://{username}:{encoded_password}@sienna-sphinx-6116.7s5.aws-ap-south-1.cockroachlabs.cloud:26257/{database}?sslmode=verify-full"

        # Create SQLAlchemy engine for CockroachDB
        engine = create_engine(DATABASE_URL)
        metadata = MetaData()

        # Reflect existing tables or define them
        users = Table('users', metadata, autoload_with=engine)
        badges = Table('badges', metadata, autoload_with=engine)
        uses = Table('uses', metadata, autoload_with=engine)

        # Connect to CockroachDB
        with engine.connect() as cockroach_conn:
            trans = cockroach_conn.begin()
            try:
                # Fetch data from CockroachDB

                # Restore 'users' table
                users_query = select([users])
                users_result = cockroach_conn.execute(users_query).fetchall()

                # Restore 'badges' table
                badges_query = select([badges])
                badges_result = cockroach_conn.execute(badges_query).fetchall()

                # Restore 'uses' table
                uses_query = select([uses])
                uses_result = cockroach_conn.execute(uses_query).fetchall()

                # Connect to SQLite3
                sqlite_conn = sqlite3.connect('iota.db')
                sqlite_cursor = sqlite_conn.cursor()

                # Clear existing data
                sqlite_cursor.execute("DELETE FROM users")
                sqlite_cursor.execute("DELETE FROM badges")
                sqlite_cursor.execute("DELETE FROM uses")

                # Insert data into 'users' table
                sqlite_cursor.executemany(
                    "INSERT INTO users (user_id, first_name, last_name, username, approved) VALUES (?, ?, ?, ?, ?)",
                    users_result
                )

                # Insert data into 'badges' table
                sqlite_cursor.executemany(
                    "INSERT INTO badges (id, user_id, badge_name) VALUES (?, ?, ?)",
                    badges_result
                )

                # Insert data into 'uses' table
                sqlite_cursor.executemany(
                    "INSERT INTO uses (user_id) VALUES (?)",
                    uses_result
                )

                # Commit the changes
                sqlite_conn.commit()
                sqlite_conn.close()

                # Commit the transaction in CockroachDB
                trans.commit()
                await update.message.reply_text("<b>Database restored from CockroachDB successfully!</b>", parse_mode="html")
            except Exception as e:
                trans.rollback()
                sqlite_conn.close()
                await update.message.reply_text(f"<b>Error during restore: {e}</b>", parse_mode="html")
            finally:
                engine.dispose()
    except SQLAlchemyError as e:
        await update.message.reply_text(f"<b>Database connection error: {e}</b>", parse_mode="html")
    except Exception as e:
        await update.message.reply_text(f"<b>Unexpected error: {e}</b>", parse_mode="html")

async def leaderboard_command(update: Update, context: CallbackContext):
    users_badges = get_all_users_and_badges()

    if not users_badges:
        await update.message.reply_text(reply_to_message_id=update.message.message_id,text="<b>No users or badges found.</b>",parse_mode="html")
        return

    leaderboard_text = "<b><i><code>     🏆 𝐿𝐸𝐴𝐷𝐵𝑂𝐴𝑅𝐷 🏆</code></i></b>\n\n"

    for i, (user_id, username, first_name, badge_count) in enumerate(users_badges):
        if i >= 10:
            break
        # Sanitize the first name
        sanitized_first_name = sanitize_name(first_name)
        display_name = f"@{username}" if username else sanitized_first_name
        leaderboard_text += f"<code><blockquote><b>{display_name:<20} : {badge_count:2} badges\n</b></blockquote></code>"

    await update.message.reply_text(reply_to_message_id=update.message.message_id,text=leaderboard_text,parse_mode="html")

# ... (rest of your code remains unchanged)

def main():
    application = Application.builder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("add", give_badge))
    application.add_handler(CommandHandler("remove", remove_badge_command))
    application.add_handler(CommandHandler("approve", approve_command))
    application.add_handler(CommandHandler("unapprove", unapprove_command))
    application.add_handler(CommandHandler("badgecase", my_badge))
    application.add_handler(CommandHandler("start", send_welcome))
    application.add_handler(CommandHandler("clear_database", clear_database_command))
    application.add_handler(CommandHandler("leadboard", leaderboard_command))

    application.add_handler(CommandHandler("broadcast", broadcast_message))
    application.add_handler(CommandHandler("leaderboard", leaderboard_command))
    application.add_handler(CommandHandler("users", users_command))
    application.add_handler(CommandHandler("backup", backup_command))
    application.add_handler(CommandHandler("restore", restore_command))

    application.run_polling()

if __name__ == '__main__':
    main()