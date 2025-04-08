import os
from telegram.ext import ConversationHandler
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import re
import time
from telegram.ext.dispatcher import run_async
from telegram import User, PhotoSize, ParseMode
import telegram
import logging
logging.basicConfig(level=logging.INFO)
import random
import string

# Your bot token (get this from BotFather)
BOT_TOKEN = "7921044809:AAEtRGLlWVM6RzDVZis3QjZpIxW1l3Vfd5c"

# Get the port from the environment variable (Render sets this)
PORT = int(os.environ.get('PORT', '8443'))  # Default to 8443 if not set

# Your application URL (Render provides this or you can set it)
APP_URL = 'https://hbg-slow.onrender.com'
if not APP_URL:
    print("APP_URL environment variable not set.  You MUST configure this on Render.")
    exit(1)  # Exit if APP_URL is not defined.

# Create the Updater and Dispatcher

updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher



AUCTION_GROUP_ID=-1002455896075
AUC_NAME="HBG_NEW_GROUP_FHG"
owners =[1947921832, 1381668733]
OWNER = 1381668733
SUBMISSION_GROUP_ID=-1002652165076
# Set pokemons,teams,tms name here
LEGENDARY_POKEMON_NAMES = ["Articuno", "Zapdos", "Moltres", "Raikou", "Entei", "Suicune", "Regirock", "Regice", "Registeel", "Latias", "Latios", "Uxie", "Mesprit", "Azelf", "Heatran", "Regigigas", "Cresselia", "Cobalion", "Terrakion", "Virizion", "Buzzwole", "Thundurus", "Tornadus", "Landorus", "Type: Null", "Silvally", "Tapu Koko", "Tapu Bulu", "Tapu Fini", "Tapu Lele", "Nihilego", "Pheromosa", "Xurkitree", "Celesteela", "Kartana", "Guzzlord", "Poipole", "Naganadel", "Stakataka", "Blacephalon", "Kubfu", "Urshifu", "Regieleki", "Regidrago", "Glastrier", "Spectrier", "Enamorus", "Wo-chien", "Chien-pao", "Ting-lu", "Chi-yu", "Okidogi", "Munkidori", "Fezandipiti", "Ogerpon", "Mewtwo", "Lugia", "Ho-oh", "Kyogre", "Groudon", "Rayquaza", "Dialga", "Palkia", "Giratina", "Reshiram", "Zekrom", "Kyurem", "Xerneas", "Yveltal", "Zygarde", "Cosmog", "Cosmoem", "Solgaleo", "Lunala", "Necrozma", "Zacian", "Zamazenta", "Eternatus", "Calyrex", "Koraidon", "Miraidon", "Terapagos", "Mew", "Celebi", "Jirachi", "Deoxys", "Phione", "Manaphy", "Darkrai", "Arceus", "shaymin", "Victini", "Keldeo", "Meloetta", "Genesect", "Diancie", "Hoopa", "Volcanion", "Megearna", "Marshadow", "Zeraora", "Meltan", "Melmetal", "Zarude"]

NON_LEGENDARY_POKEMON_NAMES = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran-F", "Nidorina", "Nidoqueen", "Nidoran-M", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetchd", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr-Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Dratini", "Dragonair", "Dragonite", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Larvitar", "Pupitar", "Tyranitar", "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple", "Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo", "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Tropius", "Chimecho", "Absol", "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Turtwig", "Grotle", "Torterra", "Chimchar", "Monferno", "Infernape", "Piplup", "Prinplup", "Empoleon", "Starly", "Staravia", "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune", "Shinx", "Luxio", "Luxray", "Budew", "Roserade", "Cranidos", "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam-Plant", "Mothim", "Combee", "Vespiquen", "Pachirisu", "Buizel", "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom", "Drifloon", "Drifblim", "Buneary", "Lopunny", "Mismagius", "Honchkrow", "Glameow", "Purugly", "Chingling", "Stunky", "Skuntank", "Bronzor", "Bronzong", "Bonsly", "Mime-Jr", "Happiny", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp", "Munchlax", "Riolu", "Lucario", "Hippopotas", "Hippowdon", "Skorupi", "Drapion", "Croagunk", "Toxicroak", "Carnivine", "Finneon", "Lumineon", "Mantyke", "Snover", "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth", "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z", "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom,Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog", "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole", "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Basculin-Red-Striped", "Sandile", "Krokorok", "Krookodile", "Darumaka", "Darmanitan-Standard", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask", "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark", "Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite", "Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet", "Accelgor", "Stunfisk", "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta", "Chespin", "Thwackey", "Rillaboom", "Scorbunny", "Raboot", "Cinderace", "Sobble", "Drizzile", "Inteleon", "Skwovet", "Greedent", "Rookidee", "Corvisquire", "Corviknight", "Blipbug", "Dottler", "Orbeetle", "Nickit", "Thievul", "Gossifleur", "Eldegoss", "Wooloo", "Dubwool", "Chewtle", "Drednaw", "Yamper", "Boltund", "Rolycoly", "Carkol", "Coalossal", "Applin", "Flapple", "Appletun", "Silicobra", "Sandaconda", "Cramorant", "Arrokuda", "Barraskewda", "Toxel", "Toxtricity-Amped", "Sizzlipede", "Centiskorch", "Clobbopus", "Grapploct", "Sinistea", "Polteageist", "Hatenna", "Hattrem", "Hatterene", "Impidimp", "Morgrem", "Grimmsnarl", "Obstagoon", "Perrserker", "Cursola", "Sirfetchd", "Mr-Rime", "Runerigus", "Milcery", "Alcremie", "Falinks", "Pincurchin", "Snom", "Frosmoth", "Stonjourner", "Eiscue-Ice", "Indeedee-Male", "Morpeko-Full-Belly", "Cufant", "Copperajah", "Dracozolt", "Arctozolt", "Dracovish", "Dartrix", "Decidueye", "Litten", "Torracat", "Incineroar", "Popplio", "Brionne", "Primarina", "Pikipek", "Trumbeak", "Toucannon", "Yungoos", "Gumshoos", "Grubbin", "Charjabug", "Vikavolt", "Crabrawler", "Crabominable", "Oricorio-Baile", "Cutiefly", "Ribombee", "Rockruff", "Lycanroc-Midday", "Wishiwashi-Solo", "Mareanie", "Toxapex", "Mudbray", "Mudsdale", "Dewpider", "Araquanid", "Fomantis", "Lurantis", "Morelull", "Shiinotic", "Salandit", "Salazzle", "Stufful", "Bewear", "Bounsweet", "Steenee", "Tsareena", "Comfey", "Oranguru", "Passimian", "Wimpod", "Golisopod", "Sandygast", "Palossand", "Pyukumuku", "Type-Null", "Silvally", "Minior-Red-Meteor", "Komala", "Turtonator", "Togedemaru", "Mimikyu-Disguised", "Bruxish", "Drampa", "Dhelmise", "Jangmo-O", "Hakamo-O", "Kommo-O", "Poipole", "Naganadel"]

SHINY_POKEMON_NAMES = LEGENDARY_POKEMON_NAMES + NON_LEGENDARY_POKEMON_NAMES

