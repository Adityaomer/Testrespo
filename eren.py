from telethon import TelegramClient, events
from pymongo import MongoClient
import random
import asyncio
from telethon.tl.types import InputMediaDice
from telethon.tl.custom import Button
from datetime import datetime, timedelta
import uuid 
from telethon.errors import  FloodWaitError
from telethon.tl.custom import Button
from telethon.tl.types import User as TelegramUser 
from datetime import datetime, timedelta
from keep_alive import keep_alive, start_requesting


def check_suspension(func):
    async def wrapper(event):
        print(f"[DEBUG] Entering check_suspension for user {event.sender_id}")
        user_id = event.sender_id
        chat_id = event.chat_id
        user = users.find_one({"_id": user_id})

        if user and user.get('is_banned'):
            print(f"[DEBUG] User {user_id} is banned.")
            await client.send_message(chat_id, "🚫 Your account has been permanently banned. You cannot use bot commands.")
            return

        if user and user.get('suspended_until') and user['suspended_until'] > datetime.now():
            time_left = user['suspended_until'] - datetime.now()
            minutes, seconds = divmod(time_left.seconds, 60)
            print(f"[DEBUG] User {user_id} is suspended for {minutes}m {seconds}s.")
            await client.send_message(chat_id, f"🚫 Your account is suspended. You can use bot commands again in {minutes}m {seconds}s.")
            return
        print(f"[DEBUG] check_suspension passing control to {func.__name__}")
        await func(event)
        print(f"[DEBUG] Exiting check_suspension for user {event.sender_id}")
    return wrapper

def handle_flood_control(func):
    async def wrapper(event):
        print(f"[DEBUG] Entering handle_flood_control for command {func.__name__}")
        chat_id = event.chat_id
        try:
            await func(event)
            print(f"[DEBUG] handle_flood_control successfully executed {func.__name__}")
        except FloodWaitError as e:
            print(f"[DEBUG] FloodWaitError in {func.__name__}: Sleeping for {e.seconds} seconds")
            try:
                await client.send_message(chat_id, f"⏳ Too many requests! Please wait {e.seconds} seconds before trying again.")
            except Exception as reply_err:
                print(f"[DEBUG] Failed to send flood wait message to user: {reply_err}")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"[DEBUG] An unexpected error occurred in {func.__name__}: {e}")
            try:
                await client.send_message(chat_id, f"An unexpected error occurred: {e}")
            except Exception as reply_err:
                print(f"[DEBUG] Failed to send error message to user: {reply_err}")
        print(f"[DEBUG] Exiting handle_flood_control for command {func.__name__}")
    return wrapper


