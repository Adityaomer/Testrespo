
import asyncio
import logging
import random
import re
import string

from telethon import TelegramClient, events, Button
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

# Telegram API credentials (replace with your own)
API_ID = int("23599783")
API_HASH = "62c4987db06716e25c4d68dcdcdc1ea5"
BOT_TOKEN = '7921044809:AAEtRGLlWVM6RzDVZis3QjZpIxW1l3Vfd5c'

# Group and User IDs
AUCTION_GROUP_ID = -1002455896075
AUC_NAME = "HBG_NEW_GROUP_FHG"
owners = [1947921832, 1381668733]
OWNER = 1381668733
SUBMISSION_GROUP_ID = -1002652165076
BACKUP_GROUP_ID = -1002347695416  # Define the backup group ID

# Data lists
LEGENDARY_POKEMON_NAMES = ["Articuno", "Zapdos", "Moltres", "Raikou", "Entei", "Suicune", "Regirock", "Regice", "Registeel", "Latias", "Latios", "Uxie", "Mesprit", "Azelf", "Heatran", "Regigigas", "Cresselia", "Cobalion", "Terrakion", "Virizion", "Buzzwole", "Thundurus", "Tornadus", "Landorus", "Type: Null", "Silvally", "Tapu Koko", "Tapu Bulu", "Tapu Fini", "Tapu Lele", "Nihilego", "Pheromosa", "Xurkitree", "Celesteela", "Kartana", "Guzzlord", "Poipole", "Naganadel", "Stakataka", "Blacephalon", "Kubfu", "Urshifu", "Regieleki", "Regidrago", "Glastrier", "Spectrier", "Enamorus", "Wo-chien", "Chien-pao", "Ting-lu", "Chi-yu", "Okidogi", "Munkidori", "Fezandipiti", "Ogerpon", "Mewtwo", "Lugia", "Ho-oh", "Kyogre", "Groudon", "Rayquaza", "Dialga", "Palkia", "Giratina", "Reshiram", "Zekrom", "Kyurem", "Xerneas", "Yveltal", "Zygarde", "Cosmog", "Cosmoem", "Solgaleo", "Lunala", "Necrozma", "Zacian", "Zamazenta", "Eternatus", "Calyrex", "Koraidon", "Miraidon", "Terapagos", "Mew", "Celebi", "Jirachi", "Deoxys", "Phione", "Manaphy", "Darkrai", "Arceus", "shaymin", "Victini", "Keldeo", "Meloetta", "Genesect", "Diancie", "Hoopa", "Volcanion", "Megearna", "Marshadow", "Zeraora", "Meltan", "Melmetal", "Zarude"]

NON_LEGENDARY_POKEMON_NAMES = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran-F", "Nidorina", "Nidoqueen", "Nidoran-M", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetchd", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr-Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Dratini", "Dragonair", "Dragonite", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Larvitar", "Pupitar", "Tyranitar", "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple", "Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo", "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Tropius", "Chimecho", "Absol", "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Turtwig", "Grotle", "Torterra", "Chimchar", "Monferno", "Infernape", "Piplup", "Prinplup", "Empoleon", "Starly", "Staravia", "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune", "Shinx", "Luxio", "Luxray", "Budew", "Roserade", "Cranidos", "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam-Plant", "Mothim", "Combee", "Vespiquen", "Pachirisu", "Buizel", "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom", "Drifloon", "Drifblim", "Buneary", "Lopunny", "Mismagius", "Honchkrow", "Glameow", "Purugly", "Chingling", "Stunky", "Skuntank", "Bronzor", "Bronzong", "Bonsly", "Mime-Jr", "Happiny", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp", "Munchlax", "Riolu", "Lucario", "Hippopotas", "Hippowdon", "Skorupi", "Drapion", "Croagunk", "Toxicroak", "Carnivine", "Finneon", "Lumineon", "Mantyke", "Snover", "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth", "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z", "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom,Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog", "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole", "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Basculin-Red-Striped", "Sandile", "Krokorok", "Krookodile", "Darumaka", "Darmanitan-Standard", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask", "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark", "Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite", "Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet", "Accelgor", "Stunfisk", "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta", "Chespin", "Thwackey", "Rillaboom", "Scorbunny", "Raboot", "Cinderace", "Sobble", "Drizzile", "Inteleon", "Skwovet", "Greedent", "Rookidee", "Corvisquire", "Corviknight", "Blipbug", "Dottler", "Orbeetle", "Nickit", "Thievul", "Gossifleur", "Eldegoss", "Wooloo", "Dubwool", "Chewtle", "Drednaw", "Yamper", "Boltund", "Rolycoly", "Carkol", "Coalossal", "Applin", "Flapple", "Appletun", "Silicobra", "Sandaconda", "Cramorant", "Arrokuda", "Barraskewda", "Toxel", "Toxtricity-Amped", "Sizzlipede", "Centiskorch", "Clobbopus", "Grapploct", "Sinistea", "Polteageist", "Hatenna", "Hattrem", "Hatterene", "Impidimp", "Morgrem", "Grimmsnarl", "Obstagoon", "Perrserker", "Cursola", "Sirfetchd", "Mr-Rime", "Runerigus", "Milcery", "Alcremie", "Falinks", "Pincurchin", "Snom", "Frosmoth", "Stonjourner", "Eiscue-Ice", "Indeedee-Male", "Morpeko-Full-Belly", "Cufant", "Copperajah", "Dracozolt", "Arctozolt", "Dracovish", "Dartrix", "Decidueye", "Litten", "Torracat", "Incineroar", "Popplio", "Brionne", "Primarina", "Pikipek", "Trumbeak", "Toucannon", "Yungoos", "Gumshoos", "Grubbin", "Charjabug", "Vikavolt", "Crabrawler", "Crabominable", "Oricorio-Baile", "Cutiefly", "Ribombee", "Rockruff", "Lycanroc-Midday", "Wishiwashi-Solo", "Mareanie", "Toxapex", "Mudbray", "Mudsdale", "Dewpider", "Araquanid", "Fomantis", "Lurantis", "Morelull", "Shiinotic", "Salandit", "Salazzle", "Stufful", "Bewear", "Bounsweet", "Steenee", "Tsareena", "Comfey", "Oranguru", "Passimian", "Wimpod", "Golisopod", "Sandygast", "Palossand", "Pyukumuku", "Type-Null", "Silvally", "Minior-Red-Meteor", "Komala", "Turtonator", "Togedemaru", "Mimikyu-Disguised", "Bruxish", "Drampa", "Dhelmise", "Jangmo-O", "Hakamo-O", "Kommo-O", "Poipole", "Naganadel"]

SHINY_POKEMON_NAMES = LEGENDARY_POKEMON_NAMES + NON_LEGENDARY_POKEMON_NAMES