POKEMON_TEAM = ["Hp", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed"]

TM = ["Tm02", "Tm03", "Tm09", "Tm10", "Tm13", "Tm14", "Tm15", "Tm22", "Tm23", "Tm24", "Tm25", "Tm26", "Tm28", "Tm29", "Tm30", "Tm31", "Tm34", "Tm35", "Tm36", "Tm38", "Tm39", "Tm40", "Tm42", "Tm43", "Tm46", "Tm47", "Tm48", "Tm49", "Tm50", "Tm51", "Tm52", "Tm53", "Tm54", "Tm55", "Tm57", "Tm58", "Tm59", "Tm62", "Tm65", "Tm66", "Tm67", "Tm68", "Tm71", "Tm72", "Tm76", "Tm78", "Tm79", "Tm80", "Tm81", "Tm82", "Tm83", "Tm84", "Tm85", "Tm89", "Tm91", "Tm93", "Tm94", "Tm95", "Tm97", "Tm98", "Tm99"]
collection = {}
limit = {
    "legendary": 12, 
    "non-legendary" : 15, 
    "shiny" : 20, 
    "tm" : 15, 
    "team" : 5
    }
approved_users=[1947921832,1381668733]
seller_data = {}
seller_lead = {}
seller_old = {}
legendary_list = []
non_legendary_list = []
shiny_list = []
tm_list = []
team_list = []
legendary_item = []
non_legendary_item = []
shiny_item = []
tm_item = []
team_item = []
buyers = {
    "legendary" : [], 
    "non-legendary" : [], 
    "shiny" : [], 
    "tm" : [], 
    "team" : [], 
    "legendary_name" : [], 
    "non-legendary_name" : [], 
    "shiny_name" : [], 
    "tm_name" : [], 
    "team_name" : []
         }
back = {
    "legendary" : [], 
    "non-legendary" : [], 
    "shiny" : [], 
    "tm" : [], 
    "team" : []
       }

ITEM_NAME, NATURE_PAGE, ITEM_DETAILS, POKEMON_IV, MOVESET_PAGE, BOOSTED, BASE_PRICE = range(7)
CHECKING, STOPPED = range(2)
HANDLE_BID = 1
auction = "start"
sub = "on"
user_list=[]
bist=[]
pokemons = {}
tms = {}
current_add=[]
pokemons["name"] = []
pokemons["item_name"] = []
pokemons["seller_id"] = []
pokemons["boosted"] = []
pokemons["moveset_page"] = []
pokemons["iv_page"] = []
pokemons["nature"] = []
pokemons["lv"] = []
pokemons["base"] = []
pokemons["types"] = []
pokemons["category"] = []
pokemons["picture"] = []
pokemons["msg_id"] = []
tms["category"] = []
tms["details"] = []
tms["item_name"] = []
tms["base"] = []
tms["msg_id"] = []
tms["name"] = []
tms["seller_id"] = []
no=0
video = "https://files.catbox.moe/4v63m2.jpg"
bot_name = "HBG_SLOW_AUCTIONBOT"
channels = ['@HBG_NEW_GROUP_FHG' , '@HBG_AUCTION_TRADE']
BROADCAST_MESSAGE = 1
ADD_VIDEO = 1
backup = -1002347695416

def check_working(update: Update, context: CallbackContext):
    """Checks if the message contains 'working?' and replies with 'Yep, perfectly fine'."""
    message_text = update.message.text.lower()  # Convert to lowercase for case-insensitive matching

    if "working?" in message_text:
        update.message.reply_text("Yep, perfectly fine")

def generate(length=10):
  characters = string.ascii_letters + string.digits  # Combine letters and digits
  random_string = ''.join(random.choice(characters) for i in range(length))
  return random_string


def back_up(update: Update, context: CallbackContext):
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

def check_message(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in approved_users:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return

    chat_id = update.effective_chat.id
    message = update.message.text
    part = message.split(":")
    
    if len(part) != 11:
        update.message.reply_text("Error: Message must contain exactly 11 parts.")
        return

    category = part[0]
    try:
        i = int(part[1])
    except ValueError:
        update.message.reply_text("Error: Second part must be an integer.")
        return
    if category == "legendary":
        l = legendary_item
        slist = legendary_list
    elif category == "non-legendary":
        l = non_legendary_item
        slist = non_legendary_list
    elif category == "shiny":
        l = shiny_item
        slist = shiny_list
    elif category == "team":
        l = team_item
        slist = team_list
    elif category == "tm":
        l = tm_item
        slist = tm_list
    else:
        update.message.reply_text("Error: Invalid category.")
        return
    bd = buyers[category]
    nam = buyers[f"{category}_name"]
    bk = back[category]

    
    while len(l) <= i:
        l.append("NA")
        slist.append("NA")
        bd.append(0) 
        nam.append(0)
        bk.append(0) 

    l[i] = part[2] +":"+ part[3]
    slist[i] = part[4] + ":" + part[5]
    bd[i] = float(part[6])
    nam[i] = int(part[7]) if is_digit(part[7]) else "None"
    iddata =  part[5].split("-")
    sid= int(iddata[1]) 
    
    if sid not in seller_lead:
        seller_lead[sid] = {}
        seller_lead[sid]["item"] = []
        seller_lead[sid]["bag"] = []
    if sid not in seller_old:
        seller_old[sid] = {}
        seller_old[sid]["item"] = 0
        seller_old[sid]["bag"] = 0    
    seller_lead[sid]["item"].append(f"{category}${part[2]}:{part[3]}") 
    seller_old[sid]["item"]+=1
    bk[i] = int(part[8]) 
    collection[part[9]] = f"{category}_{i}_{part[10]}"
def auction_mode(update,context):
    global auction
    user_id = update.effective_user.id
    if user_id in owners:
        
        pass
    else:
        update.message.reply_text("You are not an approved user.")
        return
    r = update.message.text.split(" ") 
    if len(r) != 2:
        update.message.reply_text("wrong format \n format /auction <start/end>")
        return
    if r[1] != "start" and r[1] != "end":
        update.message.reply_text(" wrong argument provided \n available argument `start` or `end`") 
        return
    else:
        update.message.reply_text(f"Changed Auction status from {auction} to {r[1]}") 
        auction = r[1]
        if r[1] == "end":
            buyers_list(update, context) 
            sellers_list(update, context) 
            try:
              context.bot.send_message(backup,seller_old) 
            except:
              update.message.reply(" memory_suceeded") 
            for cat in back:
              for i in back[cat]:
                    context.bot.delete_message(chat_id=backup,message_id=i) 
           

            keyboard = [
    [
        InlineKeyboardButton("YES", callback_data='clear_yes'),
        InlineKeyboardButton("NO", callback_data='clear_no'),
    ]
]

            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text("DO YOU WANT TO CLEAR All OLD DATA?", reply_markup=reply_markup)
def submission_mode(update, context):
            
    global sub
    user_id = update.effective_user.id
    if user_id in approved_users:
        
        pass
    else:
        update.message.reply_text("You are not an approved user.")
        return
    r = update.message.text.split(" ") 
    if len(r) != 2:
        update.message.reply_text("wrong format \n format /submission <on/off>")
        return
    if r[1] != "on" and r[1] != "off":
        update.message.reply_text(" wrong argument provided \n available argument `on` or `off`") 
        return
    else:
        update.message.reply_text(f"Changed Auction status from {sub} to {r[1]}") 
        sub = r[1]

def store(update, context):
    if int(update.effective_user.id) != OWNER:
        update.message.reply_text("You are not autherised to access that command so go away ")  
        return
    global video
    video=update.message.photo.file_id
    update.message.reply_text(f"video stored successfully!\n`{video}`")

def is_digit(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

def start(update: Update, context: CallbackContext):
    user_id=update.message.from_user.id 
    if user_id != update.message.chat.id:
        context.bot.send_message(chat_id=update.message.chat.id,text="𝑇ℎ𝑖𝑠 𝑐𝑜𝑚𝑚𝑎𝑛𝑑 𝑐𝑎𝑛 𝑜𝑛𝑙𝑦 𝑏𝑒 𝑢𝑠𝑒𝑑 𝑖𝑛 𝑑𝑚")
        return ConversationHandler.END
    if user_id not in user_list:
        user_list.append(user_id) 
    user=update.message.from_user
    
    for channel_username in channels:
        try:
    # Get the chat object for the channel
            chat = context.bot.get_chat(channel_username)

    # Check if the user is a member of the channel
            member = context.bot.get_chat_member(chat_id=chat.id, user_id=user.id)

    # If the user is not a member, exit the function
            if member.status not in ['member', 'creator', 'administrator']:
                download_link = f"https://t.me/HBG_NEW_GROUP_FHG"
                download_linker = f"https://t.me/HBG_AUCTION_TRADE"

            # Send the download link with inline keyboard
                keyboard = InlineKeyboardMarkup([[
                     InlineKeyboardButton("Channel link", url=download_link), InlineKeyboardButton("Group link", url=download_linker)
            ]])
                try:
                    context.bot.send_photo(chat_id=update.message.chat.id,photo=video,caption=f"""♦𝑊𝑒𝑙𝑐𝑜𝑚𝑒 {update.message.from_user.name}

🔸𝑌𝑜𝑢 𝐶𝑎𝑛 𝑆𝑢𝑏𝑚𝑖𝑡 𝑌𝑜𝑢𝑟 𝑃𝑜𝑘𝑒𝑚𝑜𝑛 𝑇ℎ𝑟𝑜𝑢𝑔ℎ 𝑇ℎ𝑖𝑠 𝐵𝑜𝑡 𝐹𝑜𝑟 𝐴𝑢𝑐𝑡𝑖𝑜𝑛

🔻𝐵𝑢𝑡 𝐵𝑒𝑓𝑜𝑟𝑒 𝑈𝑠𝑖𝑛𝑔 𝑌𝑜𝑢 𝐻𝑎𝑣𝑒 𝑇𝑜 𝐽𝑜𝑖𝑛 𝑂𝑢𝑟 𝐴𝑢𝑐𝑡𝑖𝑜𝑛 𝐺𝑟𝑜𝑢𝑝 𝐵𝑦 𝐶𝑙𝑖𝑐𝑘𝑖𝑛𝑔 𝐵𝑒𝑙𝑜𝑤 𝑇𝑤𝑜 𝐵𝑢𝑡𝑡𝑜𝑛𝑠 𝐴𝑛𝑑 𝑇ℎ𝑒𝑛 𝐶𝑙𝑖𝑐𝑘 '𝐽𝑜𝑖𝑛𝑒𝑑' 𝐵𝑢𝑡𝑡𝑜𝑛
<blockquote>𝘾𝙧𝙚𝙖𝙩𝙤𝙧 :</blockquote> @l0_Mr_unknown_0l""",reply_markup=keyboard, parse_mode="html")
                except Exception as e:
                    update.message.reply_text(f"Error checking channel membership: {e}")
                return

        except Exception as e:
            update.message.reply_text(f"Error checking channel membership: {e}")
            return
    ar = context.args[0] if context.args else None
    if ar:
        if ar not in collection:
            update.message.reply_text("something wrong with item please contact admin") 
            return ConversationHandler.END
        rar = collection[ar]  
        sp = rar.split("_") 
        cat = sp[0]
        id = int(sp[1]) 
        if cat == "legendary":
            item_name = legendary_item[id]
        elif cat == "non-legendary":
            item_name = non_legendary_item[id]
        elif cat == "shiny":
            item_name = shiny_item[id]
        elif cat == "team":
            item_name = team_item[id]
        elif cat == "tm":
            item_name = tm_item[id]
        context.user_data["inform"] = str(ar) 
        update.message.reply_text(
    f"          (⁠✷⁠‿⁠✷⁠)         \n"
    f"Enter the amount of Poke Dollars you want to bid for {item_name} "
    "or use /cancel to stop bidding \n\n"
    f"NOTE :  your bid must be in 'PDs'",
    parse_mode="html",
    disable_web_page_preview=True
)
        return HANDLE_BID
        
    else:
        download_link = f"https://t.me/HBG_NEW_GROUP_FHG"

            # Send the download link with inline keyboard
        keyboard = InlineKeyboardMarkup([[
             InlineKeyboardButton("Channel link", url=download_link)
            ]])
        context.bot.send_photo(chat_id=update.message.chat.id,photo=video,caption=f"""𝙒𝙚𝙡𝙘𝙤𝙢𝙚 {update.message.from_user.name} , 
🅃🄾 🄰🄳🄳 🄸🅃🄴🄼🅂 🄵🄾🅁 🄰🅄🄲🅃🄸🄾🄽 🅄🅂🄴 /add
<blockquote>𝘾𝙧𝙚𝙖𝙩𝙤𝙧 :</blockquote> @l0_Mr_unknown_0l""",reply_markup=keyboard, parse_mode="html")

def handle_bid (update, context):
    message = update.message
    ar = context.user_data.get("inform") 
    rar = collection[ar]
    sp = rar.split("_") 
    category = sp[0]
    cat = category
    id = int(sp[1]) 
    msg = int(sp[2]) 
    if len(buyers[category]) <= id:
        message.reply_text("something wrong with item please contact admin") 
        return ConversationHandler.END
    if cat == "legendary":
        item_name = legendary_item[id]
        lis = legendary_list[id]
    elif cat == "non-legendary":
        item_name = non_legendary_item[id]
        lis = non_legendary_list[id]
    elif cat == "shiny":
        item_name = shiny_item[id]
        lis = shiny_list[id]
    elif cat == "team":
        item_name = team_item[id]
        lis = team_list[id]
    elif cat == "tm":
        item_name = tm_item[id]
        lis = tm_list[id]
    required = 100

    if not buyers[category][id]:
        message.reply_text("something wrong with item please contact admin") 
        return ConversationHandler.END
    if is_digit(message.text):
        if (float(message.text)-float(buyers[category][id])) >= required:
            message.reply_text("<blockquote>🎊 BID SUCCESS FULLY PLACED 📨 </blockquote> \n 🖇 please check to confirm ",parse_mode = "html") 
        
            Inline_keyboard = [
                    [
                        InlineKeyboardButton("Place Your Bid 🎴", url=f'https://t.me/{bot_name}?start={ar}')
                    ]
        ]
            buyers[category][id] = int(message.text) 
            buyers[f"{category}_name"][id] = update.message.from_user.id
            reply_markup = InlineKeyboardMarkup(Inline_keyboard)
            context.bot.edit_message_text(chat_id=backup,message_id=back[category][id],text=f"{category}:{id}:{item_name}:{lis}:{update.message.text}:{update.message.from_user.id}:{back[category][id]}:{ar}:{msg}",disable_web_page_preview=True) 
            context.bot.edit_message_text(
    chat_id=AUCTION_GROUP_ID,
    message_id=msg,
    text=f"""
╔══════════════════════════╗
<b>The Bid Page of {item_name}</b>
highest bid - {update.message.text} Pds
Bidder      - {update.message.from_user.first_name}\n(@{update.message.from_user.username}) 
╚══════════════════════════╝""",
    reply_markup=reply_markup,
    parse_mode='HTML',disable_web_page_preview=True)
            
        
        else:
            message.reply_text(f"<b>INSUFFICIENT FUND: Minimum increment must be by {required}</b>\n\n ---------------------\nYou must bid : <b>{int(buyers[category][id]) + required}</b> Atleast ",parse_mode = "html",disable_web_page_preview=True)
        return ConversationHandler.END 
    else:
        message.reply_text(f"Wrong format only write amount in numbers to bid on {item_name}",disable_web_page_preview=True)
        return ConversationHandler.END

def send_long_message(bot, chat_id, text):
    max_length = 4096 # Telegram's max message length
    parts = [text[i:i + max_length] for i in range(0, len(text), max_length)]

    for part in parts:
        bot.send_message(chat_id=chat_id, text=part, parse_mode="html")
        
def broadcast(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter the message you want to broadcast:")
    return BROADCAST_MESSAGE

def broadcast_message(update, context):
    message = update.message
    message_id=message.message_id
    for user_id in user_list:
        try:
            context.bot.forward_message(chat_id=user_id,from_chat_id=update.message.chat_id,message_id=message_id)
        except Exception as e:
            print(f"Error sending message to {user_id}: {e}")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Broadcast complete!")
    return ConversationHandler.END
def add(update, context):
    chatid=update.message.chat.id
    user = update.effective_user
    user_id = user.id
    usern=user.first_name
    for channel_username in channels:
        try:
    # Get the chat object for the channel
            chat = context.bot.get_chat(channel_username)

    # Check if the user is a member of the channel
            member = context.bot.get_chat_member(chat_id=chat.id, user_id=user.id)

    # If the user is not a member, exit the function
            if member.status not in ['member', 'creator', 'administrator']:
                download_link = f"https://t.me/HBG_NEW_GROUP_FHG"
                download_linker = f"https://t.me/HBG_AUCTION_TRADE"

            # Send the download link with inline keyboard
                keyboard = InlineKeyboardMarkup([[
                     InlineKeyboardButton("Channel link", url=download_link), InlineKeyboardButton("Group link", url=download_linker)
            ]])
                context.bot.send_photo(chat_id=update.message.chat.id,photo=video,caption=f"""♦𝑊𝑒𝑙𝑐𝑜𝑚𝑒 {update.message.from_user.name}

🔸𝑌𝑜𝑢 𝐶𝑎𝑛 𝑆𝑢𝑏𝑚𝑖𝑡 𝑌𝑜𝑢𝑟 𝑃𝑜𝑘𝑒𝑚𝑜𝑛 𝑇ℎ𝑟𝑜𝑢𝑔ℎ 𝑇ℎ𝑖𝑠 𝐵𝑜𝑡 𝐹𝑜𝑟 𝐴𝑢𝑐𝑡𝑖𝑜𝑛

🔻𝐵𝑢𝑡 𝐵𝑒𝑓𝑜𝑟𝑒 𝑈𝑠𝑖𝑛𝑔 𝑌𝑜𝑢 𝐻𝑎𝑣𝑒 𝑇𝑜 𝐽𝑜𝑖𝑛 𝑂𝑢𝑟 𝐴𝑢𝑐𝑡𝑖𝑜𝑛 𝐺𝑟𝑜𝑢𝑝 𝐵𝑦 𝐶𝑙𝑖𝑐𝑘𝑖𝑛𝑔 𝐵𝑒𝑙𝑜𝑤 𝑇𝑤𝑜 𝐵𝑢𝑡𝑡𝑜𝑛𝑠 𝐴𝑛𝑑 𝑇ℎ𝑒𝑛 𝐶𝑙𝑖𝑐𝑘 '𝐽𝑜𝑖𝑛𝑒𝑑' 𝐵𝑢𝑡𝑡𝑜𝑛
<blockquote>𝘾𝙧𝙚𝙖𝙩𝙤𝙧 :</blockquote> @l0_Mr_unknown_0l""",reply_markup=keyboard, parse_mode="html")
                return

        except Exception as e:
            update.message.reply_text(f"Error checking channel membership: {e}")
            return
    if user_id != chatid:
        context.bot.send_message(chat_id=update.message.chat.id,text="𝑇ℎ𝑖𝑠 𝑐𝑜𝑚𝑚𝑎𝑛𝑑 𝑐𝑎𝑛 𝑜𝑛𝑙𝑦 𝑏𝑒 𝑢𝑠𝑒𝑑 𝑖𝑛 𝑑𝑚 समझा🧐")
        return ConversationHandler.END
    if user_id not in user_list:
        user_list.append(user_id)
    if auction != "start":
        update.message.reply_text("Sorry for inconvenience but there is no current auction going on") 
        return
    if sub != "on":
        update.message.reply_text("Sorry for inconvenience but Submission for the current auction has now ended \n Do try on the next auction") 
        return
    keyboard = [
        [
            InlineKeyboardButton("LEGENDARY", callback_data=f'legendary'),
            InlineKeyboardButton("NON-LEGENDARY", callback_data=f'non-legendary'),
        ],
        [
            InlineKeyboardButton("SHINY", callback_data=f'shiny'),
            InlineKeyboardButton("TEAM", callback_data='team'),
        ],
        [
            InlineKeyboardButton("TM", callback_data='tm')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if user_id in current_add:
        update.message.reply_text("please complete on going submission \n      -OR-     \n     -Use /cancel Command")
    else:
        message = update.message.reply_text('<blockquote>𝑊𝐻𝐴𝑇 𝑌𝑂𝑈 𝑊𝐴𝑁𝑇 𝑇𝑂 𝑆𝐸𝐿𝐿 𝐼𝑁 𝐼𝐻𝐺 𝐴𝑈𝐶𝑇𝐼𝑂𝑁?</blockquote>\n𝐶ℎ𝑜𝑜𝑠𝑒 𝑓𝑟𝑜𝑚 𝑏𝑒𝑙𝑜𝑤 🎐', reply_markup=reply_markup, parse_mode='HTML')
        context.user_data['message_id'] = message.message_id  
        current_add.append(user_id) 

        return ITEM_NAME
        
def category(update, context):
    user = update.effective_user
    query = update.callback_query

    callback_data = query.data
    context.user_data['category'] = callback_data
    if callback_data in ["legendary ", "non-legendary", "shiny", "tm", "team"]:
        if limit[callback_data]<=len(buyers[callback_data]):
            context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                  message_id=context.user_data.get('message_id'),
                                  text=f"<blockquote>Really Sorry fellows !! \nBut slots for this category is full</blockquote>",parse_mode="html")
            current_add.remove(update.message.from_user.id) 
            return ConversationHandler.END 

    if callback_data == 'legendary':

        reply_text = f"𝐻𝐸𝑌 {user.full_name.upper()}! 𝑊𝐻𝐼𝐶𝐻 𝐿𝐸𝐺𝐸𝑁𝐷𝐴𝑅𝑌 𝑃𝑂𝐾𝐸𝑀𝑂𝑁 𝑌𝑂𝑈 𝑊𝐴𝑁𝑇 𝑇𝑂 𝑆𝐸𝐿𝐿?"
    elif callback_data == 'non-legendary':
        reply_text = f"𝐻𝐸𝑌 {user.full_name.upper()}! 𝑊𝐻𝐼𝐶𝐻 𝑁𝑂𝑁-𝐿𝐸𝐺𝐸𝑁𝐷𝐴𝑅𝑌 𝑃𝑂𝐾𝐸𝑀𝑂𝑁 𝑌𝑂𝑈 𝑊𝐴𝑁𝑇 𝑇𝑂 𝑆𝐸𝐿𝐿?"
    elif callback_data == 'shiny':
        reply_text = f"𝐻𝐸𝑌 {user.full_name.upper()}! 𝑊𝐻𝐼𝐶𝐻 𝑆𝐻𝐼𝑁𝑌 𝑃𝑂𝐾𝐸𝑀𝑂𝑁 𝑌𝑂𝑈 𝑊𝐴𝑁𝑇 𝑇𝑂 𝑆𝐸𝐿𝐿?"
    elif callback_data == 'team':
        reply_text = f"𝐻𝐸𝑌 {user.full_name.upper()}! 𝑊𝐻𝐼𝐶𝐻 𝑇𝐸𝐴𝑀 𝑌𝑂𝑈 𝑊𝐴𝑁𝑇 𝑇𝑂 𝑆𝐸𝐿𝐿?"
    elif callback_data == 'tm':
        reply_text = f"𝐻𝐸𝑌 {user.full_name.upper()}! 𝑊𝐻𝐼𝐶𝐻 𝑇𝑀 𝑌𝑂𝑈 𝑊𝐴𝑁𝑇 𝑇𝑂 𝑆𝐸𝐿𝐿? (PLEASE TELL THE TM NUMBER NOT TM NAME)."
    elif callback_data.startswith("confirm_sell"):
        button(update,context)
        return
    elif callback_data.startswith('item'):
        items(update, context) 
        return    
    elif callback_data.startswith('my'):
        myitems(update, context) 
        return
    elif callback_data.startswith('bag'):
        mybag(update, context) 
        return
    elif callback_data.startswith('clear'):
        clear_all(update, context) 
        return
    else:
        submission(update, context)
        return 

    context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                  message_id=context.user_data.get('message_id'),
                                  text=f"<blockquote>{reply_text}</blockquote>",parse_mode="html")        
def users(update,context):
    usersl="7048431897" if len(user_list) == 0 else "  "
    for user in user_list:
        usersl=f"{usersl},{user}"
    context.bot.send_message(chat_id=update.message.chat.id,text=usersl)


def item_name(update, context):
    item_name = update.message.text.title()
    category = context.user_data['category']

    if category == 'legendary':
        if item_name in LEGENDARY_POKEMON_NAMES:
            context.user_data["item_name"] = item_name
            update.message.reply_text(f"𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝑇𝐻𝐸 𝑁𝐴𝑇𝑈𝑅𝐸 𝑃𝐴𝐺𝐸 𝑂𝐹 <blockquote>{item_name.upper()}</blockquote> 𝐹𝑟𝑜𝑚 @HeXamonbot", parse_mode='HTML')
            return NATURE_PAGE
        else:
            update.message.reply_text(f"{item_name} 𝑖𝑠 𝑛𝑜𝑡 𝑎 𝑛𝑎𝑚𝑒 𝑜𝑓 𝑎 𝑙𝑒𝑔𝑒𝑛𝑑𝑎𝑟𝑦 𝑃𝑜𝑘é𝑚𝑜𝑛. 𝑃𝑙𝑒𝑎𝑠𝑒 𝑝𝑟𝑜𝑣𝑖𝑑𝑒 𝑎 𝑣𝑎𝑙𝑖𝑑 𝑙𝑒𝑔𝑒𝑛𝑑𝑎𝑟𝑦 𝑃𝑜𝑘é𝑚𝑜𝑛 𝑛𝑎𝑚𝑒.")
    elif category == 'non-legendary':
        if item_name in NON_LEGENDARY_POKEMON_NAMES:
            update.message.reply_text(f"𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝑇𝐻𝐸 𝑁𝐴𝑇𝑈𝑅𝐸 𝑃𝐴𝐺𝐸 𝑂𝐹 <blockquote>{item_name} </blockquote> 𝐹𝑟𝑜𝑚 @HeXamonbot",parse_mode="html")
            context.user_data["item_name"] =item_name
            return NATURE_PAGE
        else:
            update.message.reply_text(f"{item_name} 𝑖𝑠 𝑛𝑜𝑡 𝑎 𝑛𝑎𝑚𝑒 𝑜𝑓 𝑎 𝑁𝑜𝑛-𝑙𝑒𝑔𝑒𝑛𝑑𝑎𝑟𝑦 𝑃𝑜𝑘é𝑚𝑜𝑛. 𝑃𝑙𝑒𝑎𝑠𝑒 𝑝𝑟𝑜𝑣𝑖𝑑𝑒 𝑎 𝑣𝑎𝑙𝑖𝑑 𝑁𝑜𝑛-𝑙𝑒𝑔𝑒𝑛𝑑𝑎𝑟𝑦 𝑃𝑜𝑘é𝑚𝑜𝑛 𝑛𝑎𝑚𝑒.")
    elif category == 'shiny':
        if item_name in SHINY_POKEMON_NAMES:
            update.message.reply_text(f"𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝑇𝐻𝐸 𝑁𝐴𝑇𝑈𝑅𝐸 𝑃𝐴𝐺𝐸 𝑂𝐹 <blockquote>{item_name} </blockquote>𝐹𝑟𝑜𝑚 @HeXamonbot",parse_mode="html")
            context.user_data["item_name"] = item_name
            return NATURE_PAGE
        else:
            update.message.reply_text(f"{item_name} 𝑖𝑠 𝑛𝑜𝑡 𝑎 𝑛𝑎𝑚𝑒 𝑜𝑓 𝑎 𝑃𝑜𝑘é𝑚𝑜𝑛. 𝑃𝑙𝑒𝑎𝑠𝑒 𝑝𝑟𝑜𝑣𝑖𝑑𝑒 𝑎 𝑣𝑎𝑙𝑖𝑑 𝑃𝑜𝑘é𝑚𝑜𝑛 𝑛𝑎𝑚𝑒.")
    elif category == 'team':
        if item_name in POKEMON_TEAM:
            update.message.reply_text(f"𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝑇𝐻𝐸 𝑇𝑒𝑎𝑚 𝑃𝐴𝐺𝐸 𝑂𝐹 <blockquote>{item_name}</blockquote> 𝐹𝑟𝑜𝑚 @HeXamonbot" ,parse_html="html" )
            context.user_data["item_name"] = item_name
            return ITEM_DETAILS
        else:
            update.message.reply_text(f"{item_name} 𝑖𝑠 𝑛𝑜𝑡 𝑎 𝑛𝑎𝑚𝑒 𝑜𝑓 𝑎 𝑇𝑒𝑎𝑚 𝑃𝑙𝑒𝑎𝑠𝑒 𝑝𝑟𝑜𝑣𝑖𝑑𝑒 𝑎 𝑣𝑎𝑙𝑖𝑑 𝑇𝑒𝑎𝑚 𝑛𝑎𝑚𝑒.")
    elif category == 'tm':
        if item_name in TM:
            update.message.reply_text(f"𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝑇𝐻𝐸 𝑇𝑚 𝑃𝐴𝐺𝐸 𝑂𝐹 <blockquote> {item_name} </blockquote>𝐹𝑟𝑜𝑚 @HeXamonbot",parse_mode="html")
            context.user_data["item_name"] = item_name
            return ITEM_DETAILS
        else:
            update.message.reply_text(f"{item_name} 𝑖𝑠 𝑛𝑜𝑡 𝑎 𝑛𝑎𝑚𝑒 𝑜𝑓 𝑎 𝑇𝑚. 𝑃𝑙𝑒𝑎𝑠𝑒 𝑝𝑟𝑜𝑣𝑖𝑑𝑒 𝑎 𝑣𝑎𝑙𝑖𝑑 𝑇𝑚 𝑛𝑎𝑚𝑒.")

def nature_page(update, context):
    user = update.effective_user
    user_id = user.id

    item_name = context.user_data.get("item_name")  # Using get() method to avoid KeyError

    if item_name:
        if update.message.caption:
           caption_text = update.message.caption
           if "Nature" in caption_text and "Lv" in caption_text:
               if update.message.forward_from and update.message.forward_from.id == 572621020:
                   lines = caption_text.split("\n") 
                   fline = lines[0]
                   sline = lines[1]
                   lenat = fline.split(" ") 
                   natle = fline.split(":") 
                   typ = sline.split(":") 
                   # Save photo file_id
                   photo = update.message.photo[-1]  # Get the largest photo size
                   context.user_data["picture"] = photo.file_id

                   # Save nature and level in user_data
                   context.user_data["nature"] = natle[1]
                   context.user_data["lv"] = lenat[1]
                   context.user_data["ty"] = str(typ[1]) 

                   # Forward the message to the submission group
                   context.bot.forward_message(chat_id=SUBMISSION_GROUP_ID, from_chat_id=update.message.chat_id,
                                               message_id=update.message.message_id)
                   update.message.reply_text("<blockquote>𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝐼𝑉/𝐸𝑉 𝑃𝐴𝐺𝐸 𝑂𝐹 𝑌𝑂𝑈𝑅 𝑃𝑂𝐾𝐸𝑀𝑂𝑁</blockquote> 𝐹𝑅𝑂𝑀 @HeXamonbot ",parse_mode="html")
                   return POKEMON_IV
               else:
                   update.message.reply_text("<blockquote>𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝐹𝑅𝑂𝑀 @HeXamonbot</blockquote> 𝑜𝑡ℎ𝑒𝑟𝑤𝑖𝑠𝑒 𝑝𝑟𝑜𝑐𝑒𝑠𝑠 𝑤𝑖𝑙𝑙 𝑛𝑜𝑡 𝑤𝑜𝑟𝑘 𝑓𝑜𝑟 𝑠𝑒𝑛𝑑 𝑡𝑜 𝑠𝑢𝑏𝑚𝑖𝑠𝑠𝑖𝑜𝑛",parse_mode="html")
                   return NATURE_PAGE
           else:
               update.message.reply_text("<blockquote>𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 NATURE 𝑃𝐴𝐺𝐸 𝑂𝐹 𝑌𝑂𝑈𝑅 𝑃𝑂𝐾𝐸𝑀𝑂𝑁 </blockquote>𝐹𝑅𝑂𝑀 @HeXamonbot ",parse_mode="html")
               return NATURE_PAGE
        else:
            update.message.reply_text("PLEASE DON'T SEND ONLY PHOTO/DETAILS. <blockquote>FORWARD FULL PAGE FROM @HeXamonbot</blockquote>",parse_mode="html")
            return NATURE_PAGE


def item_details(update, context):
    user = update.effective_user
    user_id = user.id

    item_name = context.user_data.get("item_name")
    category = context.user_data.get("category")

    if item_name:
       if update.message.forward_from and update.message.forward_from.id == 572621020:
           update.message.reply_text(f"𝑃𝑙𝑒𝑎𝑠𝑒 𝑡𝑒𝑙𝑙 𝑏𝑎𝑠𝑒 𝑓𝑜𝑟 𝑦𝑜𝑢𝑟 <blockquote>'{category.upper()}'[{item_name}]</blockquote>",parse_mode="html")
           # Forward the information to submission group
           context.bot.forward_message(chat_id=SUBMISSION_GROUP_ID, from_chat_id=update.message.chat_id,
                                       message_id=update.message.message_id)


           context.user_data["details"] = update.message.text
           return BASE_PRICE
       else:
           update.message.reply_text(f"<blockquote>PLEASE FORWARD INFORMATION OF {item_name}</blockquote> FROM @HeXamonbot",parse_mode="html")
           return ITEM_DETAILS
    else:
        update.message.reply_text("<blockquote>PLEASE TELL ITEM NAME AT FIRST</blockquote>",parse_mode="html")
        return ITEM_NAME

def pokemon_iv(update, context):
    if update.message.caption:
        if "IV" in update.message.caption and "EV" in update.message.caption:
            if update.message.forward_from and update.message.forward_from.id == 572621020:
                context.user_data["iv_page"] =f"`{update.message.caption}`"
                update.message.reply_text("<blockquote>𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝑇𝐻𝐸 𝑀𝑂𝑉𝐸𝑆𝐸𝑇 𝑃𝐴𝐺𝐸 𝑂𝐹 𝑌𝑂𝑈𝑅 𝑃𝑂𝐾𝐸𝑀𝑂𝑁</blockquote> 𝐹𝑅𝑂𝑀 @HeXamonbot",parse_mode= "html")
                return MOVESET_PAGE
            else:
                update.message.reply_text("<blockquote>PLEASE FORWARD FROM @HeXamonbot.</blockquote> OTHERWISE PROCESS WILL NOT EXCUTE.",parse_mode="html")
                return POKEMON_IV
        else:
            update.message.reply_text("<blockquote>𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝐼𝑉/𝐸𝑉 𝑃𝐴𝐺𝐸 𝑂𝐹 𝑌𝑂𝑈𝑅 𝑃𝑂𝐾𝐸𝑀𝑂𝑁</blockquote> 𝐹𝑅𝑂𝑀 @HeXamonbot",parse_mode="html")
            return POKEMON_IV
    else:
        update.message.reply_text("<blockquote>Please forward right page of ivs/evs</blockquote> from @HeXamonbot.",parse_mode="html")
        return POKEMON_IV

def moveset_page(update, context):
    if update.message.caption:
        if "Power" in update.message.caption and "Accuracy" in update.message.caption:
            if update.message.forward_from and update.message.forward_from.id == 572621020:
                context.user_data["moveset_page"] = update.message.caption
                update.message.reply_text("<blockquote>PLEASE TELL ME IS ANY IV IS BOOSTED?</blockquote>\n <code> Yes </code> or <code> No </code>",parse_mode="html")
                return BOOSTED
            else:
                update.message.reply_text("<blockquote>Please forward from @HeXamonbot</blockquote>",parse_mode="html")
                return MOVESET_PAGE
        else:
            update.message.reply_text("<blockquote>Please forward right page of moveset </blockquote> from @HeXamonbot",parse_mode="html")
            return MOVESET_PAGE
    else:
        update.message.reply_text("<blockquote>Please forward right page of moveset </blockquote>from @HeXamonbot",parse_mode="html")
        return MOVESET_PAGE

def boosted(update, context):
    boosted = update.message.text.title()
    item_name = context.user_data.get("item_name")

    if boosted == 'Yes':
        context.user_data["boosted"] = boosted
        update.message.reply_text(f"𝑃𝐿𝐸𝐴𝑆𝐸 𝑇𝐸𝐿𝐿 𝑀𝐸 𝑇𝐻𝐸 𝐵𝐴𝑆𝐸 𝑃𝑅𝐼𝐶𝐸 𝐹𝑂𝑅 𝑌𝑂𝑈𝑅 <blockquote>{item_name}</blockquote>",parse_mode="html")
        return BASE_PRICE

    elif boosted == 'No':
         context.user_data["boosted"] = boosted
         update.message.reply_text(f"𝑃𝐿𝐸𝐴𝑆𝐸 𝑇𝐸𝐿𝐿 𝑀𝐸 𝑇𝐻𝐸 𝐵𝐴𝑆𝐸 𝑃𝑅𝐼𝐶𝐸 𝐹𝑂𝑅 𝑌𝑂𝑈𝑅<blockquote> {item_name}</blockquote>",parse_mode="html")
         return BASE_PRICE

    else:
         update.message.reply_text("<blockquote>𝐼 𝑊𝐼𝐿𝐿 𝐴𝐶𝐶𝐸𝑃𝑇 𝑂𝑁𝐿𝑌 𝑌𝐸𝑆/𝑁𝑂 𝑆𝑂 𝐺𝐼𝑉𝐸 𝐴𝑁𝑆𝑊𝐸𝑅 𝐼𝑁</blockquote>\n <code>𝑌𝐸𝑆 / 𝑁𝑂</code>",parse_mode="html")
         return BOOSTED

def base_price(update, context):
    base = update.message.text
    seller_id=update.message.from_user.id
    s_n=update.message.from_user.name
    item_name = context.user_data.get("item_name")
    seller = update.message.from_user
    boosted = context.user_data.get("boosted")
    moveset_page = context.user_data.get("moveset_page")
    iv_page = context.user_data.get("iv_page")
    nature = context.user_data.get("nature")
    lv = context.user_data.get("lv")
    details = context.user_data.get("details")
    types = str(context.user_data.get("ty")) 
    category = context.user_data.get("category")  # Added category variable
    picture = context.user_data.get("picture")

    # Assuming seller is an object with an id attribute
    seller_id = seller.id

    # Create a dictionary to store the seller's data
    seller_data[seller_id] = {}

# Save each variable in the dictionary if it contains data
    seller_data[seller_id]["item_name"] = item_name
    seller_data[seller_id]["seller"] = seller
    seller_data[seller_id]["boosted"] = boosted
    seller_data[seller_id]["moveset_page"] = moveset_page
    seller_data[seller_id]["iv_page"] = iv_page
    seller_data[seller_id]["nature"] = nature
    seller_data[seller_id]["lv"] = lv
    seller_data[seller_id]["details"] = details
    seller_data[seller_id]["types"] = types
    seller_data[seller_id]["category"] = category
    seller_data[seller_id]["picture"] = picture
    seller_data[seller_id]["base_price"] = base
    seller_data[seller_id]["name"] = seller.name


    try:
        number_text = update.message.text
        number = float(number_text[:-1]) * 1000 if number_text[-1].lower() == 'k' else float(number_text)
        if number % 100 == 0:
            if category in ['legendary', 'non-legendary', 'shiny']:
                update.message.reply_text(f"𝑇𝐻𝐴𝑁𝐾 𝑌𝑂𝑈 𝐹𝑂𝑅 𝐴𝐷𝐷 𝑌𝑂𝑈𝑅 𝑃𝑂𝐾𝐸𝑀𝑂𝑁 𝐼𝑁 𝐼𝐻𝐺 𝐴𝑈𝐶𝑇𝐼𝑂𝑁. <blockquote> 𝑌𝑂𝑈𝑅 {item_name}[{nature}] 𝐻𝐴𝑆 𝐵𝐸𝐸𝑁 𝑆𝐸𝑁𝑇 𝐹𝑂𝑅 𝑆𝑈𝐵𝑀𝐼𝑆𝑆𝐼𝑂𝑁</blockquote>",parse_mode="html")
                pokemons["item_name"].append(item_name) 
                pokemons["seller_id"].append(seller_id) 
                pokemons["boosted"].append(boosted) 
                pokemons["moveset_page"].append(moveset_page) 
                pokemons["iv_page"].append(iv_page) 
                pokemons["nature"].append(nature) 
                pokemons["lv"].append(lv) 
                pokemons["types"].append(f"{types}") 
                pokemons["category"].append(category) 
                pokemons["picture"].append(picture) 
                pokemons["base"].append(f"{number}")
                pokemons["name"].append(s_n) 


                context.user_data["base"] = number
                # Inline options
                inline_keyboard = [
                    [
                        InlineKeyboardButton("Approve", callback_data=f'papprove_{len(pokemons["picture"])-1}'),
                    ],
                    [
                        InlineKeyboardButton("Disapprove:👇", callback_data=f'disapprove_{len(pokemons["picture"])-1}'),
                    ],
                    [
                        InlineKeyboardButton("RIP Nature", callback_data=f'ripnature_{len(pokemons["picture"])-1}'),
                        InlineKeyboardButton("RIP IVs/EVs", callback_data=f'ripivsevs_{len(pokemons["picture"])-1}'),
                    ],
                    [
                        InlineKeyboardButton("Base High", callback_data=f'pbasehigh_{len(pokemons["picture"])-1}'),
                        InlineKeyboardButton("Wrong Information", callback_data=f'pwronginfo_{len(pokemons["picture"])-1}'),
                    ],
                    [
                        InlineKeyboardButton("Useless Poke", callback_data=f'uselesspoke_{len(pokemons["picture"])-1}'),
                        InlineKeyboardButton("Not in Demand", callback_data=f'notindemand_{len(pokemons["picture"])-1}'),
                    ]
                ]

                reply_markup = InlineKeyboardMarkup(inline_keyboard)

                # Sending message with inline options to submission group
                message = context.bot.send_photo(chat_id=SUBMISSION_GROUP_ID, photo=picture, caption=f"""
POKEMON CATEGORY: {category}

POKEMON DETAILS:-

NAME: {item_name}
LEVEL: {lv}
NATURE: {nature}
TYPES: {types}

IV AND EV POINTS:-
<code>{iv_page}</code>

MOVESETS:-
{moveset_page}

BOOSTED: {boosted}
BASE PRICE: {number}

SELLER USERNAME:- {seller.name}
SELLER ID:- {seller.id}
""", reply_markup=reply_markup, parse_mode="html")
                pokemons["msg_id"].append(message.message_id) 
            elif category in ['team', 'tm']:
                update.message.reply_text(f"<blockquote>𝑇𝐻𝐴𝑁𝐾 𝑌𝑂𝑈 𝐹𝑂𝑅 𝐴𝐷𝐷 𝑌𝑂𝑈𝑅 {category} 𝐼𝑁 𝐼𝐺𝐻 𝐴𝑈𝐶𝑇𝐼𝑂𝑁 𝑌𝑂𝑈𝑅 {category} 𝐻𝐴𝑆 𝐵𝐸𝐸𝑁 𝑆𝐸𝑁𝑇 𝐹𝑂𝑅 𝑆𝑈𝐵𝑀𝐼𝑆𝑆𝐼𝑂𝑁</blockquote>",parse_mode="html")
                tms["category"].append(category) 
                tms["details"].append(details) 
                tms["item_name"].append(item_name) 
                tms["base"].append(f"{number}")
                tms["name"].append(s_n)
                tms["seller_id"].append(seller_id)             
                context.user_data["base"]=number
                # Inline options
                Inline_keyboard = [
                    [
                        InlineKeyboardButton("Approve", callback_data=f'tapprove_{len(tms["details"])-1}')
                    ],
                    [
                        InlineKeyboardButton("Disapprove", callback_data=f'disapprove_{len(tms["details"])-1}')
                    ],
                    [
                        InlineKeyboardButton("Wrong Info", callback_data=f'twronginfo_{len(tms["details"])-1}'),
                        InlineKeyboardButton("Useless Team", callback_data=f'uselessteam_{len(tms["details"])-1}')
                    ],
                    [
                        InlineKeyboardButton("Base high", callback_data=f'tbasehigh_{len(tms["details"])-1}'),
                        InlineKeyboardButton("Wrong Display", callback_data=f'wrongdisplay_{len(tms["details"])-1}')
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(Inline_keyboard)
                #send message to submission group
                message = context.bot.send_message(chat_id=SUBMISSION_GROUP_ID, text=f"""
{category.upper()} NAME: {item_name}

{category.upper()} DETAILS:
{details}

BASE PRICE: {number}

SELLER USERNAME: {seller.name}
SELLER ID: {seller.id}
""", reply_markup=reply_markup, parse_mode="html")

                tms["msg_id"].append(message.message_id) 
            del seller_data[seller_id]
            current_add.remove(seller.id) 
            return ConversationHandler.END
        else:
            update.message.reply_text(f"<blockquote>OUR ADMINS DECIDE THAT BASE PRICE SHOULD BE MULTIPLE OF 100. BUT YOU TELL ({number_text}) IT IS MULTIPLE OF 100. SO IT WILL BE NOT ACCEPTED BY US.</blockquote>",parse_mode="html")
            return BASE_PRICE
    except ValueError:
        update.message.reply_text("<blockquote>PLEASE WRITE FULL NUMBER OR GIVE IN FORMAT [(number)k]. NO OTHER FORMAT WILL ACCEPT.</blockquote>",parse_mode="html" )
        return BASE_PRICE

def add_users(update,context):
    message_text=update.message.text
    data=message_text.split(" ")
    usersp=data[1]
    usersq=usersp.split(",")
    for user in usersq:
        user_list.append(int(user))
def stats(update, context):
    query = update.callback_query
    if query.data.startswith('papprove'):
        stats = "APPROVED"
    elif query.data.startswith('tapprove'):
        stats = "APPROVED"
    else:
        stats = "DISAPPROVED"

    return stats

def submission(update, context):
    admin = update.effective_user
    admin_name = admin.name

    query = update.callback_query
    callback_data = query.data

    approved = 'APPROVED'
    disapproved = 'DISAPPROVED'
    user_id = update.effective_user.id
    if user_id in approved_users:
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return

    query = update.callback_query
    callback_data = query.data
    id = int(callback_data.split('_')[1]) 
    Stats = stats(update, context)
    if query.data.startswith('papprove') or query.data.startswith('papprove') or query.data.startswith('uselesspoke') or query.data.startswith('ripnature') or query.data.startswith('ripivsevs') or query.data.startswith('pbasehigh') or query.data.startswith('notindemand') or query.data.startswith('pwronginfo') or query.data.startswith('disapprove'):
        seller_name = pokemons["name"][id]
        item_name = pokemons["item_name"][id]
        seller_id = pokemons["seller_id"][id]
        boosted = pokemons["boosted"][id]
        moveset_page = pokemons["moveset_page"][id]
        iv_page = pokemons["iv_page"][id]
        nature = pokemons["nature"][id]
        lv = pokemons["lv"][id]
        types = pokemons["types"][id]
        category = pokemons["category"][id]
        picture = pokemons["picture"][id]
        base_price = pokemons["base"][id]
        message_id = pokemons["msg_id"][id]
        mid = message_id
        pmessage = f"POKEMON NAME: {item_name}\nLEVEL: {lv}\nNATURE: {nature}\nTYPES: {types}\n\nIVs AND EVs:\n{iv_page}\n\nMOVESETS :\n{moveset_page}\n\nBoosted: {boosted}\nBase Price: {base_price}"
        updated_text = f"POKEMON CATEGORY: {category}\n\n > POKEMON DETAILS:-\n\nNAME: {item_name}\nLEVEL: {lv}\nNATURE: {nature}\nTYPES: {types}\n\n > IV AND EV POINTS:-\n{iv_page}\n\n > MOVESETS:-\n{moveset_page}\n\nBOOSTED: {boosted}\n\nBASE PRICE: {base_price}\n\n > SELLER USERNAME:- {seller_name}\n > SELLER ID:- {seller_id}\n\nIT HAS BEEN {Stats} BY {admin.full_name}({admin_name})\n"
    if query.data.startswith('tapprove') or query.data.startswith('wrongdisplay') or query.data.startswith('uselessteam') or query.data.startswith('twronginfo') or query.data.startswith('disapprove') or query.data.startswith('tbasehigh'):
        category = tms["category"][id]
        details = tms["details"][id]
        item_name = tms["item_name"][id]
        base_price = tms["base"][id]
        mid = tms["msg_id"][id]
        seller_id = tms["seller_id"][id]
        seller_name = tms["name"][id]
        
        tupdated_text = f"{category.upper()} \n > NAME: {item_name}\n\n{category.upper()} DETAILS:\n{details}\n\nBASE PRICE: {base_price}\n\n > SELLER USERNAME: {seller_name}\n > SELLER ID: {seller_id}\n\nIt has been {Stats} by {admin.full_name}({admin.name})\n"



    if limit[category] <=len(buyers[category]):
        context.bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=mid,
            text=f"Sorry Admins but Slots for this Category is full",parse_mode="html"
        )
        context.bot.send_message(
        chat_id=seller_id,
        text=f"<blockquote>YOUR {item_name} WOULD HAVE BEEN APPROVED BUT UNFORTUNATELY ALL SLOTS ARE FULL \n PLEASE TRY ON THE NEXT AUCTION.</blockquote>"
    ,parse_mode="html")
        return 
    if seller_id not in seller_lead:
        seller_lead[seller_id]={}
        seller_lead[seller_id]["bag"] = [] 
        seller_lead[seller_id]["item"] = [] 
    if seller_id not in seller_old:
        seller_old[seller_id]={}
        seller_old[seller_id]["bag"] = 0
        seller_old[seller_id]["item"] = 0  
    item_id = 1234
    if category == "legendary":
        item_id = len(legendary_list) 
    elif category == "non-legendary":
        item_id = len(non_legendary_list)
    elif category == "shiny":
        item_id = len(shiny_list) 
    elif category == "tm":
        item_id = len(tm_list) 
    elif category == "team":
        item_id = len(team_list)
    if callback_data.startswith('papprove'):
        
        context.bot.send_message(
        chat_id=seller_id,
        text=f"<blockquote>YOUR {item_name}[LV:{lv} & NATURE:{nature}] HAS BEEN APPROVED FOR NEXT AUCTION.</blockquote>"
    ,parse_mode="html")

        
        mm = context.bot.send_photo(
    chat_id=AUCTION_GROUP_ID,
    photo=picture,
    caption=f"""<code>╔══════════════════════════╗
<blockquote><b><i>POKEMON DETAILS:</i></b></blockquote>
╚══════════════════════════╝</code>
<i><b>NAME:</b></i> {item_name}
<i><b>LEVEL:</b></i> {lv}
<i><b>NATURE:</b></i> {nature}
<i><b>TYPE:</b></i> {types}

<code>╔══════════════════════════╗</code>
<blockquote><b><i>IVS/EVS:</i></b></blockquote>
<code>╚══════════════════════════╝</code>
<code>{iv_page}</code>

<code>╔══════════════════════════╗</code>
<blockquote><b><i>MOVESETS:</i></b></blockquote>
<code>╚══════════════════════════╝</code>
<code>{moveset_page}</code>

<i><b>BOOSTED:</b></i> {boosted}
<i><b>BASE PRICE:</b></i> {base_price}

<i><b>Item Id:</b></i> <code>{item_id}</code>""",
    parse_mode="HTML"
)

        msid = mm.message_id
        Inline_keyboard = [
                    [
                        InlineKeyboardButton("Bid Arriving...", url=f'https://t.me/{bot_name}?start={category}_{item_id}')
                    ]
        ]
        reply_markup = InlineKeyboardMarkup(Inline_keyboard)
        ne = context.bot.send_message(
        chat_id=AUCTION_GROUP_ID,text=f"""The Bid Page of {item_name}

highest bid - {base_price}
Bidder      - None""",reply_markup=reply_markup) 
        neid = ne.message_id
        rstr = generate() 
        while rstr in collection:
            rstr = generate()
        collection[rstr] = f"{category}_{item_id}_{neid}"
        Inline_keyboard = [
                    [
                        InlineKeyboardButton("Place Your Bid 🎴", url=f'https://t.me/{bot_name}?start={rstr}')
                    ]
        ]
        buyers[category].append(base_price) 
        buyers[f"{category}_name"].append("None") 
        reply_markup = InlineKeyboardMarkup(Inline_keyboard)
        context.bot.edit_message_text(
    chat_id=AUCTION_GROUP_ID,
    message_id=neid,
    text=f"""
╔══════════════════════════╗
<b>The Bid Page of {item_name}</b>
highest bid - {base_price} Pds
Bidder      - None
╚══════════════════════════╝""",
    reply_markup=reply_markup,
    parse_mode='HTML'
)
        seller_lead[seller_id]["item"].append(f"{category}$<a href='https://t.me/{AUC_NAME}/{mm.message_id}'>{item_name}</a>")
        seller_old[seller_id]["item"]+=1
        bac= context.bot.send_message(chat_id = backup, text= f"{category}:{item_id}:<a href='https://t.me/{AUC_NAME}/{msid}'>{item_name}</a>:{item_name}({nature}):{seller_name}-{seller_id}:{base_price}:None", disable_web_page_preview=True)
        back[f"{category}"].append(bac.message_id)    
        
        context.bot.edit_message_text(chat_id = backup, message_id = bac.message_id, text= f"{category}:{item_id}:<a href='https://t.me/{AUC_NAME}/{msid}'>{item_name}</a>:{item_name}({nature}):{seller_name}-{seller_id}:{base_price}:None:{bac.message_id}:{rstr}:{neid}", disable_web_page_preview=True)
        try:
            context.bot.edit_message_caption(
        chat_id=update.callback_query.message.chat_id,
        message_id=message_id,
        caption=f"{updated_text}\n Item Id `{rstr}`", parse_mode="markdown")
        except:
            query.edit_message_text("Error Occurred in editing but no problem should be there in approval") 
        if category == "legendary":

            legendary_list.append(f"{item_name}({nature}):{seller_name}-{seller_id}")
            legendary_item.append(f"<a href='https://t.me/{AUC_NAME}/{mm.message_id}'>{item_name}</a>") 
        elif category == "non-legendary":

           
            non_legendary_list.append(f"{item_name}({nature}):{seller_name}-{seller_id}")
            non_legendary_item.append(f"<a href='https://t.me/{AUC_NAME}/{mm.message_id}'>{item_name}</a>") 
        elif category == "shiny":

            shiny_list.append(f"{item_name}({nature}):{seller_name}-{seller_id}")
            shiny_item.append(f"<a href='https://t.me/{AUC_NAME}/{mm.message_id}'>{item_name}</a>") 
    if callback_data.startswith('tapprove'):
        context.bot.send_message(chat_id=seller_id, text=f"<blockquote>𝑌𝑜𝑢𝑟 {item_name} 𝐻𝑎𝑠 𝐵𝑒𝑒𝑛 𝑎𝑝𝑝𝑟𝑜𝑣𝑒𝑑.</blockquote>",parse_mode="html")
        

        
        mm=context.bot.send_message(chat_id=AUCTION_GROUP_ID, text=f"""<code>╔══════════════════════════╗</code>
{category.upper()} NAME: {item_name}

<blockquote>{category.upper()} DETAILS:</blockquote>
{details}

BASE PRICE: {base_price}
Item id {item_id}
<code>╚══════════════════════════╝</code>""", parse_mode="HTML")

        msid=mm.message_id
        Inline_keyboard = [
                    [
                        InlineKeyboardButton("Bid Arriving...", url=f'https://t.me/{bot_name}?start={category}_{item_id}')
                    ]
        ]
        reply_markup = InlineKeyboardMarkup(Inline_keyboard)
        ne = context.bot.send_message(
        chat_id=AUCTION_GROUP_ID,text=f"""The Bid Page of {item_name}

highest bid - {base_price}
Bidder      - None""",reply_markup=reply_markup) 
        neid = ne.message_id
        rstr = generate() 
        while rstr in collection:
            rstr = generate()
        collection[rstr] = f"{category}_{item_id}_{neid}"
        Inline_keyboard = [
                    [
                        InlineKeyboardButton("Place Your Bid 🎴", url=f'https://t.me/{bot_name}?start={rstr}')
                    ]
        ]
        buyers[category].append(base_price) 
        buyers[f"{category}_name"].append("None") 
        reply_markup = InlineKeyboardMarkup(Inline_keyboard)
        context.bot.edit_message_text(
    chat_id=AUCTION_GROUP_ID,
    message_id=neid,
    text=f"""
╔══════════════════════════╗
<b>The Bid Page of {item_name}</b>
highest bid - {base_price} Pds
Bidder      - None
╚══════════════════════════╝""",
    reply_markup=reply_markup,
    parse_mode='HTML'
)
        try:
            context.bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=mid,
            text=f"{tupdated_text}\n Item Id `{rstr}`",parse_mode="html"
        )
        except:
            query.edit_message_text("Error Occurred in editing but no problem should be there in approval") 
        seller_lead[seller_id]["item"].append(f"{category}$<a href='https://t.me/{AUC_NAME}/{mm.message_id}'>{item_name}</a>")
        seller_old[seller_id]["item"]+=1
        bac= context.bot.send_message(chat_id = backup, text= f"{category}:{item_id}:<a href='https://t.me/{AUC_NAME}/{msid}'>{item_name}</a>:{item_name}:{seller_name}-{seller_id}:{base_price}:None", disable_web_page_preview=True)
        back[f"{category}"].append(bac.message_id) 
        context.bot.edit_message_text(chat_id = backup, message_id = bac.message_id, text= f"{category}:{item_id}:<a href='https://t.me/{AUC_NAME}/{msid}'>{item_name}</a>:{item_name}:{seller_name}-{seller_id}:{base_price}:None:{bac.message_id}:{rstr}:{neid}", disable_web_page_preview=True)
        if category == "team":  
            team_list.append(f"{item_name} Team:{seller_name}-{seller_id}")
            team_item.append(f"<a href='https://t.me/{AUC_NAME}/{msid}'>{item_name}</a>") 
        elif category == "tm":            
            tm_list.append(f"{item_name}:{seller_name}-{seller_id}")
            tm_item.append(f"<a href='https://t.me/{AUC_NAME}/{msid}'>{item_name}</a>")
    if callback_data.startswith('disapprove'):
        update.callback_query.answer(text="PLEASE CHOOSE ANY REASON FROM BELOW TO DISAPPPROVE.", show_alert=True)

    if callback_data.startswith('ripnature'):
        context.bot.send_message(chat_id=seller_id, text=f"<blockquote>YOUR {item_name}[{nature}] </blockquote>HAS BEEN DISAPPROVED FOR IT'S RIP NATURE",parse_mode="html" )
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=updated_text)

    if callback_data.startswith('ripivsevs'):
        context.bot.send_message(chat_id=seller_id, text=f"<blockquote>YOUR {item_name}[{nature}] </blockquote>HAS BEEN DISAPPROVED FOR IT'S RIP IV/EV",parse_mode="html" )
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=updated_text)

    if callback_data.startswith('uselesspoke'):
        context.bot.send_message(chat_id=seller_id, text=f"<blockquote>YOUR {item_name} </blockquote>HAS BEEN DISAPPROVED BECAUSE IT IS USELESS POKEMON",parse_mode="html" )
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=updated_text)

    if callback_data.startswith('notindemand'):
        context.bot.send_message(chat_id=seller_id, text=f"<blockquote>YOUR {item_name} </blockquote>HAS BEEN DISAPPROVED BECAUSE IT IS NOT IN DEMAND",parse_mode="html" )
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=updated_text)

    if callback_data.startswith('twronginfo'):
        context.bot.send_message(chat_id=seller_id, text=f"<blockquote>YOUR {item_name} </blockquote>HAS BEEN DISAPPROVED BECAUSE YOU GIVE WRONG INFORMATION.",parse_mode="html" )
        # Edit the message with the updated text and photo
        context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=message_id,
                                      text=tupdated_text)

    if callback_data.startswith('uselessteam'):
        context.bot.send_message(chat_id=seller_id, text=f"<blockquote>Your team </blockquote>is disapproved because it is useless",parse_mode="html" )
        # Edit the message with the updated text and photo
        context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=message_id,
                                      text=tupdated_text)

    if callback_data.startswith('tbasehigh'):
        context.bot.send_message(chat_id=seller_id, text="<blockquote>Your tm </blockquote>has been disapproved because it's base is too high.",parse_mode="html" )
        # Edit the message with the updated text and photo
        context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=message_id,
                                      text=tupdated_text)

    if callback_data.startswith('wrongdisplay'):
        context.bot.send_message(chat_id=seller_id, text=f"<blockquote>Your {item_name}</blockquote> has been disapproved because you give wrong display of it",parse_mode="html" )
        # Edit the message with the updated text and photo
        context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                      message_id=message_id,
                                      text=tupdated_text)

    if callback_data.startswith('pbasehigh'):
        context.bot.send_message(chat_id=seller_id, text=f" <blockquote>Your {item_name} </blockquote>has been disapproved because it's base is too high",parse_mode="html" )
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=updated_text)

    if callback_data.startswith('pwronginfo'):
        context.bot.send_message(chat_id=seller_id, text=f" <blockquote>Your {item_name} </blockquote>is disapproved because you gave wrong information of it",parse_mode="html" )
        # Edit the message with the updated text and photo
        context.bot.edit_message_caption(chat_id=update.callback_query.message.chat_id,
                                         message_id=message_id,
                                         caption=updated_text)