API_ID= '23734455'
API_HASH = '40972650709e0e2b0aa58734f3524261'
BOT_TOKEN = '7347127289:AAFW1Ihrr2jEM-ygdZK_vbbOwyWT2tzqoF8'
MONGO_URI = 'mongodb+srv://souradeepmandal35:bFEAKgXFjg8TKMr5@cluster0.njm46bj.mongodb.net/'
client = TelegramClient('@Eren_Yeagerrobot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)


db = MongoClient(MONGO_URI)['shinobixs']
users = db["users"]
groups_collection = db['groups']
characters_db = db["characterss"]
bank_vault = db["bank_vault"]
chat_message_counts_db = db["chat_message_counts"]
bot_settings = db["bot_settings"]
fishing_items_db = db["fishing_items"]
scouting_items_db = db["scouting_items"]
user_spam_counts_db = db["user_spam_counts"]

JOIN_BONUS = 20000
ADMIN_ID = 1381668733 
UPLOAD_LOG_CHANNEL_ID = -1002889135530 
VAULT_CAPACITY = 50000000 
VAULT_UPGRADE_AMOUNT = 1000000 
MAX_VAULT_CAPACITY = 1000000000 
VAULT_UPGRADE_COST = 10000 
VAULT_UPGRADE_LEVEL_REQUIREMENT = 10 
DAILY_BONUS = 1000 
ROB_PERCENTAGE = 0.50 
ROB_SUCCESS_CHANCE = 0.5 
ROB_PENALTY_PERCENTAGE = 0.10 
ROB_COOLDOWN_HOURS = 0.1 
BANKROB_USER_COOLDOWN_HOURS = 1.0
BANKROB_COOLDOWN_HOURS = 5.0 
FISH_COOLDOWN_MINUTES = 5 
MAX_ROD_DURABILITY = 10 
MAX_SCOUT_DURABILITY = 10 
WEEKLY_BONUS = 7500 
MONTHLY_BONUS = 30000
WEEKLY_COOLDOWN_DAYS = 7
MONTHLY_COOLDOWN_DAYS = 30
MAX_BALANCE_LIMIT = 1479452374976123674

LEVEL_UP_IMAGE_URL = "https://graph.org/file/d432f73e2ba634a3368db-cdc7d2aa0d62a71024.jpg" 
LEVEL_DOWN_IMAGE_URL = "https://graph.org/file/edc70c9df9136a4e7a0e9-55086d546732f9c7cc.jpg" 
TOP_USERS_IMAGE_URL = "https://graph.org/file/1466f1d4113b8a851d306-40685c5a74554f98e1.jpg" 
TOP_GROUPS_IMAGE_URL = "https://graph.org/file/0e5532cbaa7662ab89348-f5f3a38d66ffcac94d.jpg"
CTOP_USERS_IMAGE_URL  = "https://graph.org/file/55b042f10f0c860a62ea6-a9ac00c2a219df1766.jpg" 


SPAM_MESSAGE_THRESHOLD = 10
SPAM_TIME_WINDOW_SECONDS = 60
SPAM_SUSPENSION_DURATION_SECONDS = 300
BANK_ROB_SUCCESS_CHANCE = 0.20 
BANK_ROB_PERCENTAGE = 0.10 
BANK_ROB_PENALTY_PERCENTAGE = 0.15 
BANK_ROB_GLOBAL_COOLDOWN_MINUTES = 2345 
BANK_STARTING_BALANCE = 1000000 
CHARACTER_SUMMON_COST = 5000 
DROP_MESSAGE_THRESHOLD = 50
DROP_COOLDOWN_MINUTES = 4 
SLOT_ANIMATION_COOLDOWN = 4 
SCOUT_COOLDOWN_MINUTES = 5 
active_bluffmaster_games = {}

SCOUT_PRICES = {
    "Common Rock": 50,
    "Uncommon Branch": 150,
    "Rare Gem": 500,
    "Epic Relic": 2000,
    "Legendary Artifact": 10000,
    "Junk Twig": 5,
    "Common Leaf": 60,
    "Uncommon Stone": 180,
    "Rare Fossil": 700,
    "Epic Map": 2500,
    "Legendary Compass": 12000,
    "Junk Pebble": 10,
    "ODM Gear": 1000,
    "Titan Serum": 5000,
    "Scout Supplies": 500,
    "Eren Jaeger (Shifter)": 10000,
    "Colossal Titan": 8000,
    "Survey Map": 200,
    "Mikasa's Scarf": 3000,
    "Sasha's Potato": 50,
    "Thunder Spear": 2500,
    "Beast Titan Hair": 4000,
    "Armored Titan Plate": 3500,
    "Founding Titan Key": 9000,
    "Levi's Blade": 4500,
    "Hange's Goggles": 1200,
    "Titan Injection Syringe": 6000,
    "Marleyan Gold": 2000,
    "Garrison Badge": 800,
    "Survey Corps Cloak": 1500,
    "Annie's Ring": 3500,
    "Titan Crystal Fragment": 3000,
    "Sasha's Bow": 1000,
    "Jean's Mane": 400,
    "Connie's Hat": 300,
    "Reiner's Helmet": 2000,
    "Bertholdt's Shoes": 250,
    "Falco's Feather": 900,
    "Pieck's Cart": 2200,
    "Zeke's Glasses": 3200,
    "Historia's Crown": 7000,
    "Ymir's Journal": 5000,
    "Grisha's Notebook": 4000,
    "Wall Rose Brick": 100,
    "Wall Maria Dust": 80,
    "Hitch's Cat": 600,
    "Moblit's Sketch": 1100,
    "Marco's Badge": 1300,
    "Gunther's Bandana": 400,
    "Petra's Pin": 900,
    "Oluo's Teeth": 150,
    "Hannes' Flask": 700,
    "Krista's Letter": 1700,
    "Flegel's Pass": 600,
    "Wall Sina Seal": 120,
    "Marleyan Radio": 2100,
    "Cart Titan Gear": 2600,
    "Jaw Titan Claw": 4800,
    "War Hammer Crystal": 9500,
    "Paradis Island Flower": 300,
    "Sasha's Hidden Meat": 2000,
    "Armin's Book": 1800,
    "Annie's Crystal": 7000,
    "Founding Titan Spine": 12000,
}

FISH_PRICES = {
    "Small Fry": 100,
    "River Perch": 150,
    "Lake Trout": 300,
    "Catfish": 400,
    "Golden Carp": 1000,
    "Electric Eel": 1200,
    "Mysterious Crate": 3000,
    "Sunken Treasure": 10000,
    "Old Boot": 10,
    "Rusty Can": 5,
    "Rainbow Trout": 350,
    "Deep Sea Monster": 5000,
    "Ancient Relic": 7500,
    "Mermaid's Tear": 15000,
    "Mudskipper": 80,
    "Dace": 120,
    "Minnow": 70,
    "Pike": 320,
    "Sturgeon": 450,
    "Walleye": 380,
    "Arowana": 1500,
    "Mahi-Mahi": 1800,
    "Bluefin Tuna": 2000,
    "Dragon Scale": 4000,
    "Kraken Ink": 4500,
    "Triton's Trident": 20000,
    "Lost Atlantis Map": 25000,
    "Tangled Net": 15,
    "Broken Compass": 20,
    "Perch": 110,
    "Carp": 130,
    "Salmon": 370,
    "Trout": 330,
    "Swordfish": 2200,
    "Marlin": 2500,
    "Pearl Necklace": 5000,
    "Enchanted Shell": 5500,
    "Poseidon's Crown": 30000,
    "Algae": 2,
    "Goby": 90,
    "Bass": 280,
    "Giant Squid": 3000,
    "Coral Fragment": 6000,
    "Lost Pirate Ship": 40000,
    "Water Logged Wood": 8,
    "Tilapia": 140,
    "Cod": 420,
    "Kraken Spawn": 7000,
    "Seaweed Wrap": 6500,
    "Abyssal Pearl": 50000,
    "Plastic Bottle": 3
}

async def get_random_character_from_db(is_raredrop_only=False, desired_rarity=None):
    query = {}
    if is_raredrop_only:
        query = {"is_raredrop_only": True}
    elif desired_rarity:
        query = {"rarity": desired_rarity}
    else:
        
        query = {"$or": [{"is_raredrop_only": False}, {"is_raredrop_only": {"$exists": False}}]}
    all_characters = list(characters_db.find(query))
    if not all_characters:
        return None 
    total_weight = sum(char["weight"] for char in all_characters)
    if total_weight == 0:
        return random.choice(all_characters) 

    rand = random.uniform(0, total_weight)
    cumulative_weight = 0
    for char in all_characters:
        cumulative_weight += char["weight"]
        if rand < cumulative_weight:
            return char


async def handle_referral_reward(referrer_id, new_user_id):
    referrer_user = users.find_one({"_id": referrer_id})
    new_user_entity = await client.get_entity(new_user_id)
    new_user_name = new_user_entity.first_name if new_user_entity else "a new user"

    if not referrer_user:
        print(f"Referrer {referrer_id} not found when trying to give reward.")
        return

    users.update_one({"_id": referrer_id}, {"$inc": {"referrals_count": 1}})
    referrer_user = users.find_one({"_id": referrer_id})
    current_referrals = referrer_user["referrals_count"]
    total_reward_amount = 0
    total_kryon_reward = 0
    character_reward_name = None
    reward_details = []
    base_coin_reward = 10000
    total_reward_amount += base_coin_reward
    reward_details.append(f"₹{base_coin_reward:,} coins (base reward)")

    if current_referrals % 4 == 0:
        total_reward_amount += 20000
        total_kryon_reward += 1
        reward_details.append(f"₹20,000 coins and Ꝿ1 Kryon (4-invite milestone)")

    if current_referrals % 10 == 0:
        total_reward_amount += 50000
        total_kryon_reward += 2
        reward_details.append(f"₹50,000 coins and Ꝿ2 Kryon (10-invite milestone)")

    if current_referrals % 16 == 0:
        total_reward_amount += 75000
        random_character = await get_random_character_from_db(is_raredrop_only=False)
        if random_character:
            users.update_one(
                {"_id": referrer_id},
                {"$push": {"characters": random_character}},
                upsert=True
            )
            character_reward_name = random_character['name']
            reward_details.append(f"₹75,000 coins and a random character: {random_character['name']} ({random_character['rarity']}) (16-invite milestone)")
        else:
            reward_details.append(f"₹75,000 coins (16-invite milestone, no random character available)")

    if current_referrals % 26 == 0:
        total_reward_amount += 85000
        total_kryon_reward += 2
        special_character = await get_random_character_from_db(desired_rarity="Special")
        if special_character:
            users.update_one(
                {"_id": referrer_id},
                {"$push": {"characters": special_character}},
                upsert=True
            )
            character_reward_name = special_character['name']
            reward_details.append(f"₹85,000 coins, Ꝿ2 Kryon, and a Special character: {special_character['name']} (26-invite milestone)")
        else:
            reward_details.append(f"₹85,000 coins and Ꝿ2 Kryon (26-invite milestone, no Special character available)")

    if current_referrals % 40 == 0:
        total_reward_amount += 100000
        total_kryon_reward += 10
        reward_details.append(f"₹100,000 coins and Ꝿ10 Kryon (40-invite milestone)")

    if current_referrals % 50 == 0:
        total_reward_amount += 100000
        total_kryon_reward += 100
        reward_details.append(f"₹100,000 coins and Ꝿ100 Kryon (50-invite milestone)")

    if total_reward_amount > 0:
        current_balance = referrer_user.get('balance', 0)
        new_balance = min(current_balance + total_reward_amount, MAX_BALANCE_LIMIT)
        users.update_one({"_id": referrer_id}, {"$set": {"balance": new_balance}})

        if new_balance < current_balance + total_reward_amount:
            reward_details.append(f"Your balance has been capped at ₹{MAX_BALANCE_LIMIT:,}.")

    if total_kryon_reward > 0:
        users.update_one({"_id": referrer_id}, {"$inc": {"kryon_balance": total_kryon_reward}})

    reward_message_to_referrer = f"""🎉 Congratulations! {new_user_name} joined using your referral link!

You received:
"""

    if reward_details:
        reward_message_to_referrer += "- " + "\n- ".join(reward_details)
    else:
        reward_message_to_referrer += "No specific rewards this time."

    try:
        await client.send_message(referrer_id, reward_message_to_referrer)
    except Exception as e:
        print(f"Failed to send referral reward message to {referrer_id}: {e}")


active_bet_games = {}  
active_higherlower_games = {} 
active_gifts = {} 
active_drops = {}

if not bank_vault.find_one({"_id": "bank_balance"}):
    bank_vault.insert_one({"_id": "bank_balance", "balance": BANK_STARTING_BALANCE, "last_rob_time": None})

if not bot_settings.find_one({"_id": "global_settings"}):
    bot_settings.insert_one({"_id": "global_settings", "is_rare_drop_mode_active": False})

if fishing_items_db.count_documents({}) == 0:
    initial_fishing_items = [
        {"_id": "common_fish_1", "name": "Small Fry", "value": 100, "rarity": "Common", "weight": 50},
        {"_id": "common_fish_2", "name": "River Perch", "value": 150, "rarity": "Common", "weight": 45},
        {"_id": "uncommon_fish_1", "name": "Lake Trout", "value": 300, "rarity": "Uncommon", "weight": 30},
        {"_id": "uncommon_fish_2", "name": "Catfish", "value": 400, "rarity": "Uncommon", "weight": 25},
        {"_id": "rare_fish_1", "name": "Golden Carp", "value": 1000, "rarity": "Rare", "weight": 10},
        {"_id": "rare_fish_2", "name": "Electric Eel", "value": 1200, "rarity": "Rare", "weight": 8},
        {"_id": "epic_item_1", "name": "Mysterious Crate", "value": 3000, "rarity": "Epic", "weight": 3},
        {"_id": "legendary_item_1", "name": "Sunken Treasure", "value": 10000, "rarity": "Legendary", "weight": 1},
        {"_id": "junk_item_1", "name": "Old Boot", "value": 10, "rarity": "Junk", "weight": 60}, # High weight for junk
        {"_id": "junk_item_2", "name": "Rusty Can", "value": 5, "rarity": "Junk", "weight": 55},
        {"_id": "uncommon_fish_3", "name": "Rainbow Trout", "value": 350, "rarity": "Uncommon", "weight": 28},
        {"_id": "rare_fish_3", "name": "Deep Sea Monster", "value": 5000, "rarity": "Rare", "weight": 5},
        {"_id": "epic_item_2", "name": "Ancient Relic", "value": 7500, "rarity": "Epic", "weight": 2},
        {"_id": "legendary_item_2", "name": "Mermaid's Tear", "value": 15000, "rarity": "Legendary", "weight": 0.5},
        {"_id": "common_fish_3", "name": "Mudskipper", "value": 80, "rarity": "Common", "weight": 52},
        {"_id": "common_fish_4", "name": "Dace", "value": 120, "rarity": "Common", "weight": 48},
        {"_id": "common_fish_5", "name": "Minnow", "value": 70, "rarity": "Common", "weight": 55},
        {"_id": "uncommon_fish_4", "name": "Pike", "value": 320, "rarity": "Uncommon", "weight": 27},
        {"_id": "uncommon_fish_5", "name": "Sturgeon", "value": 450, "rarity": "Uncommon", "weight": 22},
        {"_id": "uncommon_fish_6", "name": "Walleye", "value": 380, "rarity": "Uncommon", "weight": 26},
        {"_id": "rare_fish_4", "name": "Arowana", "value": 1500, "rarity": "Rare", "weight": 9},
        {"_id": "rare_fish_5", "name": "Mahi-Mahi", "value": 1800, "rarity": "Rare", "weight": 7},
        {"_id": "rare_fish_6", "name": "Bluefin Tuna", "value": 2000, "rarity": "Rare", "weight": 6},
        {"_id": "epic_item_3", "name": "Dragon Scale", "value": 4000, "rarity": "Epic", "weight": 2.5},
        {"_id": "epic_item_4", "name": "Kraken Ink", "value": 4500, "rarity": "Epic", "weight": 2.2},
        {"_id": "legendary_item_3", "name": "Triton's Trident", "value": 20000, "rarity": "Legendary", "weight": 0.8},
        {"_id": "legendary_item_4", "name": "Lost Atlantis Map", "value": 25000, "rarity": "Legendary", "weight": 0.7},
        {"_id": "junk_item_3", "name": "Tangled Net", "value": 15, "rarity": "Junk", "weight": 58},
        {"_id": "junk_item_4", "name": "Broken Compass", "value": 20, "rarity": "Junk", "weight": 50},
        {"_id": "common_fish_6", "name": "Perch", "value": 110, "rarity": "Common", "weight": 49},
        {"_id": "common_fish_7", "name": "Carp", "value": 130, "rarity": "Common", "weight": 46},
        {"_id": "uncommon_fish_7", "name": "Salmon", "value": 370, "rarity": "Uncommon", "weight": 29},
        {"_id": "uncommon_fish_8", "name": "Trout", "value": 330, "rarity": "Uncommon", "weight": 31},
        {"_id": "rare_fish_7", "name": "Swordfish", "value": 2200, "rarity": "Rare", "weight": 5.5},
        {"_id": "rare_fish_8", "name": "Marlin", "value": 2500, "rarity": "Rare", "weight": 4.5},
        {"_id": "epic_item_5", "name": "Pearl Necklace", "value": 5000, "rarity": "Epic", "weight": 2.8},
        {"_id": "epic_item_6", "name": "Enchanted Shell", "value": 5500, "rarity": "Epic", "weight": 2.6},
        {"_id": "legendary_item_5", "name": "Poseidon's Crown", "value": 30000, "rarity": "Legendary", "weight": 0.6},
        {"_id": "junk_item_5", "name": "Algae", "value": 2, "rarity": "Junk", "weight": 65},
        {"_id": "common_fish_8", "name": "Goby", "value": 90, "rarity": "Common", "weight": 51},
        {"_id": "uncommon_fish_9", "name": "Bass", "value": 280, "rarity": "Uncommon", "weight": 32},
        {"_id": "rare_fish_9", "name": "Giant Squid", "value": 3000, "rarity": "Rare", "weight": 4},
        {"_id": "epic_item_7", "name": "Coral Fragment", "value": 6000, "rarity": "Epic", "weight": 2.4},
        {"_id": "legendary_item_6", "name": "Lost Pirate Ship", "value": 40000, "rarity": "Legendary", "weight": 0.4},
        {"_id": "junk_item_6", "name": "Water Logged Wood", "value": 8, "rarity": "Junk", "weight": 57},
        {"_id": "common_fish_9", "name": "Tilapia", "value": 140, "rarity": "Common", "weight": 47},
        {"_id": "uncommon_fish_10", "name": "Cod", "value": 420, "rarity": "Uncommon", "weight": 23},
        {"_id": "rare_fish_10", "name": "Kraken Spawn", "value": 7000, "rarity": "Rare", "weight": 3},
        {"_id": "epic_item_8", "name": "Seaweed Wrap", "value": 6500, "rarity": "Epic", "weight": 2.1},
        {"_id": "legendary_item_7", "name": "Abyssal Pearl", "value": 50000, "rarity": "Legendary", "weight": 0.3},
        {"_id": "junk_item_7", "name": "Plastic Bottle", "value": 3, "rarity": "Junk", "weight": 62}
    ]
    fishing_items_db.insert_many(initial_fishing_items)
    print("Initialized fishing items in the database.")

if scouting_items_db.count_documents({}) == 0:
    initial_scouting_items = [
        {"_id": "odm_gear", "name": "ODM Gear", "value": 1000, "rarity": "Common", "weight": 50},
        {"_id": "titan_serum", "name": "Titan Serum", "value": 5000, "rarity": "Rare", "weight": 5},
        {"_id": "scout_supplies", "name": "Scout Supplies", "value": 500, "rarity": "Common", "weight": 60},
        {"_id": "eren_jaeger", "name": "Eren Jaeger (Shifter)", "value": 10000, "rarity": "Legendary", "weight": 1},
        {"_id": "colossal_titan", "name": "Colossal Titan", "value": 8000, "rarity": "Epic", "weight": 2},
        {"_id": "survey_map", "name": "Survey Map", "value": 200, "rarity": "Common", "weight": 70},
        {"_id": "mikasa_scarf", "name": "Mikasa's Scarf", "value": 3000, "rarity": "Rare", "weight": 8},
        {"_id": "potato", "name": "Sasha's Potato", "value": 50, "rarity": "Junk", "weight": 80},
        {"_id": "thunder_spear", "name": "Thunder Spear", "value": 2500, "rarity": "Uncommon", "weight": 20},
        {"_id": "beast_titan_hair", "name": "Beast Titan Hair", "value": 4000, "rarity": "Epic", "weight": 3},
        {"_id": "armored_plate", "name": "Armored Titan Plate", "value": 3500, "rarity": "Rare", "weight": 6},
        {"_id": "founding_key", "name": "Founding Titan Key", "value": 9000, "rarity": "Legendary", "weight": 1},
        {"_id": "levi_blade", "name": "Levi's Blade", "value": 4500, "rarity": "Epic", "weight": 4},
        {"_id": "hange_goggles", "name": "Hange's Goggles", "value": 1200, "rarity": "Uncommon", "weight": 18},
        {"_id": "syringe", "name": "Titan Injection Syringe", "value": 6000, "rarity": "Rare", "weight": 5},
        {"_id": "marleyan_gold", "name": "Marleyan Gold", "value": 2000, "rarity": "Uncommon", "weight": 15},
        {"_id": "garrison_badge", "name": "Garrison Badge", "value": 800, "rarity": "Common", "weight": 40},
        {"_id": "survey_cloak", "name": "Survey Corps Cloak", "value": 1500, "rarity": "Uncommon", "weight": 25},
        {"_id": "annie_ring", "name": "Annie's Ring", "value": 3500, "rarity": "Rare", "weight": 7},
        {"_id": "crystal_fragment", "name": "Titan Crystal Fragment", "value": 3000, "rarity": "Rare", "weight": 8},
        {"_id": "sasha_bow", "name": "Sasha's Bow", "value": 1000, "rarity": "Uncommon", "weight": 22},
        {"_id": "jean_mane", "name": "Jean's Mane", "value": 400, "rarity": "Junk", "weight": 60},
        {"_id": "connie_hat", "name": "Connie's Hat", "value": 300, "rarity": "Junk", "weight": 65},
        {"_id": "reiner_helmet", "name": "Reiner's Helmet", "value": 2000, "rarity": "Uncommon", "weight": 18},
        {"_id": "bertholdt_shoes", "name": "Bertholdt's Shoes", "value": 250, "rarity": "Junk", "weight": 70},
        {"_id": "falco_feather", "name": "Falco's Feather", "value": 900, "rarity": "Common", "weight": 35},
        {"_id": "pieck_cart", "name": "Pieck's Cart", "value": 2200, "rarity": "Uncommon", "weight": 16},
        {"_id": "zeke_glasses", "name": "Zeke's Glasses", "value": 3200, "rarity": "Rare", "weight": 9},
        {"_id": "historia_crown", "name": "Historia's Crown", "value": 7000, "rarity": "Epic", "weight": 2},
        {"_id": "yimir_journal", "name": "Ymir's Journal", "value": 5000, "rarity": "Epic", "weight": 3},
        {"_id": "grisha_notebook", "name": "Grisha's Notebook", "value": 4000, "rarity": "Rare", "weight": 7},
        {"_id": "wall_rose_brick", "name": "Wall Rose Brick", "value": 100, "rarity": "Junk", "weight": 75},
        {"_id": "wall_maria_dust", "name": "Wall Maria Dust", "value": 80, "rarity": "Junk", "weight": 78},
        {"_id": "hitch_cat", "name": "Hitch's Cat", "value": 600, "rarity": "Common", "weight": 38},
        {"_id": "moblit_sketch", "name": "Moblit's Sketch", "value": 1100, "rarity": "Uncommon", "weight": 20},
        {"_id": "marco_badge", "name": "Marco's Badge", "value": 1300, "rarity": "Uncommon", "weight": 19},
        {"_id": "gunther_bandana", "name": "Gunther's Bandana", "value": 400, "rarity": "Junk", "weight": 60},
        {"_id": "petra_pin", "name": "Petra's Pin", "value": 900, "rarity": "Common", "weight": 36},
        {"_id": "oluo_teeth", "name": "Oluo's Teeth", "value": 150, "rarity": "Junk", "weight": 72},
        {"_id": "hannes_flask", "name": "Hannes' Flask", "value": 700, "rarity": "Common", "weight": 39},
        {"_id": "krista_letter", "name": "Krista's Letter", "value": 1700, "rarity": "Uncommon", "weight": 17},
        {"_id": "flegel_pass", "name": "Flegel's Pass", "value": 600, "rarity": "Common", "weight": 37},
        {"_id": "sina_seal", "name": "Wall Sina Seal", "value": 120, "rarity": "Junk", "weight": 77},
        {"_id": "marleyan_radio", "name": "Marleyan Radio", "value": 2100, "rarity": "Uncommon", "weight": 15},
        {"_id": "cart_titan_gear", "name": "Cart Titan Gear", "value": 2600, "rarity": "Uncommon", "weight": 14},
        {"_id": "jaw_titan_claw", "name": "Jaw Titan Claw", "value": 4800, "rarity": "Epic", "weight": 2},
        {"_id": "warhammer_crystal", "name": "War Hammer Crystal", "value": 9500, "rarity": "Legendary", "weight": 1},
        {"_id": "paradis_flower", "name": "Paradis Island Flower", "value": 300, "rarity": "Junk", "weight": 68},
        {"_id": "sasha_meat", "name": "Sasha's Hidden Meat", "value": 2000, "rarity": "Rare", "weight": 10},
        {"_id": "armin_book", "name": "Armin's Book", "value": 1800, "rarity": "Uncommon", "weight": 13},
        {"_id": "annie_crystal", "name": "Annie's Crystal", "value": 7000, "rarity": "Epic", "weight": 2},
        {"_id": "founding_titan_spine", "name": "Founding Titan Spine", "value": 12000, "rarity": "Legendary", "weight": 1},
    ]
    scouting_items_db.insert_many(initial_scouting_items)

@client.on(events.ChatAction)
async def handle_chat_action(event):
    if event.user_added and event.user_id == (await client.get_me()).id:
        if event.is_group or event.is_channel:
            chat_id = event.chat_id
            if not groups_collection.find_one({"_id": chat_id}):
                groups_collection.insert_one({"_id": chat_id, "added_date": datetime.now()})
                print(f"Bot added to new group/channel: {chat_id}")
            else:
                print(f"Bot re-added to existing group/channel: {chat_id}")

    elif event.user_left and event.user_id == (await client.get_me()).id:
        if event.is_group or event.is_channel:
            chat_id = event.chat_id
            groups_collection.delete_one({"_id": chat_id})
            print(f"Bot removed from group/channel: {chat_id}")

@client.on(events.NewMessage(pattern="/start"))
@check_suspension
@handle_flood_control
async def start(event):
    user_id = event.sender_id
    user_exists = users.find_one({"_id": user_id})


    sender_entity = await client.get_entity(user_id)
    user_first_name = sender_entity.first_name if sender_entity else "User"
    
    bot_entity = await client.get_me()
    bot_username = bot_entity.username if bot_entity.username else "@Eren_Yeagerrobot" 

    welcome_message = f"Hey {user_first_name}, Hey there, I'm EREN YEAGER — your Game Bot!Need guidance? Just hit the Usage button for all the basics.\n\n Spotted a bug or have a feature in mind? Tap the Support button and let us know!Want to stay updated on new features and improvements? The Updates button has you covered!"

    if event.is_private:
        
        referred_by_id = None
        start_payload = event.text.split(' ', 1)
        if len(start_payload) > 1 and start_payload[1].startswith("ref_"):
            referral_code = start_payload[1][4:] 
            referrer_user = users.find_one({"referral_code": referral_code})
            if referrer_user:
                referred_by_id = referrer_user["_id"]
                print(f"User {user_id} referred by {referred_by_id}")
            else:
                print(f"Invalid referral code: {referral_code}")

        if not user_exists:
            JOIN_BONUS = 20000         
            initial_balance = JOIN_BONUS
            if referred_by_id:
                initial_balance += 20000 

            users.insert_one({
                "_id": user_id,
                "balance": initial_balance,
                "vault_balance": 0,
                "last_daily_claim": None,
                "last_rob_attempt": None,
                "mode": "active",
                "suspended_until": None,
                "level": 1,
                "xp": 0,
                "level_up_xp": 100,
                "joined_date": datetime.now(), 
                "kryon_balance": 0, 
                "fishing_rod_durability": 30, 
                "scouting_gear_durability": 30, 
                "referral_code": str(uuid.uuid4())[:8], 
                "referred_by": referred_by_id, 
                "referrals_count": 0, 
                "last_weekly_claim": None,
                "last_monthly_claim": None, 
                "user_vault_capacity": VAULT_CAPACITY, 
                "vault_upgrades_done": 0
            })
            welcome_message = f"🎉 Welcome! You've received ₹{initial_balance:,} joining bonus!"

            if referred_by_id:
                welcome_message += f" (including an extra ₹20,000 for joining via a referral link)!"
                await handle_referral_reward(referred_by_id, user_id) 
            
            welcome_message += f"\n\n" + f"Hey {user_first_name}, Hey there, I'm EREN YEAGER — your Game Bot!Need guidance? Just hit the Usage button for all the basics.\n\n Spotted a bug or have a feature in mind? Tap the Support button and let us know!Want to stay updated on new features and improvements? The Updates button has you covered!"
            welcome_message += f"\n🎣 You also received 30 free fishing rod uses! Use /fish to start fishing."
            welcome_message += f"\n🗺️ You also received 30 free scout gear uses! Use /scout to start scouting."
        else:
            
            if user_exists.get('mode') is None:
                users.update_one({"_id": user_id}, {"$set": {"mode": "active"}})
                user_exists['mode'] = 'active'
            if user_exists.get('level') is None:
                users.update_one({"_id": user_id}, {"$set": {"level": 1, "xp": 0, "level_up_xp": 100}})
                user_exists['level'] = 1
                user_exists['xp'] = 0  
                user_exists['level_up_xp'] = 100 
            if user_exists.get('joined_date') is None:
                users.update_one({"_id": user_id}, {"$set": {"joined_date": datetime.now()}})
            if user_exists.get('kryon_balance') is None:
                users.update_one({"_id": user_id}, {"$set": {"kryon_balance": 0}})
            if user_exists.get('fishing_rod_durability') is None:
                users.update_one({"_id": user_id}, {"$set": {"fishing_rod_durability": 0}})
            if user_exists.get('referral_code') is None:
                users.update_one({"_id": user_id}, {"$set": {"referral_code": str(uuid.uuid4())[:8]}})
            if user_exists.get('referred_by') is None:
                users.update_one({"_id": user_id}, {"$set": {"referred_by": None}})
            if user_exists.get('referrals_count') is None:
                users.update_one({"_id": user_id}, {"$set": {"referrals_count": 0}})
            if user_exists.get('last_weekly_claim') is None:
                users.update_one({"_id": user_id}, {"$set": {"last_weekly_claim": None}})
            if user_exists.get('last_monthly_claim') is None:
                users.update_one({"_id": user_id}, {"$set": {"last_monthly_claim": None}})
            if user_exists.get('user_vault_capacity') is None:
                users.update_one({"_id": user_id}, {"$set": {"user_vault_capacity": VAULT_CAPACITY}})
            if user_exists.get('vault_upgrades_done') is None:
                users.update_one({"_id": user_id}, {"$set": {"vault_upgrades_done": 0}})
            
            welcome_message = "You're already registered! Use /bal to check your balance.\n\n" + welcome_message
        buttons = [
            [Button.url("Usage", "https://example.com/usage")], 
            [Button.url("Updates", "https://t.me/Eren_Yeager_Updates"), Button.url("Support", "https://t.me/AACBotSupport")],
            [Button.url("Add Me", f"https://t.me/{bot_username}?startgroup=true")]
        ]
        start_image_url = "https://graph.org/file/fd2888ffb24d7eaefc1c1-323fd0a043e165504a.jpg" 

        try:
            await client.send_message(event.chat_id, welcome_message, file=start_image_url, buttons=buttons, parse_mode='md')
        except Exception as e:
            print(f"Failed to send start image: {e}. Sending text message with buttons instead.")
            await event.reply(welcome_message, buttons=buttons, parse_mode='md')
    else: 
        pm_button = [Button.url("PM", f"https://t.me/{bot_username}")]
        await event.reply("**Hey, I'm EREN YEAGER!**\n\nCurious to know more? Start a chat with me in PM — let the story unfold! ", buttons=[pm_button])

async def _is_user_in_groups(user_id, group_ids):
        """Checks if a user is a member of all specified groups."""
        for group_id in group_ids:
            is_member = False
            try:
                async for participant in client.iter_participants(group_id, limit=200):
                    if participant.id == user_id:
                        is_member = True
                        break
                if not is_member:
                    print(f"DEBUG: User {user_id} not found in participants of group {group_id}.")
                    return False
            except Exception as e:
                print(f"DEBUG: Error checking group {group_id} for user {user_id}: {e}")
               
                return False
        return True

@client.on(events.NewMessage(pattern="/(bal|balance)"))
@check_suspension
@handle_flood_control
async def balance(event):
    user_id = event.sender_id

        
    GROUP_ID_1 = -1002476319830 
    GROUP_ID_2 = -1002891841494  
    required_group_ids = [GROUP_ID_1, GROUP_ID_2]

    if not await _is_user_in_groups(user_id, required_group_ids):
        group1_invite_link = "https://t.me/Eren_Yeager_Updates"  
        group2_invite_link = "https://t.me/AACBotSupport"  
            
        buttons = [
            [Button.url("Join Group 1", group1_invite_link)],
            [Button.url("Join Group 2", group2_invite_link)],
            [Button.inline("I have joined both groups", data=f"joined_check_{user_id}")]
        ]
        await event.reply("Access Denied: Please join both required groups to use this command.", buttons=buttons)
        return
        
    await _display_user_balance(event, user_id)


@client.on(events.CallbackQuery(data=lambda d: d.startswith(b"joined_check_")))
@check_suspension
@handle_flood_control
async def handle_joined_check_callback(event):
        user_id = event.sender_id
        chat_id = event.chat_id
        original_message_id = event.query.msg_id

        GROUP_ID_1 = -1002476319830 
        GROUP_ID_2 = -1002891841494 
        required_group_ids = [GROUP_ID_1, GROUP_ID_2]

        if await _is_user_in_groups(user_id, required_group_ids):
            await client.delete_messages(chat_id, original_message_id) 
            await _display_user_balance(event, user_id) 
        else:
            await event.answer("You are not in both required groups.", alert=True) 


async def _display_user_balance(event, user_id):
    user = users.find_one({"_id": user_id})
    if not user:
        await event.reply("You're not registered yet. Use /start first.")
        return
    if user.get('mode') is None:
        users.update_one({"_id": user_id}, {"$set": {"mode": "active"}})
        user['mode'] = 'active' 
    if user.get('level') is None:
        users.update_one({"_id": user_id}, {"$set": {"level": 1, "xp": 0, "level_up_xp": 100}})
        user['level'] = 1
        user['xp'] = 0
        user['level_up_xp'] = 100
    sender_entity = await client.get_entity(user_id)
    user_first_name = sender_entity.first_name if sender_entity else "User"
    formatted_vault_capacity = format_currency_to_display(user.get('user_vault_capacity', VAULT_CAPACITY))
    xp_bar_with_percent = get_xp_bar_with_percentage(user.get('xp', 0), user.get('level_up_xp', 100), bar_length=11) 
    response_message = f"""**❐: Account info of {user_first_name}** 
`╭──────────────────────╮`
``` ○ Level - {user.get('level', 1)}```
``` ○ Balance:     ₹{user['balance']:,}```
``` ○ Vault:   ₹{user.get('vault_balance', 0):,} / ₹{formatted_vault_capacity}    ```
``` ○ XP: {user.get('xp', 0):,} / {user.get('level_up_xp', 100):,}  ```
``` ○ Level Progress: {xp_bar_with_percent}   ```
``` ○ Kryon:      Ꝿ{user.get('kryon_balance', 0):,}  ```
`╰──────────────────────╯`"""
    await event.reply(response_message, parse_mode='md')

@client.on(events.NewMessage(pattern="/daily"))
@check_suspension
@handle_flood_control
async def daily_bonus(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    now = datetime.now()
    last_claim = user.get("last_daily_claim")

    if last_claim and (now - last_claim) < timedelta(hours=24):
        time_left = timedelta(hours=24) - (now - last_claim)
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await event.reply(f"⏳ You can claim your next daily bonus in {hours}h {minutes}m.")
        return

    current_balance = user.get('balance', 0)
    new_balance = min(current_balance + DAILY_BONUS, MAX_BALANCE_LIMIT)
    users.update_one(
        {"_id": user_id},
        {"$set": {"balance": new_balance}, "$set": {"last_daily_claim": now}}
    )
    await give_xp(user_id, 10) 
    if new_balance < current_balance + DAILY_BONUS:
        await event.reply(f"✅ You claimed your daily bonus of ₹{DAILY_BONUS:,}! (Balance capped at ₹{MAX_BALANCE_LIMIT:,})")
    else:
        await event.reply(f"✅ You claimed your daily bonus of ₹{DAILY_BONUS:,}!")

@client.on(events.NewMessage(pattern="/weekly"))
@check_suspension
@handle_flood_control
async def weekly_bonus(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    now = datetime.now()
    last_claim = user.get("last_weekly_claim")

    if last_claim and (now - last_claim) < timedelta(days=WEEKLY_COOLDOWN_DAYS):
        time_left = timedelta(days=WEEKLY_COOLDOWN_DAYS) - (now - last_claim)
        days, seconds = time_left.days, time_left.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await event.reply(f"⏳ You can claim your next weekly bonus in {days}d {hours}h {minutes}m.")
        return
    current_balance = user.get('balance', 0)
    new_balance = min(current_balance + WEEKLY_BONUS, MAX_BALANCE_LIMIT)
    users.update_one(
        {"_id": user_id},
        {"$set": {"balance": new_balance}, "$set": {"last_weekly_claim": now}}
    )
    await give_xp(user_id, 20) 
    if new_balance < current_balance + WEEKLY_BONUS:
        await event.reply(f"✅ You claimed your weekly bonus of ₹{WEEKLY_BONUS:,}! (Balance capped at ₹{MAX_BALANCE_LIMIT:,})")
    else:
        await event.reply(f"✅ You claimed your weekly bonus of ₹{WEEKLY_BONUS:,}!")

@client.on(events.NewMessage(pattern="/monthly"))
@check_suspension
@handle_flood_control
async def monthly_bonus(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    now = datetime.now()
    last_claim = user.get("last_monthly_claim")

    if last_claim and (now - last_claim) < timedelta(days=MONTHLY_COOLDOWN_DAYS):
        time_left = timedelta(days=MONTHLY_COOLDOWN_DAYS) - (now - last_claim)
        days, seconds = time_left.days, time_left.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await event.reply(f"⏳ You can claim your next monthly bonus in {days}d {hours}h {minutes}m.")
        return
    current_balance = user.get('balance', 0)
    new_balance = min(current_balance + MONTHLY_BONUS, MAX_BALANCE_LIMIT)
    users.update_one(
        {"_id": user_id},
        {"$set": {"balance": new_balance}, "$set": {"last_monthly_claim": now}}
    )
    await give_xp(user_id, 50) 
    if new_balance < current_balance + MONTHLY_BONUS:
        await event.reply(f"✅ You claimed your monthly bonus of ₹{MONTHLY_BONUS:,}! (Balance capped at ₹{MAX_BALANCE_LIMIT:,})")
    else:
        await event.reply(f"✅ You claimed your monthly bonus of ₹{MONTHLY_BONUS:,}!")

@client.on(events.NewMessage(pattern=r"/dice (\d+) (even|odd|e|o|E|O)"))
@check_suspension
@handle_flood_control
async def dice(event):
    user_id = event.sender_id
    match = event.pattern_match
    amount = int(match.group(1))
    guess_raw = match.group(2).lower()

    if guess_raw in ["o", "O"]:
        guess = "odd"
    elif guess_raw in ["e", "E"]:
        guess = "even"
    else:
        guess = guess_raw

    user = users.find_one({"_id": user_id})
    if not user:
        await event.reply("Use /start to register first.")
        return
    if amount > user['balance']:
        await event.reply("❌ Not enough balance.")
        return
    dice_msg = await client.send_message(event.chat_id, file=InputMediaDice("🎲"))
    await asyncio.sleep(4)
    dice_value = dice_msg.media.value 
    result = "even" if dice_value % 2 == 0 else "odd"
    if guess == result:
        current_balance = user.get('balance', 0)
        reward = amount * 1
        new_balance = min(current_balance + reward, MAX_BALANCE_LIMIT)

        if new_balance < current_balance + reward:
            result_msg = f"🎲 Dice rolled: {dice_value} ({result})\n✅ You won ₹{reward:,}! (Balance capped at ₹{MAX_BALANCE_LIMIT:,})"
        else:
            result_msg = f"🎲 Dice rolled: {dice_value} ({result})\n✅ You won ₹{reward:,}!"

        users.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
        await give_xp(user_id, amount // 1000 + 5) 
    else:
        new_balance = user['balance'] - amount
        result_msg = f"🎲 Dice rolled: {dice_value} ({result})\n❌ You lost ₹{amount:,}." 
        await take_xp(user_id, amount // 2000 + 5) 
    users.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
    await event.reply(result_msg)

@client.on(events.NewMessage(pattern=r"/bet (\d+)"))
@check_suspension
@handle_flood_control
async def bet_game(event):

    user_id = event.sender_id
    match = event.pattern_match
    amount = int(match.group(1))

    user = users.find_one({"_id": user_id})
    if not user:
        await event.reply("Use /start to register first.")
        return
    
    if amount <= 0:
        await event.reply("❌ Bet amount must be positive.")
        return

    if amount > 5000:
        await event.reply("❌ Maximum bet amount for Mines is ₹5,000.")
        return

    if user['balance'] < amount:
        await event.reply("❌ Not enough balance to start this bet game.")
        return

    users.update_one({"_id": user_id}, {"$inc": {"balance": -amount}})

    if user_id in active_bet_games:
        await event.reply("⚠️ You already have an ongoing bet game!")
        return

    num_bombs = random.randint(2, 3)
    all_boxes = list(range(9))
    bombs = random.sample(all_boxes, num_bombs) 
    
    active_bet_games[user_id] = {
        "bombs": bombs,
        "initial_bet": amount, 
        "current_winnings_coins": 0,
        "current_winnings_kryon": 0,
        "hits": [],
        "safe_boxes_to_clear": 9 - num_bombs
    }

    buttons = []
    for i in range(9):
        buttons.append(Button.inline("❓", data=f"mine_{i}"))
    
    keyboard = [
        buttons[0:3],
        buttons[3:6],
        buttons[6:9]
    ]

    await event.reply(
        f"💣 Mines Game Started! There are {num_bombs} bombs.\nTap safe boxes, avoid the 💣!\nEarn from each safe box!",
        buttons=keyboard
    )

@client.on(events.CallbackQuery(data=lambda d: d.startswith(b"mine_")))
@check_suspension
@handle_flood_control
async def handle_mine_click(event):
    user_id = event.sender_id
    if user_id not in active_bet_games:
        await event.answer("❌ No active Mines game. Use /bet <amount> to start.")
        return

    game = active_bet_games[user_id]
    
    parts = event.data.decode().split("_")
    action = parts[1] 

    initial_bet = game['initial_bet'] 

    if action == "cashout":
        total_coins_earned = game['current_winnings_coins']
        total_kryon_earned = game['current_winnings_kryon']

        if total_coins_earned > 0:
            current_balance = users.find_one({"_id": user_id}).get('balance', 0)
            new_balance = min(current_balance + total_coins_earned, MAX_BALANCE_LIMIT)
            users.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
            if new_balance < current_balance + total_coins_earned:
                result_message = f"💰 You cashed out! You secured ₹{total_coins_earned:,} coins (capped at ₹{MAX_BALANCE_LIMIT:,})"
            else:
                result_message = f"💰 You cashed out! You secured ₹{total_coins_earned:,} coins"

        if total_kryon_earned > 0:
            users.update_one({"_id": user_id}, {"$inc": {"kryon_balance": total_kryon_earned}})
        
        result_message += ". Game Over!"

        await event.edit(result_message, buttons=None) # Remove buttons
        del active_bet_games[user_id]
        return

    box = int(action)

    if box in game['hits']:
        await event.answer("⛔ Already opened!")
        return

    game['hits'].append(box)

    if box in game['bombs']:
        total_coins_earned = 0
        total_kryon_earned = 0

        result_message = f"💥 Boom! You hit a bomb on box {box+1}.\n"\
                         f"Game Over! You lost all your current earnings!"
        if total_kryon_earned > 0:
            result_message += f" and Ꝿ{total_kryon_earned} Kryon"
        result_message += "."
        
        await event.edit(result_message, buttons=None)
        await give_xp(user_id, total_coins_earned // 1000 + total_kryon_earned * 10)
        del active_bet_games[user_id]
    else:
        reward_amount_per_box = int(initial_bet * 0.1) 
        is_kryon_reward = random.random() < 0.05

        if is_kryon_reward:
            kryon_reward = random.randint(1, 3) 
            game['current_winnings_kryon'] += kryon_reward
            reward_message_text = f"🎉 You found Ꝿ{kryon_reward} Kryon!"
            await give_xp(user_id, 25) 
        else:
            game['current_winnings_coins'] += reward_amount_per_box
            reward_message_text = f"✅ You found ₹{reward_amount_per_box:,} coins!"
            await give_xp(user_id, reward_amount_per_box // 1000 + 5) 

        safe_hits = [h for h in game['hits'] if h not in game['bombs']]
        if len(safe_hits) == game['safe_boxes_to_clear']:
            total_coins_earned = game['current_winnings_coins'] + initial_bet 
            total_kryon_earned = game['current_winnings_kryon']

            if total_coins_earned > 0:
                current_balance = users.find_one({"_id": user_id}).get('balance', 0)
                new_balance = min(current_balance + total_coins_earned, MAX_BALANCE_LIMIT)
                users.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
                if new_balance < current_balance + total_coins_earned:
                    final_win_message = f"🎉 Congratulations! You cleared all safe spots!\n"\
                                        f"Total Winnings: ₹{total_coins_earned:,} coins (capped at ₹{MAX_BALANCE_LIMIT:,})"
                else:
                    final_win_message = f"🎉 Congratulations! You cleared all safe spots!\n"\
                                        f"Total Winnings: ₹{total_coins_earned:,} coins"

            if total_kryon_earned > 0:
                users.update_one({"_id": user_id}, {"$inc": {"kryon_balance": total_kryon_earned}})

            if total_kryon_earned > 0:
                final_win_message += f" and Ꝿ{total_kryon_earned} Kryon"
            final_win_message += ". Game Over!"

            await event.edit(final_win_message, buttons=None) 
            await give_xp(user_id, initial_bet // 500 + 50) 
            del active_bet_games[user_id]
        else:
            updated_buttons = []
            for i in range(9):
                if i in game['hits']:
                    emoji = "✅" if i not in game['bombs'] else "💥"
                else:
                    emoji = "❓"
                updated_buttons.append(Button.inline(emoji, data=f"mine_{i}"))
            
            if len(safe_hits) >= 3:
                updated_buttons.append(Button.inline("💰 Cash Out", data=f"mine_cashout"))

            updated_keyboard = [
                updated_buttons[0:3],
                updated_buttons[3:6],
                updated_buttons[6:9]
            ]
            if len(updated_buttons) > 9: 
                updated_keyboard.append([updated_buttons[9]])

            current_winnings_display = f"Current Winnings: ₹{game['current_winnings_coins']:,} coins"
            if game['current_winnings_kryon'] > 0:
                current_winnings_display += f", Ꝿ{game['current_winnings_kryon']} Kryon"
            
            await event.edit(f"💣 Keep going! {reward_message_text}\n{current_winnings_display}\nAvoid the 💣!", buttons=updated_keyboard)

@client.on(events.NewMessage(pattern=r"/basket (\d+)"))
@check_suspension
@handle_flood_control
async def basketball_game(event):
    user_id = event.sender_id
    amount = int(event.pattern_match.group(1))

    user = users.find_one({"_id": user_id})
    if not user:
        await event.reply("❌ Not enough balance.")
        return

    if user['balance'] < amount:
        await event.reply("❌ Not enough balance.")
        return
    users.update_one({"_id": user_id}, {"$inc": {"balance": -amount}})
    await event.reply("🏀 Throwing the basketball...")
    dice_msg = await client.send_message(event.chat_id, file=InputMediaDice("🏀"))
    await asyncio.sleep(4)

    result = dice_msg.media.value  

    if result >= 3:
        reward = amount * 1
        current_balance = user.get('balance', 0)
        new_balance = min(current_balance + reward, MAX_BALANCE_LIMIT)
        users.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})

        if new_balance < current_balance + reward:
            await event.reply(f"✅ Basket Scored! You won ₹{reward:,}! (Balance capped at ₹{MAX_BALANCE_LIMIT:,})\n🎉 Congratulations!")
        else:
            await event.reply(f"✅ Basket Scored! You won ₹{reward:,}!\n🎉 Congratulations!")

        await give_xp(user_id, amount // 1000 + 5) 
    else:
        await event.reply(f"❌ Missed! You lost ₹{amount:,}. Try again!")
        await take_xp(user_id, amount // 2000 + 5) 

@client.on(events.NewMessage(pattern=r"/football (\d+)"))
@check_suspension
@handle_flood_control
async def football_game(event):
    user_id = event.sender_id
    amount = int(event.pattern_match.group(1))

    user = users.find_one({"_id": user_id})
    if not user:
        await event.reply("❌ Not enough balance.")
        return

    if user['balance'] < amount:
        await event.reply("❌ Not enough balance.")
        return
    users.update_one({"_id": user_id}, {"$inc": {"balance": -amount}})
    await event.reply("⚽ Kicking the football...")
    dice_msg = await client.send_message(event.chat_id, file=InputMediaDice("⚽"))
    await asyncio.sleep(4)

    result = dice_msg.media.value 

    if result >= 3:
        reward = amount * 1
        current_balance = user.get('balance', 0)
        new_balance = min(current_balance + reward, MAX_BALANCE_LIMIT)
        users.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})

        if new_balance < current_balance + reward:
            await event.reply(f"✅ Goal Scored! You won ₹{reward:,}! (Balance capped at ₹{MAX_BALANCE_LIMIT:,})\n🎉 Congratulations!")
        else:
            await event.reply(f"✅ Goal Scored! You won ₹{reward:,}!\n🎉 Congratulations!")

        await give_xp(user_id, amount // 1000 + 5) 
    else:
        await event.reply(f"❌ Missed! You lost ₹{amount:,}. Try again!")
        await take_xp(user_id, amount // 2000 + 5) 

@client.on(events.NewMessage(pattern=r"/spin (\d+)"))
@check_suspension
@handle_flood_control
async def spin_command(event):
    user_id = event.sender_id
    amount = int(event.pattern_match.group(1))

    if not event.is_private:
        await event.reply("❌ This command can only be used in my private chat.")
        return

    user = users.find_one({"_id": user_id})
    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    if amount <= 0:
        await event.reply("❌ Bet amount must be positive.")
        return

    if user['balance'] < amount:
        await event.reply("❌ Not enough balance.")
        return
    users.update_one({"_id": user_id}, {"$inc": {"balance": -amount}})
    slot_msg = await client.send_message(event.chat_id, file=InputMediaDice("🎰"))
    await asyncio.sleep(SLOT_ANIMATION_COOLDOWN)
    reel1 = random.randint(1, 9)
    reel2 = random.randint(1, 9)
    reel3 = random.randint(1, 9)

    outcome_message = f"🎰 Reels: {reel1}{reel2}{reel3}\n"
    reward_multiplier = 0
    kryon_reward = 0
    xp_change = 0

    if reel1 == 7 and reel2 == 7 and reel3 == 7:
        reward_multiplier = 10
        kryon_reward = 1
        outcome_message += "🎉 JACKPOT! 777! You hit the ultimate prize!"
        xp_change = amount // 500 + 50
    elif (reel1 == 7 and reel2 == 7 and reel3 != 7) or \
         (reel1 != 7 and reel2 == 7 and reel3 == 7) or \
         (reel1 == 7 and reel2 != 7 and reel3 == 7):
        reward_multiplier = 5
        outcome_message += "💰 Lucky Sevens! You got two 7s!"
        xp_change = amount // 1000 + 25
    elif (reel1 == reel2 and reel1 != reel3) or \
         (reel1 == reel3 and reel1 != reel2) or \
         (reel2 == reel3 and reel2 != reel1):
        reward_multiplier = 2
        outcome_message += "✨ Double Up! Two matching symbols!"
        xp_change = amount // 2000 + 10
    else:
        outcome_message += "❌ Better luck next time!"
        xp_change = -(amount // 2000 + 5)

    winnings = amount * reward_multiplier
    final_message = outcome_message

    if winnings > 0:
        current_balance = user.get('balance', 0)
        new_balance = min(current_balance + winnings, MAX_BALANCE_LIMIT)
        users.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
        if new_balance < current_balance + winnings:
            final_message += f"\n✅ You won ₹{winnings:,}! (Balance capped at ₹{MAX_BALANCE_LIMIT:,})"
        else:
            final_message += f"\n✅ You won ₹{winnings:,}!"

    else:
        final_message += f"\n❌ You lost ₹{amount:,}."
    
    if kryon_reward > 0:
        users.update_one({"_id": user_id}, {"$inc": {"kryon_balance": kryon_reward}})
        final_message += f"\n🎁 You also received Ꝿ{kryon_reward} Kryon!"

    if xp_change > 0:
        await give_xp(user_id, xp_change)
    elif xp_change < 0:
        await take_xp(user_id, abs(xp_change))

    await event.reply(final_message)

@client.on(events.NewMessage(pattern=r"/donate (\d+) (\d+)"))
@check_suspension
@handle_flood_control
async def donate_coins(event):
    if event.sender_id != ADMIN_ID:
        await event.reply("❌ You are not authorized to use this command.")
        return

    match = event.pattern_match
    target_user_id = int(match.group(1))
    amount = int(match.group(2))

    if amount <= 0:
        await event.reply("❌ Amount must be positive.")
        return

    target_user = users.find_one({"_id": target_user_id})
    if not target_user:
        await event.reply(f"❌ User {target_user_id} not found.")
        return

    current_balance = target_user.get('balance', 0)
    new_balance = min(current_balance + amount, MAX_BALANCE_LIMIT)
    users.update_one({"_id": target_user_id}, {"$set": {"balance": new_balance}})

    if new_balance < current_balance + amount:
        await event.reply(f"✅ Successfully gave ₹{amount:,} to user {target_user_id}. (User's balance capped at ₹{MAX_BALANCE_LIMIT:,})")
    else:
        await event.reply(f"✅ Successfully gave ₹{amount:,} to user {target_user_id}.")

@client.on(events.NewMessage(pattern=r"/donate (\d+)", func=lambda e: e.is_reply))
@check_suspension
@handle_flood_control
async def donate_via_reply(event):
    if event.sender_id != ADMIN_ID:
        await event.reply("❌ You are not authorized to use this command.")
        return

    amount = int(event.pattern_match.group(1))

    if amount <= 0:
        await event.reply("❌ Amount must be positive.")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("❌ Please reply to a user's message to use this command.")
        return

    recipient_id = reply_msg.sender_id

    if recipient_id == event.sender_id:
        await event.reply("❌ You cannot donate to yourself using this command. Use /set if you want to change your own balance.")
        return

    donor_user = users.find_one({"_id": event.sender_id})
    recipient_user = users.find_one({"_id": recipient_id})

    if not donor_user:
        await event.reply("❌ You are not registered. Use /start first.")
        return

    if not recipient_user:
        await event.reply(f"❌ The user you replied to (ID: {recipient_id}) is not registered yet. They need to use /start.")
        return

    if donor_user['balance'] < amount:
        await event.reply(f"❌ Not enough balance to donate. Your balance: ₹{donor_user['balance']:,}.")
        return
    users.update_one({"_id": event.sender_id}, {"$inc": {"balance": -amount}})
    current_recipient_balance = recipient_user.get('balance', 0)
    new_recipient_balance = min(current_recipient_balance + amount, MAX_BALANCE_LIMIT)
    users.update_one({"_id": recipient_id}, {"$set": {"balance": new_recipient_balance}})

    if new_recipient_balance < current_recipient_balance + amount:
        await event.reply(f"✅ You successfully donated ₹{amount:,} to user {recipient_id}. (User's balance capped at ₹{MAX_BALANCE_LIMIT:,})")
    else:
        await event.reply(f"✅ You successfully donated ₹{amount:,} to user {recipient_id}.")

@client.on(events.NewMessage(pattern="/rob", func=lambda e: e.is_reply))
@check_suspension
@handle_flood_control
async def rob_command(event):
    robber_id = event.sender_id
    robber_user = users.find_one({"_id": robber_id})

    if not robber_user:
        await event.reply("❌ You are not registered. Use /start first.")
        return
    now = datetime.now()
    last_rob = robber_user.get('last_rob_attempt')
    if last_rob and (now - last_rob) < timedelta(hours=ROB_COOLDOWN_HOURS):
        time_left = timedelta(hours=ROB_COOLDOWN_HOURS) - (now - last_rob)
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        await event.reply(f"⏳ You can attempt another rob in {hours}h {minutes}m.")
        return
    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("❌ Please reply to a user's message to rob them.")
        return
    victim_id = reply_msg.sender_id
    if robber_id == victim_id:
        await event.reply("❌ You cannot rob yourself!")
        return

    victim_user = users.find_one({"_id": victim_id})
    if not victim_user:
        await event.reply(f"❌ The user you replied to (ID: {victim_id}) is not registered or not found.")
        return

    victim_bounty = victim_user.get('balance', 0)

    if victim_bounty <= 0:
       
        await event.reply(f"❌ {reply_msg.sender.first_name} has no Balance to rob.")
        users.update_one({"_id": robber_id}, {"$set": {"last_rob_attempt": now}})
        return
    users.update_one({"_id": robber_id}, {"$set": {"last_rob_attempt": now}})

    robber_level = robber_user.get('level', 1)
    victim_level = victim_user.get('level', 1)

    if victim_level > robber_level:
        penalty = int(robber_user.get('balance', 0) * ROB_PENALTY_PERCENTAGE) 
        if penalty > robber_user.get('balance', 0):
            penalty = robber_user.get('balance', 0) 

        bonus_to_victim = int(penalty * 0.8)

        users.update_one({"_id": robber_id}, {"$inc": {"balance": -penalty}})
        users.update_one({"_id": victim_id}, {"$inc": {"balance": bonus_to_victim}})
        await give_xp(victim_id, 20 + (penalty // 1000)) 
        await event.reply(
                f"🚨 UNO REVERSE! {reply_msg.sender.first_name} (Lv.{victim_level}) is too strong for you (Lv.{robber_level})!\n"
                f"❌ You lost ₹{penalty:,} as a penalty.\n"
                f"✅ {reply_msg.sender.first_name} gained ₹{bonus_to_victim:,} for defending!"
            )
    else:

        potential_rob_amount = int(victim_bounty * ROB_PERCENTAGE)

        if random.random() < ROB_SUCCESS_CHANCE:
            # Rob successful
            robbed_amount = potential_rob_amount
            users.update_one({"_id": victim_id}, {"$inc": {"balance": -robbed_amount}})
            
            current_robber_balance = robber_user.get('balance', 0)
            new_robber_balance = min(current_robber_balance + robbed_amount, MAX_BALANCE_LIMIT)
            users.update_one({"_id": robber_id}, {"$set": {"balance": new_robber_balance}}) 
            await give_xp(robber_id, 15 + (robbed_amount // 1000))
            
            if new_robber_balance < current_robber_balance + robbed_amount:
                await event.reply(f"💰 You successfully robbed ₹{robbed_amount:,} from {reply_msg.sender.first_name}! Your new balance is ₹{new_robber_balance:,} (capped at ₹{MAX_BALANCE_LIMIT:,})")
            else:
                await event.reply(f"💰 You successfully robbed ₹{robbed_amount:,} from {reply_msg.sender.first_name}! Your new balance is ₹{new_robber_balance:,}.")
        else:
            penalty = int(robber_user.get('balance', 0) * ROB_PENALTY_PERCENTAGE)
            users.update_one({"_id": robber_id}, {"$inc": {"balance": -penalty}})
            await event.reply(f"🚨 Your rob attempt on {reply_msg.sender.first_name} failed! You lost ₹{penalty:,} as a penalty.")


@client.on(events.NewMessage(pattern="/bankrob"))
@check_suspension
@handle_flood_control
async def bank_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})
    if event.is_reply:
        reply_msg = await event.get_reply_message()
        if not reply_msg:
            await event.reply("❌ Please reply to a user's message to use /bankrob against them.")
            return

        victim_id = reply_msg.sender_id
        victim_user = users.find_one({"_id": victim_id})

        if not victim_user:
            await event.reply(f"❌ The user you replied to (ID: {victim_id}) is not registered or not found.")
            return

        if user_id == victim_id:
            await event.reply("❌ You cannot bankrob yourself!")
            return

        if victim_user.get('mode', 'active') == 'passive':
            suspension_duration_minutes = 10
            suspended_until_time = datetime.now() + timedelta(minutes=suspension_duration_minutes)

            print(f"POLICE ALERT: User {user_id} attempted to bankrob passive user {victim_id}. Suspending {user_id} for {suspension_duration_minutes} minutes.")

            users.update_one({"_id": user_id}, {"$set": {"suspended_until": suspended_until_time}})
            await event.reply(f"🚨 Police detected your attempt to bankrob a passive user! Your account is suspended for {suspension_duration_minutes} minutes.")
            return
        else:
            now = datetime.now()
            last_bankrob_user_attempt = user.get('last_bankrob_user_attempt')
            if last_bankrob_user_attempt and (now - last_bankrob_user_attempt) < timedelta(hours=BANKROB_COOLDOWN_HOURS):
                time_left = timedelta(hours=BANKROB_COOLDOWN_HOURS) - (now - last_bankrob_user_attempt)
                hours, remainder = divmod(time_left.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                await event.reply(f"⏳ You can attempt another bankrob on a user in {hours}h {minutes}m.")
                return

            victim_vault_balance = victim_user.get('vault_balance', 0)

            if victim_vault_balance <= 0:
                await event.reply(f"❌ {reply_msg.sender.first_name} has no coins in their vault to rob.")
                users.update_one({"_id": user_id}, {"$set": {"last_bankrob_user_attempt": now}})
                return
            users.update_one({"_id": user_id}, {"$set": {"last_bankrob_user_attempt": now}})

            potential_rob_amount = int(victim_vault_balance * BANK_ROB_PERCENTAGE)

            if random.random() < BANK_ROB_SUCCESS_CHANCE:
                robbed_amount = potential_rob_amount
                users.update_one({"_id": victim_id}, {"$inc": {"vault_balance": -robbed_amount}})

                current_robber_balance = user.get('balance', 0)
                new_robber_balance = min(current_robber_balance + robbed_amount, MAX_BALANCE_LIMIT)
                users.update_one({"_id": user_id}, {"$set": {"balance": new_robber_balance}})

                if new_robber_balance < current_robber_balance + robbed_amount:
                    await event.reply(f"💰 You successfully robbed ₹{robbed_amount:,} from {reply_msg.sender.first_name}'s vault! (Your balance capped at ₹{MAX_BALANCE_LIMIT:,})")
                else:
                    await event.reply(f"💰 You successfully robbed ₹{robbed_amount:,} from {reply_msg.sender.first_name}'s vault!")
            else:
                penalty = int(user.get('balance', 0) * BANK_ROB_PENALTY_PERCENTAGE)
                if penalty > user.get('balance', 0):
                    penalty = user.get('balance', 0) 
                users.update_one({"_id": user_id}, {"$inc": {"balance": -penalty}})
                await event.reply(f"🚨 Your vault robbery attempt on {reply_msg.sender.first_name} failed! You lost ₹{penalty:,} as a penalty.")
            return
    if user.get('mode', 'active') == 'passive':
        await event.reply("🛡️ You cannot attempt bank robberies while in passive mode. Use /active to switch to active mode.")
        return

    bank = bank_vault.find_one({"_id": "bank_balance"})
    if not bank:
        await event.reply("❌ Bank vault not found. Please contact an admin.")
        return
    now = datetime.now()
    last_rob_time = user.get('last_bankrob_attempt')

    if last_rob_time and (now - last_rob_time) < timedelta(hours=BANKROB_COOLDOWN_HOURS):
        time_left = timedelta(hours=BANKROB_COOLDOWN_HOURS) - (now - last_rob_time)
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await event.reply(f"⏳ You can attempt another bankrob in {hours}h {minutes}m.")
        return

    current_bank_balance = bank.get('balance', 0)

    if current_bank_balance <= 0:
        await event.reply("❌ The bank vault is currently empty. No coins to rob!")
        bank_vault.update_one({"_id": "bank_balance"}, {"$set": {"last_rob_time": now}})
        return

    bank_vault.update_one({"_id": "bank_balance"}, {"$set": {"last_rob_time": now}})

    potential_rob_amount = int(current_bank_balance * BANK_ROB_PERCENTAGE)
    if potential_rob_amount <= 0:
        await event.reply("❌ The bank vault has too few coins to rob effectively. Try again later!")
        return

    if random.random() < BANK_ROB_SUCCESS_CHANCE:
        robbed_amount = potential_rob_amount
        current_user_balance = user.get('balance', 0)
        new_user_balance = min(current_user_balance + robbed_amount, MAX_BALANCE_LIMIT)
        users.update_one({"_id": user_id}, {"$set": {"balance": new_user_balance}})

        bank_vault.update_one({"_id": "bank_balance"}, {"$inc": {"balance": -robbed_amount}})
        
        if new_user_balance < current_user_balance + robbed_amount:
            await event.reply(f"🎉 You successfully robbed ₹{robbed_amount:,} from the bank vault! (Your balance capped at ₹{MAX_BALANCE_LIMIT:,})")
        else:
            await event.reply(f"🎉 You successfully robbed ₹{robbed_amount:,} from the bank vault!")
    else:

        penalty = int(user.get('balance', 0) * BANK_ROB_PENALTY_PERCENTAGE)
        if penalty > user.get('balance', 0):
            penalty = user.get('balance', 0) 
        users.update_one({"_id": user_id}, {"$inc": {"balance": -penalty}})
        await event.reply(f"🚨 Your bank robbery attempt failed! You lost ₹{penalty:,} as a penalty.")
    users.update_one({"_id": user_id}, {"$set": {"last_bankrob_attempt": now}}) # Update user's last bankrob attempt time

@client.on(events.NewMessage(pattern="/passive"))
@check_suspension
@handle_flood_control
async def set_passive_mode(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered. Use /start first.")
        return

    if user.get('mode', 'active') == 'passive':
        await event.reply("🛡️ You are already in passive mode.")
    else:
        users.update_one({"_id": user_id}, {"$set": {"mode": "passive"}})
        await event.reply("🛡️ You are now in passive mode. You can avoide  bank robberies.")

@client.on(events.NewMessage(pattern="/active"))
@check_suspension
@handle_flood_control
async def set_active_mode(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered. Use /start first.")
        return

    if user.get('mode', 'active') == 'active':
        await event.reply("⚔️ You are already in active mode.")
    else:
        users.update_one({"_id": user_id}, {"$set": {"mode": "active"}})
        await event.reply("⚔️ You are now in active mode.")

@client.on(events.NewMessage(pattern=r"/resettimer", func=lambda e: e.is_reply))
async def reset_cooldown_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply("❌ You are not authorized to use this command.")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("❌ Please reply to a user's message to reset their cooldowns.")
        return

    target_user_id = reply_msg.sender_id
    target_user = users.find_one({"_id": target_user_id})

    if not target_user:
        await event.reply(f"❌ User {target_user_id} not found.")
        return

    users.update_one(
        {"_id": target_user_id},
        {"$set": {
            "last_daily_claim": None,
            "last_rob_attempt": None,
            "last_bankrob_user_attempt": None,
            "suspended_until": None
        }}
    )
    await event.reply(f"✅ All cooldowns and suspensions reset for user {target_user_id}.")

@client.on(events.NewMessage(pattern=r"/higherlower (\d+)(?:\s|$)", func=lambda e: not e.is_reply))
@check_suspension
@handle_flood_control
async def higherlower_solo_command(event):
    user_id = event.sender_id
    amount = int(event.pattern_match.group(1))

    user = users.find_one({"_id": user_id})
    if not user:
        await event.reply("Use /start to register first.")
        return

    if user['balance'] < amount:
        await event.reply("❌ Not enough balance.")
        return
    
    if amount > 20000:
        await event.reply("❌ Maximum bet amount for Higher or Lower (solo) is ₹2,000.")
        return

    if amount <= 0:
        await event.reply("❌ Bet amount must be positive.")
        return

    if user_id in active_higherlower_games and active_higherlower_games[user_id].get("game_type") == "solo":
        await event.reply("⚠️ You already have an ongoing solo Higher or Lower game! Finish it or wait.")
        return

    users.update_one({"_id": user_id}, {"$inc": {"balance": -amount}})


    game_cards = [random.randint(1, 13) for _ in range(5)]
    current_card = game_cards[0]
    
    active_higherlower_games[user_id] = {
        "game_type": "solo",
        "game_cards": game_cards,
        "current_round": 0,
        "current_card": current_card,
        "amount": amount,
        "initial_bet": amount,
    }

    cards_display = ", ".join([get_card_name(card) for card in game_cards]) 

    buttons = [
        [Button.inline("Higher ⬆️", data=f"hl_higher")],
        [Button.inline("Lower ⬇️", data=f"hl_lower")],
        [Button.inline("Cash Out 💰", data=f"hl_cashout")]
    ]

    msg = await event.reply(
        f"🃏 Higher or Lower!\nYour 5 cards are: {cards_display}\n\n"\
        f"Round 1/5: Your current card is: {get_card_name(current_card)}\n"\
        f"Do you think the next card will be Higher or Lower?",
        buttons=buttons
    )
    active_higherlower_games[user_id]["message_id"] = msg.id

@client.on(events.NewMessage(pattern=r"/higherlower (\d+)(?:\s|$)", func=lambda e: e.is_reply))
@check_suspension
@handle_flood_control
async def higherlower_challenge_command(event):
    challenger_id = event.sender_id
    bet_amount = int(event.pattern_match.group(1))

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("❌ Please reply to a user's message to challenge them in Higher or Lower.")
        return

    challenged_id = reply_msg.sender_id

    if challenger_id == challenged_id:
        await event.reply("❌ You cannot challenge yourself!")
        return
    
    if bet_amount <= 0:
        await event.reply("❌ Bet amount must be positive.")
        return

    if bet_amount > 20000:
        await event.reply("❌ Maximum bet amount for a Higher or Lower challenge is ₹2,000.")
        return

    challenger_user = users.find_one({"_id": challenger_id})
    challenged_user = users.find_one({"_id": challenged_id})

    if not challenger_user or not challenged_user:
        await event.reply("❌ Both players must be registered with the bot to participate. Use /start first.")
        return
    if challenged_user.get('is_banned'):
        await event.reply(f"🚫 {reply_msg.sender.first_name} is permanently banned and cannot accept challenges.")
        return
    if challenged_user.get('suspended_until') and challenged_user['suspended_until'] > datetime.now():
        await event.reply(f"🚫 {reply_msg.sender.first_name} is currently suspended and cannot accept challenges.")
        return

    if challenger_user['balance'] < bet_amount:
        await event.reply(f"❌ You don't have enough balance. You need ₹{bet_amount:,} but have ₹{challenger_user['balance']:,}.")
        return
    
    if challenged_user['balance'] < bet_amount:
        await event.reply(f"❌ {reply_msg.sender.first_name} doesn't have enough balance. They need ₹{bet_amount:,} to accept this challenge.")
        return

    # Check for active games for either player
    if challenger_id in active_higherlower_games and active_higherlower_games[challenger_id].get("game_type") != "solo_ended":
        await event.reply("⚠️ You already have an ongoing Higher or Lower game or pending challenge. Finish it or wait.")
        return
    if challenged_id in active_higherlower_games and active_higherlower_games[challenged_id].get("game_type") != "solo_ended":
        await event.reply(f"⚠️ {reply_msg.sender.first_name} already has an ongoing Higher or Lower game or pending challenge.")
        return

    game_id = str(uuid.uuid4())
    active_higherlower_games[game_id] = {
        "game_type": "challenge",
        "challenger_id": challenger_id,
        "challenged_id": challenged_id,
        "bet_amount": bet_amount,
        "status": "pending_acceptance",
        "chat_id": event.chat_id,
        "message_id": None, 
    }

    challenger_name = (await client.get_entity(challenger_id)).first_name
    challenged_name = (await client.get_entity(challenged_id)).first_name

    challenge_message = (
        f"🎲 {challenger_name} has challenged {challenged_name} to a Higher or Lower game!\n\n"
        f"Bet Amount: ₹{bet_amount:,}\n"
        f"Winner takes all (₹{bet_amount * 2:,})!\n\n"
        f"{challenged_name}, do you accept this challenge?"
    )

    buttons = [
        [Button.inline("✅ Accept", data=f"hl_challenge_accept_{game_id}")],
        [Button.inline("❌ Reject", data=f"hl_challenge_reject_{game_id}")]
    ]

    msg = await event.reply(challenge_message, buttons=buttons, parse_mode='md')
    active_higherlower_games[game_id]["message_id"] = msg.id

    await event.reply(f"Challenge sent to {challenged_name}!")

@client.on(events.CallbackQuery(data=lambda d: d.startswith(b"hl_")))
@check_suspension
@handle_flood_control
async def handle_higherlower_click(event):
    if event.data.startswith(b"hl_challenge_accept_") or event.data.startswith(b"hl_challenge_reject_"):
        return
    user_id = event.sender_id
    game = None
    game_id_from_data = None
    data_parts = event.data.decode().split("_")
    action = data_parts[1]

    if len(data_parts) == 3:
        game_id_from_data = data_parts[2]
        game = active_higherlower_games.get(game_id_from_data) 
    else: 
        game = active_higherlower_games.get(user_id) 
    
    if not game or (game.get("game_type") == "challenge" and user_id not in [game["challenger_id"], game["challenged_id"]]):
        await event.answer("❌ No active Higher or Lower game for you, or you are not part of this game.", alert=True)
        return
    if game.get("game_type") not in ["solo", "challenge", "solo_ended"]:
        await event.answer("❌ An error occurred with your game state. Please start a new game.", alert=True)
        if game_id_from_data:
            del active_higherlower_games[game_id_from_data]
        elif user_id in active_higherlower_games: 
            del active_higherlower_games[user_id]
        return

    if game.get("game_type") == "solo_ended":
        del active_higherlower_games[user_id]
        await event.answer("❌ Your previous solo game has ended. Please start a new one.", alert=True)
        return

    action = data_parts[1]

    current_player_prefix = None
    opponent_player_prefix = None
    current_player_id = user_id
    opponent_player_id = None
    current_card = None
    actual_bet = 0
    game_cards = [] 
    current_round = 0
    pot_amount = None 


    if game.get("game_type") == "challenge":
        if action != "cashout" and user_id != game["current_player_turn_id"]:
            await event.answer("⏳ It's not your turn! Please wait for the other player.", alert=True)
            return
        if user_id == game["challenger_id"]:
            current_player_prefix = "challenger"
            opponent_player_prefix = "challenged"
            current_player_id = game["challenger_id"]
            opponent_player_id = game["challenged_id"]
        else:
            current_player_prefix = "challenged"
            opponent_player_prefix = "challenger"
            current_player_id = game["challenged_id"]
            opponent_player_id = game["challenger_id"]

        current_card = game[f'{current_player_prefix}_game_cards'][game['current_global_round']]
        opponent_card_for_comparison = game[f'{opponent_player_prefix}_game_cards'][game['current_global_round']]
        
        actual_bet = game['bet_amount'] 
        pot_amount = game['pot_amount']
        game_cards = game[f'{current_player_prefix}_game_cards'] 
        current_round = game['current_global_round'] 

    

    elif game.get("game_type") == "solo":
        current_card = game['current_card']
        current_winnings = game['amount'] 
        actual_bet = game['initial_bet'] 
        game_cards = game['game_cards']
        current_round = game['current_round']
        opponent_card_for_comparison = None 

    
    if action == "cashout":
        if game.get("game_type") == "solo":
            if current_winnings > 0:
                current_balance = users.find_one({"_id": user_id}).get('balance', 0)
                new_balance = min(current_balance + current_winnings, MAX_BALANCE_LIMIT)
                users.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
                if new_balance < current_balance + current_winnings:
                    result_message = f"✅ You cashed out! You won a total of ₹{current_winnings:,}! (Balance capped at ₹{MAX_BALANCE_LIMIT:,})!"
                else:
                    result_message = f"✅ You cashed out! You won a total of ₹{current_winnings:,}!"
            else:
                result_message = f"You cashed out with ₹0 winnings."
            
            await event.edit(result_message, buttons=None) 
            game["game_type"] = "solo_ended" 

       
        


        else: 
            winner_id = opponent_player_id
            loser_id = current_player_id
            pot_amount = game["pot_amount"]

            current_balance = users.find_one({"_id": winner_id}).get('balance', 0)
            new_balance = min(current_balance + pot_amount, MAX_BALANCE_LIMIT) 
            users.update_one({"_id": winner_id}, {"$set": {"balance": new_balance}})
            
            winner_name = (await client.get_entity(winner_id)).first_name
            loser_name = (await client.get_entity(loser_id)).first_name

            result_message = f"❌ {loser_name} cashed out! {winner_name} wins the total pot of ₹{pot_amount:,}!"
            if new_balance < current_balance + pot_amount:
                result_message += f" (Balance capped at ₹{MAX_BALANCE_LIMIT:,})"

            await event.edit(result_message, buttons=None)


            if game['chat_id'] != event.chat_id and loser_id:
                try:
                    await client.send_message(loser_id, f"🎲 Higher or Lower Challenge Update:\nYou cashed out. {winner_name} won ₹{pot_amount:,} from your challenge.")
                except Exception as e:
                    print(f"Failed to notify loser user {loser_id}: {e}")
            

            if game['chat_id'] != event.chat_id and winner_id != user_id: 
                try:
                    await client.send_message(winner_id, f"🎲 Higher or Lower Challenge Update:\n{loser_name} cashed out. You won ₹{pot_amount:,} from your challenge with them!")
                except Exception as e:
                    print(f"Failed to notify winner user {winner_id}: {e}")

            del active_higherlower_games[game_id_from_data] 

        return


    card_name_current = get_card_name(current_card)
    

    next_card = None 
    if game.get("game_type") == "solo":
        
        if current_round < 4: 
            next_card = game_cards[current_round + 1]
            card_name_next = get_card_name(next_card)
        else:
            card_name_next = "N/A (Last Round)" 
        
        ranked_current_card = get_ranked_card_value(current_card)
        ranked_next_card = get_ranked_card_value(next_card) if next_card is not None else -1
    else: 
        next_card = opponent_card_for_comparison 
        card_name_next = get_card_name(next_card)
        ranked_current_card = get_ranked_card_value(current_card)
        ranked_next_card = get_ranked_card_value(next_card)


    correct_guess = False
    if game.get("game_type") == "solo" and current_round == 4 and next_card is None:
        correct_guess = True 
    elif action == "higher":
        if ranked_next_card > ranked_current_card:
            correct_guess = True
    elif action == "lower":
        if ranked_next_card < ranked_current_card:
            correct_guess = True
    if correct_guess:
        if game.get("game_type") == "solo":
            if current_round < 4:
                game['current_card'] = next_card
                game['current_round'] += 1
                game['amount'] = current_winnings * 2 
            else: 
                game['amount'] = current_winnings * 2 
            
            updated_winnings_display = game['amount']

            win_message_suffix = ""
            current_user_balance = users.find_one({"_id": user_id}).get('balance', 0)
            potential_balance_after_win = current_user_balance + updated_winnings_display
            if potential_balance_after_win > MAX_BALANCE_LIMIT:
                win_message_suffix = f" (Your total balance capped at ₹{MAX_BALANCE_LIMIT:,})!"

            
            if game['current_round'] >= 4: 
                final_message = (
                    f"🎉 Correct! {card_name_current} vs {card_name_next}\n"
                    f"You've completed all 5 rounds! Your total winnings: ₹{updated_winnings_display:,}{win_message_suffix}"
                )
                current_balance = users.find_one({"_id": user_id}).get('balance', 0)
                new_balance = min(current_balance + updated_winnings_display, MAX_BALANCE_LIMIT)
                users.update_one({"_id": user_id}, {"$set": {"balance": new_balance}})
                await give_xp(user_id, actual_bet // 500 + 50) 
                game["game_type"] = "solo_ended" 
                await event.edit(final_message, buttons=None)
            else:
                current_game_message = (
                    f"✅ Correct! {card_name_current} vs {card_name_next}\n"
                    f"Round {game['current_round'] + 1}/5: Your current card is: {get_card_name(game['current_card'])}\n"
                    f"Your current winnings: ₹{updated_winnings_display:,}{win_message_suffix}\n"
                    f"Do you think the next card will be Higher or Lower?"
                )
                buttons = [
                    [Button.inline("Higher ⬆️", data=b"hl_higher"), Button.inline("Lower ⬇️", data=b"hl_lower")],
                    [Button.inline("Cash Out 💰", data=b"hl_cashout")]
                ]
                await event.edit(current_game_message, buttons=buttons, parse_mode='md')
                await give_xp(user_id, actual_bet // 2000 + 15) 
        
        else: 
            game[f'{current_player_prefix}_round_correct'] = True
            game[f'{current_player_prefix}_round_guess_made'] = True
            
            challenger_name = (await client.get_entity(game['challenger_id'])).first_name
            challenged_name = (await client.get_entity(game['challenged_id'])).first_name

            round_status_message = f"✅ Correct! {card_name_current} vs {card_name_next} for {((await client.get_entity(current_player_id))).first_name}.\n"

            if game['challenger_round_guess_made'] and game['challenged_round_guess_made']:
                if game['challenger_round_correct'] and not game['challenged_round_correct']:
                    round_winner_id = game['challenger_id']
                    game['rounds_won_challenger'] += 1
                elif not game['challenger_round_correct'] and game['challenged_round_correct']:
                    round_winner_id = game['challenged_id']
                    game['rounds_won_challenged'] += 1
                else: 
                    round_winner_id = None 

                if round_winner_id:
                    round_status_message += f"{((await client.get_entity(round_winner_id))).first_name} won Round {game['current_global_round'] + 1}!\n"
                else:
                    round_status_message += f"Round {game['current_global_round'] + 1} was a draw!\n"
                game['current_global_round'] += 1
                game['challenger_round_guess_made'] = False
                game['challenged_round_guess_made'] = False
                game['challenger_round_correct'] = False
                game['challenged_round_correct'] = False

                await give_xp(current_player_id, actual_bet // 2000 + 15) 
                if game['current_global_round'] == 5:
                    final_message = f"Game Over! All 5 rounds completed.\n"
                    if game['rounds_won_challenger'] > game['rounds_won_challenged']:
                        winner_id = game['challenger_id']
                        loser_id = game['challenged_id']
                        winner_name = challenger_name
                        loser_name = challenged_name
                        final_message += f"🎉 {winner_name} wins the challenge {game['rounds_won_challenger']}-{game['rounds_won_challenged']} and takes the pot of ₹{pot_amount:,}!\n"
                        current_balance = users.find_one({"_id": winner_id}).get('balance', 0)
                        new_balance = min(current_balance + pot_amount, MAX_BALANCE_LIMIT)
                        users.update_one({"_id": winner_id}, {"$set": {"balance": new_balance}})
                        await give_xp(winner_id, actual_bet // 500 + 50)
                        await take_xp(loser_id, actual_bet // 500 + 50)
                    elif game['rounds_won_challenged'] > game['rounds_won_challenger']:
                        winner_id = game['challenged_id']
                        loser_id = game['challenger_id']
                        winner_name = challenged_name
                        loser_name = challenger_name
                        final_message += f"🎉 {winner_name} wins the challenge {game['rounds_won_challenged']}-{game['rounds_won_challenger']} and takes the pot of ₹{pot_amount:,}!\n"
                        current_balance = users.find_one({"_id": winner_id}).get('balance', 0)
                        new_balance = min(current_balance + pot_amount, MAX_BALANCE_LIMIT)
                        users.update_one({"_id": winner_id}, {"$set": {"balance": new_balance}})
                        await give_xp(winner_id, actual_bet // 500 + 50)
                        await take_xp(loser_id, actual_bet // 500 + 50)
                    else:
                        final_message += f"🤝 It's a draw! Both players won {game['rounds_won_challenger']} rounds. Bets refunded.\n"
                        users.update_one({"_id": game['challenger_id']}, {"$inc": {"balance": actual_bet}})
                        users.update_one({"_id": game['challenged_id']}, {"$inc": {"balance": actual_bet}})
                        await give_xp(game['challenger_id'], actual_bet // 2000 + 15)
                        await give_xp(game['challenged_id'], actual_bet // 2000 + 15)
                    if game['chat_id'] != event.chat_id:
                        if game['challenger_id'] != user_id: 
                            try:
                                await client.send_message(game['challenger_id'], f"🎲 Higher or Lower Challenge Update:\n{final_message}")
                            except Exception as e:
                                print(f"Failed to notify challenger {game['challenger_id']}: {e}")
                        if game['challenged_id'] != user_id: 
                            try:
                                await client.send_message(game['challenged_id'], f"🎲 Higher or Lower Challenge Update:\n{final_message}")
                            except Exception as e:
                                print(f"Failed to notify challenged {game['challenged_id']}: {e}")

                    del active_higherlower_games[game_id_from_data]
                    await event.edit(final_message, buttons=None, parse_mode='md')
                    return
                game['current_player_turn_id'] = game['challenger_id']

                current_game_message = (
                    f"{round_status_message}\n"
                    f"🎲 {challenger_name} vs {challenged_name} - Pot: ₹{pot_amount:,}\n\n"
                    f"{challenger_name}'s Cards: {', '.join([get_card_name(card) for card in game['challenger_game_cards']])}\n"
                    f"{challenged_name}'s Cards: {', '.join([get_card_name(card) for card in game['challenged_game_cards']])}\n\n"
                    f"It's {challenger_name}'s turn (Round {game['current_global_round'] + 1}/5).\n"
                    f"Your card: {get_card_name(game['challenger_game_cards'][game['current_global_round']])} vs Opponent's card: {get_card_name(game['challenged_game_cards'][game['current_global_round']])}"
                )
                buttons = [
                    [Button.inline("Higher ⬆️", data=f"hl_higher_{game_id_from_data}"), Button.inline("Lower ⬇️", data=f"hl_lower_{game_id_from_data}")],
                    [Button.inline("Cash Out 💰", data=f"hl_cashout_{game_id_from_data}")]
                ]
                await event.edit(current_game_message, buttons=buttons, parse_mode='md')
                return
            else: 
                game["current_player_turn_id"] = opponent_player_id 

                current_game_message = (
                    f"{round_status_message}\n"
                    f"🎲 {challenger_name} vs {challenged_name} - Pot: ₹{pot_amount:,}\n\n"
                    f"{challenger_name}'s Cards: {', '.join([get_card_name(card) for card in game['challenger_game_cards']])}\n"
                    f"{challenged_name}'s Cards: {', '.join([get_card_name(card) for card in game['challenged_game_cards']])}\n\n"
                    f"It's {((await client.get_entity(opponent_player_id))).first_name}'s turn (Round {game['current_global_round'] + 1}/5).\n"
                    f"Your card: {get_card_name(game[f'{opponent_player_prefix}_game_cards'][game['current_global_round']])} vs Opponent's card: {get_card_name(game[f'{current_player_prefix}_game_cards'][game['current_global_round']])}" # Opponent's current card for comparison
                )
                buttons = [
                    [Button.inline("Higher ⬆️", data=f"hl_higher_{game_id_from_data}"), Button.inline("Lower ⬇️", data=f"hl_lower_{game_id_from_data}")],
                    [Button.inline("Cash Out 💰", data=f"hl_cashout_{game_id_from_data}")]
                ]
                await event.edit(current_game_message, buttons=buttons, parse_mode='md')
                await give_xp(user_id, actual_bet // 2000 + 15) 
                return

    else: 
        final_message_prefix = ""
        if game.get("game_type") == "solo":
            final_message_prefix = f"❌ Incorrect! {card_name_current} vs {card_name_next}\n"
            final_message = final_message_prefix + f"You lost your bet of ₹{actual_bet:,}. Game Over!"
            
            await take_xp(user_id, actual_bet // 2000 + 15) 
            game["game_type"] = "solo_ended" 
            await event.edit(final_message, buttons=None)

        else: 
            winner_id = opponent_player_id
            loser_id = current_player_id
            pot_amount = game["pot_amount"]

            current_balance = users.find_one({"_id": winner_id}).get('balance', 0)
            new_balance = min(current_balance + pot_amount, MAX_BALANCE_LIMIT)
            users.update_one({"_id": winner_id}, {"$set": {"balance": new_balance}})
            
            winner_name = (await client.get_entity(winner_id)).first_name
            loser_name = (await client.get_entity(loser_id)).first_name

            final_message = (
                f"❌ Incorrect! {card_name_current} vs {card_name_next}\n"
                f"{loser_name} lost! {winner_name} won the Higher or Lower challenge and took the total pot of ₹{pot_amount:,}!\n"
            )
            if new_balance < current_balance + pot_amount:
                final_message += f" (Balance capped at ₹{MAX_BALANCE_LIMIT:,})"
            
           
            if game['chat_id'] != event.chat_id and loser_id:
                try:
                    await client.send_message(loser_id, f"🎲 Higher or Lower Challenge Update:\nYou lost the challenge. {winner_name} won ₹{pot_amount:,} from your challenge.\n")
                except Exception as e:
                    print(f"Failed to notify loser user {loser_id}: {e}")
            if game['chat_id'] != event.chat_id and winner_id != user_id: 
                try:
                    await client.send_message(winner_id, f"🎲 Higher or Lower Challenge Update:\n{loser_name} lost the challenge. You won ₹{pot_amount:,} from your challenge with them!\n")
                except Exception as e:
                    print(f"Failed to notify winner user {winner_id}: {e}")

            await take_xp(loser_id, actual_bet // 2000 + 15)
            del active_higherlower_games[game_id_from_data] 
            await event.edit(final_message, buttons=None)

        

@client.on(events.CallbackQuery(data=lambda d: d.startswith(b"hl_challenge_accept_")))
@check_suspension
@handle_flood_control
async def handle_higherlower_accept_challenge(event):
    user_id = event.sender_id
    game_id = event.data.decode().split("_")[3]

    if game_id not in active_higherlower_games:
        await event.answer("❌ This challenge is no longer active.", alert=True)
        await event.edit("❌ This challenge is no longer active.", buttons=None)
        return

    game = active_higherlower_games[game_id]

    if user_id != game['challenged_id']:
        await event.answer("❌ You are not the challenged player for this game.", alert=True)
        return
    
    if game['status'] != "pending_acceptance":
        await event.answer("❌ This challenge has already been accepted or cancelled.", alert=True)
        return

    challenger_id = game['challenger_id']
    bet_amount = game['bet_amount']

    challenger_user = users.find_one({"_id": challenger_id})
    challenged_user = users.find_one({"_id": user_id}) # user_id is the challenged_id here

    # Re-check balances before deducting
    if challenger_user['balance'] < bet_amount:
        await event.answer(f"❌ Challenger ({challenger_user.get('first_name', 'User')}) no longer has enough balance (₹{bet_amount:,}). Challenge cancelled.", alert=True)
        await event.edit(f"❌ Challenge cancelled: Challenger ({challenger_user.get('first_name', 'User')}) insufficient funds.", buttons=None)
        del active_higherlower_games[game_id]
        return
    
    if challenged_user['balance'] < bet_amount:
        await event.answer(f"❌ You no longer have enough balance (₹{bet_amount:,}). Challenge cancelled.", alert=True)
        await event.edit(f"❌ Challenge cancelled: You have insufficient funds.", buttons=None)
        del active_higherlower_games[game_id]
        return

    
    users.update_one({"_id": challenger_id}, {"$inc": {"balance": -bet_amount}})
    users.update_one({"_id": user_id}, {"$inc": {"balance": -bet_amount}})

    
    challenger_game_cards = [random.randint(1, 13) for _ in range(5)]
    challenged_game_cards = [random.randint(1, 13) for _ in range(5)]

    game.update({
        "challenger_game_cards": challenger_game_cards,
        "challenged_game_cards": challenged_game_cards,
        "current_global_round": 0,
        "challenger_round_guess_made": False, 
        "challenged_round_guess_made": False, 
        "challenger_round_correct": False, 
        "challenged_round_correct": False,
        "rounds_won_challenger": 0, 
        "rounds_won_challenged": 0, 
        "status": "active",
        "pot_amount": bet_amount * 2,
        "current_player_turn_id": challenger_id, 
    })

    cards_display_challenger = ", ".join([get_card_name(card) for card in challenger_game_cards])
    cards_display_challenged = ", ".join([get_card_name(card) for card in challenged_game_cards])

    challenger_name = (await client.get_entity(challenger_id)).first_name
    challenged_name = (await client.get_entity(user_id)).first_name

    game_start_message = (
        f"🎉 Challenge Accepted!\n\n"
        f"🎲 {challenger_name} vs {challenged_name} - Pot: ₹{game['pot_amount']:,}\n\n"
        f"{challenger_name}'s Cards: {cards_display_challenger}\n"
        f"{challenged_name}'s Cards: {cards_display_challenged}\n\n"
        f"It's {challenger_name}'s turn (Round 1/5).\n"
        f"Your card: {get_card_name(challenger_game_cards[0])} vs Opponent's card: {get_card_name(challenged_game_cards[0])}"
    )

    buttons = [
        [Button.inline("Higher ⬆️", data=f"hl_higher_{game_id}"), Button.inline("Lower ⬇️", data=f"hl_lower_{game_id}")],
        [Button.inline("Cash Out 💰", data=f"hl_cashout_{game_id}")]
    ]

    await event.edit(game_start_message, buttons=buttons, parse_mode='md')
    await event.answer("Challenge accepted!")


@client.on(events.CallbackQuery(data=lambda d: d.startswith(b"hl_challenge_reject_")))
@check_suspension
@handle_flood_control
async def handle_higherlower_reject_challenge(event):
    user_id = event.sender_id
    game_id = event.data.decode().split("_")[3]

    if game_id not in active_higherlower_games:
        await event.answer("❌ This challenge is no longer active.", alert=True)
        await event.edit("❌ This challenge is no longer active.", buttons=None)
        return

    game = active_higherlower_games[game_id]

    if user_id != game['challenged_id'] and user_id != game['challenger_id']:
        await event.answer("❌ You are not part of this challenge.", alert=True)
        return

    if game['status'] != "pending_acceptance":
        await event.answer("❌ This challenge has already been accepted or cancelled.", alert=True)
        return
    
    del active_higherlower_games[game_id]

    challenger_name = (await client.get_entity(game['challenger_id'])).first_name
    challenged_name = (await client.get_entity(game['challenged_id'])).first_name

    await event.edit(f"❌ {challenged_name} has rejected the Higher or Lower challenge from {challenger_name}. Game cancelled.", buttons=None)
    await event.answer("Challenge rejected.")

def get_card_name(card_value):
    CARD_RANKS = {
        1: "Ace", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 
        8: "8", 9: "9", 10: "10", 11: "Jack", 12: "Queen", 13: "King"
    }
    return CARD_RANKS.get(card_value, str(card_value))

def get_ranked_card_value(card_value):
    if card_value == 1:  
        return 14
    return card_value 

PAGE_SIZE = 10

async def send_collection_page(event, user_id, page_num):
    user = users.find_one({"_id": user_id})
    if not user:
        await event.reply("Use /start to register first.")
        return

    characters_collection = user.get('characters', [])
    total_characters = len(characters_collection)
    total_pages = (total_characters + PAGE_SIZE - 1) // PAGE_SIZE

    if total_characters == 0:
        await event.reply("Your collection is empty!")
        return

    if page_num < 1 or page_num > total_pages:
        await event.reply(f"Invalid page number. Please enter a number between 1 and {total_pages}.")
        return

    start_index = (page_num - 1) * PAGE_SIZE
    end_index = start_index + PAGE_SIZE
    characters_on_page = characters_collection[start_index:end_index]

    response_text = f"📜 Your Character Collection (Page {page_num}/{total_pages}):\n\n"
    character_summary = {} 
    for char in characters_on_page:
        char_name = char["name"]
        rarity = char.get("rarity", "Unknown")
        key = (char_name, rarity)
        if key not in character_summary:
            character_summary[key] = {"count": 0, "_id": char["_id"]} 
        character_summary[key]["count"] += 1

    for (char_name, rarity), data in character_summary.items():
        char_code_display = f' (Code: `{data["_id"]}`)' if data["_id"] else ""
        response_text += f'• {char_name} ({rarity}): {data["count"]}x{char_code_display}\n'

    buttons = []
    if page_num > 1:
        buttons.append(Button.inline("⬅️ Back", data=f"collection_page_{page_num - 1}"))
    if page_num < total_pages:
        buttons.append(Button.inline("Next ➡️", data=f"collection_page_{page_num + 1}"))
    
    if buttons:
        if isinstance(event, events.CallbackQuery.Event):
            await event.edit(response_text, buttons=[buttons])
        else:
            await event.reply(response_text, buttons=[buttons])
    else:
        if isinstance(event, events.CallbackQuery.Event):
            await event.edit(response_text, buttons=[]) 
        else:
            await event.reply(response_text)


@client.on(events.NewMessage(pattern="/collection"))
@check_suspension
@handle_flood_control
async def collection_command(event):
    user_id = event.sender_id
    await send_collection_page(event, user_id, 1) 

@client.on(events.CallbackQuery(data=lambda d: d.startswith(b"collection_page_")))
@check_suspension
@handle_flood_control
async def handle_collection_pagination(event):
    user_id = event.sender_id
    page_num = int(event.data.decode().split("_")[2])
    await event.answer() 
    await send_collection_page(event, user_id, page_num)

@client.on(events.NewMessage())
async def message_counter_and_drop_handler(event):
    if event.is_private or not event.is_group:
        return

    user_id = event.sender_id
    chat_id = event.chat_id
    current_time = datetime.now()

    if user_id == ADMIN_ID:
        print(f"[DEBUG] User {user_id} is admin. Skipping spam detection.")
        user_doc = users.find_one({"_id": user_id})
        if user_doc and user_doc.get('is_suspended') and user_doc.get('suspended_until') and user_doc['suspended_until'] > current_time:
            print(f"[DEBUG] Admin {user_id} is suspended. Ignoring message.")
            return
        pass
    else:
        user_doc = users.find_one({"_id": user_id})
        if user_doc and user_doc.get('is_suspended') and user_doc.get('suspended_until') and user_doc['suspended_until'] > current_time:
            print(f"[DEBUG] User {user_id} is suspended. Ignoring message.")
            return 
        user_spam_doc = user_spam_counts_db.find_one({"_id": user_id})
        if not user_spam_doc:
            user_spam_counts_db.insert_one({"_id": user_id, "messages": [{"timestamp": current_time, "chat_id": chat_id}]})
        else:
            recent_messages = [
                msg for msg in user_spam_doc["messages"]
                if current_time - msg["timestamp"] < timedelta(seconds=10)
            ]
            recent_messages.append({"timestamp": current_time, "chat_id": chat_id})
            user_spam_counts_db.update_one(
                {"_id": user_id},
                {"$set": {"messages": recent_messages}}
            )

            if len(recent_messages) >= 10:
                suspension_end_time = current_time + timedelta(minutes=10)
                users.update_one(
                    {"_id": user_id},
                    {"$set": {"is_suspended": True, "suspended_until": suspension_end_time}},
                    upsert=True
                )
                try:
                    sender = await event.get_sender()
                    user_first_name = sender.first_name if isinstance(sender, TelegramUser) else "User"
                    user_link = f"[{user_first_name}](tg://user?id={user_id})"
                    await client.send_message(
                        chat_id,
                        f"📛 {user_link} ɪs Spamming : ʙʟᴏᴄᴋᴇᴅ ғᴏʀ 𝟷𝟶 ᴍɪɴᴜᴛᴇs ғᴏʀ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ.",
                        parse_mode='md'
                    )
                    print(f"[SPAM_CONTROL] User {user_id} suspended for spamming in chat {chat_id}.")
                except Exception as e:
                    print(f"[ERROR] Failed to send spam suspension message to chat {chat_id}: {e}")

    chat_doc = chat_message_counts_db.find_one({"_id": chat_id})
    if not chat_doc:
        chat_message_counts_db.insert_one({"_id": chat_id, "count": 1, "drop_message_threshold": DROP_MESSAGE_THRESHOLD})
        current_count = 1
        current_drop_threshold = DROP_MESSAGE_THRESHOLD
    else:
        chat_message_counts_db.update_one({"_id": chat_id}, {"$inc": {"count": 1}})
        current_count = chat_doc["count"] + 1
        current_drop_threshold = chat_doc.get("drop_message_threshold", DROP_MESSAGE_THRESHOLD)

    if current_count >= current_drop_threshold:
        if chat_id in active_drops:
            print(f"Skipping drop in chat {chat_id} due to active drop.")
            return
        chat_message_counts_db.update_one({"_id": chat_id}, {"$set": {"count": 0}})
        global_settings = bot_settings.find_one({"_id": "global_settings"})
        is_rare_drop_active = global_settings.get("is_rare_drop_mode_active", False) if global_settings else False

        await trigger_character_drop(event.chat_id, is_raredrop=is_rare_drop_active)

async def trigger_character_drop(chat_id, is_raredrop=False):
    summoned_character = await get_random_character_from_db(is_raredrop_only=is_raredrop)
    if not summoned_character:
        message_text = "ℹ️ No characters available for drops." if not is_raredrop else "ℹ️ No rare characters available for drops."
        await client.send_message(chat_id, message_text + " Ask an admin to upload some!")
        print(f"No {'rare ' if is_raredrop else ''}characters in DB for drop in chat {chat_id}.")
        return

    character_name = summoned_character["name"]
    character_rarity = summoned_character["rarity"]
    character_image_url = summoned_character.get("image_url")

    message_text = f"🚨 A wild **{character_rarity} character** appeared!\n\n"
    message_text += f"Identify this character and be the first to type `/collect <character name>` within {DROP_COOLDOWN_MINUTES} minutes to claim it!"

    msg = None
    if character_image_url:
        try:
            msg = await client.send_message(chat_id, message_text, file=character_image_url, parse_mode='md')
            print(f"Attempted to send image from URL: {character_image_url}")
        except Exception as e:
            print(f"Failed to send image from URL {character_image_url}: {e}. Sending text message instead.")
    
    if msg is None: 
        msg = await client.send_message(chat_id, message_text, parse_mode='md')

    active_drops[chat_id] = {
        "character": summoned_character,
        "drop_time": datetime.now(),
        "message_id": msg.id
    }
    print(f"Character '{character_name}' dropped in chat {chat_id}.")


@client.on(events.CallbackQuery(data=lambda d: d.startswith(b"collect_char_")))
@check_suspension
@handle_flood_control
async def handle_collect_character_click(event):
    await event.answer("❌ This method of collecting characters is no longer active. Please use the /collect <character name> command.")
    try:
        await client.edit_message(event.chat_id, event.message.id, "This character drop button is no longer active. Please use the `/collect <character name>` command for future drops.")
    except Exception as e:
        print(f"Error editing old collect button message: {e}")
    return

@client.on(events.NewMessage(pattern=r"/collect (.+)"))
@check_suspension
@handle_flood_control
async def collect_command(event):
    user_id = event.sender_id
    chat_id = event.chat_id
    current_time = datetime.now()

    if chat_id not in active_drops:
        await event.reply("❌ No character drop is currently active in this chat.")
        return

    drop_info = active_drops[chat_id]
    dropped_character = drop_info["character"]
    drop_time = drop_info["drop_time"]
    drop_message_id = drop_info["message_id"]
    if (current_time - drop_time) > timedelta(minutes=DROP_COOLDOWN_MINUTES):
        await event.reply("❌ This character drop has expired!")
        del active_drops[chat_id] 
        try:
            await client.edit_message(chat_id, drop_message_id, "⌛ This character drop has expired. Better luck next time!")
        except Exception as e:
            print(f"Error editing expired message: {e}")
        return

    given_character_name_raw = event.pattern_match.group(1).strip()
    expected_character_name_raw = dropped_character["name"]
    def normalize_name(name):
        return set(name.lower().replace('-', ' ').split())

    given_words = normalize_name(given_character_name_raw)
    expected_words = normalize_name(expected_character_name_raw)
    if not given_words.issubset(expected_words):
        await event.reply(f"❌ Incorrect character name. Make sure you type a part of or the full name correctly. The character is a {dropped_character['rarity']} character.")
        return
    if chat_id not in active_drops or active_drops[chat_id]["message_id"] != drop_message_id: 
        await event.reply("❌ This character has already been collected or the drop has expired.")
        return
    users.update_one(
        {"_id": user_id},
        {"$push": {"characters": dropped_character}},
        upsert=True
    )
    groups_collection.update_one(
        {"_id": chat_id},
        {"$inc": {"characters_collected": 1}},
        upsert=True 
    )
    del active_drops[chat_id]
    sender_entity = await event.get_sender()
    claimer_name = sender_entity.first_name if sender_entity else "Someone"

    await event.reply(f"🎉 You successfully collected **{dropped_character['name']}** ({dropped_character['rarity']}) from **{dropped_character.get('anime_name', 'Unknown Source')}**!")
    try:
        await client.edit_message(chat_id, drop_message_id, f"🎉 **{dropped_character['name']}** ({dropped_character['rarity']}) has been collected by {claimer_name}!")
    except Exception as e:
        print(f"Error editing drop message after collection: {e}")

@client.on(events.NewMessage(pattern=r"/show (.+)"))
@check_suspension
@handle_flood_control
async def show_character_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("Use /start to register first.")
        return

    characters_collection = user.get('characters', [])

    if not characters_collection:
        await event.reply("Your collection is empty! Nothing to show.")
        return

    target_character_name_raw = event.pattern_match.group(1).strip()

    def normalize_name(name):
        return set(name.lower().replace('-', ' ').split())
    matching_characters = []
    for char in characters_collection:
        if char["_id"] == target_character_name_raw: 
            matching_characters = [char] 
            break

        char_name_normalized = normalize_name(char["name"])
        target_name_normalized = normalize_name(target_character_name_raw)

        if target_name_normalized.issubset(char_name_normalized):
            matching_characters.append(char)

    if not matching_characters:
        await event.reply(f"❌ Character '{target_character_name_raw}' not found in your collection.")
        return

    if len(matching_characters) == 1:
        char_data = matching_characters[0]
        
        rarity_emojis = {
            "Common": "⚪", "Rare": "🟣", "Epic": "🟡", "Legendary": "🟠",
            "Special": "🌟", "Limited": "👑", "Mythic": "🔮", "Love": "💖",
            "Summer": "☀️", "Winter": "❄️", "Rainy season": "☔", "Aesthetic": "🎨"
        }
        selected_emoji = rarity_emojis.get(char_data["rarity"], "")

        # Get the user's first name
        user_entity = await event.get_sender()
        user_first_name = user_entity.first_name if isinstance(user_entity, TelegramUser) else "User"

        response_text = f"""🔍 𝗖𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 𝗗𝗲𝘁𝗮𝗶𝗹𝘀 𝗳𝗼𝗿 «{user_first_name}»\n\n✨ 𝗡𝗮𝗺𝗲: {char_data["name"]}    \n🌏 𝗦𝗼𝘂𝗿𝗰𝗲: {char_data.get('anime_name', 'N/A')}  \n{selected_emoji} 𝗥𝗮𝗿𝗶𝘁𝘆: {char_data["rarity"]}\n\n\n🆔 𝗖𝗼𝗱𝗲: `{char_data["_id"]}`\n
"""

        if char_data.get('image_url'):
            image_url = char_data.get('image_url')
            try:
                await client.send_message(event.chat_id, response_text, file=image_url, parse_mode='md')
            except Exception as e:
                print(f"Failed to send image for /show command from URL {image_url}: {e}. Sending text message instead.")
                await event.reply(response_text, parse_mode='md')
        else:
            await event.reply(response_text, parse_mode='md')
        return 

    
    unique_characters_by_code = {}
    for char in matching_characters:
        unique_characters_by_code[char["_id"]] = char

    buttons = []
    for char_id, char in unique_characters_by_code.items():
        rarity_emojis = {
            "Common": "⚪", "Rare": "🟣", "Epic": "🟡", "Legendary": "🟠",
            "Special": "🌟", "Limited": "👑", "Mythic": "🔮", "Love": "💖",
            "Summer": "☀️", "Winter": "❄️", "Rainy season": "☔", "Aesthetic": "🎨"
        }
        selected_emoji = rarity_emojis.get(char["rarity"], "")
        buttons.append([Button.inline(f'{selected_emoji} {char["name"]} ({char["rarity"]}) - {char["_id"]}', data=f"show_select_{char['_id']}")])
    
    await event.reply(
        f"Multiple characters found for '{target_character_name_raw}'. Please select which one to view:",
        buttons=buttons
    )


@client.on(events.CallbackQuery(data=lambda d: d.startswith(b"show_select_")))
@check_suspension
@handle_flood_control
async def handle_show_rarity_selection(event):
    user_id = event.sender_id
    char_id_to_show = event.data.decode().split("_")[2]
    user = users.find_one({"_id": user_id})
    if not user:
        await event.answer("❌ Use /start to register first.")
        return

    characters_collection = user.get('characters', [])
    selected_character = next((char for char in characters_collection if char["_id"] == char_id_to_show), None)

    if not selected_character:
        await event.answer("❌ Character not found in your collection.")
        try:
            await client.edit_message(event.chat_id, event.message_id, "❌ Character not found or has been removed from your collection.", buttons=None)
        except Exception:
            pass
        return

    rarity_emojis = {
        "Common": "⚪", "Rare": "🟣", "Epic": "🟡", "Legendary": "🟠",
        "Special": "🌟", "Limited": "👑", "Mythic": "🔮", "Love": "💖",
        "Summer": "☀️", "Winter": "❄️", "Rainy season": "☔", "Aesthetic": "🎨"
    }
    selected_emoji = rarity_emojis.get(selected_character["rarity"], "")

    
    user_entity = await event.get_sender()
    user_first_name = user_entity.first_name if isinstance(user_entity, TelegramUser) else "User"

    response_text = f"""🔍 𝗖𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 𝗗𝗲𝘁𝗮𝗶𝗹𝘀 𝗳𝗼𝗿 «{user_first_name}»\n\n✨ 𝗡𝗮𝗺𝗲: {selected_character["name"]}    \n🌏 𝗦𝗼𝘂𝗿𝗰𝗲: {selected_character.get('anime_name', 'N/A')}  \n{selected_emoji} 𝗥𝗮𝗿𝗶𝘁𝘆: {selected_character["rarity"]}\n\n\n🆔 𝗖𝗼𝗱𝗲: `{selected_character["_id"]}`
"""

    if selected_character.get('image_url'):
        image_url = selected_character.get('image_url')
        try:
            await client.delete_messages(event.chat_id, event.message_id)
            await client.send_message(event.chat_id, message=response_text, file=image_url, parse_mode='md')
        except Exception as e:
            print(f"Failed to delete old message or send new message with image for /show rarity selection: {e}. Sending text message to new message.")
            await client.send_message(event.chat_id, response_text, parse_mode='md')
    else:
        try:
            await client.delete_messages(event.chat_id, event.message_id)
            await client.send_message(event.chat_id, response_text, parse_mode='md')
        except Exception as e:
            print(f"Failed to delete old message or send new text message for /show rarity selection: {e}. Responding to event with text.")
            await event.reply(response_text, parse_mode='md') 

    await event.answer() 

@client.on(events.NewMessage(pattern=r"/upload (.+?) (.+?) (.+?) (.+)"))
async def upload_character_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user or not user.get('is_promoted', False):
        await event.reply("❌ You are not authorized to use this command. Only promoted users can upload characters.")
        return

    match = event.pattern_match
    name = match.group(1).strip()
    anime_name = match.group(2).strip()
    rarity = match.group(3).strip().capitalize() 
    image_link = match.group(4).strip()

    rarity_emojis = {
        "Common": "⚪", "Rare": "🟣", "Epic": "🟡", "Legendary": "🟠",
        "Special": "🌟", "Limited": "👑", "Mythic": "🔮", "Love": "💖",
        "Summer": "☀️", "Winter": "❄️", "Rainy season": "☔", "Aesthetic": "🎨"
    }
    selected_emoji = rarity_emojis.get(rarity, "") 

    valid_rarities = ["Common", "Rare", "Epic", "Legendary", "Special", "Limited", "Mythic", "Love", "Summer", "Winter", "Rainy",]
    if rarity not in valid_rarities:
        await event.reply(f"❌ Invalid rarity. Supported rarities are: {', '.join(valid_rarities)}.")
        return

    if not (image_link.startswith("http://") or image_link.startswith("https://")):
        await event.reply("❌ Invalid image link. Please provide a full URL (http:// or https://).")
        return

    weight_map = {"Common": 40, "Rare": 20, "Epic": 8, "Legendary": 2, "Special": 0.5, "Limited": 0.1, "Mythic": 0.05, "Love": 1, "Summer": 5.0, "Winter": 5.0, "Rainy": 5.0,}
    assigned_weight = weight_map.get(rarity, 1)

    unique_code = str(uuid.uuid4().int)[:5] 

    character_data = {
        "_id": unique_code, 
        "name": name,
        "anime_name": anime_name,
        "rarity": rarity,
        "image_url": image_link,
        "weight": assigned_weight,
        "is_raredrop_only": False 
    }

    characters_db.insert_one(character_data)
    await event.reply(f"✅ Character **{name}** ({rarity}) from **Source: {anime_name}** uploaded successfully!\nUnique Code: `{unique_code}`")

    log_message = f"🆕 𝗡𝗲𝘄 𝗖𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 𝗨𝗽𝗹𝗼𝗮𝗱𝗲𝗱!\n\n"
    log_message += f"✨ 𝗡𝗮𝗺𝗲: {name} \n"
    log_message += f"📌 𝗦𝗼𝘂𝗿𝗰𝗲: {anime_name} \n"
    log_message += f"{selected_emoji} 𝗥𝗮𝗿𝗶𝘁𝘆: {rarity} \n\n\n"
    log_message += f"🆔 𝗖𝗼𝗱𝗲: `{unique_code}`"

    try:
        await client.send_message(UPLOAD_LOG_CHANNEL_ID, log_message, file=image_link, parse_mode='md')
        print(f"Successfully sent character upload log with image to channel {UPLOAD_LOG_CHANNEL_ID}.")
    except Exception as e:
        print(f"Failed to send image with upload log to channel {UPLOAD_LOG_CHANNEL_ID}: {e}. Sending text message instead.")
        try:
            await client.send_message(UPLOAD_LOG_CHANNEL_ID, log_message + f"\n[Image Link]({image_link})", parse_mode='md', link_preview=False)
        except Exception as text_e:
            print(f"Failed to send text upload log to channel {UPLOAD_LOG_CHANNEL_ID}: {text_e}.")

@client.on(events.NewMessage(pattern=r"/rarecupload (.+?) (.+?) (.+?) (.+)"))
async def rare_character_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user or not user.get('is_promoted', False):
        await event.reply("❌ You are not authorized to use this command. Only promoted users can upload rare drop characters.")
        return

    match = event.pattern_match
    name = match.group(1).strip()
    anime_name = match.group(2).strip()
    rarity = match.group(3).strip().capitalize() 
    image_link = match.group(4).strip()

    rarity_emojis = {
        "Common": "⚪", "Rare": "🟣", "Epic": "🟡", "Legendary": "🟠",
        "Special": "🌟", "Limited": "👑", "Mythic": "🔮", "Love": "💖",
        "Summer": "☀️", "Winter": "❄️", "Rainy season": "☔", "Aesthetic": "🎨"
    }
    selected_emoji = rarity_emojis.get(rarity, "") 

    valid_rarities = ["Summer", "Winter", "Rainy", "Aesthetic", "Love"]
    if rarity not in valid_rarities:
        await event.reply(f"❌ Invalid rarity. Supported rarities for rare uploads are: {', '.join(valid_rarities)}.")
        return
    if not (image_link.startswith("http://") or image_link.startswith("https://")):
        await event.reply("❌ Invalid image link. Please provide a full URL (http:// or https://).")
        return
    weight_map = {"Summer": 5.0, "Winter": 5.0, "Rainy": 5.0, "Aesthetic": 3.0, "Love": 0.08}
    assigned_weight = weight_map.get(rarity, 1)
    unique_code = str(uuid.uuid4().int)[:5]

    character_data = {
        "_id": unique_code,
        "name": name,
        "anime_name": anime_name,
        "rarity": rarity,
        "image_url": image_link,
        "weight": assigned_weight,
        "is_raredrop_only": True 
    }

    characters_db.insert_one(character_data)
    await event.reply(f"✅ Rare Drop Character **{name}** ({rarity}) from **Source: {anime_name}** uploaded successfully!\nUnique Code: `{unique_code}`")

    log_message = f"🆕 𝗡𝗲𝘄 𝗥𝗮𝗿𝗲 𝗗𝗿𝗼𝗽 𝗖𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 𝗨𝗽𝗹𝗼𝗮𝗱𝗲𝗱!\n\n"
    log_message += f"✨ 𝗡𝗮𝗺𝗲: {name} \n"
    log_message += f"📌 𝗦𝗼𝘂𝗿𝗰𝗲: {anime_name} \n"
    log_message += f"{selected_emoji} 𝗥𝗮𝗿𝗶𝘁𝘆: {rarity} \n"
    log_message += f"🆔 𝗖𝗼𝗱𝗲: `{unique_code}`"

    try:
        await client.send_message(UPLOAD_LOG_CHANNEL_ID, log_message, file=image_link, parse_mode='md')
        print(f"Successfully sent rare character upload log with image to channel {UPLOAD_LOG_CHANNEL_ID}.")
    except Exception as e:
        print(f"Failed to send image with rare upload log to channel {UPLOAD_LOG_CHANNEL_ID}: {e}. Sending text message instead.")
        try:
            await client.send_message(UPLOAD_LOG_CHANNEL_ID, log_message + f"\n[Image Link]({image_link})", parse_mode='md', link_preview=False)
        except Exception as text_e:
            print(f"Failed to send text rare upload log to channel {UPLOAD_LOG_CHANNEL_ID}: {text_e}.")

@client.on(events.NewMessage(pattern=r"/removechar (.+)"))
async def remove_character_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})
    if not user or not user.get('is_promoted', False):
        await event.reply("❌ You are not authorized to use this command. Only promoted users can upload characters.")
        return

    char_code = event.pattern_match.group(1).strip()
    result = characters_db.delete_one({"_id": char_code})

    if result.deleted_count > 0:
        await event.reply(f"✅ Character with code `{char_code}` removed successfully from the database.")
    else:
        await event.reply(f"❌ No character found with code `{char_code}`.")

@client.on(events.NewMessage(pattern=r"/bbpromote", func=lambda e: e.is_reply))
async def bbpromote_reply_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply("❌ You are not authorized to use this command. Only the bot owner can promote users.")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("❌ Please reply to a user's message to promote them.")
        return

    target_user_id = reply_msg.sender_id
    target_user = users.find_one({"_id": target_user_id})

    if not target_user:
        await event.reply(f"❌ User {target_user_id} not found in bot's database. They need to use /start first.")
        return

    if target_user.get('is_promoted', False):
        await event.reply(f"ℹ️ User {target_user_id} is already promoted.")
    else:
        users.update_one({"_id": target_user_id}, {"$set": {"is_promoted": True}})
        await event.reply(f"✅ User {target_user_id} has been promoted to a character manager!")

@client.on(events.NewMessage(pattern=r"/bbpromote (\d+)"))
async def bbpromote_id_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply("❌ You are not authorized to use this command. Only the bot owner can promote users.")
        return

    match = event.pattern_match
    target_user_id = int(match.group(1))

    target_user = users.find_one({"_id": target_user_id})

    if not target_user:
        await event.reply(f"❌ User {target_user_id} not found in bot's database. They need to use /start first.")
        return

    if target_user.get('is_promoted', False):
        await event.reply(f"ℹ️ User {target_user_id} is already promoted.")
    else:
        users.update_one({"_id": target_user_id}, {"$set": {"is_promoted": True}})
        await event.reply(f"✅ User {target_user_id} has been promoted to a character manager!")

@client.on(events.NewMessage(pattern=r"/bbdemote", func=lambda e: e.is_reply))
async def bbdemote_reply_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply("❌ You are not authorized to use this command. Only the bot owner can demote users.")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("❌ Please reply to a user's message to demote them.")
        return

    target_user_id = reply_msg.sender_id
    target_user = users.find_one({"_id": target_user_id})

    if not target_user:
        await event.reply(f"❌ User {target_user_id} not found in bot's database.")
        return

    if not target_user.get('is_promoted', False):
        await event.reply(f"ℹ️ User {target_user_id} is not currently promoted.")
    else:
        users.update_one({"_id": target_user_id}, {"$set": {"is_promoted": False}})
        await event.reply(f"✅ User {target_user_id} has been demoted from character manager.")

@client.on(events.NewMessage(pattern=r"/bbdemote (\d+)"))
async def bbdemote_id_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply("❌ You are not authorized to use this command. Only the bot owner can demote users.")
        return

    match = event.pattern_match
    target_user_id = int(match.group(1))

    target_user = users.find_one({"_id": target_user_id})

    if not target_user:
        await event.reply(f"❌ User {target_user_id} not found in bot's database.")
        return

    if not target_user.get('is_promoted', False):
        await event.reply(f"ℹ️ User {target_user_id} is not currently promoted.")
    else:
        users.update_one({"_id": target_user_id}, {"$set": {"is_promoted": False}})
        await event.reply(f"✅ User {target_user_id} has been demoted from character manager.")

@client.on(events.NewMessage(pattern=r"/gift (.+)", func=lambda e: e.is_reply))
@check_suspension
@handle_flood_control
async def gift_command(event):
    sender_id = event.sender_id
    character_code = event.pattern_match.group(1).strip()

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("❌ Please reply to a user's message to gift them a character.")
        return

    recipient_id = reply_msg.sender_id

    if sender_id == recipient_id:
        await event.reply("❌ You cannot gift a character to yourself!")
        return

    sender_user = users.find_one({"_id": sender_id})
    recipient_user = users.find_one({"_id": recipient_id})

    if not sender_user:
        await event.reply("❌ You are not registered. Use /start first.")
        return

    if not recipient_user:
        await event.reply(f"❌ The user you replied to (ID: {recipient_id}) is not registered or not found.")
        return
    sender_characters = sender_user.get('characters', [])
    character_to_gift = next((char for char in sender_characters if char["_id"] == character_code), None)

    if not character_to_gift:
        await event.reply(f"❌ You do not own a character with code `{character_code}`.")
        return

    gift_id = str(uuid.uuid4())
    
    gift_message_text = (
        f"🎁 **Character Gift Offer!**\n\n"
        f"**From:** {(await event.get_sender()).first_name}\n"
        f"**To:** {(await reply_msg.get_sender()).first_name}\n"
        f"**Character:** {character_to_gift['name']} ({character_to_gift['rarity']}) [Code: `{character_to_gift['_id']}`]\n\n"
        f"Both parties must accept this gift to complete the transfer."
    )

    active_gifts[gift_id] = {
        "sender_id": sender_id,
        "recipient_id": recipient_id,
        "character": character_to_gift,
        "chat_id": event.chat_id,
        "sender_accepted": False,
        "recipient_accepted": False,
        "message_text": gift_message_text
    }

    buttons = [
        [Button.inline("✅ Accept Gift (Sender)", data=f"gift_accept_sender_{gift_id}")],
        [Button.inline("✅ Accept Gift (Recipient)", data=f"gift_accept_recipient_{gift_id}")],
        [Button.inline("❌ Cancel Gift", data=f"gift_cancel_{gift_id}")]
    ]

    msg = await event.reply(gift_message_text, buttons=buttons, parse_mode='md')
    active_gifts[gift_id]['message_id'] = msg.id
    await event.reply(f"Gift offer for {character_to_gift['name']} sent to {(await reply_msg.get_sender()).first_name}!")


@client.on(events.CallbackQuery(data=lambda d: d.startswith(b"gift_")))
@check_suspension
@handle_flood_control
async def handle_gift_callback(event):
    user_id = event.sender_id
    data_parts = event.data.decode().split("_")
    action = data_parts[1]
    
    gift_id = data_parts[3] if action.startswith("accept") else data_parts[2]

    if gift_id not in active_gifts:
        await event.answer("❌ This gift offer is no longer active or has expired.")
        try:
            await event.edit("❌ This gift offer is no longer active or has expired.", buttons=None)
        except Exception:
            pass
        return

    gift = active_gifts[gift_id]
    if user_id != gift['sender_id'] and user_id != gift['recipient_id']:
        await event.answer("❌ You are not part of this gift offer.")
        return
    
    if action.startswith("accept"):
        if user_id == gift['sender_id']:
            if gift['sender_accepted']:
                await event.answer("✅ You have already accepted this gift.")
                return
            gift['sender_accepted'] = True
            await event.answer("✅ You accepted the gift!")
        elif user_id == gift['recipient_id']:
            if gift['recipient_accepted']:
                await event.answer("✅ You have already accepted this gift.")
                return
            gift['recipient_accepted'] = True
            await event.answer("✅ You accepted the gift!")
        sender_accepted_button_text = "✅ Accepted (Sender)" if gift['sender_accepted'] else "✅ Accept Gift (Sender)"
        recipient_accepted_button_text = "✅ Accepted (Recipient)" if gift['recipient_accepted'] else "✅ Accept Gift (Recipient)"

        updated_buttons = [
            [Button.inline(sender_accepted_button_text, data=f"gift_accept_sender_{gift_id}")],
            [Button.inline(recipient_accepted_button_text, data=f"gift_accept_recipient_{gift_id}")],
            [Button.inline("❌ Cancel Gift", data=f"gift_cancel_{gift_id}")]
        ]
        await event.edit(gift['message_text'], buttons=updated_buttons, parse_mode='md')

        if gift['sender_accepted'] and gift['recipient_accepted']:
            sender_user = users.find_one({"_id": gift['sender_id']})
            recipient_user = users.find_one({"_id": gift['recipient_id']})
            character_present_in_sender = next((char for char in sender_user.get('characters', []) if char["_id"] == gift['character']['_id']), None)
            
            if not character_present_in_sender:
                await event.edit(f"❌ Gift failed: The sender no longer owns **{gift['character']['name']}**.", buttons=None)
                del active_gifts[gift_id]
                return
            users.update_one(
                {"_id": gift['sender_id']},
                {"$pull": {"characters": {"_id": gift['character']['_id']}}}
            )

            users.update_one(
                {"_id": gift['recipient_id']},
                {"$push": {"characters": gift['character']}},
                upsert=True 
            )

            sender_entity = await client.get_entity(gift['sender_id'])
            recipient_entity = await client.get_entity(gift['recipient_id'])
            
            final_message_text = (
                f"🎉 **Gift Completed!** 🎉\n\n"
                f"**{gift['character']['name']}** has been successfully transferred from "\
                f"{sender_entity.first_name if sender_entity else 'Sender'} to "\
                f"{recipient_entity.first_name if recipient_entity else 'Recipient'}!"
            )
            await event.edit(final_message_text, buttons=None, parse_mode='md')
            del active_gifts[gift_id]

    elif action == "cancel":
        await event.answer("❌ You cancelled the gift offer.")
        sender_entity = await client.get_entity(gift['sender_id'])
        recipient_entity = await client.get_entity(gift['recipient_id'])

        cancel_message_text = (
            f"❌ **Gift Cancelled!** ❌\n\n"
            f"The gift offer of **{gift['character']['name']}** from "\
            f"{sender_entity.first_name if sender_entity else 'Sender'} to "\
            f"{recipient_entity.first_name if recipient_entity else 'Recipient'} has been cancelled."
        )
        await event.edit(cancel_message_text, buttons=None, parse_mode='md')
        del active_gifts[gift_id]

async def give_xp(user_id, xp_amount):
    user = users.find_one({"_id": user_id})
    if not user:
        return

    current_xp = user.get('xp', 0)
    current_level = user.get('level', 1)
    level_up_xp = user.get('level_up_xp', 100)

    new_xp = current_xp + xp_amount
    
    while new_xp >= level_up_xp:
        current_level += 1
        new_xp -= level_up_xp 
        level_up_xp = int(level_up_xp * 1.5) 
        try:
            user_entity = await client.get_entity(user_id)
            level_up_message = f"🎉 Congratulations {user_entity.first_name}! You leveled up to Level {current_level}! You need {level_up_xp:,} XP for the next level."
            try:
                await client.send_message(user_id, message=level_up_message, file=LEVEL_UP_IMAGE_URL, parse_mode='md')
            except Exception as e_img:
                print(f"Error sending level up image to user {user_id}: {e_img}. Sending text message instead.")
                await client.send_message(user_id, level_up_message, parse_mode='md')
        except Exception as e:
            print(f"Error fetching user entity or sending level up message to user {user_id}: {e}")

    users.update_one(
        {"_id": user_id},
        {"$set": {"xp": new_xp, "level": current_level, "level_up_xp": level_up_xp}}
    )

async def take_xp(user_id, xp_amount):
    user = users.find_one({"_id": user_id})
    if not user:
        return 

    current_xp = user.get('xp', 0)
    current_level = user.get('level', 1)
    level_up_xp = user.get('level_up_xp', 100)

    new_xp = current_xp - xp_amount

    while new_xp < 0 and current_level > 1:
        current_level -= 1
        level_up_xp = int(level_up_xp / 1.5) if level_up_xp > 1 else 100 
        new_xp = level_up_xp + new_xp 

        try:
            user_entity = await client.get_entity(user_id)
            level_down_message = f"📉 Oh no, {user_entity.first_name}! You de-leveled to Level {current_level}! You now need {level_up_xp:,} XP for the next level." # Corrected message
            try:
                await client.send_message(user_id, message=level_down_message, file=LEVEL_DOWN_IMAGE_URL, parse_mode='md')
            except Exception as e_img:
                print(f"Error sending level down image to user {user_id}: {e_img}. Sending text message instead.")
                await client.send_message(user_id, level_down_message, parse_mode='md')
        except Exception as e:
            print(f"Error fetching user entity or sending level down message to user {user_id}: {e}")
    new_xp = max(0, new_xp)
    
    users.update_one(
        {"_id": user_id},
        {"$set": {"xp": new_xp, "level": current_level, "level_up_xp": level_up_xp}}
    )

@client.on(events.NewMessage(pattern=r"/setdrop (\d+)"))
@check_suspension
@handle_flood_control
async def set_drop_threshold(event):
    if not event.is_group:
        await event.reply("❌ This command can only be used in groups.")
        return

    try:
        permissions = await client.get_permissions(event.chat_id, event.sender_id)

        if not permissions.is_admin and not permissions.is_creator:
            await event.reply("❌ You must be an administrator in this group to use this command.")
            return
    except Exception as e:
        print(f"Error checking admin status: {e}")
        await event.reply("❌ Could not verify your admin status. Please try again or contact support.")
        return

    chat_id = event.chat_id
    new_threshold = int(event.pattern_match.group(1))

    if new_threshold <= 0:
        await event.reply("❌ The drop limit must be a positive number.")
        return
    
    if new_threshold < 50:
        await event.reply("❌ The drop limit cannot be set to less than 50 messages.")
        return
    
    chat_message_counts_db.update_one(
        {"_id": chat_id},
        {"$set": {"drop_message_threshold": new_threshold}},
        upsert=True
    )
    await event.reply(f"✅ Character drop limit for this group set to {new_threshold} messages.")

@client.on(events.NewMessage(pattern=r"/admindrop (\d+)"))
async def admindrop_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply("❌ You are not authorized to use this command. Only the bot owner can set admin drop thresholds.")
        return

    if not event.is_group:
        await event.reply("❌ This command can only be used in groups.")
        return

    chat_id = event.chat_id
    new_threshold = int(event.pattern_match.group(1))

    if new_threshold <= 0:
        await event.reply("❌ The drop limit must be a positive number.")
        return

    chat_message_counts_db.update_one(
        {"_id": chat_id},
        {"$set": {"drop_message_threshold": new_threshold}},
        upsert=True
    )
    await event.reply(f"✅ Admin drop limit for this group set to {new_threshold} messages.")

@client.on(events.NewMessage(pattern=r"/raredrop (start|stop)?"))
async def raredrop_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply("❌ You are not authorized to use this command. Only the bot owner can trigger rare drops.")
        return

    arg = event.pattern_match.group(1)

    global_settings = bot_settings.find_one({"_id": "global_settings"})
    is_rare_drop_active = global_settings.get("is_rare_drop_mode_active", False) if global_settings else False

    if arg == "start":
        if is_rare_drop_active:
            await event.reply("✅ Rare drop mode is already **activated**.")
            return
        bot_settings.update_one({"_id": "global_settings"}, {"$set": {"is_rare_drop_mode_active": True}}, upsert=True)
        await event.reply("✅ Rare drop mode has been **activated** for all groups. All drops will now be rare characters.")
        return
    elif arg == "stop":
        if not is_rare_drop_active:
            await event.reply("✅ Rare drop mode is already **deactivated**.")
            return
        bot_settings.update_one({"_id": "global_settings"}, {"$set": {"is_rare_drop_mode_active": False}}, upsert=True)
        await event.reply("✅ Rare drop mode has been **deactivated**. Normal drops will resume.")
        return

    if not event.is_group:
        await event.reply("❌ This command can only be used in groups.")
        return

    chat_id = event.chat_id
    if chat_id in active_drops:
        await event.reply(f"⚠️ There is already an active character drop in this chat. Please wait for it to be collected or expire.")
        return

    await event.reply("Initiating a single rare character drop...")
    await trigger_character_drop(event.chat_id, is_raredrop=True)
async def get_total_bounty_ranking(user_id):
    all_users = list(users.find({}))

    users_with_bounty = []
    for user_data in all_users:
        balance = user_data.get('balance', 0)
        vault_balance = user_data.get('vault_balance', 0)
        total_bounty = balance + vault_balance
        users_with_bounty.append({"_id": user_data["_id"], "total_bounty": total_bounty})

    users_with_bounty.sort(key=lambda x: x["total_bounty"], reverse=True)

    user_rank = -1
    for i, user_data in enumerate(users_with_bounty):
        if user_data["_id"] == user_id:
            user_rank = i + 1
            break
            
    return user_rank, len(users_with_bounty)
async def get_vault_ranking(user_id):
    all_users = list(users.find({}))
    users_with_vault_balance = []
    for user_data in all_users:
        vault_balance = user_data.get('vault_balance', 0)
        users_with_vault_balance.append({"_id": user_data["_id"], "vault_balance": vault_balance})
    users_with_vault_balance.sort(key=lambda x: x["vault_balance"], reverse=True)

    user_rank = -1
    for i, user_data in enumerate(users_with_vault_balance):
        if user_data["_id"] == user_id:
            user_rank = i + 1
            break
            
    return user_rank, len(users_with_vault_balance)
def get_collection_rank(user_characters):
    if not user_characters:
        return "None"

    rarity_scores = {
        "Common": 1,
        "Rare": 5,
        "Epic": 20,
        "Legendary": 100,
        "Special": 500,
        "Limited": 1000 
    }

    total_collection_score = 0
    for char in user_characters:
        total_collection_score += rarity_scores.get(char.get("rarity", "Common"), 1)

    # Define thresholds for ranks
    if total_collection_score >= 10000:
        return "💎 Diamond"
    elif total_collection_score >= 2000:
        return "🏆 Platinum"
    elif total_collection_score >= 800:
        return "🥇 Gold"
    elif total_collection_score >= 500:
        return "🥈 Silver"
    else:
        return "🥉 Bronze"

def get_descriptive_rank(level):
    if level < 5:
        return "Novice"
    elif level < 10:
        return "Apprentice"
    elif level < 20:
        return "Journeyman"
    elif level < 30:
        return "Expert"
    elif level < 40:
        return "Master"
    elif level < 50:
        return "Grandmaster"
    else:
        
        return f"Legendary (Level {level})"


def get_xp_bar(current_xp, level_up_xp, bar_length=8): 
    if level_up_xp == 0: 
        return "■■■■■■■■" 

    filled_blocks = int(round(bar_length * current_xp / level_up_xp))
    empty_blocks = bar_length - filled_blocks
    xp_bar = "■" * filled_blocks + "□" * empty_blocks
    
    xp_needed = level_up_xp - current_xp
    return f"[{xp_bar}] ({xp_needed:,} XP for next level)"

def get_xp_bar_with_percentage(current_xp, level_up_xp, bar_length=15): 
    if level_up_xp == 0:
        return "[■■■■■■■■■■]" 
    
    percentage = (current_xp / level_up_xp) * 100 
    filled_blocks = int(round(bar_length * current_xp / level_up_xp))
    empty_blocks = bar_length - filled_blocks
    
    xp_bar = "■" * filled_blocks + "□" * empty_blocks 
    
    return f"[{xp_bar}]"

def format_currency_to_display(amount):
    if amount >= 1_000_000_000:
        return f"{amount / 1_000_000_000:.0f}B"
    elif amount >= 1_000_000:
        return f"{amount / 1_000_000:.0f}M"
    elif amount >= 1_000:
        return f"{amount / 1_000:.0f}K"
    else:
        return f"{amount:,}" 

@client.on(events.NewMessage(pattern="/profile"))
@check_suspension
@handle_flood_control
async def profile_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return
    sender_entity = await event.get_sender()
    user_name = sender_entity.first_name if sender_entity else "User"
    username_tag = f"@{sender_entity.username}" if sender_entity.username else "N/A"

    joined_date = user.get('joined_date', datetime.now()).strftime('%d-%m-%Y')
    global_rank, total_users = await get_total_bounty_ranking(user_id)
    descriptive_rank = get_descriptive_rank(user.get('level', 1))
    xp_bar = get_xp_bar(user.get('xp', 0), user.get('level_up_xp', 100))
    response_text = "`Your Journey`\n\n" 
    response_text += f"[u -`{user_id}`]\n" 
    response_text += "────────────────────────\n"
    response_text += f"Username: {username_tag}\n"
    response_text += f"Rank: {descriptive_rank}\n"
    response_text += f"Passive: {'Yes' if user.get('mode') == 'passive' else 'No'}\n"
    response_text += f"Global Rank: `{global_rank}`\n" 
    response_text += "────────────────────────\n"
    response_text += f"Balance: ₹`{user.get('balance', 0):,}`\n" 
    response_text += f"Kryon: Ꝿ{user.get('kryon_balance', 0):,}\n" 
    response_text += f"Vault: ₹`{user.get('vault_balance', 0):,}`/`{user.get('user_vault_capacity', VAULT_CAPACITY):,}`\n" 
    response_text += f"Fishing Rod Durability: `{user.get('fishing_rod_durability', 0)}`/{MAX_ROD_DURABILITY}\n" 
    response_text += f"Scouting Gear Durability: `{user.get('scouting_gear_durability', 0)}`/{MAX_SCOUT_DURABILITY}\n" 
    response_text += "────────────────────────\n"
    response_text += f"Level: `{user.get('level', 1)}`\n" 
    response_text += f"{xp_bar}" 

    profile_photo_file = None
    try:
        profile_photos = await client.get_profile_photos(user_id)
        if profile_photos:
            profile_photo_file = profile_photos[0]
    except Exception as e:
        print(f"Error fetching profile picture for user {user_id}: {e}")

    if profile_photo_file:
        await event.reply(file=profile_photo_file, message=response_text, parse_mode='md')
    else:
        await event.reply(response_text, parse_mode='md')

@client.on(events.NewMessage(pattern="/statsbot"))
@handle_flood_control
async def statsbot_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply('You do not have permission to use this command.')
        return
    user_count = users.count_documents({})
    group_count = groups_collection.count_documents({})

    response = (
        f"**Bot Statistics:**\n"
        f"Total Users: {user_count}\n"
        f"Total Groups: {group_count}"
    )

    await event.reply(response)

@client.on(events.NewMessage(pattern='/broadcast'))
@handle_flood_control
async def broadcast(event):
    if event.sender_id != ADMIN_ID:
        await event.reply('You do not have permission to use this command.')
        return
    message = event.message.message.split(' ', 1)
    if event.is_reply:
        reply_message = await event.get_reply_message()
        text = reply_message.text
    elif len(message) > 1:
        text = message[1]
    else:
        await event.reply('Please provide a message or reply to one.')
        return

    users_data = users.find() 
    for user_doc in users_data: 
        try:
            await client.send_message(user_doc['_id'], text) 
        except Exception as e:
            print(f"Failed to send message to {user_doc['_id']}: {e}")
    await event.reply('Broadcast sent to all users.')

@client.on(events.NewMessage(pattern='/bbroad'))
@handle_flood_control
async def bbroadcast(event):
    if event.sender_id != ADMIN_ID:
        await event.reply('You do not have permission to use this command.')
        return

    message = event.message.message.split(' ', 1)
    groups = groups_collection.find()

    if event.is_reply:
        reply_message = await event.get_reply_message()
        for group in groups:
            try:
                await client.send_message(
                    group['_id'], 
                    reply_message, 
                    link_preview=False, 
                )
                print(f"Message sent to group {group['_id']}.") 
            except Exception as e:
                print(f"Failed to send message to group {group['_id']}: {e}") 
        await event.reply('Broadcast sent to all groups (attempting to preserve format).')
    elif len(message) > 1:
        text = message[1]
        for group in groups:
            try:
                await client.send_message(
                    group['_id'], 
                    text,
                    parse_mode='md' 
                )
                print(f"Message sent to group {group['_id']}.")  
            except Exception as e:
                print(f"Failed to send message to group {group['_id']}: {e}") 
        await event.reply('Broadcast sent to all groups.')
    else:
        await event.reply('Please provide a message or reply to one.')
        return

@client.on(events.NewMessage(pattern=r"^/fish$"))
@check_suspension
@handle_flood_control
async def fish_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return
    current_rod_durability = user.get('fishing_rod_durability', 0)
    if current_rod_durability <= 0:
        await event.reply("🎣 Your fishing rod is broken or you don't have one! Please buy a new one from the /shop.")
        return
    now = datetime.now()
    last_fish_time = user.get("last_fish_time")
    if last_fish_time and (now - last_fish_time) < timedelta(minutes=FISH_COOLDOWN_MINUTES):
        time_left = timedelta(minutes=FISH_COOLDOWN_MINUTES) - (now - last_fish_time)
        minutes, seconds = divmod(time_left.seconds, 60)
        await event.reply(f"⏳ You can fish again in {minutes}m {seconds}s.")
        return
    await event.reply("🎣 You cast your line...")

    all_fishing_items = list(fishing_items_db.find({}))
    if not all_fishing_items:
        await event.reply("🎣 There are no items to fish for! Please tell the bot owner to add some.")
        users.update_one({"_id": user_id}, {"$set": {"last_fish_time": now}})
        return
    total_weight = sum(item["weight"] for item in all_fishing_items)
    if total_weight == 0:
        caught_item = random.choice(all_fishing_items) 
    else:
        rand = random.uniform(0, total_weight)
        cumulative_weight = 0
        caught_item = None
        for item in all_fishing_items:
            cumulative_weight += item["weight"]
            if rand < cumulative_weight:
                caught_item = item
                break
    
    if not caught_item:
        await event.reply("🎣 You cast your line but caught nothing! Try again.")
        users.update_one({"_id": user_id}, {"$set": {"last_fish_time": now}}) 
        return
    new_rod_durability = current_rod_durability - 1
    users.update_one(
        {"_id": user_id},
        {"$set": {"fishing_rod_durability": new_rod_durability}}
    )
    users.update_one(
        {"_id": user_id},
        {"$push": {"fishing_inventory": caught_item}}, 
        upsert=True 
    )
    users.update_one(
        {"_id": user_id},
        {"$set": {"last_fish_time": now}}
    )
    xp_gain = max(5, caught_item["value"] // 200)
    await give_xp(user_id, xp_gain)

    response_message = (
        f"🎣 You cast your line and caught a **{caught_item['name']}** ({caught_item['rarity']})! "
        f"It has been added to your inventory.\n"
    )
    if new_rod_durability > 0:
        response_message += f"Your fishing rod now has {new_rod_durability} uses left."
    else:
        response_message += "Your fishing rod broke! Buy a new one from the /shop."

    await event.reply(response_message)

@client.on(events.NewMessage(pattern=r"^/listfish$"))
@check_suspension
@handle_flood_control
async def list_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    fishing_inventory = user.get('fishing_inventory', [])

    if not fishing_inventory:
        await event.reply("🎣 Your fishing inventory is empty. Go fishing with /fish!")
        return

    item_counts = {}
    for item in fishing_inventory:
        key = (item["name"], item["rarity"])
        item_counts[key] = item_counts.get(key, 0) + 1

    response_text = "🎣 **Your Fishing Inventory:**\n\n"
    for (name, rarity), count in item_counts.items():
        response_text += f"• {name} ({rarity}): {count}x\n"
    
    buttons = []
    total_inventory_value = 0
    if fishing_inventory:
        buttons.append(Button.inline("💸 Sell All Fish", data=b"sell_all_fish"))
    
    await event.reply(response_text, parse_mode='md', buttons=buttons)

@client.on(events.CallbackQuery(data=b"sell_all_fish"))
@check_suspension
@handle_flood_control
async def handle_sell_all_fish(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    fishing_inventory = user.get('fishing_inventory', [])

    if not fishing_inventory:
        await event.reply("🎣 Your fishing inventory is empty. Go fishing with /fish!")
        return

    total_value = sum(item["value"] for item in fishing_inventory)
    new_balance = min(user.get('balance', 0) + total_value, MAX_BALANCE_LIMIT)

    users.update_one(
        {"_id": user_id},
        {"$set": {"balance": new_balance, "fishing_inventory": []}}
    )

    await event.reply(f"💸 You sold all fish in your inventory for ₹{total_value:,}!")

@client.on(events.NewMessage(pattern=r"/charstats"))
@check_suspension
@handle_flood_control
async def character_stats_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user or not user.get('is_promoted', False):
        await event.reply('❌ You are not authorized to use this command.')
        return

    rarity_counts = {}
    total_characters = 0
    for char in characters_db.find({}):
        rarity = char.get("rarity", "Unknown")
        rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1
        total_characters += 1

    response_text = "📊 **Character Statistics:**\n\n"
    if not rarity_counts:
        response_text += "No characters have been uploaded yet."
    else:
        for rarity, count in rarity_counts.items():
            response_text += f"**{rarity}:** {count} characters\n"
        response_text += "\n" 
        response_text += f"**Total Characters: {total_characters}**"

    await event.reply(response_text, parse_mode='md')


@client.on(events.NewMessage(pattern=r"/ctop"))
@check_suspension
@handle_flood_control
async def ctop_command(event):
    all_users = list(users.find({}))
    users_with_char_counts = []

    for user_data in all_users:
        character_count = len(user_data.get('characters', []))
        if character_count > 0: 
            users_with_char_counts.append({
                "_id": user_data["_id"],
                "character_count": character_count
            })

    users_with_char_counts.sort(key=lambda x: x["character_count"], reverse=True)
    top_users = users_with_char_counts[:10]

    if not top_users:
        await event.reply("📊 No characters have been collected by any user yet.")
        return

    response_text = "✨ --Top 10 Users Of This Group--\n\n"
    for i, user_data in enumerate(top_users):
        user_id = user_data["_id"]
        char_count = user_data["character_count"]
        try:
            user_entity = await client.get_entity(user_id)
            user_display_name = user_entity.first_name if user_entity.first_name else (f"@{user_entity.username}" if user_entity.username else f"User {user_id}")
            if user_entity.username:
                user_display_name = f"[{user_display_name}](tg://user?id={user_id})"
            else:
                user_display_name = f"[{user_display_name}](tg://user?id={user_id})"
        except Exception:
            user_display_name = f"User {user_id}"
        
        response_text += f"{i+1}. {user_display_name} ⇒ {char_count}\n"

    try:
        await event.reply(message=response_text, file=CTOP_USERS_IMAGE_URL, parse_mode='md')
    except Exception as e:
        print(f"Failed to send /ctop image: {e}. Sending text message instead.")
        await event.reply(response_text, parse_mode='md')


@client.on(events.NewMessage(pattern=r"/rank"))
@check_suspension
@handle_flood_control
async def rank_command(event):

    top_chats_cursor = groups_collection.find().sort("characters_collected", -1).limit(10) 
    top_chats = list(top_chats_cursor)

    if not top_chats:
        await event.reply("📊 No characters have been collected in any group yet.")
        return

    response_text = "✨ --Top 10 Groups--\n\n"
    for i, chat_doc in enumerate(top_chats):
        chat_id = chat_doc["_id"]
        char_collected_count = chat_doc.get("characters_collected", 0)
        try:
            chat_entity = await client.get_entity(chat_id)
            chat_title = chat_entity.title if chat_entity.title else f"Unnamed Group {chat_id}"
            chat_display_name = chat_title
        except Exception:
            chat_display_name = f"Group ID: {chat_id}"
        
        response_text += f"{i+1}. {chat_display_name} ⇒ {char_collected_count}\n"

    try:
        await client.send_message(event.chat_id, message=response_text, file=TOP_GROUPS_IMAGE_URL, parse_mode='md')
    except Exception as e:
        print(f"Failed to send /rank image: {e}. Sending text message instead.")
        await event.reply(response_text, parse_mode='md')


@client.on(events.NewMessage(pattern=r"/top"))
@check_suspension
@handle_flood_control
async def top_command(event):
    all_users = list(users.find({}))
    users_with_total_chars = []

    for user_data in all_users:
        total_characters = len(user_data.get('characters', []))
        if total_characters > 0:
            users_with_total_chars.append({
                "_id": user_data["_id"],
                "total_characters": total_characters
            })

    users_with_total_chars.sort(key=lambda x: x["total_characters"], reverse=True)

    # Get top 10 users
    top_users = users_with_total_chars[:10]

    if not top_users:
        await event.reply("📊 No characters have been collected by any user yet.")
        return

    response_text = "✨ --Global Top 10 Collectors--\n\n"
    for i, user_data in enumerate(top_users):
        user_id = user_data["_id"]
        char_count = user_data["total_characters"]
        try:
            user_entity = await client.get_entity(user_id)
            user_display_name = user_entity.first_name if user_entity.first_name else (f"@{user_entity.username}" if user_entity.username else f"User {user_id}")
        except Exception:
            user_display_name = f"User {user_id}"
        
        response_text += f"{i+1}. {user_display_name} ⇒ {char_count}\n"

    try:
        await client.send_message(event.chat_id, message=response_text, file=TOP_USERS_IMAGE_URL, parse_mode='md')
    except Exception as e:
        print(f"Failed to send /top image: {e}. Sending text message instead.")
        await event.reply(response_text, parse_mode='md')


@client.on(events.NewMessage(pattern=r"/leaderboard"))
@check_suspension
@handle_flood_control
async def leaderboard_command(event):
    all_users = list(users.find({}))
    users_with_total_balance = []

    for user_data in all_users:
        balance = user_data.get('balance', 0)
        vault_balance = user_data.get('vault_balance', 0)
        total_balance = balance + vault_balance
        users_with_total_balance.append({
            "_id": user_data["_id"],
            "total_balance": total_balance
        })
    users_with_total_balance.sort(key=lambda x: x["total_balance"], reverse=True)

    top_users = users_with_total_balance[:10]

    if not top_users:
        await event.reply("📊 No users found with a balance to display on the leaderboard.")
        return

    response_text = "👑 --Top 10 Richest Users--\n\n"
    for i, user_data in enumerate(top_users):
        user_id = user_data["_id"]
        total_balance = user_data["total_balance"]
        try:
            user_entity = await client.get_entity(user_id)
            user_display_name = user_entity.first_name if user_entity.first_name else (f"@{user_entity.username}" if user_entity.username else f"User {user_id}")
            if user_entity.username:
                user_display_name = f"[{user_display_name}](tg://user?id={user_id})"
            else:
                user_display_name = f"[{user_display_name}](tg://user?id={user_id})"
        except Exception:
            user_display_name = f"User {user_id}"
        
        response_text += f"{i+1}. {user_display_name} ⇒ ₹{total_balance:,}\n"

    try:
        await client.send_message(event.chat_id, message=response_text, file=TOP_USERS_IMAGE_URL, parse_mode='md')
    except Exception as e:
        print(f"Failed to send /leaderboard image: {e}. Sending text message instead.")
        await event.reply(response_text, parse_mode='md')

@client.on(events.NewMessage(pattern=r"/bban (\d+)"))
async def bban_user_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply('❌ You are not authorized to use this command.')
        return

    target_user_id = int(event.pattern_match.group(1))

    target_user = users.find_one({"_id": target_user_id})
    if not target_user:
        await event.reply(f"❌ User {target_user_id} not found in bot's database.")
        return

    if target_user.get('is_banned', False):
        await event.reply(f"ℹ️ User {target_user_id} is already banned.")
        return

    users.update_one({"_id": target_user_id}, {"$set": {"is_banned": True}})
    await event.reply(f"✅ User {target_user_id} has been banned.")

@client.on(events.NewMessage(pattern=r"/bban", func=lambda e: e.is_reply))
async def bban_user_reply_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply('❌ You are not authorized to use this command.')
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("❌ Please reply to a user's message to ban them.")
        return

    target_user_id = reply_msg.sender_id

    target_user = users.find_one({"_id": target_user_id})
    if not target_user:
        await event.reply(f"❌ User {target_user_id} not found in bot's database.")
        return

    if target_user.get('is_banned', False):
        await event.reply(f"ℹ️ User {target_user_id} is already banned.")
        return
    
    users.update_one({"_id": target_user_id}, {"$set": {"is_banned": True}})
    await event.reply(f"✅ User {target_user_id} has been banned.")

@client.on(events.NewMessage(pattern=r"/unbban (\d+)"))
async def unbban_user_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply('❌ You are not authorized to use this command.')
        return

    target_user_id = int(event.pattern_match.group(1))

    target_user = users.find_one({"_id": target_user_id})
    if not target_user:
        await event.reply(f"❌ User {target_user_id} not found in bot's database.")
        return

    if not target_user.get('is_banned', False):
        await event.reply(f"ℹ️ User {target_user_id} is not currently banned.")
        return

    users.update_one({"_id": target_user_id}, {"$set": {"is_banned": False}})
    await event.reply(f"✅ User {target_user_id} has been unbanned.")

@client.on(events.NewMessage(pattern=r"/unbban", func=lambda e: e.is_reply))
async def unbban_user_reply_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply('❌ You are not authorized to use this command.')
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("❌ Please reply to a user's message to unban them.")
        return

    target_user_id = reply_msg.sender_id

    target_user = users.find_one({"_id": target_user_id})
    if not target_user:
        await event.reply(f"❌ User {target_user_id} not found in bot's database.")
        return

    if not target_user.get('is_banned', False):
        await event.reply(f"ℹ️ User {target_user_id} is not currently banned.")
        return

    users.update_one({"_id": target_user_id}, {"$set": {"is_banned": False}})
    await event.reply(f"✅ User {target_user_id} has been unbanned.")

@client.on(events.NewMessage(pattern=r"/sellfish (.+?)(?:\\s+(\\d+|all))?$"))
@check_suspension
@handle_flood_control
async def sellfish_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    fish_name_raw = event.pattern_match.group(1).strip()
    quantity_str = event.pattern_match.group(2)

    fishing_inventory = user.get('fishing_inventory', [])

    if not fishing_inventory:
        await event.reply("🎣 Your fishing inventory is empty. Nothing to sell!")
        return

    fish_to_sell = []
    total_value = 0
    sold_count = 0
    remaining_inventory = []
    def normalize_name(name):
        return name.lower().replace('-', ' ')

    normalized_sell_name = normalize_name(fish_name_raw)
    for item in fishing_inventory:
        normalized_item_name = normalize_name(item["name"])
        if normalized_item_name == normalized_sell_name:
            fish_to_sell.append(item)
        else:
            remaining_inventory.append(item)

    if not fish_to_sell:
        await event.reply(f"❌ You don't have any '{fish_name_raw}' in your inventory.")
        return

    if quantity_str and quantity_str.lower() != 'all':
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                await event.reply("❌ Quantity must be a positive number.")
                return
        except ValueError:
            await event.reply("❌ Invalid quantity. Please specify a number or 'all'.")
            return
        
        if quantity > len(fish_to_sell):
            await event.reply(f"❌ You only have {len(fish_to_sell)} {fish_name_raw}(s) to sell.")
            return
        selected_fish = fish_to_sell[:quantity]
        remaining_inventory.extend(fish_to_sell[quantity:])

    else:
        selected_fish = fish_to_sell

    for fish_item in selected_fish:
        total_value += fish_item["value"]
        sold_count += 1

    users.update_one(
        {"_id": user_id},
        {"$inc": {"balance": total_value}, "$set": {"fishing_inventory": remaining_inventory}}
    )

    await event.reply(f"✅ Successfully sold {sold_count} {fish_name_raw}(s) for ₹{total_value:,}!")

@client.on(events.NewMessage(pattern=r"/referral"))
@check_suspension
@handle_flood_control
async def referral_command(event):
    user_id = event.sender_id

    if not event.is_private:
        bot_entity = await client.get_me()
        bot_username = bot_entity.username if bot_entity.username else "@Eren_Yeagerrobot"
        buttons = [[Button.url("Refer Link", f"https://t.me/{bot_username}?start=referral")] ]
        await event.reply("Message me privately to get your refer link", buttons=buttons)
        return

    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return
    
    referral_code = user.get('referral_code')
    referrals_count = user.get('referrals_count', 0)

    if not referral_code:
        new_referral_code = str(uuid.uuid4())[:8]
        users.update_one({"_id": user_id}, {"$set": {"referral_code": new_referral_code}})
        referral_code = new_referral_code

    bot_entity = await client.get_me()
    bot_username = bot_entity.username if bot_entity.username else "@Eren_Yeagerrobot"

    referral_link = f"https://t.me/{bot_username}?start=ref_{referral_code}"

    response_message = (
        f'''🔗 **Your Unique Referral Link:**

{referral_link}

Share this link with your friends! When they join the bot using your link and become a registered user, you will receive rewards.

**👥 Your Current Referrals:** {referrals_count}

**Referral Rewards:**
• Every invite: ₹10,000 coins
• Every 4 invites: +₹20,000 coins + Ꝿ1 Kryon
• Every 10 invites: +₹50,000 coins + Ꝿ2 Kryon
• Every 16 invites: +₹75,000 coins + Random Character
• Every 26 invites: +₹85,000 coins + Special Rarity Character + Ꝿ2 Kryon
• Every 40 invites: +₹100,000 coins + Ꝿ10 Kryon
• Every 50 invites: +₹100,000 coins + Ꝿ100 Kryon
(New users joining via your link also receive an extra ₹20,000 joining bonus!)
'''
    )
    
    await event.reply(response_message, parse_mode='md')
SHOP_ITEMS = {
    "item1": {
        "name": "Character Pack",
        "description": "Receive a random rare character!",
        "cost_kryon": 500,
        "type": "character_pack"
    },
    "item2": {
        "name": "XP Boost (Small)",
        "description": "Gain 5000 XP instantly! (Currently a placeholder for future temporary buffs)",
        "cost_kryon": 100,
        "type": "xp_boost",
        "amount": 5000
    },
    "item3": {
        "name": "Coin Multiplier (1 Hour)",
        "description": "Double your coin gains for 1 hour! (Currently a placeholder for future temporary buffs)",
        "cost_kryon": 200,
        "type": "coin_multiplier",
        "duration_minutes": 60
    },
    "item4": {
        "name": "Fishing Rod",
        "description": f"A sturdy fishing rod with {MAX_ROD_DURABILITY} uses. Essential for fishing!",
        "cost_kryon": 50, 
        "type": "fishing_rod"
    },
    "item5": {
        "name": "Scout Gear",
        "description": f"Essential gear for scouting missions. {MAX_SCOUT_DURABILITY} uses.",
        "cost_kryon": 50,
        "type": "scout_gear",
    }
}

@client.on(events.NewMessage(pattern="/shop"))
@check_suspension
@handle_flood_control
async def shop_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    shop_message = "🛍️ **Welcome to the Shop!** 🛍️\n\n"
    shop_message += "To purchase Kryon (our premium currency), please contact `@Eren_yager_god`  for payment details. Once you've made a payment, send a screenshot of your payment to `@Eren_yager_god` for verification.\n\n"
    shop_message += "**Current Kryon Price:** 100 Kryon = ₹40 INR \n\n" # Added Kryon price here
    shop_message += "Here's what you can buy with Kryon:\n\n"

    buttons = []
    for item_id, item_data in SHOP_ITEMS.items():
        shop_message += f"**{item_data['name']}**\n"
        shop_message += f"  Cost: Ꝿ{item_data['cost_kryon']:,} Kryon\n"
        shop_message += f"  Description: **{item_data['description']}**\n\n"
        buttons.append([Button.inline(f"Buy {item_data['name']} (Ꝿ{item_data['cost_kryon']:,})", data=f"buy_shop_item_{item_id}")])
    
    await event.reply(shop_message, buttons=buttons, parse_mode='md')

@client.on(events.CallbackQuery(data=lambda d: d.startswith(b"buy_shop_item_")))
@check_suspension
async def handle_shop_buy_callback(event):
    user_id = event.sender_id
    item_id = event.data.decode().split("_")[3]

    user = users.find_one({"_id": user_id})
    if not user:
        await event.answer("❌ You are not registered. Use /start first.")
        return

    item_data = SHOP_ITEMS.get(item_id)

    if not item_data:
        await event.answer("❌ Invalid item selected.")
        return

    current_kryon_balance = user.get('kryon_balance', 0)
    cost = item_data['cost_kryon']

    if current_kryon_balance < cost:
        await event.answer(f"❌ Not enough Kryon! You need Ꝿ{cost:,} but have Ꝿ{current_kryon_balance:,}.", alert=True)
        return
    users.update_one({"_id": user_id}, {"$inc": {"kryon_balance": -cost}})
    if item_data['type'] == "character_pack":
        summoned_character = await get_random_character_from_db(is_raredrop_only=False)
        if summoned_character:
            users.update_one(
                {"_id": user_id},
                {"$push": {"characters": summoned_character}},
                upsert=True
            )
            await event.answer(f"✅ You bought a {item_data['name']} and received **{summoned_character['name']}** ({summoned_character['rarity']})!", alert=True)
            await client.send_message(event.chat_id, f"🎉 Congratulations! You received **{summoned_character['name']}** ({summoned_character['rarity']}) from your Character Pack!")
        else:
            await event.answer("❌ No characters available to be summoned. Please contact an admin.", alert=True)
            users.update_one({"_id": user_id}, {"$inc": {"kryon_balance": cost}})

    elif item_data['type'] == "xp_boost":
        xp_amount = item_data['amount']
        await give_xp(user_id, xp_amount)
        await event.answer(f"✅ You bought a {item_data['name']} and gained {xp_amount:,} XP!", alert=True)
        await client.send_message(event.chat_id, f"🎉 Your XP has been boosted by {xp_amount:,}!")

    elif item_data['type'] == "coin_multiplier":
        bonus_coins = 100000 
        users.update_one({"_id": user_id}, {"$inc": {"balance": bonus_coins}})
        await event.answer(f"✅ You bought a {item_data['name']} and received ₹{bonus_coins:,} as a temporary placeholder!", alert=True)
        await client.send_message(event.chat_id, f"🎉 You received a Coin Multiplier! (For now, you've gained ₹{bonus_coins:,} as a bonus)")

    elif item_data['type'] == "fishing_rod":
        users.update_one({"_id": user_id}, {"$set": {"fishing_rod_durability": MAX_ROD_DURABILITY}})
        await event.answer(f"✅ You bought a new Fishing Rod! It has {MAX_ROD_DURABILITY} uses.", alert=True)
        await client.send_message(event.chat_id, f"🎣 You bought a new Fishing Rod! You can now use /fish {MAX_ROD_DURABILITY} times.")

    elif item_data['type'] == "scout_gear":
        users.update_one({"_id": user_id}, {"$set": {"scouting_gear_durability": MAX_SCOUT_DURABILITY}})
        await event.answer(f"✅ You bought new Scout Gear! It has {MAX_SCOUT_DURABILITY} uses.", alert=True)
        await client.send_message(event.chat_id, f"🗺️ You bought new Scout Gear! You can now use /scout {MAX_SCOUT_DURABILITY} times.")

    else:
        await event.answer(f"✅ You bought a {item_data['name']}! (Effect not yet implemented for this item type)", alert=True)

    try:
        updated_kryon_balance = users.find_one({"_id": user_id}).get('kryon_balance', 0)
        await event.edit(f"You purchased an item! Your new Kryon balance: Ꝿ{updated_kryon_balance:,}", buttons=None)
    except Exception as e:
        print(f"Error editing shop message after purchase: {e}")

@client.on(events.NewMessage(pattern=r"/addkryon (\d+) (\d+)"))
async def add_kryon_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply('❌ You are not authorized to use this command.')
        return

    match = event.pattern_match
    target_user_id = int(match.group(1))
    amount = int(match.group(2))

    if amount <= 0:
        await event.reply("❌ Amount must be positive.")
        return

    target_user = users.find_one({"_id": target_user_id})
    if not target_user:
        await event.reply(f"❌ User {target_user_id} not found in bot's database.")
        return
    
    users.update_one({"_id": target_user_id}, {"$inc": {"kryon_balance": amount}})
    await event.reply(f"✅ Successfully added Ꝿ{amount:,} Kryon to user {target_user_id}.")

@client.on(events.NewMessage(pattern=r"/airdrop (\d+) (coins|kryon)"))
async def airdrop_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply('❌ You are not authorized to use this command.')
        return

    match = event.pattern_match
    amount = int(match.group(1))
    currency_type = match.group(2).lower()

    if amount <= 0:
        await event.reply("❌ Airdrop amount must be positive.")
        return

    update_field = ""
    currency_symbol = ""
    if currency_type == "coins":
        update_field = "balance"
        currency_symbol = "₹"
    elif currency_type == "kryon":
        update_field = "kryon_balance"
        currency_symbol = "Ꝿ"
    else:
        await event.reply("❌ Invalid currency type. Use 'coins' or 'kryon'.")
        return
    success_count = 0
    for user_doc in users.find({}):
        try:
            recipient_entity = await client.get_entity(user_doc['_id'])
            user_first_name = recipient_entity.first_name if recipient_entity else "User"

            if currency_type == "coins":
                current_balance = user_doc.get('balance', 0)
                new_balance = min(current_balance + amount, MAX_BALANCE_LIMIT)
                users.update_one({"_id": user_doc['_id']}, {"$set": {update_field: new_balance}})
                if new_balance < current_balance + amount:
                    personal_message = (
                        f"HURR!!! {user_first_name}\n\n"
                        f"airplane mistakenly drop {currency_symbol}{amount:,} {currency_type}\n\n"
                        f"you are lucky today (Balance capped at ₹{MAX_BALANCE_LIMIT:,})"
                    )
                else:
                    personal_message = (
                        f"HURR!!! {user_first_name}\n\n"
                        f"airplane mistakenly drop {currency_symbol}{amount:,} {currency_type}\n\n"
                        f"you are lucky today "
                    )
            else:
                users.update_one({"_id": user_doc['_id']}, {"$inc": {update_field: amount}})
                personal_message = (
                    f"HURR!!! {user_first_name}\n\n"
                    f"airplane mistakenly drop {currency_symbol}{amount:,} {currency_type}\n\n"
                    f"you are lucky today "
                )

            success_count += 1
            print(f"Airdropped {amount} {currency_type} to user {user_doc['_id']}")
            try:
                await client.send_message(user_doc['_id'], personal_message)
            except Exception as notify_e:
                print(f"Failed to send airdrop notification to user {user_doc['_id']}: {notify_e}")

        except Exception as e:
            print(f"Failed to airdrop to user {user_doc['_id']}: {e}")
            
    await event.reply(f"✅ Successfully airdropped {currency_symbol}{amount:,} {currency_type} to {success_count} users!")

@client.on(events.NewMessage(pattern=r"/exchangekryon (\d+) (.+)"))
@check_suspension
@handle_flood_control
async def exchange_kryon_command(event):
    user_id = event.sender_id
    match = event.pattern_match
    kryon_cost = int(match.group(1))
    character_code = match.group(2).strip()

    if not event.is_private:
        await event.respond("❌ This command can only be used in my private chat.")
        return

    user = users.find_one({"_id": user_id})
    if not user:
        await event.respond("❌ You are not registered yet. Use /start first.")
        return
    
    if kryon_cost <= 0:
        await event.respond("❌ Kryon amount must be positive.")
        return

    current_kryon_balance = user.get('kryon_balance', 0)
    if current_kryon_balance < kryon_cost:
        await event.respond(f"❌ Not enough Kryon! You need Ꝿ{kryon_cost:,} but have Ꝿ{current_kryon_balance:,}.")
        return
    character_to_exchange = characters_db.find_one({"_id": character_code})
    if not character_to_exchange:
        await event.respond(f"❌ Character with code `{character_code}` not found in the character database.")
        return
    user_characters = user.get('characters', [])
    if any(char["_id"] == character_code for char in user_characters):
        await event.respond(f"❌ You already own **{character_to_exchange['name']}** (Code: `{character_code}`).")
        return
    users.update_one({"_id": user_id}, {"$inc": {"kryon_balance": -kryon_cost}})
    users.update_one(
        {"_id": user_id},
        {"$push": {"characters": character_to_exchange}},
        upsert=True
    )
    await event.respond(
        f"✅ Successfully exchanged Ꝿ{kryon_cost:,} Kryon for **{character_to_exchange['name']}** "
        f"({character_to_exchange['rarity']}) (Code: `{character_code}`). "
        f"It has been added to your collection!"
    )


@client.on(events.NewMessage(pattern=r"/refreshgames"))
@check_suspension
@handle_flood_control
async def refresh_games_command(event):
    user_id = event.sender_id

    refreshed_games = []

    if user_id in active_higherlower_games:
        if active_higherlower_games[user_id].get("game_type") == "solo":
            del active_higherlower_games[user_id]
            refreshed_games.append("Higher or Lower (solo)")
        else:
            games_to_clear = [
                game_id for game_id, game_data in active_higherlower_games.items()
                if game_data.get("game_type") == "challenge" and \
                   (game_data.get("challenger_id") == user_id or game_data.get("challenged_id") == user_id)
            ]
            for game_id in games_to_clear:
                del active_higherlower_games[game_id]
                refreshed_games.append(f"Higher or Lower (challenge ID: {game_id[:8]}...)")


    if user_id in active_bet_games:
        del active_bet_games[user_id]
        refreshed_games.append("Bet Game")

    if refreshed_games:
        await event.reply(f"✅ Your active games have been refreshed: {', '.join(refreshed_games)}.")
    else:
        await event.reply("ℹ️ You had no active games to refresh.")

@client.on(events.NewMessage(pattern=r"/bluffmaster (?P<bet_amount>\d+)?"))
@check_suspension
@handle_flood_control
async def bluffmaster_command(event):
    user_id = event.sender_id
    chat_id = event.chat_id
    bet_amount_str = event.pattern_match.group('bet_amount')
    bet_amount = int(bet_amount_str) if bet_amount_str else 0 

    user = users.find_one({"_id": user_id})
    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    if bet_amount < 0:
        await event.reply("❌ Bet amount cannot be negative.")
        return
    
    if bet_amount > user.get('balance', 0):
        await event.reply("❌ You don't have enough balance to start this game with that bet.")
        return
    for game_id, game_data in active_bluffmaster_games.items():
        if user_id in game_data['players']:
            await event.reply("⚠️ You are already in an active Bluff Master game! Please finish it or wait.")
            return

    game_id = str(uuid.uuid4())[:8] 
    active_bluffmaster_games[game_id] = {
        "status": "waiting_for_players",
        "players": [user_id],
        "host_id": user_id,
        "chat_id": chat_id,
        "bet_amount": bet_amount,
        "message_id": None,
        "player_hands": {},
        "current_player_turn": None,
        "last_bid": None,
        "turn_order": [],
        "penalty_points": {user_id: 0},
        "game_round": 0
    }

    host_name = (await client.get_entity(user_id)).first_name
    buttons = [
        [Button.inline("Join Game", data=f"bluffmaster_join_{game_id}")],
        [Button.inline("Start Game", data=f"bluffmaster_start_{game_id}")]
    ]

    game_message = (
        f"🃏 Bluff Master Game (ID: `{game_id}`)\n\n"
        f"Host: {host_name}\n"
        f"Bet per player: ₹{bet_amount:,}\n"
        f"Players joined: 1 (Currently: {host_name})\n\n"
        f"Click 'Join Game' to participate! Host can click 'Start Game' when ready."
    )

    msg = await event.reply(game_message, buttons=buttons, parse_mode='md')
    active_bluffmaster_games[game_id]["message_id"] = msg.id

    await event.reply(f"Bluff Master game created with ID: `{game_id}`. Waiting for players...")


@client.on(events.CallbackQuery(data=lambda d: d.startswith(b"bluffmaster_join_")))
@check_suspension
@handle_flood_control
async def handle_bluffmaster_join_callback(event):
    user_id = event.sender_id
    game_id = event.data.decode().split("_")[2]
    
    game = active_bluffmaster_games.get(game_id)

    if not game:
        await event.answer("❌ This game does not exist or has ended.", alert=True)
        return

    if game["status"] != "waiting_for_players":
        await event.answer("❌ This game has already started or is no longer accepting players.", alert=True)
        return

    if user_id in game['players']:
        await event.answer("⚠️ You have already joined this game!", alert=True)
        return


    user_data = users.find_one({"_id": user_id})
    if not user_data or user_data.get('balance', 0) < game['bet_amount']:
        await event.answer(f"❌ You don't have enough balance (₹{game['bet_amount']:,}) to join this game.", alert=True)
        return

    game['players'].append(user_id)
    game['penalty_points'][user_id] = 0 
    
    player_names = []
    for p_id in game['players']:
        try:
            entity = await client.get_entity(p_id)
            player_names.append(entity.first_name)
        except Exception:
            player_names.append(f"User_{p_id}") 

    host_name = (await client.get_entity(game['host_id'])).first_name
    buttons = [
        [Button.inline("Join Game", data=f"bluffmaster_join_{game_id}")],
        [Button.inline("Start Game", data=f"bluffmaster_start_{game_id}")]
    ]

    game_message = (
        f"🃏 Bluff Master Game (ID: `{game_id}`)\n\n"
        f"Host: {host_name}\n"
        f"Bet per player: ₹{game['bet_amount']:,}\n"
        f"Players joined: {len(game['players'])} (Currently: {', '.join(player_names)})\n\n"
        f"Click 'Join Game' to participate! Host can click 'Start Game' when ready."
    )

    await event.edit(game_message, buttons=buttons, parse_mode='md')
    await event.answer("✅ You have joined the Bluff Master game!", alert=True)


@client.on(events.CallbackQuery(data=lambda d: d.startswith(b"bluffmaster_start_")))
@check_suspension
@handle_flood_control
async def handle_bluffmaster_start_callback(event):
    user_id = event.sender_id
    game_id = event.data.decode().split("_")[2]
    
    game = active_bluffmaster_games.get(game_id)

    if not game:
        await event.answer("❌ This game does not exist or has ended.", alert=True)
        return

    if user_id != game['host_id']:
        await event.answer("❌ Only the host can start the game!", alert=True)
        return

    if game["status"] != "waiting_for_players":
        await event.answer("❌ This game has already started or cannot be started.", alert=True)
        return

    if len(game['players']) < 2:
        await event.answer("❌ You need at least 2 players to start the game.", alert=True)
        return
    players_in_game_after_check = []
    for p_id in game['players']:
        user_data = users.find_one({"_id": p_id})
        if user_data and user_data.get('balance', 0) >= game['bet_amount']:
            users.update_one({"_id": p_id}, {"$inc": {"balance": -game['bet_amount']}})
            game['player_hands'][p_id] = random.randint(1, 6)
            players_in_game_after_check.append(p_id)
        else:
            game['penalty_points'].pop(p_id, None)

    game['players'] = players_in_game_after_check

    if len(game['players']) < 2:
        await event.edit("❌ Not enough players with sufficient balance to start the game. Game cancelled.", buttons=None)
        del active_bluffmaster_games[game_id]
        return

    shuffled_players = random.sample(game['players'], len(game['players']))
    game['turn_order'] = shuffled_players
    game['current_player_turn'] = shuffled_players[0] 
    game['status'] = "in_progress"

    all_player_names = []
    for p_id in game['players']:
        all_player_names.append((await client.get_entity(p_id)).first_name)

    for p_id, card in game['player_hands'].items():
        try:
            await client.send_message(p_id, f"🃏 Bluff Master Game (ID: `{game_id}`): Your secret number is **{card}**.")
        except Exception as e:
            print(f"Failed to send private card to user {p_id}: {e}")

    first_player_name = (await client.get_entity(game['current_player_turn'])).first_name
    
    game_message = (
        f"🃏 Bluff Master Game (ID: `{game_id}`) - Started!\n\n"
        f"Players: {', '.join(all_player_names)}\n"
        f"Bet per player: ₹{game['bet_amount']:,}\n\n"
        f"It's {first_player_name}'s turn! {first_player_name}, use `/place [number]` to place your card."
    )

    await event.edit(game_message, buttons=None, parse_mode='md')
    await event.answer("✅ Game started! Check your private messages for your secret card.", alert=True)

async def hourly_tax_task():
    while True:
        await asyncio.sleep(3600)
        print("[Hourly Tax Task] Starting hourly tax collection.")

        all_users = list(users.find({}))
        users_with_balance = sorted(
            [u for u in all_users if u.get('balance', 0) > 0],
            key=lambda x: x.get('balance', 0),
            reverse=True
        )

        num_top_users = max(1, int(len(users_with_balance) * 0.10))
        top_user_ids = {u['_id'] for u in users_with_balance[:num_top_users]}

        for user in all_users:
            user_id = user['_id']
            current_balance = user.get('balance', 0)
            if current_balance <= 0:
                continue 
            tax_rate = 0.01 
            if user_id in top_user_ids:
                tax_rate = 0.05 

            tax_amount = int(current_balance * tax_rate)
            if current_balance - tax_amount < 0:
                tax_amount = current_balance
            users.update_one(
                {"_id": user_id},
                {"$inc": {"balance": -tax_amount}}
            )
            print(f"[Hourly Tax Task] Deducted ₹{tax_amount:,} ({tax_rate*100:.0f}%) from user {user_id}'s balance. New balance: ₹{current_balance - tax_amount:,}")

        print("[Hourly Tax Task] Hourly tax collection completed.")

asyncio.get_event_loop().create_task(hourly_tax_task())


@client.on(events.NewMessage(pattern=r"/deduct"))
async def deduct_top_users_command(event):
    if event.sender_id != ADMIN_ID:
        await event.reply('❌ You do not have permission to use this command.')
        return

    all_users = list(users.find({}))
    users_with_total_balance = []

    for user_data in all_users:
        balance = user_data.get('balance', 0)
        vault_balance = user_data.get('vault_balance', 0)
        total_balance = balance + vault_balance
        users_with_total_balance.append({
            "_id": user_data["_id"],
            "total_balance": total_balance
        })

    users_with_total_balance.sort(key=lambda x: x["total_balance"], reverse=True)

    top_users = users_with_total_balance[:10]
    affected_users = []

    for user_data in top_users:
        user_id = user_data["_id"]
        users.update_one({"_id": user_id}, {"$set": {"balance": 2_000_000, "level": 10, "xp": 0, "level_up_xp": 10056}})
        try:
            await client.send_message(user_id, "⚠️ Your balance has been set to ₹20,000,000 and your level/XP reset by the bot admin due to a leaderboard reset.")
        except Exception:
            pass
        affected_users.append(str(user_id))

    await event.reply(f"✅ Deducted top 10 users' balances to ₹20,000,000 and reset their levels/XP. User IDs affected: {', '.join(affected_users)}")


@client.on(events.NewMessage(pattern=r"/take (\d+) (\d+)"))
@check_suspension
async def take_coins(event):
    if event.sender_id != ADMIN_ID:
        await event.reply("❌ You are not authorized to use this command.")
        return

    match = event.pattern_match
    target_user_id = int(match.group(1))
    amount = int(match.group(2))

    if amount <= 0:
        await event.reply("❌ Amount must be positive.")
        return

    target_user = users.find_one({"_id": target_user_id})
    if not target_user:
        await event.reply(f"❌ User {target_user_id} not found.")
        return

    if target_user['balance'] < amount:
        await event.reply(f"❌ User {target_user_id} only has ₹{target_user['balance']:,}. Cannot take ₹{amount:,}.")
        return

    users.update_one({"_id": target_user_id}, {"$inc": {"balance": -amount}})
    await event.reply(f"✅ Successfully took ₹{amount:,} from user {target_user_id}.")

@client.on(events.NewMessage(pattern=r"/set (\d+) (\d+)"))
@check_suspension
async def set_coins(event):
    if event.sender_id != ADMIN_ID:
        await event.reply("❌ You are not authorized to use this command.")
        return

    match = event.pattern_match
    target_user_id = int(match.group(1))
    amount = int(match.group(2))

    if amount < 0:
        await event.reply("❌ Amount cannot be negative.")
        return

    target_user = users.find_one({"_id": target_user_id})
    if not target_user:
        await event.reply(f"❌ User {target_user_id} not found.")
        return

    new_balance = min(amount, MAX_BALANCE_LIMIT) 
    users.update_one({"_id": target_user_id}, {"$set": {"balance": new_balance}})

    if new_balance < amount:
        await event.reply(f"✅ Successfully set balance of user {target_user_id} to ₹{new_balance:,}. (Capped at ₹{MAX_BALANCE_LIMIT:,})")
    else:
        await event.reply(f"✅ Successfully set balance of user {target_user_id} to ₹{new_balance:,}.")

@client.on(events.NewMessage(pattern=r"/transfer (\d+)", func=lambda e: e.is_reply))
@check_suspension
@handle_flood_control
async def transfer_coins(event):
    sender_id = event.sender_id
    match = event.pattern_match
    amount = int(match.group(1))

    if amount <= 0:
        await event.reply("❌ Amount must be positive.")
        return

    reply_msg = await event.get_reply_message()
    if not reply_msg:
        await event.reply("❌ Please reply to a user's message to use this command.")
        return

    target_user_id = reply_msg.sender_id

    if sender_id == target_user_id:
        await event.reply("❌ You cannot transfer coins to yourself.")
        return

    sender_user = users.find_one({"_id": sender_id})
    target_user = users.find_one({"_id": target_user_id})

    if not sender_user:
        await event.reply("❌ You are not registered. Use /start first.")
        return

    if not target_user:
        await event.reply(f"❌ The user you replied to (ID: {target_user_id}) is not registered or not found.")
        return

    if sender_user['balance'] < amount:
        await event.reply(f"❌ Not enough balance to transfer. Your balance: ₹{sender_user['balance']:,}.")
        return

    users.update_one({"_id": sender_id}, {"$inc": {"balance": -amount}})
    current_recipient_balance = target_user.get('balance', 0)
    new_recipient_balance = min(current_recipient_balance + amount, MAX_BALANCE_LIMIT)
    users.update_one({"_id": target_user_id}, {"$set": {"balance": new_recipient_balance}})

    if new_recipient_balance < current_recipient_balance + amount:
        await event.reply(f"✅ Successfully transferred ₹{amount:,} to user {target_user_id}. (User's balance capped at ₹{MAX_BALANCE_LIMIT:,})")
    else:
        await event.reply(f"✅ Successfully transferred ₹{amount:,} to user {target_user_id}.")

@client.on(events.NewMessage(pattern=r"/deposit (\d+)"))
@check_suspension
@handle_flood_control
async def deposit_coins(event):
    user_id = event.sender_id
    amount = int(event.pattern_match.group(1))

    if amount <= 0:
        await event.reply("❌ Deposit amount must be positive.")
        return

    if amount < 1000:
        await event.reply("❌ Minimum deposit amount is ₹1,000.")
        return

    user = users.find_one({"_id": user_id})
    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    user_balance = user.get('balance', 0)
    user_vault_balance = user.get('vault_balance', 0)
    user_vault_capacity = user.get('user_vault_capacity', VAULT_CAPACITY) 

    if user_balance < amount:
        await event.reply(f"❌ Not enough Balance to deposit. Your current Balance: ₹{user_balance:,}.")
        return

    if user_vault_balance + amount > user_vault_capacity:
        await event.reply(f"❌ Vault capacity exceeded! You can only deposit up to ₹{user_vault_capacity - user_vault_balance:,} more.")
        return

    users.update_one(
        {"_id": user_id},
        {"$inc": {"balance": -amount, "vault_balance": amount}}
    )
    await event.reply(f"✅ Successfully deposited ₹{amount:,} to your vault.")


@client.on(events.NewMessage(pattern=r"/withdraw (\d+)"))
@check_suspension
@handle_flood_control
async def withdraw_coins(event):
    user_id = event.sender_id
    amount = int(event.pattern_match.group(1))

    if amount <= 0:
        await event.reply("❌ Withdraw amount must be positive.")
        return

    if amount < 1000:
        await event.reply("❌ Minimum withdrawal amount is ₹1,000.")
        return

    user = users.find_one({"_id": user_id})
    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    user_vault_balance = user.get('vault_balance', 0)

    if user_vault_balance < amount:
        await event.reply(f"❌ Not enough coins in your vault to withdraw. Your vault balance: ₹{user_vault_balance:,}.")
        return

    current_balance = user.get('balance', 0)
    potential_new_balance = current_balance + amount

    if potential_new_balance > MAX_BALANCE_LIMIT:
        warning_message = (
            f"⚠️ Warning: Withdrawing ₹{amount:,} would exceed your maximum balance limit of ₹{MAX_BALANCE_LIMIT:,}.\n"
            f"Your balance will be capped at ₹{MAX_BALANCE_LIMIT:,}."
        )
        await event.reply(warning_message)
        return

    new_balance = min(current_balance + amount, MAX_BALANCE_LIMIT)

    users.update_one(
        {"_id": user_id},
        {"$set": {"balance": new_balance}, "$inc": {"vault_balance": -amount}}
    )
    if new_balance < current_balance + amount:
        await event.reply(f"✅ Successfully withdrew ₹{amount:,} from your vault. Your balance is now ₹{new_balance:,} (capped at ₹{MAX_BALANCE_LIMIT:,}).")
    else:
        await event.reply(f"✅ Successfully withdrew ₹{amount:,} from your vault.")

@client.on(events.NewMessage(pattern=r"/updatevault"))
@check_suspension
@handle_flood_control
async def update_vault_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    user_level = user.get('level', 1) 
    vault_upgrades_done = user.get('vault_upgrades_done', 0) 
    
    required_level = VAULT_UPGRADE_LEVEL_REQUIREMENT + vault_upgrades_done

    if user_level < required_level:
        await event.reply(f"❌ You need to be at least Level {required_level} to upgrade your vault. You are currently Level {user_level}.")
        return

    current_vault_capacity = user.get('user_vault_capacity', VAULT_CAPACITY)
    if current_vault_capacity >= MAX_VAULT_CAPACITY:
        await event.reply(f"✅ Your vault is already at maximum capacity (₹{MAX_VAULT_CAPACITY:,}).")
        return

    user_balance = user.get('balance', 0)
    if user_balance < VAULT_UPGRADE_COST:
        await event.reply(f"❌ Not enough balance to upgrade. You need ₹{VAULT_UPGRADE_COST:,} but have ₹{user_balance:,}.")
        return

    new_vault_capacity = min(current_vault_capacity + VAULT_UPGRADE_AMOUNT, MAX_VAULT_CAPACITY)
    cost_to_deduct = VAULT_UPGRADE_COST

    users.update_one(
        {"_id": user_id},
        {"$inc": {"balance": -cost_to_deduct, "vault_upgrades_done": 1}, "$set": {"user_vault_capacity": new_vault_capacity}}
    )


    await event.reply(
        f"🎉 Your vault capacity has been upgraded from ₹{current_vault_capacity:,} to ₹{new_vault_capacity:,} for a cost of ₹{cost_to_deduct:,}."
    )
   

@client.on(events.NewMessage(pattern="/help"))
@check_suspension
async def help_command(event):
    help_message = """
📚 **Bot Commands Reference** 📚

**💰 Economy Commands:**
`/bal` or `/balance` - Check your current balance and vault.
`/daily` - Claim your daily bonus.
`/deposit <amount>` - Deposit coins from your balance to your vault.
`/withdraw <amount>` - Withdraw coins from your vault to your balance.
`/rob` (reply to user) - Attempt to rob another user's balance.
`/bankrob` - Attempt to rob the global bank vault. Use with caution!
`/transfer <amount>` (reply to user) - Transfer coins to another user.
`/shop` - Browse and purchase items with Kryon.
`/sellfish <fish name> [quantity|all]` - Sell fish from your inventory for coins.
`/exchangekryon <kryon_amount> <character_code>` - Exchange Kryon for a specific character (DM only).

**🎲 Game Commands:**
`/dice <amount> <even|odd|e|o>` - Bet on dice roll (even/odd).
`/bet <amount>` - Start a minesweeper-like game.
`/basket <amount>` - Play a basketball game.
`/football <amount>` - Play a football game.
`/spin <amount>` - Play a lucky spin game for coins and Kryon (DM only).
`/higherlower <amount>` - Play a higher or lower card game.

**🎭 Character & Collection Commands:**
`/collection` - View your collected characters.
`/show <character name/code>` - View details of a specific character in your collection.
`/fish` - Go fishing and catch items.
`/listfish` - View your fishing inventory.
`/scout` - Go scouting and find items.
`/listscout` - View your scouting inventory.

**🛡️ Mode Commands:**
`/passive` - Switch to passive mode (immune to user robberies, cannot rob others).
`/active` - Switch to active mode (can be robbed, can rob others).

**⚙️ Admin & Manager Commands:** (Requires special permissions)
`/donate <user_id> <amount>` - Admin: Give coins to a user. (Also works by replying)
`/take <user_id> <amount>` - Admin: Take coins from a user.
`/set <user_id> <amount>` - Admin: Set a user's balance.
`/removesuspension <user_id>` - Admin: Remove a user's suspension.
`/resettimer` (reply to user) - Admin: Reset all cooldowns/suspensions for a user.
`/upload <name> <anime_name> <rarity> <image_link>` - Promoted: Upload a new character.
`/rarecupload <name> <anime_name> <rarity> <image_link>` - Promoted: Upload a rare-drop-only character.
`/removechar <char_code>` - Admin: Remove a character by its unique code.
`/bbpromote <user_id>` (or reply) - Admin: Promote a user to character manager.
`/bbdemote <user_id>` (or reply) - Admin: Demote a character manager.
`/setdrop <threshold>` - Group Admin: Set message threshold for character drops in a group.
`/admindrop <threshold>` - Bot Admin: Set message threshold for character drops in a group (can override).
`/raredrop (start|stop)?` - Bot Admin: Trigger a single rare drop or toggle rare drop mode.
`/charstats` - Promoted: View statistics on uploaded characters.
`/ctop` - View top users by character collection count.
`/rank` - Admin: View top groups by characters collected.
`/top` - Admin: View global top collectors by total characters.
`/leaderboard` - View the top 10 richest users by total balance.
`/bban <user_id>` (or reply) - Admin: Permanently ban a user.
`/unbban <user_id>` (or reply) - Admin: Unban a user.
`/addkryon <user_id> <amount>` - Admin: Add Kryon to a user's balance.
`/airdrop <amount> <coins|kryon>` - Admin: Airdrop coins or Kryon to all users.
`/statsbot` - Admin: View bot usage statistics.
`/broadcast <message>` - Admin: Send a message to all users. (Also works by replying)
`/bbroad <message>` - Admin: Send a message to all groups. (Also works by replying)

For more detailed information on a specific command, type the command directly.
"""
    await event.respond(help_message, parse_mode='md')

@client.on(events.NewMessage(pattern=r"^/scout$"))
@check_suspension
@handle_flood_control
async def scout_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    current_gear_durability = user.get('scouting_gear_durability', 0)
    if current_gear_durability <= 0:
        await event.reply("🛡️ Your scouting gear is broken or missing! Please buy new gear from the /shop.")
        return

    now = datetime.now()
    last_scout_time = user.get("last_scout_time")

    if last_scout_time and (now - last_scout_time) < timedelta(minutes=SCOUT_COOLDOWN_MINUTES):
        time_left = timedelta(minutes=SCOUT_COOLDOWN_MINUTES) - (now - last_scout_time)
        minutes, seconds = divmod(time_left.seconds, 60)
        await event.reply(f"⏳ You can scout again in {minutes}m {seconds}s.")
        return

    await event.reply("🗺️ You set out on a scouting mission...")

    all_scouting_items = list(scouting_items_db.find({}))
    if not all_scouting_items:
        await event.reply("🗺️ There are no items to find! Please tell the bot owner to add some.")
        users.update_one({"_id": user_id}, {"$set": {"last_scout_time": now}})
        return
    total_weight = sum(item["weight"] for item in all_scouting_items)
    if total_weight == 0:
        found_item = random.choice(all_scouting_items)
    else:
        rand = random.uniform(0, total_weight)
        cumulative_weight = 0
        found_item = None
        for item in all_scouting_items:
            cumulative_weight += item["weight"]
            if rand < cumulative_weight:
                found_item = item
                break

    if not found_item:
        await event.reply("🗺️ You scouted but found nothing! Try again.")
        users.update_one({"_id": user_id}, {"$set": {"last_scout_time": now}})
        return

    new_gear_durability = current_gear_durability - 1
    users.update_one(
        {"_id": user_id},
        {"$set": {"scouting_gear_durability": new_gear_durability}}
    )

    users.update_one(
        {"_id": user_id},
        {"$push": {"scouting_inventory": found_item}},
        upsert=True
    )
    users.update_one(
        {"_id": user_id},
        {"$set": {"last_scout_time": now}}
    )

    xp_gain = max(5, found_item["value"] // 200)
    await give_xp(user_id, xp_gain)

    response_message = (
        f"🗺️ You scouted and found **{found_item['name']}** ({found_item['rarity']})! "
        f"It has been added to your inventory.\n"
    )
    if new_gear_durability > 0:
        response_message += f"Your scouting gear now has {new_gear_durability} uses left."
    else:
        response_message += f"Your scouting gear broke! Buy new gear from the /shop. It provides {MAX_SCOUT_DURABILITY} uses."

    await event.reply(response_message)

@client.on(events.NewMessage(pattern=r"^/listscout$"))
@check_suspension
@handle_flood_control
async def listscout_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    scouting_inventory = user.get('scouting_inventory', [])

    if not scouting_inventory:
        await event.reply("🗺️ Your scouting inventory is empty. Go scouting with /scout!")
        return

    item_counts = {}
    for item in scouting_inventory:
        key = (item["name"], item["rarity"])
        item_counts[key] = item_counts.get(key, 0) + 1

    response_text = "🗺️ **Your Scouting Inventory:**\n\n"
    for (name, rarity), count in item_counts.items():
        response_text += f"• {name} ({rarity}): {count}x\n"
    
    buttons = []
    if scouting_inventory:
        buttons.append(Button.inline("💸 Sell All Scout Items", data=b"sell_all_scout"))
    
    await event.reply(response_text, parse_mode='md', buttons=buttons)

@client.on(events.CallbackQuery(data=b"sell_all_scout"))
@check_suspension
@handle_flood_control
async def handle_sell_all_scout(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user:
        await event.reply("❌ You are not registered yet. Use /start first.")
        return

    scouting_inventory = user.get('scouting_inventory', [])

    if not scouting_inventory:
        await event.reply("🗺️ Your scouting inventory is empty. Go scouting with /scout!")
        return

    total_value = 0
    for item in scouting_inventory:
        item_name = item.get("name")
        if item_name and item_name in SCOUT_PRICES:
            total_value += SCOUT_PRICES[item_name]
        else:
            print(f"[WARNING] Unknown scouting item or missing price for: {item_name}")

    new_balance = min(user.get('balance', 0) + total_value, MAX_BALANCE_LIMIT)

    users.update_one(
        {"_id": user_id},
        {"$set": {"balance": new_balance, "scouting_inventory": []}}
    )

    await event.reply(f"💸 You sold all scouting items in your inventory for ₹{total_value:,}!")


@client.on(events.NewMessage(pattern=r"/place (\d+)"))
@check_suspension
@handle_flood_control
async def bluffmaster_place_command(event):
    print(f"[DEBUG] Entering bluffmaster_place_command for user {event.sender_id}")
    user_id = event.sender_id
    chat_id = event.chat_id
    placed_number = int(event.pattern_match.group(1))

    print(f"[DEBUG] bluffmaster_place_command: user_id={user_id}, chat_id={chat_id}, placed_number={placed_number}")

    try:
        game = None
        game_id = None
        for g_id, g_data in active_bluffmaster_games.items():
            if user_id in g_data['players']:
                game = g_data
                game_id = g_id
                break

        if not game:
            print(f"[DEBUG] bluffmaster_place_command: No active game found for user {user_id}.")
            await client.send_message(chat_id, "❌ You are not in an active Bluff Master game in this chat.")
            return

        print(f"[DEBUG] bluffmaster_place_command: Game found (ID: {game_id}), status: {game['status']}")

        if game["status"] != "in_progress":
            print(f"[DEBUG] bluffmaster_place_command: Game not in progress. Status: {game['status']}")
            await client.send_message(chat_id, "❌ The game is not in progress.")
            return

        if user_id != game['current_player_turn']:
            print(f"[DEBUG] bluffmaster_place_command: Not user's turn. Current turn: {game['current_player_turn']}")
            await client.send_message(chat_id, "❌ It's not your turn!")
            return
        
        if not (1 <= placed_number <= 6):
            print(f"[DEBUG] bluffmaster_place_command: Invalid placed number: {placed_number}")
            await client.send_message(chat_id, "❌ You can only place a number between 1 and 6.")
            return

        if game['last_bid'] is not None and placed_number <= game['last_bid']:
            print(f"[DEBUG] bluffmaster_place_command: Placed number {placed_number} is not higher than last bid {game['last_bid']}.")
            await client.send_message(chat_id, f"❌ You must place a number higher than the last bid of {game['last_bid']}.")
            return 

        game['last_bid'] = placed_number
        game['last_bid_player_id'] = user_id
        print(f"[DEBUG] bluffmaster_place_command: last_bid updated to {placed_number}, by user {user_id}")

        current_turn_index = game['turn_order'].index(user_id)
        next_turn_index = (current_turn_index + 1) % len(game['turn_order'])
        game['current_player_turn'] = game['turn_order'][next_turn_index]
        print(f"[DEBUG] bluffmaster_place_command: Turn advanced to {game['current_player_turn']}")

        current_player_entity = await client.get_entity(user_id)
        current_player_name = current_player_entity.first_name if current_player_entity else f"User_{user_id}"

        next_player_entity = await client.get_entity(game['current_player_turn'])
        next_player_name = next_player_entity.first_name if next_player_entity else f"User_{game['current_player_turn']}"
        print(f"[DEBUG] bluffmaster_place_command: Current player name: {current_player_name}, Next player name: {next_player_name}")

        player_names_for_display = []
        for p_id in game['players']:
            p_entity = await client.get_entity(p_id)
            player_names_for_display.append(p_entity.first_name if p_entity else f"User_{p_id}")

        updated_game_message = (
            f"🃏 Bluff Master Game (ID: `{game_id}`)\n\n"
            f"Players: {', '.join(player_names_for_display)}\n"
            f"Bet per player: ₹{game['bet_amount']:,}\n\n"
            f"Last bid: **{game['last_bid']}** by {current_player_name}\n\n"
            f"It's {next_player_name}'s turn! {next_player_name}, use `/place [number]` to place your card."
        )

        await client.edit_message(game['chat_id'], game['message_id'], updated_game_message, parse_mode='md')
        print(f"[DEBUG] bluffmaster_place_command: Main game message edited.")
        try:
            await client.send_message(game['current_player_turn'],
                                      f"🃏 Bluff Master Game (ID: `{game_id}`): It's your turn to play! "
                                      f"The last placed number was **{game['last_bid']}** by {current_player_name}. "
                                      f"Use `/place [number]` in the group chat to make your move or `/bluff` to call bluff.", parse_mode='md')
            print(f"[DEBUG] bluffmaster_place_command: DM sent to next player {next_player_name}.")
        except Exception as dm_err:
            print(f"[DEBUG] Failed to send DM to next player {next_player_name}: {dm_err}")
        if event.is_private:
            await client.send_message(chat_id, "✅ Your move has been placed.")
        else: 
            await client.send_message(chat_id, "✅ Your move has been placed. Check the main game message for updates.")


        print(f"[DEBUG] bluffmaster_place_command: Exiting successfully.")
    except Exception as e:
        print(f"[DEBUG] Error in bluffmaster_place_command caught by try-except: {e}")
        await client.send_message(chat_id, f"An unexpected error occurred while placing your number: {e}")
    print(f"[DEBUG] Exiting bluffmaster_place_command for user {user_id}")

@client.on(events.NewMessage(pattern=r"/bluff"))
@check_suspension
@handle_flood_control
async def bluff_command(event):
    print(f"[DEBUG] Entering bluff_command for user {event.sender_id}")
    user_id = event.sender_id
    chat_id = event.chat_id

    game = None
    game_id = None
    for g_id, g_data in active_bluffmaster_games.items():
        if user_id in g_data['players']:
            game = g_data
            game_id = g_id
            break

    if not game:
        print(f"[DEBUG] bluff_command: No active game found for user {user_id}.")
        await client.send_message(chat_id, "❌ You are not in an active Bluff Master game in this chat.")
        return

    print(f"[DEBUG] bluff_command: Game found (ID: {game_id}), status: {game['status']}")

    if game["status"] != "in_progress":
        print(f"[DEBUG] bluff_command: Game not in progress. Status: {game['status']}")
        await client.send_message(chat_id, "❌ The game is not in progress.")
        return
    if user_id != game['current_player_turn']:
        print(f"[DEBUG] bluff_command: Not user's turn. Current turn: {game['current_player_turn']}")
        await client.send_message(chat_id, "❌ It's not your turn to call bluff! It's currently "
                                   f"{(await client.get_entity(game['current_player_turn'])).first_name}'s turn.")
        return

    if user_id == game['last_bid_player_id']:
        print(f"[DEBUG] bluff_command: User tried to bluff their own bid.")
        await client.send_message(chat_id, "❌ You cannot bluff your own bid.")
        return

    if game['last_bid'] is None or game['last_bid_player_id'] is None:
        print(f"[DEBUG] bluff_command: No last bid to bluff.")
        await client.send_message(chat_id, "❌ There is no active bid to bluff. Someone needs to place a number first.")
        return
    bluffed_player_id = game['last_bid_player_id']
    bluffed_player_actual_card = game['player_hands'][bluffed_player_id]
    bluffed_player_bid = game['last_bid']

    bluffed_player_entity = await client.get_entity(bluffed_player_id)
    bluffed_player_name = bluffed_player_entity.first_name if bluffed_player_entity else f"User_{bluffed_player_id}"

    caller_entity = await client.get_entity(user_id)
    caller_name = caller_entity.first_name if caller_entity else f"User_{user_id}"

    outcome_message = ""
    is_bluff = (bluffed_player_actual_card != bluffed_player_bid)
    loser_id = None
    winner_id = None

    print(f"[DEBUG] bluff_command: Caller {caller_name} ({user_id}) called bluff on {bluffed_player_name} ({bluffed_player_id}).")
    print(f"[DEBUG] bluff_command: Bluffed player's actual card: {bluffed_player_actual_card}, Bid: {bluffed_player_bid}")

    if is_bluff:
        outcome_message = (
            f"🃏 {caller_name} called bluff on {bluffed_player_name}!\n"
            f"{bluffed_player_name}'s actual card was **{bluffed_player_actual_card}**, but they placed **{bluffed_player_bid}**.\n"
            f"It was a **BLUFF**! {bluffed_player_name} loses this round."
        )
        loser_id = bluffed_player_id
        winner_id = user_id 
    else:
        outcome_message = (
            f"🃏 {caller_name} called bluff on {bluffed_player_name}!\n"
            f"{bluffed_player_name}'s actual card was **{bluffed_player_actual_card}**, and they placed **{bluffed_player_bid}**.\n"
            f"It was **NOT a bluff**! {caller_name} loses this round for calling incorrectly."
        )
        loser_id = user_id 
        winner_id = bluffed_player_id 

    game['penalty_points'][loser_id] = game['penalty_points'].get(loser_id, 0) + 1
    print(f"[DEBUG] bluff_command: Player {loser_id} now has {game['penalty_points'][loser_id]} penalty points.")

    if game['penalty_points'][loser_id] >= 3: 
        print(f"[DEBUG] bluff_command: Game over! {loser_id} reached 3 penalty points.")
        game_over_message = f"\n\nGame Over! {bluffed_player_name} reached 3 penalty points. "
        if loser_id == bluffed_player_id: 
            game_over_message += f"{caller_name} wins!"
            users.update_one({"_id": winner_id}, {"$inc": {"balance": game['bet_amount']}})
            users.update_one({"_id": loser_id}, {"$inc": {"balance": -game['bet_amount']}})
            await client.send_message(loser_id, f"You lost the Bluff Master game (ID: `{game_id}`). Your bet of ₹{game['bet_amount']:,} has been deducted.")
            await client.send_message(winner_id, f"You won the Bluff Master game (ID: `{game_id}`)! You gained ₹{game['bet_amount']:,}.")
        else: 
            game_over_message += f"{bluffed_player_name} wins!"
            users.update_one({"_id": winner_id}, {"$inc": {"balance": game['bet_amount']}})
            users.update_one({"_id": loser_id}, {"$inc": {"balance": -game['bet_amount']}})
            await client.send_message(loser_id, f"You lost the Bluff Master game (ID: `{game_id}`). Your bet of ₹{game['bet_amount']:,} has been deducted.")
            await client.send_message(winner_id, f"You won the Bluff Master game (ID: `{game_id}`)! You gained ₹{game['bet_amount']:,}.")

        outcome_message += game_over_message
        await client.send_message(chat_id, outcome_message, parse_mode='md')
        del active_bluffmaster_games[game_id]
        print(f"[DEBUG] bluff_command: Game {game_id} deleted.")
        return
    game['game_round'] += 1
    print(f"[DEBUG] bluff_command: Starting new round. Round: {game['game_round']}")

    game['current_player_turn'] = winner_id
    game['last_bid'] = None 
    game['last_bid_player_id'] = None 
    for p_id in game['players']:
        game['player_hands'][p_id] = random.randint(1, 6)
        try:
            await client.send_message(p_id, f"🃏 Bluff Master Game (ID: `{game_id}`): New round! Your secret number is **{game['player_hands'][p_id]}**.")
        except Exception as e:
            print(f"Failed to send new round card to user {p_id}: {e}")

    next_turn_player_entity = await client.get_entity(game['current_player_turn'])
    next_turn_player_name = next_turn_player_entity.first_name if next_turn_player_entity else f"User_{game['current_player_turn']}"

    outcome_message += (
        f"\n\nIt's now {next_turn_player_name}'s turn to start the new round! "
        f"{next_turn_player_name}, use `/place [number]` to place your card."
    )

    await client.send_message(chat_id, outcome_message, parse_mode='md')
    print(f"[DEBUG] Exiting bluff_command for user {user_id}")

@client.on(events.NewMessage(pattern=r"/donatescout"))
async def donate_scout_durability_command(event):
    user_id = event.sender_id
    chat_id = event.chat_id
    if event.sender_id != ADMIN_ID:
        await event.reply("❌ You are not authorized to use this command.")
        return

    try:
        updated_count = 0
        for user in users.find({}):
            if user.get("scouting_gear_durability") != MAX_SCOUT_DURABILITY:
                users.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"scouting_gear_durability": MAX_SCOUT_DURABILITY}}
                )
                updated_count += 1
        
        await event.reply(f"🗺️ Successfully donated full scout gear durability ({MAX_SCOUT_DURABILITY} uses) to {updated_count} users!")
    except Exception as e:
        print(f"Error donating scout durability: {e}")
        await event.reply("An error occurred while donating scout durability.")

@client.on(events.NewMessage(pattern=r"/stopbluffmaster"))
async def stop_bluffmaster_command(event):
    user_id = event.sender_id
    chat_id = event.chat_id
    try:
        permissions = await client.get_permissions(chat_id, user_id)
        if not permissions.is_admin and not permissions.is_creator:
            await event.reply("🚫 You don't have permission to use this command.")
            return
    except Exception as e:
        print(f"Error checking permissions for user {user_id} in chat {chat_id}: {e}")
        await event.reply("An error occurred while checking your permissions.")
        return

    game_to_stop = None
    game_id_to_stop = None
    for g_id, g_data in list(active_bluffmaster_games.items()): 
        if g_data.get('chat_id') == chat_id:
            game_to_stop = g_data
            game_id_to_stop = g_id
            break

    if not game_to_stop:
        await event.reply("❌ No active Bluff Master game found in this chat.")
        return

    bet_amount = game_to_stop['bet_amount']
    refund_count = 0
    for player_id in game_to_stop['players']:
        try:

            users.update_one({"_id": player_id}, {"$inc": {"balance": bet_amount}})
            refund_count += 1
            await client.send_message(player_id, f"💸 Your bet of ₹{bet_amount:,} for Bluff Master game (ID: `{game_id_to_stop}`) has been refunded because the game was stopped by an administrator.")
        except Exception as e:
            print(f"Error refunding bet to user {player_id}: {e}")

    del active_bluffmaster_games[game_id_to_stop]
    await event.reply(f"✅ Bluff Master game (ID: `{game_id_to_stop}`) has been stopped. {refund_count} players were refunded ₹{bet_amount:,} each.")
    print(f"[DEBUG] Bluff Master game {game_id_to_stop} in chat {chat_id} stopped by admin {user_id}.")

@client.on(events.NewMessage(pattern=r"/reupload (.+?) (.+?) (.+?) (.+?) (.+)"))
@check_suspension
@handle_flood_control
async def reupload_character_command(event):
    user_id = event.sender_id
    user = users.find_one({"_id": user_id})

    if not user or not user.get('is_promoted', False):
        await event.reply("❌ You are not authorized to use this command. Only promoted users can reupload characters.")
        return

    match = event.pattern_match
    char_code = match.group(1).strip() 
    name = match.group(2).strip()
    anime_name = match.group(3).strip()
    rarity = match.group(4).strip().capitalize()
    image_link = match.group(5).strip()

    
    rarity_emojis = {
        "Common": "⚪", "Rare": "🟣", "Epic": "🟡", "Legendary": "🟠",
        "Special": "🌟", "Limited": "👑", "Mythic": "🔮", "Love": "💖",
        "Summer": "☀️", "Winter": "❄️", "Rainy season": "☔", "Aesthetic": "🎨"
    }
    selected_emoji = rarity_emojis.get(rarity, "")

    valid_rarities_upload = ["Common", "Rare", "Epic", "Legendary", "Special", "Limited", "Mythic", "Love"]
    valid_raredrop_rarities = ["Summer", "Winter", "Rainy season", "Aesthetic", "Love"]
    
   
    existing_character = characters_db.find_one({"_id": char_code})
    if existing_character and existing_character.get('is_raredrop_only'):
        valid_rarities = valid_raredrop_rarities
        weight_map = {"Summer": 5.0, "Winter": 5.0, "Rainy season": 5.0, "Aesthetic": 3.0, "Love": 0.08}
    else:
        valid_rarities = valid_rarities_upload
        weight_map = {"Common": 40, "Rare": 20, "Epic": 8, "Legendary": 2, "Special": 0.5, "Limited": 0.1, "Mythic": 0.05, "Love": 1}

    if rarity not in valid_rarities:
        await event.reply(f"❌ Invalid rarity. Supported rarities for this character type are: {', '.join(valid_rarities)}.")
        return

    if not (image_link.startswith("http://") or image_link.startswith("https://")):
        await event.reply("❌ Invalid image link. Please provide a full URL (http:// or https://).")
        return

    assigned_weight = weight_map.get(rarity, 1)

    if not existing_character:
        await event.reply(f"❌ Character with code `{char_code}` not found in the database. Please use /upload to add new characters.")
        return

    
    update_data = {
        "name": name,
        "anime_name": anime_name,
        "rarity": rarity,
        "image_url": image_link,
        "weight": assigned_weight
    }

    characters_db.update_one({"_id": char_code}, {"$set": update_data})

    await event.reply(f"✅ Character **{name}** (`{char_code}`) updated successfully!\n**Source:** {anime_name}\n**Rarity:** {rarity}")

    
    users_with_character_updated = 0
    for user_doc in users.find({"characters._id": char_code}):
        updated_characters = []
        for char_in_collection in user_doc.get('characters', []):
            if char_in_collection["_id"] == char_code:
                
                updated_characters.append({
                    "_id": char_code,
                    "name": name,
                    "anime_name": anime_name,
                    "rarity": rarity,
                    "image_url": image_link,
                    "weight": assigned_weight,
                    "is_raredrop_only": existing_character.get('is_raredrop_only', False) 
                })
            else:
                updated_characters.append(char_in_collection)
        users.update_one({"_id": user_doc["_id"]}, {"$set": {"characters": updated_characters}})
        users_with_character_updated += 1
    print(f"[DEBUG] Updated character `{char_code}` in {users_with_character_updated} user collections.")

    log_message = f"🔄 𝗖𝗵𝗮𝗿𝗮𝗰𝘁𝗲𝗿 𝗨𝗽𝗱𝗮𝘁𝗲𝗱!\n\n"
    log_message += f"✨ 𝗡𝗮𝗺𝗲: {name} \n"
    log_message += f"📌 𝗦𝗼𝘂𝗿𝗰𝗲: {anime_name} \n"
    log_message += f"{selected_emoji} 𝗥𝗮𝗿𝗶𝘁𝘆: {rarity} \n"
    log_message += f"🆔 𝗖𝗼𝗱𝗲: `{char_code}`"

    try:
        await client.send_message(UPLOAD_LOG_CHANNEL_ID, log_message, file=image_link, parse_mode='md')
        print(f"Successfully sent character update log with image to channel {UPLOAD_LOG_CHANNEL_ID}.")
    except Exception as e:
        print(f"Failed to send image with update log to channel {UPLOAD_LOG_CHANNEL_ID}: {e}. Sending text message instead.")
        try:
            await client.send_message(UPLOAD_LOG_CHANNEL_ID, log_message + f"\n[Image Link]({image_link})", parse_mode='md', link_preview=False)
        except Exception as text_e:
            print(f"Failed to send text update log to channel {UPLOAD_LOG_CHANNEL_ID}: {text_e}.")

@client.on(events.NewMessage(pattern=r"/search (.+)"))
@check_suspension
@handle_flood_control
async def search_character_command(event):
    user_id = event.sender_id
    search_query_raw = event.pattern_match.group(1).strip()
    found_character = None

    # Re-using the rarity_emojis dictionary
    rarity_emojis = {
        "Common": "⚪", "Rare": "🟣", "Epic": "🟡", "Legendary": "🟠",
        "Special": "🌟", "Limited": "👑", "Mythic": "🔮", "Love": "💖",
        "Summer": "☀️", "Winter": "❄️", "Rainy season": "☔", "Aesthetic": "🎨"
    }

    # Option 1: Search by exact code (5-digit numeric)
    if search_query_raw.isdigit() and len(search_query_raw) == 5:
        found_character = characters_db.find_one({"_id": search_query_raw})

    # Option 2: Search by exact name (case-insensitive)
    if not found_character:
        found_character = characters_db.find_one({"name": {"$regex": f"^{search_query_raw}$", "$options": "i"}})
        
    # Option 3: Search by normalized partial name (if no exact match found)
    if not found_character:
        def normalize_name_for_search(name_to_normalize):
            return set(name_to_normalize.lower().replace('-', ' ').split())

        search_normalized = normalize_name_for_search(search_query_raw)
        
        best_match_score = 0
        potential_matches = []
        for char in characters_db.find({}):
            char_name_normalized = normalize_name_for_search(char["name"])
            
            score = len(search_normalized.intersection(char_name_normalized))
            
            if score > best_match_score:
                best_match_score = score
                potential_matches = [char]
            elif score > 0 and score == best_match_score:
                potential_matches.append(char)
        
        if potential_matches:
            # Prioritize matches where the raw query is a substring of the name
            for char_match in potential_matches:
                if search_query_raw.lower() in char_match["name"].lower():
                    found_character = char_match
                    break
            if not found_character:
                found_character = potential_matches[0] # Fallback to first if no exact substring match among top scores

    if not found_character:
        await event.reply(f"❌ Character '{search_query_raw}' not found in the database.")
        return

    # Calculate Globally Collected count
    global_collected_count = users.count_documents({"characters._id": found_character["_id"]})

    # Determine Owned By list
    owners = []
    for user_doc in users.find({"characters._id": found_character["_id"]}).limit(5): # Limit to 5 owners for display
        try:
            owner_entity = await client.get_entity(user_doc["_id"])
            if owner_entity:
                owners.append(owner_entity.first_name if owner_entity.first_name else f"User_{user_doc['_id']}")
        except Exception as e:
            print(f"Error fetching owner entity {user_doc['_id']}: {e}")
            owners.append(f"User_{user_doc['_id']}") # Fallback if fetching entity fails
    
    if owners:
        owned_by_text = ", ".join(owners)
        if global_collected_count > 5: # If there are more than 5, indicate it
            owned_by_text += " and more..."
    else:
        owned_by_text = "No one currently owns this."

    selected_emoji = rarity_emojis.get(found_character["rarity"], "❓") # Default to '❓' if rarity not in map

    response_text = f"""
🔰 𝗖𝗛𝗔𝗥𝗔𝗖𝗧𝗘𝗥 𝗜𝗡𝗙𝗢:

✨ 𝗡𝗔𝗠𝗘: {found_character["name"]}
🌏 𝗦𝗢𝗨𝗥𝗖𝗘: {found_character.get("anime_name", "N/A")}
💠 𝗥𝗔𝗥𝗜𝗧𝗬: {selected_emoji} {found_character["rarity"]}
🌐 𝗚𝗟𝗢𝗕𝗔𝗟𝗟𝗬 𝗖𝗢𝗟𝗟𝗘𝗖𝗧𝗘𝗗: {global_collected_count} Times

💎 𝗢𝗪𝗡𝗘𝗗 𝗕𝗬: {owned_by_text}
"""

    if found_character.get('image_url'):
        try:
            await client.send_message(event.chat_id, message=response_text, file=found_character['image_url'], parse_mode='md')
        except Exception as e:
            print(f"Failed to send image for /search command: {e}")
            await event.reply(response_text, parse_mode='md') # Send text only if image fails
    else:
        await event.reply(response_text, parse_mode='md')
keep_alive()
start_requesting()
print("Bot is running...")
client.run_until_disconnected()