POKEMON_TEAM = ["Hp", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed"]

TM = ["Tm02", "Tm03", "Tm09", "Tm10", "Tm13", "Tm14", "Tm15", "Tm22", "Tm23", "Tm24", "Tm25", "Tm26", "Tm28", "Tm29", "Tm30", "Tm31", "Tm34", "Tm35", "Tm36", "Tm38", "Tm39", "Tm40", "Tm42", "Tm43", "Tm46", "Tm47", "Tm48", "Tm49", "Tm50", "Tm51", "Tm52", "Tm53", "Tm54", "Tm55", "Tm57", "Tm58", "Tm59", "Tm62", "Tm65", "Tm66", "Tm67", "Tm68", "Tm71", "Tm72", "Tm76", "Tm78", "Tm79", "Tm80", "Tm81", "Tm82", "Tm83", "Tm84", "Tm85", "Tm89", "Tm91", "Tm93", "Tm94", "Tm95", "Tm97", "Tm98", "Tm99"]

# Auction variables
auction = "start"
sub = "on"
limit = {
    "legendary": 12, 
    "non-legendary" : 15, 
    "shiny" : 20, 
    "tm" : 15, 
    "team" : 5
    }
approved_users = [1947921832, 1381668733]
collection = {}
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
current_add = []
pokemons = {}
items = {}
status = {}
status["1947921832"] = "OFF"
status["1381668733"] = "OFF"
user_list = []
video = "https://files.catbox.moe/4v63m2.jpg"
bot_name = "HBG_SLOW_AUCTIONBOT"
channels = ['@HBG_NEW_GROUP_FHG' , '@HBG_AUCTION_TRADE']


# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the client
client = TelegramClient('auction_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Helper functions
def generate(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def is_digit(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

async def check_channel_membership(user_id, channels):
    for channel_username in channels:
        try:
            chat = await client.get_entity(channel_username)
            member = await client.get_participant(chat, user_id)
            if member:
                return True
        except Exception as e:
            logging.error(f"Error checking channel membership for {channel_username}: {e}")
    return False

async def send_long_message(chat_id, text):
    max_length = 4096
    for i in range(0, len(text), max_length):
        await client.send_message(chat_id, text[i:i + max_length], parse_mode='html')

# Command handlers

@client.on(events.NewMessage(pattern='(?i)working\?'))
async def check_working(event):
    await event.reply('Yep, perfectly fine')

@client.on(events.NewMessage(pattern='(?i)/back_up'))
async def back_up(event):
    user_id = event.sender_id
    if user_id not in owners:
        await event.reply("You are not an approved user.")
        return
        
    status["1947921832"] = "ON"
    await event.reply("Bot started! I'll check all messages for 'hi'. Use /stop to stop.")

@client.on(events.NewMessage(pattern='(?i)/stop'))
async def stop(event):
    user_id = event.sender_id
    if user_id not in owners:
        await event.reply("You are not an approved user.")
        return
    # Remove the user-specific flag
    status["1947921832"] = "OFF"
    await event.reply("Bot stopped! You can restart it with /back_up.")

@client.on(events.NewMessage)
async def check_message(event):
    user_id = event.sender_id
    if user_id not in owners:
        return
    if f"{user_id}" not in status:
        return
    if status[f"{user_id}"] != "ON":
        return
    message = event.text
    part = message.split(":")

    if len(part) != 11:
        await event.reply("Error: Message must contain exactly 11 parts.")
        return

    category = part[0]
    try:
        i = int(part[1])
    except ValueError:
        await event.reply("Error: Second part must be an integer.")
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
        await event.reply("Error: Invalid category.")
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

    l[i] = part[2] + ":" + part[3]
    slist[i] = part[4] + ":" + part[5]
    bd[i] = float(part[6])
    nam[i] = int(part[7]) if is_digit(part[7]) else "None"
    iddata = part[5].split("-")
    sid = int(iddata[1])

    if sid not in seller_lead:
        seller_lead[sid] = {}
        seller_lead[sid]["item"] = []
        seller_lead[sid]["bag"] = []
    if sid not in seller_old:
        seller_old[sid] = {}
        seller_old[sid]["item"] = 0
        seller_old[sid]["bag"] = 0
    seller_lead[sid]["item"].append(f"{category}${part[2]}:{part[3]}")
    seller_old[sid]["item"] += 1
    bk[i] = int(part[8])
    collection[part[9]] = f"{category}_{i}_{part[10]}"

@client.on(events.NewMessage(pattern='(?i)/auction'))
async def auction_mode(event):
    global auction
    user_id = event.sender_id
    if user_id not in owners:
        await event.reply("You are not an approved user.")
        return
    r = event.text.split(" ")
    if len(r) != 2:
        await event.reply("wrong format \n format /auction <start/end>")
        return
    if r[1] != "start" and r[1] != "end":
        await event.reply(" wrong argument provided \n available argument `start` or `end`")
        return
    else:
        await event.reply(f"Changed Auction status from {auction} to {r[1]}")
        auction = r[1]
        if r[1] == "end":
            await buyers_list(event)
            await sellers_list(event)
            try:
                await client.send_message(BACKUP_GROUP_ID, str(seller_old))
            except:
                await event.reply(" memory_suceeded")
            for cat in back:
                for i in back[cat]:
                    try:
                        await client.delete_messages(BACKUP_GROUP_ID, i)
                    except Exception as e:
                        logging.error(f"Error deleting message {i} in backup group: {e}")

            keyboard = [
                [
                    Button.inline("YES", 'clear_yes'),
                    Button.inline("NO", 'clear_no'),
                ]
            ]
            await event.reply("DO YOU WANT TO CLEAR All OLD DATA?", buttons=keyboard)

@client.on(events.NewMessage(pattern='(?i)/submission'))
async def submission_mode(event):
    global sub
    user_id = event.sender_id
    if user_id not in approved_users:
        await event.reply("You are not an approved user.")
        return
    r = event.text.split(" ")
    if len(r) != 2:
        await event.reply("wrong format \n format /submission <on/off>")
        return
    if r[1] != "on" and r[1] != "off":
        await event.reply(" wrong argument provided \n available argument `on` or `off`")
        return
    else:
        await event.reply(f"Changed Auction status from {sub} to {r[1]}")
        sub = r[1]

@client.on(events.NewMessage(pattern='(?i)/store'))
async def store(event):
    if int(event.sender_id) != OWNER:
        await event.reply("You are not authorized to access that command so go away ")
        return
    global video
    video = event.message.media
    await event.reply(f"video stored successfully!\n`{video}`")

@client.on(events.NewMessage(pattern='(?i)/add_users'))
async def add_users(event):
    message_text = event.text
    data = message_text.split(" ")
    usersp = data[1]
    usersq = usersp.split(",")
    for user in usersq:
        user_list.append(int(user))

@client.on(events.NewMessage(pattern='(?i)/current'))
async def current_list(event):
    """Displays the current list of items with limits and available slots."""
    if event.sender_id not in approved_users:
        await event.reply("You are not an approved user.")
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

    await event.reply(message, parse_mode="html")

@client.on(events.NewMessage(pattern='(?i)/approve'))
async def approve_command(event):
    user_id = event.sender_id
    if user_id not in owners:
        await event.reply("You are not the owner")
        return
    command_parts = event.text.split(" ")
    if len(command_parts) >= 2:
        try:
            u_to_ap = int(command_parts[1])
            approved_users.append(u_to_ap)
            await event.reply(f"user <a href='tg://user?id={u_to_ap}'>{u_to_ap} 🍁</a> approved", parse_mode="html")
        except ValueError:
            await event.reply("Invalid user ID provided.")
    else:
        await event.reply("OWNER SAMA!! please provide user id to approve 🥶")

@client.on(events.NewMessage(pattern='(?i)/users'))
async def users(event):
    usersl = "7048431897" if len(user_list) == 0 else "  "
    for user in user_list:
        usersl = f"{usersl},{user}"
    await event.reply(usersl)

@client.on(events.NewMessage(pattern='(?i)/start'))
async def start(event):
    user_id = event.sender_id
    if user_id != event.chat_id:
        await event.reply("This command can only be used in DM")
        return
    if user_id not in user_list:
        user_list.append(user_id)
    user = await client.get_entity(user_id)

    # Check channel membership
    is_member = await check_channel_membership(user_id, channels)
    if not is_member:
        download_link = "https://t.me/HBG_NEW_GROUP_FHG"
        download_linker = "https://t.me/HBG_AUCTION_TRADE"

        keyboard = [[
            Button.url("Channel link",download_link),
            Button.url("Group link", download_linker)
        ]]
        try:
            await client.send_file(event.chat_id, video, caption=f"""♦𝑊𝑒𝑙𝑐𝑜𝑚𝑒 {user.first_name}

🔸𝑌𝑜𝑢 𝐶𝑎𝑛 𝑆𝑢𝑏𝑚𝑖𝑡 𝑌𝑜𝑢𝑟 𝑃𝑜𝑘𝑒𝑚𝑜𝑛 𝑇ℎ𝑟𝑜𝑢𝑔ℎ 𝑇ℎ𝑖𝑠 𝐵𝑜𝑡 𝐹𝑜𝑟 𝐴𝑢𝑐𝑡𝑖𝑜𝑛

🔻𝐵𝑢𝑡 𝐵𝑒𝑓𝑜𝑟𝑒 𝑈𝑠𝑖𝑛𝑔 𝑌𝑜𝑢 𝐻𝑎𝑣𝑒 𝑇𝑜 𝐽𝑜𝑖𝑛 𝑂𝑢𝑟 𝐴𝑢𝑐𝑡𝑖𝑜𝑛 𝐺𝑟𝑜𝑢𝑝 𝐵𝑦 𝐶𝑙𝑖𝑐𝑘𝑖𝑛𝑔 𝐵𝑒𝑙𝑜𝑤 𝑇𝑤𝑜 𝐵𝑢𝑡𝑡𝑜𝑛𝑠 𝐴𝑛𝑑 𝑇ℎ𝑒𝑛 𝐶𝑙𝑖𝑐𝑘 '𝐽𝑜𝑖𝑛𝑒𝑑' 𝐵𝑢𝑡𝑡𝑜𝑛
<blockquote>𝘾𝙧𝙚𝙖𝙩𝙤𝙧 :</blockquote> @l0_Mr_unknown_0l""", buttons=keyboard, parse_mode="html")
        except Exception as e:
            await event.reply(f"Error sending message: {e}")
        return

    args = event.text.split()
    if len(args) > 1:
        ar = args[1]
        if ar not in collection:
            await event.reply("something wrong with item please contact admin")
            return
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
        context = {}  # Using a simple dictionary for context
        context["inform"] = str(ar)
        context["HANDLE_BID"] = True  # Simulate state transition
        await event.reply(
            f"          (⁠✷⁠‿⁠✷⁠)         \n"
            f"Enter the amount of Poke Dollars you want to bid for {item_name} "
            "or use /cancel to stop bidding \n\n"
            f"NOTE :  your bid must be in 'PDs'",
            parse_mode="html",
            link_preview=False
        )
        return  # Assuming you want to stop here

    else:
        download_link = "https://t.me/HBG_NEW_GROUP_FHG"

        keyboard = [[
            Button.url("Channel link", download_link)
        ]]
        await client.send_file(event.chat_id, video, caption=f"""𝙒𝙚𝙡𝙘𝙤𝙢𝙚 {user.first_name} , 
🅃🄾 🄰🄳🄳 🄸🅃🄴🄼🅂 🄵🄾🅁 🄰🅄🄲🅃🄸🄾🄽 🅄🅂🄴 /add
<blockquote>𝘾𝙧𝙚𝙖𝙩𝙤𝙧 :</blockquote> @l0_Mr_unknown_0l""", buttons=keyboard, parse_mode="html")


@client.on(events.NewMessage)
async def handle_bid(event):
    if not hasattr(event, 'context') or not event.context.get('HANDLE_BID'):
        return  # Ignore if it's not a bidding context

    message = event.message
    ar = event.context.get("inform")
    rar = collection[ar]
    sp = rar.split("_")
    category = sp[0]
    cat = category
    id = int(sp[1])
    msg = int(sp[2])
    if len(buyers[category]) <= id:
        await event.reply("something wrong with item please contact admin")
        return

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
        await event.reply("something wrong with item please contact admin")
        return

    if is_digit(message.text):
        bid_amount = int(message.text)
        if (bid_amount - float(buyers[category][id])) >= required:
            await event.reply("<blockquote>🎊 BID SUCCESS FULLY PLACED 📨 </blockquote> \n 🖇 please check to confirm ", parse_mode="html")

            keyboard = [[
                Button.url("Place Your Bid 🎴", f'https://t.me/{bot_name}?start={ar}')
            ]]
            buyers[category][id] = bid_amount
            buyers[f"{category}_name"][id] = event.sender_id

            # Edit message in backup group
            try:
                await client.edit_message(BACKUP_GROUP_ID, back[category][id],
                                        text=f"{category}:{id}:{item_name}:{lis}:{bid_amount}:{event.sender_id}:{back[category][id]}:{ar}:{msg}", link_preview=False)
            except Exception as e:
                logging.error(f"Error editing backup message: {e}")

            # Edit message in auction group
            try:
                await client.edit_message(AUCTION_GROUP_ID, msg,
                                        text=f"""
╔══════════════════════════╗
<b>The Bid Page of {item_name}</b>
highest bid - {bid_amount} Pds
Bidder      - {event.sender.first_name}\n(@{event.sender.username}) 
╚══════════════════════════╝""",
                                        buttons=keyboard, parse_mode='html', link_preview=False)
            except Exception as e:
                logging.error(f"Error editing auction message: {e}")

        else:
            await event.reply(f"<b>INSUFFICIENT FUND: Minimum increment must be by {required}</b>\n\n ---------------------\nYou must bid : <b>{int(buyers[category][id]) + required}</b> Atleast ", parse_mode="html", link_preview=False)

    else:
        await event.reply(f"Wrong format only write amount in numbers to bid on {item_name}", link_preview=False)

@client.on(events.NewMessage(pattern='(?i)/broadcast'))
async def broadcast(event):
    await event.reply("Please enter the message you want to broadcast:")

    @client.on(events.NewMessage)
    async def broadcast_message_handler(event):
        message_text = event.text
        for user_id in user_list:
            try:
                await client.send_message(user_id, message_text)
            except Exception as e:
                logging.error(f"Error sending message to {user_id}: {e}")

        await event.reply("Broadcast complete!")
        client.remove_event_handler(broadcast_message_handler)

@client.on(events.NewMessage(pattern='(?i)/add'))
async def add(event):
    chatid = event.chat_id
    user = await client.get_entity(event.sender_id)
    user_id = user.id
    usern = user.first_name

    is_member = await check_channel_membership(user_id, channels)
    if not is_member:
        download_link = "https://t.me/HBG_NEW_GROUP_FHG"
        download_linker = "https://t.me/HBG_AUCTION_TRADE"

        keyboard = [[
            Button.url("Channel link", download_link),
            Button.url("Group link", download_linker)
        ]]
        await client.send_file(event.chat_id, video, caption=f"""♦𝑊𝑒𝑙𝑐𝑜𝑚𝑒 {user.first_name}

🔸𝑌𝑜𝑢 𝐶𝑎𝑛 𝑆𝑢𝑏𝑚𝑖𝑡 𝑌𝑜𝑢𝑟 𝑃𝑜𝑘𝑒𝑚𝑜𝑛 𝑇ℎ𝑟𝑜𝑢𝑔ℎ 𝑇ℎ𝑖𝑠 𝐵𝑜𝑡 𝐹𝑜𝑟 𝐴𝑢𝑐𝑡𝑖𝑜𝑛

🔻𝐵𝑢𝑡 𝐵𝑒𝑓𝑜𝑟𝑒 𝑈𝑠𝑖𝑛𝑔 𝑌𝑜𝑢 𝐻𝑎𝑣𝑒 𝑇𝑜 𝐽𝑜𝑖𝑛 𝑂𝑢𝑟 𝐴𝑢𝑐𝑡𝑖𝑜𝑛 𝐺𝑟𝑜𝑢𝑝 𝐵𝑦 𝐶𝑙𝑖𝑐𝑘𝑖𝑛𝑔 𝐵𝑒𝑙𝑜𝑤 𝑇𝑤𝑜 𝐵𝑢𝑡𝑡𝑜𝑛𝑠 𝐴𝑛𝑑 𝑇ℎ𝑒𝑛 𝐶𝑙𝑖𝑐𝑘 '𝐽𝑜𝑖𝑛𝑒𝑑' 𝐵𝑢𝑡𝑡𝑜𝑛
<blockquote>𝘾𝙧𝙚𝙖𝙩𝙤𝙧 :</blockquote> @l0_Mr_unknown_0l""", buttons=keyboard, parse_mode="html")
        return

    if user_id != chatid:
        await event.reply("𝑇ℎ𝑖𝑠 𝑐𝑜𝑚𝑚𝑎𝑛𝑑 𝑐𝑎𝑛 𝑜𝑛𝑙𝑦 𝑏𝑒 𝑢𝑠𝑒𝑑 𝑖𝑛 𝑑𝑚 समझा🧐")
        return
    if user_id not in user_list:
        user_list.append(user_id)
    if auction != "start":
        await event.reply("Sorry for inconvenience but there is no current auction going on")
        return
    if sub != "on":
        await event.reply("Sorry for inconvenience but Submission for the current auction has now ended \n Do try on the next auction")
        return

    keyboard = [
        [
            Button.inline("LEGENDARY", 'legendary'),
            Button.inline("NON-LEGENDARY", 'non-legendary'),
        ],
        [
            Button.inline("SHINY", 'shiny'),
            Button.inline("TEAM", 'team'),
        ],
        [
            Button.inline("TM", 'tm')
        ]
    ]

    if user_id in current_add:
        await event.reply("please complete on going submission \n      -OR-     \n     -Use /cancel Command")
    else:
        msg = await event.reply('<blockquote>𝑊𝐻𝐴𝑇 𝑌𝑂𝑈 𝑊𝐴𝑁𝑇 𝑇𝑂 𝑆𝐸𝐿𝐿 𝐼𝑁 𝐼𝐻𝐺 𝐴𝑈𝐶𝑇𝐼𝑂𝑁?</blockquote>\n𝐶ℎ𝑜𝑜𝑠𝑒 𝑓𝑟𝑜𝑚 𝑏𝑒𝑙𝑜𝑤 🎐', buttons=keyboard, parse_mode='HTML')
        current_add.append(user_id)
        event.context = {"STATE": "ITEM_NAME", "message_id": msg.id}  # Store next state and message_id

@client.on(events.CallbackQuery(pattern=r'^(legendary|non-legendary|shiny|team|tm)$'))
async def category_selection(event):
    user = await client.get_entity(event.sender_id)
    callback_data = event.data.decode()
    event.context = {}

    if limit[callback_data] <= len(buyers[callback_data]):
        await event.edit_message(
            event.chat_id,
            event.message_id,
            text="<blockquote>Really Sorry fellows !! \nBut slots for this category is full</blockquote>",
            parse_mode="html"
        )
        if event.sender_id in current_add:
            current_add.remove(event.sender_id)
        return

    if callback_data == 'legendary':
        reply_text = f"𝐻𝐸𝑌 {user.first_name.upper()}! 𝑊𝐻𝐼𝐶𝐻 𝐿𝐸𝐺𝐸𝑁𝐷𝐴𝑅𝑌 𝑃𝑂𝐾𝐸𝑀𝑂𝑁 𝑌𝑂𝑈 𝑊𝐴𝑁𝑇 𝑇𝑂 𝑆𝐸𝐿𝐿?"
    elif callback_data == 'non-legendary':
        reply_text = f"𝐻𝐸𝑌 {user.first_name.upper()}! 𝑊𝐻𝐼𝐶𝐻 𝑁𝑂𝑁-𝐿𝐸𝐺𝐸𝑁𝐷𝐴𝑅𝑌 𝑃𝑂𝐾𝐸𝑀𝑂𝑁 𝑌𝑂𝑈 𝑊𝐴𝑁𝑇 𝑇𝑂 𝑆𝐸𝐿𝐿?"
    elif callback_data == 'shiny':
        reply_text = f"𝐻𝐸𝑌 {user.first_name.upper()}! 𝑊𝐻𝐼𝐶𝐻 𝑆𝐻𝐼𝑁𝑌 𝑃𝑂𝐾𝐸𝑀𝑂𝑁 𝑌𝑂𝑈 𝑊𝐴𝑁𝑇 𝑇𝑂 𝑆𝐸𝐿𝐿?"
    elif callback_data == 'team':
        reply_text = f"𝐻𝐸𝑌 {user.first_name.upper()}! 𝑊𝐻𝐼𝐶𝐻 𝑇𝐸𝐴𝑀 𝑌𝑂𝑈 𝑊𝐴𝑁𝑇 𝑇𝑂 𝑆𝐸𝐿𝐿?"
    elif callback_data == 'tm':
        reply_text = f"𝐻𝐸𝑌 {user.first_name.upper()}! 𝑊𝐻𝐼𝐶𝐻 𝑇𝑀 𝑌𝑂𝑈 𝑊𝐴𝑁𝑇 𝑇𝑂 𝑆𝐸𝐿𝐿? (PLEASE TELL THE TM NUMBER NOT TM NAME)."

    event.context = {"STATE": "ITEM_NAME_INPUT", "category": callback_data, "message_id": event.message_id}
    await event.edit_message(
        event.chat_id,
        event.message_id,
        text=f"<blockquote>{reply_text}</blockquote>",
        parse_mode="html"
    )


@client.on(events.NewMessage)
async def item_name_input(event):
    if not hasattr(event, 'context') or event.context.get("STATE") != "ITEM_NAME_INPUT":
        return
    item_name = event.text.title()
    category = event.context['category']
    event.context["item_name"] = item_name
    if category == 'legendary':
        if item_name in LEGENDARY_POKEMON_NAMES:
            
            await event.reply(f"𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝑇𝐻𝐸 𝑁𝐴𝑇𝑈𝑅𝐸 𝑃𝐴𝐺𝐸 𝑂𝐹 <blockquote>{item_name.upper()}</blockquote> 𝐹𝑟𝑜𝑚 @HeXamonbot", parse_mode='HTML')
            event.context["STATE"] = "NATURE_PAGE"
            return
        else:
            await event.reply(f"{item_name} 𝑖𝑠 𝑛𝑜𝑡 𝑎 𝑛𝑎𝑚𝑒 𝑜𝑓 𝑎 𝑙𝑒𝑔𝑒𝑛𝑑𝑎𝑟𝑦 𝑃𝑜𝑘é𝑚𝑜𝑛. 𝑃𝑙𝑒𝑎𝑠𝑒 𝑝𝑟𝑜𝑣𝑖𝑑𝑒 𝑎 𝑣𝑎𝑙𝑖𝑑 𝑙𝑒𝑔𝑒𝑛𝑑𝑎𝑟𝑦 𝑃𝑜𝑘é𝑚𝑜𝑛 𝑛𝑎𝑚𝑒.")
    elif category == 'non-legendary':
        if item_name in NON_LEGENDARY_POKEMON_NAMES:
            await event.reply(f"𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝑇𝐻𝐸 𝑁𝐴𝑇𝑈𝑅𝐸 𝑃𝐴𝐺𝐸 𝑂𝐹 <blockquote>{item_name} </blockquote> 𝐹𝑟𝑜𝑚 @HeXamonbot",parse_mode="html")
            
            event.context["STATE"] = "NATURE_PAGE"
            return
        else:
            await event.reply(f"{item_name} 𝑖𝑠 𝑛𝑜𝑡 𝑎 𝑛𝑎𝑚𝑒 𝑜𝑓 𝑎 𝑁𝑜𝑛-𝑙𝑒𝑔𝑒𝑛𝑑𝑎𝑟𝑦 𝑃𝑜𝑘é𝑚𝑜𝑛. 𝑃𝑙𝑒𝑎𝑠𝑒 𝑝𝑟𝑜𝑣𝑖𝑑𝑒 𝑎 𝑣𝑎𝑙𝑖𝑑 𝑁𝑜𝑛-𝑙𝑒𝑔𝑒𝑛𝑑𝑎𝑟𝑦 𝑃𝑜𝑘é𝑚𝑜𝑛 𝑛𝑎𝑚𝑒.")
    elif category == 'shiny':
        if item_name in SHINY_POKEMON_NAMES:
            await event.reply(f"𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝑇𝐻𝐸 𝑁𝐴𝑇𝑈𝑅𝐸 𝑃𝐴𝐺𝐸 𝑂𝐹 <blockquote>{item_name} </blockquote>𝐹𝑟𝑜𝑚 @HeXamonbot",parse_mode="html")
            
            event.context["STATE"] = "NATURE_PAGE"
            return
        else:
            await event.reply(f"{item_name} 𝑖𝑠 𝑛𝑜𝑡 𝑎 𝑛𝑎𝑚𝑒 𝑜𝑓 𝑎 𝑃𝑜𝑘é𝑚𝑜𝑛. 𝑃𝑙𝑒𝑎𝑠𝑒 𝑝𝑟𝑜𝑣𝑖𝑑𝑒 𝑎 𝑣𝑎𝑙𝑖𝑑 𝑃𝑜𝑘é𝑚𝑜𝑛 𝑛𝑎𝑚𝑒.")
    elif category == 'team':
        if item_name in POKEMON_TEAM:
            await event.reply(f"𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝑇𝐻𝐸 𝑇𝑒𝑎𝑚 𝑃𝐴𝐺𝐸 𝑂𝐹 <blockquote>{item_name}</blockquote> 𝐹𝑟𝑜𝑚 @HeXamonbot" ,parse_html="html" )
            
            event.context["STATE"] = "ITEM_DETAILS"
            return
        else:
            await event.reply(f"{item_name} 𝑖𝑠 𝑛𝑜𝑡 𝑎 𝑛𝑎𝑚𝑒 𝑜𝑓 𝑎 𝑇𝑒𝑎𝑚 𝑃𝑙𝑒𝑎𝑠𝑒 𝑝𝑟𝑜𝑣𝑖𝑑𝑒 𝑎 𝑣𝑎𝑙𝑖𝑑 𝑇𝑒𝑎𝑚 𝑛𝑎𝑚𝑒.")
    elif category == 'tm':
        if item_name in TM:
            await event.reply(f"𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝑇𝐻𝐸 𝑇𝑚 𝑃𝐴𝐺𝐸 𝑂𝐹 <blockquote> {item_name} </blockquote>𝐹𝑟𝑜𝑚 @HeXamonbot",parse_mode="html")
            
            event.context["STATE"] = "ITEM_DETAILS"
            return
        else:
            await event.reply(f"{item_name} 𝑖𝑠 𝑛𝑜𝑡 𝑎 𝑛𝑎𝑚𝑒 𝑜𝑓 𝑎 𝑇𝑚. 𝑃𝑙𝑒𝑎𝑠𝑒 𝑝𝑟𝑜𝑣𝑖𝑑𝑒 𝑎 𝑣𝑎𝑙𝑖𝑑 𝑇𝑚 𝑛𝑎𝑚𝑒.")
            
            
@client.on(events.NewMessage)
async def nature_page_input(event):
    if not hasattr(event, 'context') or event.context.get("STATE") != "NATURE_PAGE":
        return
    
    if not event.photo:
      await event.reply("Please forward the page correctly or send it as photo from hexambot")
      return
    
    if event.message.caption:
        caption_text = event.message.caption
        if "Nature" in caption_text and "Lv" in caption_text:
            forwarded_from = getattr(event.message, 'fwd_from', None)
            if forwarded_from and forwarded_from.peer_id == 572621020:
                
                lines = caption_text.split("\n")
                fline = lines[0]
                sline = lines[1]
                lenat = fline.split(" ")
                natle = fline.split(":")
                typ = sline.split(":")
                # Save photo file_id
                photo = event.message.photo

                # Save nature and level in user_data
                nature = natle[1].strip()
                lv = lenat[1].strip()
                ty = str(typ[1].strip())

                # Forward the message to the submission group
                await client.forward_messages(SUBMISSION_GROUP_ID, event.message)
                
                # Add data to context for future reference
                event.context["picture"] = photo
                event.context["nature"] = nature
                event.context["lv"] = lv
                event.context["ty"] = ty

                await event.reply("<blockquote>𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝐼𝑉/𝐸𝑉 𝑃𝐴𝐺𝐸 𝑂𝐹 𝑌𝑂𝑈𝑅 𝑃𝑂𝐾𝐸𝑀𝑂𝑁</blockquote> 𝐹𝑅𝑂𝑀 @HeXamonbot ", parse_mode="html")
                event.context["STATE"] = "POKEMON_IV"
                return
            else:
                await event.reply("<blockquote>𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝐹𝑅𝑂𝑀 @HeXamonbot</blockquote> 𝑜𝑡ℎ𝑒𝑟𝑤𝑖𝑠𝑒 𝑝𝑟𝑜𝑐𝑒𝑠𝑠 𝑤𝑖𝑙𝑙 𝑛𝑜𝑡 𝑤𝑜𝑟𝑘 𝑓𝑜𝑟 𝑠𝑒𝑛𝑑 𝑡𝑜 𝑠𝑢𝑏𝑚𝑖𝑠𝑠𝑖𝑜𝑛", parse_mode="html")
                return
        else:
            await event.reply("<blockquote>𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 NATURE 𝑃𝐴𝐺𝐸 𝑂𝐹 𝑌𝑂𝑈𝑅 𝑃𝑂𝐾𝐸𝑀𝑂𝑁 </blockquote>𝐹𝑅𝑂𝑀 @HeXamonbot ", parse_mode="html")
            return
    else:
        await event.reply("PLEASE DON'T SEND ONLY PHOTO/DETAILS. <blockquote>FORWARD FULL PAGE FROM @HeXamonbot</blockquote>", parse_mode="html")
        return
    
@client.on(events.NewMessage)
async def item_details_input(event):
    if not hasattr(event, 'context') or event.context.get("STATE") != "ITEM_DETAILS":
        return
    item_name = event.context.get("item_name")
    category = event.context.get("category")

    forwarded_from = getattr(event.message, 'fwd_from', None)
    if forwarded_from and forwarded_from.peer_id == 572621020:
      
        await event.reply(f"𝑃𝑙𝑒𝑎𝑠𝑒 𝑡𝑒𝑙𝑙 𝑏𝑎𝑠𝑒 𝑓𝑜𝑟 𝑦𝑜𝑢𝑟 <blockquote>'{category.upper()}'[{item_name}]</blockquote>",parse_mode="html")
        # Forward the information to submission group
        await client.forward_messages(SUBMISSION_GROUP_ID, event.message)

        details = event.text  # Extract item details from the message
        event.context["details"] = details
        event.context["STATE"] ="BASE_PRICE"
        return

    else:
        await event.reply(f"<blockquote>PLEASE FORWARD INFORMATION OF {item_name}</blockquote> FROM @HeXamonbot", parse_mode="html")
        return
    
@client.on(events.NewMessage)
async def pokemon_iv_input(event):
    if not hasattr(event, 'context') or event.context.get("STATE") != "POKEMON_IV":
        return
    if event.message.caption:
        if "IV" in event.message.caption and "EV" in event.message.caption:
            forwarded_from = getattr(event.message, 'fwd_from', None)
            if forwarded_from and forwarded_from.peer_id == 572621020:
                event.context["iv_page"] = f"{event.message.caption}"
                await event.reply("<blockquote>𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝑇𝐻𝐸 𝑀𝑂𝑉𝐸𝑆𝐸𝑇 𝑃𝐴𝐺𝐸 𝑂𝐹 𝑌𝑂𝑈𝑅 𝑃𝑂𝐾𝐸𝑀𝑂𝑁</blockquote> 𝐹𝑅𝑂𝑀 @HeXamonbot",parse_mode= "html")
                event.context["STATE"] = "MOVESET_PAGE"
                return
            else:
                await event.reply("<blockquote>PLEASE FORWARD FROM @HeXamonbot.</blockquote> OTHERWISE PROCESS WILL NOT EXCUTE.",parse_mode="html")
                return
        else:
            await event.reply("<blockquote>𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝐼𝑉/𝐸𝑉 𝑃𝐴𝐺𝐸 𝑂𝐹 𝑌𝑂𝑈𝑅 𝑃𝑂𝐾𝐸𝑀𝑂𝑁</blockquote> 𝐹𝑅𝑂𝑀 @HeXamonbot",parse_mode="html")
            return
    else:
        await event.reply("<blockquote>Please forward right page of ivs/evs</blockquote> from @HeXamonbot.",parse_mode="html")
        return
    
@client.on(events.NewMessage)
async def moveset_page_input(event):
    if not hasattr(event, 'context') or event.context.get("STATE") != "MOVESET_PAGE":
        return
    if event.message.caption:
        if "Power" in event.message.caption and "Accuracy" in event.message.caption:
            forwarded_from = getattr(event.message, 'fwd_from', None)
            if forwarded_from and forwarded_from.peer_id == 572621020:
                event.context["moveset_page"] = event.message.caption
                await event.reply("<blockquote>PLEASE TELL ME IS ANY IV IS BOOSTED?</blockquote>\n <code> Yes </code> or <code> No </code>",parse_mode="html")
                event.context["STATE"] = "BOOSTED"
                return
            else:
                await event.reply("<blockquote>Please forward from @HeXamonbot</blockquote>",parse_mode="html")
                return
        else:
            await event.reply("<blockquote>Please forward right page of moveset </blockquote> from @HeXamonbot",parse_mode="html")
            return
    else:
        await event.reply("<blockquote>Please forward right page of moveset </blockquote>from @HeXamonbot",parse_mode="html")
        return
    
@client.on(events.NewMessage)
async def boosted_input(event):
    if not hasattr(event, 'context') or event.context.get("STATE") != "BOOSTED":
        return
    boosted = event.text.title()
    item_name = event.context.get("item_name")

    if boosted == 'Yes':
        event.context["boosted"] = boosted
        await event.reply(f"𝑃𝐿𝐸𝐴𝑆𝐸 𝑇𝐸𝐿𝐿 𝑀𝐸 𝑇𝐻𝐸 𝐵𝐴𝑆𝐸 𝑃𝑅𝐼𝐶𝐸 𝐹𝑂𝑅 𝑌𝑂𝑈𝑅 <blockquote>{item_name}</blockquote>",parse_mode="html")
        event.context["STATE"] = "BASE_PRICE"
        return

    elif boosted == 'No':
         event.context["boosted"] = boosted
         await event.reply(f"𝑃𝐿𝐸𝐴𝑆𝐸 𝑇𝐸𝐿𝐿 𝑀𝐸 𝑇𝐻𝐸 𝐵𝐴𝑆𝐸 𝑃𝑅𝐼𝐶𝐸 𝐹𝑂𝑅 𝑌𝑂𝑈𝑅<blockquote> {item_name}</blockquote>",parse_mode="html")
         event.context["STATE"] = "BASE_PRICE"
         return

    else:
         await event.reply("<blockquote>𝐼 𝑊𝐼𝐿𝐿 𝐴𝐶𝐶𝐸𝑃𝑇 𝑂𝑁𝐿𝑌 𝑌𝐸𝑆/𝑁𝑂 𝑆𝑂 𝐺𝐼𝑉𝐸 𝐴𝑁𝑆𝑊𝐸𝑅 𝐼𝑁</blockquote>\n <code>𝑌𝐸𝑆 / 𝑁𝑂</code>",parse_mode="html")
         return
    
@client.on(events.NewMessage)
async def base_price_input(event):
    if not hasattr(event, 'context') or event.context.get("STATE") != "BASE_PRICE":
        return
    base = event.text
    seller_id = event.sender_id
    s_n = event.sender.first_name
    item_name = event.context.get("item_name")
    seller = await client.get_entity(seller_id)
    boosted = event.context.get("boosted")
    moveset_page = event.context.get("moveset_page")
    iv_page = event.context.get("iv_page")
    nature = event.context.get("nature")
    lv = event.context.get("lv")
    details = event.context.get("details")
    types = event.context.get("ty")
    category = event.context.get("category")
    picture = event.context.get("picture")
    try:
        number_text = event.text
        number = float(number_text[:-1]) * 1000 if number_text[-1].lower() == 'k' else float(number_text)
    except ValueError:
        await event.reply("PLEASE ENTER YOUR PRICE IN NUMBER FORMAT")
        return
    if number % 100 == 0:
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
        seller_data[seller_id]["name"] = seller.first_name

        if category in ['legendary', 'non-legendary', 'shiny']:
            await event.reply(f"𝑇𝐻𝐴𝑁𝐾 𝑌𝑂𝑈 𝐹𝑂𝑅 𝐴𝐷𝐷 𝑌𝑂𝑈𝑅 𝑃𝑂𝐾𝐸𝑀𝑂𝑁 𝐼𝑁 𝐼𝐻𝐺 𝐴𝑈𝐶𝑇𝐼𝑂𝑁. <blockquote> 𝑌𝑂𝑈𝑅 {item_name}[{nature}] 𝐻𝐴𝑆 𝐵𝐸𝐸𝑁 𝑆𝐸𝑁𝑇 𝐹𝑂𝑅 𝑆𝑈𝐵𝑀𝐼𝑆𝑆𝐼𝑂𝑁</blockquote>",parse_mode="html")
            context = {}  # Using a simple dictionary for context
            if not hasattr(context, 'pokemons'):
                context["pokemons"] = {}

            if not hasattr(context["pokemons"], 'item_name'):
                context["pokemons"]["item_name"] = []

            if not hasattr(context["pokemons"], 'seller_id'):
                context["pokemons"]["seller_id"] = []

            if not hasattr(context["pokemons"], 'boosted'):
                context["pokemons"]["boosted"] = []

            if not hasattr(context["pokemons"], 'moveset_page'):
                context["pokemons"]["moveset_page"] = []

            if not hasattr(context["pokemons"], 'iv_page'):
                context["pokemons"]["iv_page"] = []

            if not hasattr(context["pokemons"], 'nature'):
                context["pokemons"]["nature"] = []

            if not hasattr(context["pokemons"], 'lv'):
                context["pokemons"]["lv"] = []

            if not hasattr(context["pokemons"], 'base'):
                context["pokemons"]["base"] = []

            if not hasattr(context["pokemons"], 'types'):
                context["pokemons"]["types"] = []

            if not hasattr(context["pokemons"], 'category'):
                context["pokemons"]["category"] = []

            if not hasattr(context["pokemons"], 'picture'):
                context["pokemons"]["picture"] = []

            if not hasattr(context["pokemons"], 'msg_id'):
                context["pokemons"]["msg_id"] = []

            # Append data to respective lists in pokemons dictionary
            if not hasattr(pokemons, 'item_name'):
                pokemons["item_name"] = []
            pokemons["item_name"].append(item_name)

            if not hasattr(pokemons, 'seller_id'):
                pokemons["seller_id"] = []
            pokemons["seller_id"].append(seller_id)

            if not hasattr(pokemons, 'boosted'):
                pokemons["boosted"] = []
            pokemons["boosted"].append(boosted)

            if not hasattr(pokemons, 'moveset_page'):
                pokemons["moveset_page"] = []
            pokemons["moveset_page"].append(moveset_page)

            if not hasattr(pokemons, 'iv_page'):
                pokemons["iv_page"] = []
            pokemons["iv_page"].append(iv_page)

            if not hasattr(pokemons, 'nature'):
                pokemons["nature"] = []
            pokemons["nature"].append(nature)

            if not hasattr(pokemons, 'lv'):
                pokemons["lv"] = []
            pokemons["lv"].append(lv)

            if not hasattr(pokemons, 'types'):
                pokemons["types"] = []
            pokemons["types"].append(f"{types}")

            if not hasattr(pokemons, 'category'):
                pokemons["category"] = []
            pokemons["category"].append(category)

            if not hasattr(pokemons, 'picture'):
                pokemons["picture"] = []
            pokemons["picture"].append(picture)

            if not hasattr(pokemons, 'base'):
                pokemons["base"] = []
            pokemons["base"].append(f"{number}")

            if not hasattr(pokemons, 'name'):
                pokemons["name"] = []
            pokemons["name"].append(s_n)

            event.context["base"] = number
            # Inline options
            inline_keyboard = [
              [Button.inline("Approve", f'papprove_{len(pokemons["picture"])-1}')],
              [Button.inline("Disapprove:👇", f'disapprove_{len(pokemons["picture"])-1}')],
              [Button.inline("RIP Nature", f'ripnature_{len(pokemons["picture"])-1}'),
                Button.inline("RIP IVs/EVs", f'ripivsevs_{len(pokemons["picture"])-1}')],
              [Button.inline("RIP Moveset", f'ripmoveset_{len(pokemons["picture"])-1}'),
               Button.inline("RIP All", f'ripall_{len(pokemons["picture"])-1}')]
            ]

            # Forward all information to submission group with inline buttons
            await client.send_file(SUBMISSION_GROUP_ID, picture, caption=f"""𝐍𝐚𝐦𝐞: <code>{item_name}</code>
𝐓𝐲𝐩𝐞𝐬: <code>{types}</code>
𝐋𝐯: <code>{lv}</code>
𝐍𝐚𝐭𝐮𝐫𝐞: <code>{nature}</code>
𝐈𝐕/𝐄𝐕: <code>{iv_page}</code>
𝐌𝐨𝐯𝐞𝐬𝐞𝐭: <code>{moveset_page}</code>
𝐁𝐨𝐨𝐬𝐭𝐞𝐝: <code>{boosted}</code>
𝐁𝐀𝐒𝐄: <code>{number}</code>
Seller <code>{seller.first_name}</code>[@{seller.username}]

""", buttons=inline_keyboard, parse_mode='html')

            event.context["number"] = len(pokemons["picture"])
            if event.sender_id in current_add:
                current_add.remove(event.sender_id)
            return

        elif category in ['tm', 'team']:
            await event.reply(f"𝑇𝐻𝐴𝑁𝐾 𝑌𝑂𝑈 𝐹𝑂𝑅 𝐴𝐷𝐷 𝑌𝑂𝑈𝑅 𝐼𝑇𝐸𝑀 𝐼𝑁 𝐼𝐻𝐺 𝐴𝑈𝐶𝑇𝐼𝑂𝑁. <blockquote>𝑌𝑂𝑈𝑅 {item_name} 𝐻𝐴𝑆 𝐵𝐸𝐸𝑁 𝑆𝐸𝑁𝑇 𝐹𝑂𝑅 𝑆𝑈𝐵𝑀𝐼𝑆𝑆𝐼𝑂𝑁</blockquote>",parse_mode="html")
            context = {}  # Using a simple dictionary for context
            if not hasattr(context, 'items'):
                context["items"] = {}

            if not hasattr(context["items"], 'item_name'):
                context["items"]["item_name"] = []

            if not hasattr(context["items"], 'details'):
                context["items"]["details"] = []

            if not hasattr(context["items"], 'category'):
                context["items"]["category"] = []

            if not hasattr(context["items"], 'picture'):
                context["items"]["picture"] = []

            if not hasattr(context["items"], 'base'):
                context["items"]["base"] = []

            if not hasattr(context["items"], 'name'):
                context["items"]["name"] = []

            if not hasattr(context["items"], 'msg_id'):
                context["items"]["msg_id"] = []

            # Append data to respective lists in pokemons dictionary
            if not hasattr(items, 'item_name'):
                items["item_name"] = []
            items["item_name"].append(item_name)

            if not hasattr(items, 'details'):
                items["details"] = []
            items["details"].append(details)

            if not hasattr(items, 'category'):
                items["category"] = []
            items["category"].append(category)

            if not hasattr(items, 'picture'):
                items["picture"] = []
            items["picture"].append(event.message.media)

            if not hasattr(items, 'base'):
                items["base"] = []
            items["base"].append(number)

            if not hasattr(items, 'name'):
                items["name"] = []
            items["name"].append(s_n)

            event.context["base"] = number
            # Inline options
            inline_keyboard = [
             [Button.inline("Approve", f'iapprove_{len(items["picture"])-1}')],
             [Button.inline("Disapprove", f'idisapprove_{len(items["picture"])-1}')],
            ]

            # Forward all information to submission group with inline buttons
            await client.send_file(SUBMISSION_GROUP_ID, event.message.media, caption=f"""𝐍𝐚𝐦𝐞: <code>{item_name}</code>
𝐃𝐞𝐭𝐚𝐢𝐥𝐬: <code>{details}</code>
𝐁𝐀𝐒𝐄: <code>{number}</code>
Seller <code>{s_n}</code>

""", buttons=inline_keyboard, parse_mode='html')

            event.context["number"] = len(items["picture"])
            if event.sender_id in current_add:
                current_add.remove(event.sender_id)
            return
        else:
            await event.reply("SORRY I M NOT ABLE TO UNDERSTAND THE CATEGORY")
            return
    else:
        await event.reply("PLEASE ENTER YOUR PRICE IN NUMBER AND MULTIPLE OF 100")
        return

  
@client.on(events.CallbackQuery(pattern=r'^(papprove|disapprove|ripnature|ripivsevs|ripmoveset|ripall)_(\d+)$'))
async def pokemon_submission_actions(event):
    callback_data = event.data.decode()
    action, index = callback_data.split('_')
    index = int(index)
    

    item_name = pokemons["item_name"][index]
    seller_id = pokemons["seller_id"][index]
    boosted = pokemons["boosted"][index]
    moveset_page = pokemons["moveset_page"][index]
    iv_page = pokemons["iv_page"][index]
    nature = pokemons["nature"][index]
    lv = pokemons["lv"][index]
    types = pokemons["types"][index]
    category = pokemons["category"][index]
    picture = pokemons["picture"][index]
    number = pokemons["base"][index]
    name = pokemons["name"][index]

    seller = await client.get_entity(seller_id)
    
    try:
        # Deletes the original submission from the channel
        await event.delete()
    except Exception as e:
        logging.error(f"Error deleting the submission message in group: {e}")
        await event.reply("Sorry boss i am not admin")
    
    if action == 'papprove':
        
        code = generate(10)
        inline_keyboard = [
            [Button.url("Place Your Bid 🎴", f'https://t.me/{bot_name}?start={code}')]
        ]
        
        # Create the auction post content

        auction_post = f"""
╔══════════════════════════╗
<b>The Bid Page of {item_name}</b>
highest bid - 0 Pds
Bidder      - None 
╚══════════════════════════╝
"""

        # Send the auction post to the auction channel
        auction_message = await client.send_message(
            AUCTION_GROUP_ID,
            auction_post,
            buttons=inline_keyboard,
            parse_mode='html',
            link_preview=False
        )
        
        id = len(legendary_item) if category == "legendary" else len(non_legendary_item) if category == "non-legendary" else len(shiny_item) if category == "shiny" else len(team_item) if category == "team" else len(tm_item) if category == "tm" else "ERROR"

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
            await event.reply("Error: Invalid category.")
            return
        bd = buyers[category]
        nam = buyers[f"{category}_name"]
        bk = back[category]

        while len(l) <= id:
            l.append("NA")
            slist.append("NA")
            bd.append(0)
            nam.append(0)
            bk.append(0)

        l[id] = f"{seller.first_name}:{name}"
        slist[id] = f"{nature}-{seller_id}"
        bd[id] = 0
        nam[id] = "None"
        msg_detail = f"""{category}:{id}:{seller.first_name}:{name}:{0}:{seller_id}:{back[category][id]}:{code}:{auction_message.id}"""
        
        keyboard = [[
            Button.url("Place Your Bid 🎴", f'https://t.me/{bot_name}?start={code}')
        ]]
        back_up = await client.send_message(BACKUP_GROUP_ID, msg_detail, buttons=keyboard, link_preview=False)
        back[category][id] = back_up.id
        collection[code] = f"{category}_{id}_{auction_message.id}"
        
        try:
            await client.send_message(seller_id, f"your item <blockquote>{item_name} has been listed</blockquote>", parse_mode="html")
        except:
            await event.reply(f"item send to channel but {name} not started bot")
            
        try:
            # Send the accepted notification to the user
            await client.send_message(
            SUBMISSION_GROUP_ID,
                f"<blockquote>{item_name} Approve and added in auction by @{event.sender.username}</blockquote>", parse_mode="html"
            )
        except Exception as e:
            logging.error(f"Error sending message in submission group: {e}")
            await event.reply("Sorry Admin, I am not admin in submission group")

    elif action == 'disapprove':
        try:
            # Send the accepted notification to the user
            await client.send_message(
            SUBMISSION_GROUP_ID,
                f"<blockquote>{item_name} Disapproved by @{event.sender.username}</blockquote>", parse_mode="html"
            )
            await client.send_message(seller_id, f"your item <blockquote>{item_name} has been Disapproved By Admin For Auction</blockquote>", parse_mode="html")
            if event.sender_id in current_add:
                current_add.remove(event.sender_id)

        except Exception as e:
            logging.error(f"Error sending message in submission group: {e}")
            await event.reply("Sorry Admin, I am not admin in submission group")

    elif action == 'ripnature':
        try:
            # Send the accepted notification to the user
            await client.send_message(
            SUBMISSION_GROUP_ID,
                f"<blockquote>{item_name} Nature is not clear so re check it with @{event.sender.username}</blockquote>", parse_mode="html"
            )
        except Exception as e:
            logging.error(f"Error sending message in submission group: {e}")
            await event.reply("Sorry Admin, I am not admin in submission group")
    elif action == 'ripivsevs':
        try:
            # Send the accepted notification to the user
            await client.send_message(
            SUBMISSION_GROUP_ID,
                f"<blockquote>{item_name} IV/EVs are not clear so re check it with @{event.sender.username}</blockquote>", parse_mode="html"
            )
        except Exception as e:
            logging.error(f"Error sending message in submission group: {e}")
            await event.reply("Sorry Admin, I am not admin in submission group")
    elif action == 'ripmoveset':
        try:
            # Send the accepted notification to the user
            await client.send_message(
            SUBMISSION_GROUP_ID,
                f"<blockquote>{item_name} Moveset is not clear so re check it with @{event.sender.username}</blockquote>", parse_mode="html"
            )
        except Exception as e:
            logging.error(f"Error sending message in submission group: {e}")
            await event.reply("Sorry Admin, I am not admin in submission group")
    elif action == 'ripall':
        try:
            # Send the accepted notification to the user
            await client.send_message(
            SUBMISSION_GROUP_ID,
                f"<blockquote>{item_name}  all details are not clear so re check it with @{event.sender.username}</blockquote>", parse_mode="html"
            )
            await client.send_message(seller_id, f"your item <blockquote>{item_name} is re check it and sent again</blockquote>", parse_mode="html")

        except Exception as e:
            logging.error(f"Error sending message in submission group: {e}")
            await event.reply("Sorry Admin, I am not admin in submission group")
@client.on(events.CallbackQuery(pattern=r'^(iapprove|idisapprove)_(\d+)$'))
async def item_submission_actions(event):
    callback_data = event.data.decode()
    action, index = callback_data.split('_')
    index = int(index)
    

    item_name = items["item_name"][index]
    details = items["details"][index]
    category = items["category"][index]
    picture = items["picture"][index]
    number = items["base"][index]
    name = items["name"][index]

    try:
        # Deletes the original submission from the channel
        await event.delete()
    except Exception as e:
        logging.error(f"Error deleting the submission message in group: {e}")
        await event.reply("Sorry boss i am not admin")
    
    if action == 'iapprove':
        
        code = generate(10)
        inline_keyboard = [
            [Button.url("Place Your Bid 🎴", f'https://t.me/{bot_name}?start={code}')]
        ]
        
        # Create the auction post content

        auction_post = f"""
╔══════════════════════════╗
<b>The Bid Page of {item_name}</b>
highest bid - 0 Pds
Bidder      - None 
╚══════════════════════════╝
"""

        # Send the auction post to the auction channel
        auction_message = await client.send_message(
            AUCTION_GROUP_ID,
            auction_post,
            buttons=inline_keyboard,
            parse_mode='html',
            link_preview=False
        )
        
        id = len(legendary_item) if category == "legendary" else len(non_legendary_item) if category == "non-legendary" else len(shiny_item) if category == "shiny" else len(team_item) if category == "team" else len(tm_item) if category == "tm" else "ERROR"

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
            await event.reply("Error: Invalid category.")
            return
        bd = buyers[category]
        nam = buyers[f"{category}_name"]
        bk = back[category]

        while len(l) <= id:
            l.append("NA")
            slist.append("NA")
            bd.append(0)
            nam.append(0)
            bk.append(0)

        l[id] = f"{name}:{details}"
        slist[id] = f"TM-{id}"
        bd[id] = 0
        nam[id] = "None"
        msg_detail = f"""{category}:{id}:{name}:{details}:{0}:{7048431897}:{back[category][id]}:{code}:{auction_message.id}"""
        
        keyboard = [[
            Button.url("Place Your Bid 🎴", f'https://t.me/{bot_name}?start={code}')
        ]]
        back_up = await client.send_message(BACKUP_GROUP_ID, msg_detail, buttons=keyboard, link_preview=False)
        back[category][id] = back_up.id
        collection[code] = f"{category}_{id}_{auction_message.id}"
        
        try:
            # Send the accepted notification to the user
            await client.send_message(
            SUBMISSION_GROUP_ID,
                f"<blockquote>{item_name} Approve and added in auction by @{event.sender.username}</blockquote>", parse_mode="html"
            )
        except Exception as e:
            logging.error(f"Error sending message in submission group: {e}")
            await event.reply("Sorry Admin, I am not admin in submission group")

    elif action == 'idisapprove':
        try:
            # Send the accepted notification to the user
            await client.send_message(
            SUBMISSION_GROUP_ID,
                f"<blockquote>{item_name} Disapproved by @{event.sender.username}</blockquote>", parse_mode="html"
            )

        except Exception as e:
            logging.error(f"Error sending message in submission group: {e}")
            await event.reply("Sorry Admin, I am not admin in submission group")

@client.on(events.CallbackQuery(data=b'clear_yes'))
async def clear_yes(event):
    legendary_list.clear()
    non_legendary_list.clear()
    shiny_list.clear()
    tm_list.clear()
    team_list.clear()
    legendary_item.clear()
    non_legendary_item.clear()
    shiny_item.clear()
    tm_item.clear()
    team_item.clear()
    buyers["legendary"].clear()
    buyers["non-legendary"].clear()
    buyers["shiny"].clear()
    buyers["tm"].clear()
    buyers["team"].clear()
    buyers["legendary_name"].clear()
    buyers["non-legendary_name"].clear()
    buyers["shiny_name"].clear()
    buyers["tm_name"].clear()
    buyers["team_name"].clear()
    collection.clear()
    seller_old.clear()
    back["legendary"].clear()
    back["non-legendary"].clear()
    back["shiny"].clear()
    back["tm"].clear()
    back["team"].clear()
    await event.edit('All the items have been cleared')

@client.on(events.CallbackQuery(data=b'clear_no'))
async def clear_no(event):
    await event.edit('Okay not clearing anything')

@client.on(events.NewMessage(pattern='(?i)/cancel'))
async def cancel(event):
    if event.sender_id in current_add:
        current_add.remove(event.sender_id)
        await event.reply('Okay i have cancelled the on going submission 🫡')
    else:
        await event.reply("You haven't started any submission yet 😐")

async def buyers_list(event):
    message_bu = "<b> Here is the data of all buyers.</b>"
    await send_long_message(event.chat_id, message_bu)
    for cat in buyers:
        data = buyers[cat]
        if len(data) != 0:
            for i in range(len(data)):
                try:
                    await client.send_message(event.chat_id, f"<code>{cat}</code> :- item No {i} :- {buyers[cat][i]}", parse_mode="html")
                except:
                    await event.reply(f"some error in {cat} -> {i}")
                    pass

async def sellers_list(event):
    message_se = "<b> Here is the data of all seller.</b>"
    await send_long_message(event.chat_id, message_se)
    for name in seller_old:
        item = seller_old[name]["item"]
        bag = seller_old[name]["bag"]
        try:
            await client.send_message(event.chat_id, f"<a href='tg://user?id={name}'> {name} </a> <code>item {item}</code> \n <code> TM and Team {bag}</code>", parse_mode="html")
        except:
            await event.reply(f"Some error {name}")
            pass




    

if __name__ == '__main__':
    try:
        client.run_until_disconnected()
    except KeyboardInterrupt:
        print('Exiting...')