def sellers_list(update, context):
  items = ["legendary", "non-legendary", "shiny", "team", "tm"]
  
  for category in items:
    message = f"------[{category.upper()}]------\n"
    no = 0
    
    if category == "legendary":
      l = legendary_list
    if category == "non-legendary":
      l = non_legendary_list
    if category == "shiny":
      l = shiny_list
    if category == "team":
      l = team_list
    if category == "tm":
      l = tm_list
    for i in l:
      message += f"{no+1} - {i}\n"
      no = no+1
    context.bot.send_message(chat_id=update.message.chat.id,text=message,parse_mode="html") 
  context.bot.send_message(chat_id=update.message.chat.id,text="SENT All SELLERS LIST" ,parse_mode="html") 

def buyers_list(update, context):
  message_text = " BUYERS _ LIST \n"
  items = ["legendary", "non-legendary", "shiny", "team", "tm"]
  for category in items:
    
    message = f"------[{category.upper()}]------\n"
    if category == "legendary":
      l = legendary_item
      nam = buyers["legendary_name"]
    if category == "non-legendary":
      l = non_legendary_item
      nam = buyers["non-legendary_name"]
    if category == "shiny":
      l = shiny_item
      nam = buyers["shiny_name"]
    if category == "team":
      l = team_item
      nam = buyers["team_name"]
    if category == "tm":
      l = tm_item
      nam = buyers["tm_name"]
    i = 0
    for no in buyers[category]:
      try: 
        user = context.bot.get_chat(nam[i]) if is_digit(nam[i]) else None 
        username= "@" + user.username if is_digit(nam[i]) else "None"
      except:
        user = None
        username = "None"
      message += f"{i+1} - {l[i]} : {username} - {nam[i]} \n --- ({no} Poke Dollars) ---\n"
      if is_digit(nam[i]):
        if user.id not in seller_lead:
          seller_lead[user.id] = {}  
          seller_lead[user.id]["bag"] = [] 
          seller_lead[user.id]["item"] = [] 
        seller_lead[user.id]["bag"].append(f"{category}${l[i]} - {no} Poke Dollars") 
        if user.id not in seller_old:
          seller_old[user.id] = {}  
          seller_old[user.id]["bag"] = 0
          seller_old[user.id]["item"] = 0
        seller_old[user.id]["bag"]+=1
      i = i+1
    
    mm = context.bot.send_message(chat_id=update.message.chat.id,text=message,parse_mode="html",disable_web_page_preview=True)
    message_text = message_text + f"║•Category : <a href='https://t.me/{update.message.chat.username}/{mm.message_id}'>{category.upper()}</a>\n"
  nm = context.bot.send_message(chat_id=update.message.chat.id,text=f"<code>SENT All BUYERS LIST</code>\n╔══════════════╗\n{message_text}\n╚══════════════╝" ,parse_mode="html", disable_web_page_preview=True)
  context.bot.pin_chat_message(chat_id=update.message.chat.id, message_id=nm.message_id) 

def items(update, context):
    user_id = update.effective_user.id 
    query = update.callback_query

    

    if query:
        sp = query.data.split("_")
        if int(user_id) != int(sp[2]):
            query.answer("This is not yours 😮‍💨",) 
            return

        data = query.data
        i = 0
        message_text = f"HERE IS THE LIST OF {sp[1].upper()} FOR SALE\n╔══════════════╗" 
        if "legendary" == sp[1]:
            for item in legendary_item:
                message_text += f"\n║-{i + 1} {item}"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Non-Legendary", callback_data=f"item_non-legendary_{user_id}"),
                InlineKeyboardButton("Shiny", callback_data=f"item_shiny_{user_id}"),
                InlineKeyboardButton("Team", callback_data=f"item_team_{user_id}"),
                InlineKeyboardButton("TM", callback_data=f"item_tm_{user_id}"),
            ]])
        elif "non-legendary" == sp[1]:
            for item in non_legendary_item:
                message_text += f"\n║-{i + 1} {item}"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Legendary", callback_data=f"item_legendary_{user_id}"),
                InlineKeyboardButton("Shiny", callback_data=f"item_shiny_{user_id}"),
                InlineKeyboardButton("Team", callback_data=f"item_team_{user_id}"),
                InlineKeyboardButton("TM", callback_data=f"item_tm_{user_id}"),
            ]])
        elif "shiny" == sp[1]:
            for item in shiny_item:
                message_text += f"\n║-{i + 1} {item}"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Legendary", callback_data=f"item_legendary_{user_id}"),
                InlineKeyboardButton("Non-Legendary", callback_data=f"item_non-legendary_{user_id}"),
                InlineKeyboardButton("Team", callback_data=f"item_team_{user_id}"),
                InlineKeyboardButton("TM", callback_data=f"item_tm_{user_id}"),
            ]])
        elif "team" == sp[1]:
            for item in team_item:
                message_text += f"\n║-{i + 1} {item}"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Legendary", callback_data=f"item_legendary_{user_id}"),
                InlineKeyboardButton("Non-Legendary", callback_data=f"item_non-legendary_{user_id}"),
                InlineKeyboardButton("Shiny", callback_data=f"item_shiny_{user_id}"),
                InlineKeyboardButton("TM", callback_data=f"item_tm_{user_id}"),
            ]])
        elif "tm" == sp[1]:
            for item in tm_item:
                message_text += f"\n║-{i + 1} {item}"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Legendary", callback_data=f"item_legendary_{user_id}"),
                                InlineKeyboardButton("Non-Legendary", callback_data=f"item_non-legendary_{user_id}"),
                InlineKeyboardButton("Shiny", callback_data=f"item_shiny_{user_id}"),
                InlineKeyboardButton("Team", callback_data=f"item_team_{user_id}"),
            ]])
        else:
            message_text = "╔══════════════╗\nInvalid option selected."
            keyboard = None

        query.edit_message_text(
            text=f"{message_text}\n╚══════════════╝",
            parse_mode="html",
            disable_web_page_preview=True,
            reply_markup=keyboard
        )

    else:
        # Handle the case when there is no callback query
        message_text = "HERE IS THE LIST OF LEGENDARY POKEMONS\n╔══════════════╗"
        i = 0
        for user in legendary_item:
          message_text = f"{message_text}\n║-{i+1} {user}"
          i+=1
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("Non-Legendary", callback_data=f"item_non-legendary_{user_id}"),
            InlineKeyboardButton("Shiny", callback_data=f"item_shiny_{user_id}"),
            InlineKeyboardButton("Team", callback_data=f"item_team_{user_id}"),
            InlineKeyboardButton("TM", callback_data=f"item_tm_{user_id}"),
        ]]) 
        
        context.bot.send_message(chat_id=update.message.chat.id, text=f"{message_text}\n╚══════════════╝",reply_markup=keyboard,disable_web_page_preview=True, parse_mode="html")

def mybag(update, context):
    user_id = update.effective_user.id
    if user_id not in seller_lead:
        seller_lead[user_id] = {}
        seller_lead[user_id]["bag"] = []
        seller_lead[user_id]["item"] = []

    item_list = seller_lead[user_id]["bag"]
    legendary = []
    non_legendary = []
    shiny = []
    team = []
    tm = []

    # Categorize items
    for item in item_list:
        category, name = item.split("$")
        if category == "legendary":
            legendary.append(name)
        elif category == "non-legendary":
            non_legendary.append(name)
        elif category == "shiny":
            shiny.append(name)
        elif category == "team":
            team.append(name)
        elif category == "tm":
            tm.append(name)

    if update.callback_query:
        query = update.callback_query
        sp = query.data.split("_")

        if int(user_id) != int(sp[2]):
            query.answer("This is not yours 😮‍💨")
            return

        i = 0
        message_text = f" HERE IS THE LIST OF {sp[1].upper()} IN YOUR BAG\n╔══════════════╗"

        # Determine which category is being viewed
        if "legendary" == sp[1]:
            for item in legendary:
                message_text += f"\n║-{i + 1} {item} --- id : <code>{i}</code>"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Non-Legendary", callback_data=f"bag_non-legendary_{user_id}"),
                InlineKeyboardButton("Shiny", callback_data=f"bag_shiny_{user_id}"),
                InlineKeyboardButton("Team", callback_data=f"bag_team_{user_id}"),
                InlineKeyboardButton("TM", callback_data=f"bag_tm_{user_id}"),
            ]])
        elif "non-legendary" == sp[1]:
            for item in non_legendary:
                message_text += f"\n║-{i + 1} {item} --- id : <code>{i}</code>"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Legendary", callback_data=f"bag_legendary_{user_id}"),
                InlineKeyboardButton("Shiny", callback_data=f"bag_shiny_{user_id}"),
                InlineKeyboardButton("Team", callback_data=f"bag_team_{user_id}"),
                InlineKeyboardButton("TM", callback_data=f"bag_tm_{user_id}"),
            ]])
        elif "shiny" == sp[1]:
            for item in shiny:
                message_text += f"\n║-{i + 1} {item} --- id : <code>{i}</code>"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Legendary", callback_data=f"bag_legendary_{user_id}"),
                InlineKeyboardButton("Non-Legendary", callback_data=f"bag_non-legendary_{user_id}"),
                InlineKeyboardButton("Team", callback_data=f"bag_team_{user_id}"),
                InlineKeyboardButton("TM", callback_data=f"bag_tm_{user_id}"),
            ]])
        elif "team" == sp[1]:
            for item in team:
                message_text += f"\n║-{i + 1} {item} --- id : <code>{i}</code>"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Legendary", callback_data=f"bag_legendary_{user_id}"),
                InlineKeyboardButton("Non-Legendary", callback_data=f"bag_non-legendary_{user_id}"),
                InlineKeyboardButton("Shiny", callback_data=f"bag_shiny_{user_id}"),
                InlineKeyboardButton("TM", callback_data=f"bag_tm_{user_id}"),
            ]])
        elif "tm" == sp[1]:
            for item in tm:
                message_text += f"\n║-{i + 1} {item} --- id : <code>{i}</code>"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Legendary", callback_data=f"bag_legendary_{user_id}"),
                                InlineKeyboardButton("Non-Legendary", callback_data=f"bag_non-legendary_{user_id}"),
                InlineKeyboardButton("Shiny", callback_data=f"bag_shiny_{user_id}"),
                InlineKeyboardButton("Team", callback_data=f"bag_team_{user_id}"),
            ]])
        else:
            message_text = "╔══════════════╗\nInvalid option selected."
            keyboard = None

        query.edit_message_text(
            text=f"{message_text}\n╚══════════════╝",
            parse_mode="html",
            disable_web_page_preview=True,
            reply_markup=keyboard
        )
    else:
        # Default view when there's no callback query (show legendary items)
        message_text = "HERE IS THE LIST OF LEGENDARY ITEMS IN YOUR BAG\n╔══════════════╗"
        i = 0
        for item in legendary:
            message_text += f"\n║-{i + 1} {item} --- id : <code>{i}</code>"
            i += 1

        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("Non-Legendary", callback_data=f"bag_non-legendary_{user_id}"),
            InlineKeyboardButton("Shiny", callback_data=f"bag_shiny_{user_id}"),
            InlineKeyboardButton("Team", callback_data=f"bag_team_{user_id}"),
            InlineKeyboardButton("TM", callback_data=f"bag_tm_{user_id}"),
        ]])

        context.bot.send_message(
            chat_id=update.message.chat.id,
            text=f"{message_text}\n╚══════════════╝",
            reply_markup=keyboard,
            disable_web_page_preview=True,
            parse_mode="html"
        )
def myitems(update, context):
    user_id = update.effective_user.id
    if user_id not in seller_lead:
        seller_lead[user_id] = {}
        seller_lead[user_id]["bag"] = []
        seller_lead[user_id]["item"] = []

    item_list = seller_lead[user_id]["item"]
    
    legendary = []
    non_legendary = []
    shiny = []
    team = []
    tm = []

    # Categorize items
    for item in item_list:
        category, name = item.split("$")
        if category == "legendary":
            legendary.append(name)
        elif category == "non-legendary":
            non_legendary.append(name)
        elif category == "shiny":
            shiny.append(name)
        elif category == "team":
            team.append(name)
        elif category == "tm":
            tm.append(name)

    if update.callback_query:
        query = update.callback_query
        sp = query.data.split("_")
        query.edit_message_text(
            text=f"Wait....") 

        if int(user_id) != int(sp[2]):
            query.answer("This is not yours 😮‍💨")
            return

        i = 0
        message_text = f" HERE IS THE LIST OF YOUR {sp[1].upper()} FOR SALE\n╔══════════════╗ "

        
        if "legendary" == sp[1]:
            for item in legendary:
                message_text += f"\n║-{i + 1} {item}"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Non-Legendary", callback_data=f"my_non-legendary_{user_id}"),
                InlineKeyboardButton("Shiny", callback_data=f"my_shiny_{user_id}"),
                InlineKeyboardButton("Team", callback_data=f"my_team_{user_id}"),
                InlineKeyboardButton("TM", callback_data=f"my_tm_{user_id}"),
            ]])
        elif "non-legendary" == sp[1]:
            for item in non_legendary:
                message_text += f"\n║-{i + 1} {item}"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Legendary", callback_data=f"my_legendary_{user_id}"),
                InlineKeyboardButton("Shiny", callback_data=f"my_shiny_{user_id}"),
                InlineKeyboardButton("Team", callback_data=f"my_team_{user_id}"),
                InlineKeyboardButton("TM", callback_data=f"my_tm_{user_id}"),
            ]])
        elif "shiny" == sp[1]:
            for item in shiny:
                message_text += f"\n║-{i + 1} {item}"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Legendary", callback_data=f"my_legendary_{user_id}"),
                InlineKeyboardButton("Non-Legendary", callback_data=f"my_non-legendary_{user_id}"),
                InlineKeyboardButton("Team", callback_data=f"my_team_{user_id}"),
                InlineKeyboardButton("TM", callback_data=f"my_tm_{user_id}"),
            ]])
        elif "team" == sp[1]:
            for item in team:
                message_text += f"\n║-{i + 1} {item}"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Legendary", callback_data=f"my_legendary_{user_id}"),
                InlineKeyboardButton("Non-Legendary", callback_data=f"my_non-legendary_{user_id}"),
                InlineKeyboardButton("Shiny", callback_data=f"my_shiny_{user_id}"),
                InlineKeyboardButton("TM", callback_data=f"my_tm_{user_id}"),
            ]])
        elif "tm" == sp[1]:
            for item in tm:
                message_text += f"\n║-{i + 1} {item}"
                i += 1
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("Legendary", callback_data=f"my_legendary_{user_id}"),
                InlineKeyboardButton("Non-Legendary", callback_data=f"my_non-legendary_{user_id}"),
                InlineKeyboardButton("Shiny", callback_data=f"my_shiny_{user_id}"),
                InlineKeyboardButton("Team", callback_data=f"my_team_{user_id}"),
            ]])
        else:
            message_text = "Invalid option selected."
            keyboard = None

        query.edit_message_text(
            text=f"{message_text}\n╚══════════════╝",
            parse_mode="html",
            disable_web_page_preview=True,
            reply_markup=keyboard
        )
    else:
        # Default view when there's no callback query (show cores)
        message_text = "HERE IS THE LIST OF YOUR LEGENDARY FOR SALE\n╔══════════════╗"
        i = 0
        for item in legendary:
            message_text += f"\n║-{i + 1} {item}"
            i += 1

        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("Non-Legendary", callback_data=f"my_non-legendary_{user_id}"),
            InlineKeyboardButton("Shiny", callback_data=f"my_shiny_{user_id}"),
            InlineKeyboardButton("Team", callback_data=f"my_team_{user_id}"),
            InlineKeyboardButton("TM", callback_data=f"my_tm_{user_id}")
        ]])

        context.bot.send_message(
            chat_id=update.message.chat.id,
            text=f"{message_text}\n╚══════════════╝",
            reply_markup=keyboard,
            disable_web_page_preview=True,
            parse_mode="html"
        )

def profile(update,context):
    user = update.effective_user
    seller_id=user.id
    user_id = update.effective_user.id
    if user_id not in seller_lead:
        seller_lead[user_id] = {}
        seller_lead[user_id]["bag"] = []
        seller_lead[user_id]["item"] = []

    item_list = seller_lead[user_id]["item"]
    
    legendary = []
    non_legendary = []
    shiny = []
    team = []
    tm = []
    for item in item_list:
        category, name = item.split("$")
        if category == "legendary":
            legendary.append(name)
        elif category == "non-legendary":
            non_legendary.append(name)
        elif category == "shiny":
            shiny.append(name)
        elif category == "team":
            team.append(name)
        elif category == "tm":
            tm.append(name)
    total= len(legendary) + len(non_legendary) + len(shiny) + len(team) + len(tm) 
    if user.id in owners:
        ver="✔️"
        post="OWNER💯"
    elif user.id in approved_users:
        ver="✔️"
        post="Admin📃"
    else:
        ver="❌"
        post="member🎭"
    profile_photos = context.bot.get_user_profile_photos(user_id, limit=1)

    if profile_photos.photos:  
        photos = profile_photos.photos
        if photos [0] : 
            photo = photos[0][-1]  # Access the last element (largest size)
            
        else:
            photo = "https://files.catbox.moe/i4ivas.jpg"
    else:
        photo = "https://files.catbox.moe/i4ivas.jpg"


    leg= len(legendary) 
    non_leg= len(non_legendary) 
    shiny= len(shiny) 
    tm= len(tm) 
    team= len(team) 
    try:
      message=f"<b>Here is Profile Of {user.first_name}\n\n<blockquote>★ » Name: {user.first_name}\n★Username : @{user.username}\n★ ID: {user.id}</blockquote>\n➖➖➖➖➖➖➖➖➖➖➖☆\n┃╸ 🔺 0L : {non_leg} \n┃╸ 🔺6L : {leg}\n┃╸ 🔺 Shiny : {shiny}\n┃╸ 🔺 TMs : {tm}\n┃╸ 🔺 Teams : {team}\n┃╸💲 Total :{total}\n★➖➖➖➖➖➖➖➖➖➖☆\n┃╸ ▪️ Verified? - {ver}\n┃╸ ▫️Status : {post}\n★➖➖➖➖➖➖➖➖➖➖☆ </b>"
      context.bot.send_photo(chat_id=update.message.chat.id, photo=photo, caption=message, parse_mode="html")
    except:
      update.message.reply_text(message) 
    
def cancel(update, context):
    update.message.reply_text("DONE YOUR RUNNING COMMAND HAS STOPED.")
    if update.message.from_user.id in current_add:
        current_add.remove (update.message.from_user.id) 
    
    return ConversationHandler.END
    
def approve_command(update,context):
    user_id = update.message.from_user.id
    if user_id in owners:
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


def current(update, context):
    """
    Displays the current list of Pokémon and teams with limits and available slots.
    """

    if update.message.from_user.id not in approved_users:
        context.bot.send_message(
            chat_id=update.message.chat.id, text="You are not an approved user."
        )
        return

    total = (
        len(legendary_item)
        + len(non_legendary_item)
        + len(shiny_item)
        + len(tm_item)
        + len(team_item)
    )

    message = (
        "<code>║═════════════════════║\n"
"║𝐶𝑢𝑟𝑟𝑒𝑛𝑡 𝑙𝑖𝑠𝑡 𝑜𝑓 𝑃𝑜𝑘𝑒𝑚𝑜𝑛 & 𝑇𝑚𝑠║\n"
        "║═════════════════════║\n"
"║                          \n"
f"║★ 𝐿𝑒𝑔𝑒𝑛𝑑𝑎𝑟𝑦: {len(legendary_item)}/{limit['legendary']} [Left: {limit['legendary'] - len(legendary_item):>2}]\n" 
f"║★ 𝑁𝑜𝑛-𝑙𝑒𝑔𝑒𝑛𝑑𝑎𝑟𝑦: {len(non_legendary_item)}/{limit['non-legendary']} [Left: {limit['non-legendary'] - len(non_legendary_item):>2}]\n"
f"║★ 𝑆ℎ𝑖𝑛𝑦: {len(shiny_item)}/{limit['shiny']} [Left: {limit['shiny'] - len(shiny_item):>2}]\n"
f"║★ 𝑇𝑚𝑠: {len(tm_item)}/{limit['tm']} [Left: {limit['tm'] - len(tm_item):>2}]\n"
f"║★ 𝑇𝑒𝑎𝑚𝑠: {len(team_item)}/{limit['team']} [Left: {limit['team'] - len(team_item):>2}]\n"
"║                        \n"
f"║★ 𝑇𝑜𝑡𝑎𝑙: {total}         \n"
"║                        \n"
"║═════════════════════║</code>"
    )

    context.bot.send_message(
        chat_id=update.effective_chat.id, text=message, parse_mode="html"
    )


    
def clear_all(update, context):
    global buyers, seller_data, seller_lead, pet_list, core_list, tools_list, resources_list
    global pet_item, core_item, tools_item, resources_item
    global tools_caption, pet_picture, pet_caption, core_picture, core_caption, resources_caption
    global current_add, bist, pokemons, tms, back

    id = update.effective_user.id
    if id not in approved_users:
        update.callback_query.answer("You are not an approved user.", show_alert=True)
        return

    query = update.callback_query
    data = query.data
    if "yes" in data:
        buyers.clear()
        seller_data.clear()
        seller_lead.clear()
        legendary_list.clear()
        non_legendary_list.clear()
        team_list.clear()
        tm_list.clear()
        shiny_list.clear() 
        legendary_item.clear()
        non_legendary_item.clear()
        team_item.clear()
        shiny_item.clear()
        tm_item.clear()
        current_add.clear()
        pokemons.clear()
        tms.clear()
        back.clear()
        bist=[]
        pokemons = {}
        tms = {}
        pokemons["name"] = []
        pokemons["item_name"] = []
        pokemons["seller_id"] = []
        pokemons["boosted"] = []
        pokemons["moveset_page"] = []
        pokemons["iv_page"] = []
        pokemons["nature"] = []
        pokemons["lv"] = []
        pokemons["base"] = []
        pokemons["types"] = []
        pokemons["category"] = []
        pokemons["picture"] = []
        pokemons["msg_id"] = []
        tms["category"] = []
        tms["details"] = []
        tms["item_name"] = []
        tms["base"] = []
        tms["msg_id"] = []
        tms["name"] = []
        tms["seller_id"] = []
        no=0
        buyers = {
    "legendary" : [], 
    "non-legendary" : [], 
    "shiny" : [], 
    "tm" : [], 
    "team" : [], 
    "legendary_name" : [], 
    "non-legendary_name" : [], 
    "shiny_name" : [], 
    "tm_name" : [], 
    "team_name" : []
         }
        back = {
    "legendary" : [], 
    "non-legendary" : [], 
    "shiny" : [], 
    "tm" : [], 
    "team" : []
       }
        query.edit_message_text(text=f"Ok Roger That!\nDONE Cleared all data\n\nHave a nice day!")

    elif "no" in data:
        query.edit_message_text(text=f"Ok Roger That!\nbut remember to clear previous data before starting new Auction. Have a nice day!")

def clear(update, context):
    user_id = update.message.from_user.id
    if user_id not in owners:
        update.message.reply_text("You are not one of owner. So shut the hell up.")
        return

    keyboard = [
        [
            InlineKeyboardButton("YES", callback_data='clear_yes'),
            InlineKeyboardButton("NO", callback_data='clear_no'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("DO YOU WANT TO CLEAR All OLD DATA?", reply_markup=reply_markup)
  
  
def sell(update, context): 
    user_id = update.effective_user.id
    if user_id in approved_users:
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
    sellers_list(update, context) 
def buy(update, context):
    user_id = update.effective_user.id
    if user_id in approved_users:
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
    buyers_list(update, context) 
    

def send_collection(update, context):

    chat_id = update.effective_chat.id
    message = "Contents of the collection:\n"

    for key, value in collection.items():
        message += f"- {key}: {value}\n"  # Format each item

    context.bot.send_message(chat_id=chat_id, text=message)

def top_sellers_buyers(update, context):

    try:
        num_top = int(context.args[0]) if context.args else 5  # Default to top 5 if no argument
        if num_top <= 0:
            update.message.reply_text("Please provide a positive number for the top count.")
            return
    except (ValueError, IndexError):
        update.message.reply_text("Invalid input.  Please use: /top <number>")
        return

    if not seller_old:
        update.message.reply_text("No data available yet.")
        return

    # Sort by items sold (sellers)
    top_sellers = sorted(seller_old.items(), key=lambda item: item[1]["items"], reverse=True)[:num_top]

    # Sort by items bought (buyers) - "bag" refers to items bought
    top_buyers = sorted(seller_old.items(), key=lambda item: item[1]["bag"], reverse=True)[:num_top]

    seller_message = f"Top {len(top_sellers)} Sellers:\n"
    if not top_sellers:
        seller_message += "No sellers found.\n"
    else:
        for user_id, data in top_sellers:
            seller_message += f"User ID: {user_id}, Items Sold: {data['items']}\n"

    buyer_message = f"Top {len(top_buyers)} Buyers:\n"
    if not top_buyers:
        buyer_message += "No buyers found.\n"
    else:
        for user_id, data in top_buyers:
            buyer_message += f"User ID: {user_id}, Items Bought: {data['bag']}\n"

    update.message.reply_text(seller_message + "\n" + buyer_message)



updater = Updater("7921044809:AAEtRGLlWVM6RzDVZis3QjZpIxW1l3Vfd5c", use_context=True)
dispatcher = updater.dispatcher    
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add)],
    states={
        ITEM_NAME: [MessageHandler(Filters.text & ~Filters.command, item_name)],
        NATURE_PAGE: [MessageHandler((Filters.text | Filters.photo) & ~Filters.command, nature_page)],
        ITEM_DETAILS: [MessageHandler(Filters.text & ~Filters.command, item_details)],
        POKEMON_IV: [MessageHandler((Filters.text | Filters.photo) & ~Filters.command, pokemon_iv)],
        MOVESET_PAGE: [MessageHandler((Filters.text | Filters.photo) & ~Filters.command, moveset_page)],
        BOOSTED: [MessageHandler(Filters.text & ~Filters.command, boosted)],
        BASE_PRICE: [MessageHandler(Filters.text & ~Filters.command, base_price)],

    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler("broadcast", broadcast)],
    states={
        BROADCAST_MESSAGE: [MessageHandler(Filters.text & ~Filters.command, broadcast_message)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

bid_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        HANDLE_BID: [MessageHandler((Filters.text) & ~Filters.command, handle_bid)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)

c_hand=ConversationHandler(
        entry_points=[CommandHandler('back_up', back_up)],
        states={
            CHECKING: [
                MessageHandler(Filters.text & ~Filters.command, check_message),
                CommandHandler('stop', stop),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    
def main():

    # Add handlers (command, message, conversation handlers)

    dp = dispatcher #Use the dispatcher var to add your handlers as it is already initialized with the updater

    dp.add_handler(conversation_handler) 
    dp.add_handler(conv_handler) 
    dp.add_handler(c_hand) 
    dp.add_handler(bid_handler) 
    dp.add_handler(MessageHandler(Filters.text, check_working))
    dp.add_handler(CommandHandler('buyers', buy))
    dp.add_handler(CommandHandler('approve', approve_command))
    dp.add_handler(CommandHandler('sellers', sell))
    dp.add_handler(CommandHandler('users', users))
    dp.add_handler(CommandHandler('current', current))
    dp.add_handler(CommandHandler('add_users', add_users))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('collection', send_collection))
    dp.add_handler(CommandHandler('items',items))
    dp.add_handler(CommandHandler('profile',profile))
    dp.add_handler(CommandHandler('clear', clear))
    dp.add_handler(CommandHandler('mybag', mybag))
    dp.add_handler(CommandHandler('top', top_sellers_buyers))
    dp.add_handler(CommandHandler('auction', auction_mode))
    dp.add_handler(CommandHandler('submission', submission_mode))
    dp.add_handler(CommandHandler('myitems', myitems))

    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path="/")
    updater.bot.set_webhook(f"{APP_URL}/")

    updater.idle() #Used for persistent running

if __name__ == '__main__':
    main()