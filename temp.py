from telegram.ext import ConversationHandler
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import re
import time
from telegram.ext.dispatcher import run_async
from telegram import User, PhotoSize, ParseMode
import telegram


AUCTION_GROUP_ID=-1002196587583
OWNER=int(7048431897)
# Optional imports based on functionality
import logging  # For logging information
SUBMISSION_GROUP_ID=-1002196587583
# Set pokemons,teams,tms name here
LEGENDARY_POKEMON_NAMES = ["Articuno", "Zapdos", "Moltres", "Raikou", "Entei", "Suicune", "Regirock", "Regice", "Registeel", "Latias", "Latios", "Uxie", "Mesprit", "Azelf", "Heatran", "Regigigas", "Cresselia", "Cobalion", "Terrakion", "Virizion", "Buzzwole", "Thundurus", "Tornadus", "Landorus", "Type: Null", "Silvally", "Tapu Koko", "Tapu Bulu", "Tapu Fini", "Tapu Lele", "Nihilego", "Pheromosa", "Xurkitree", "Celesteela", "Kartana", "Guzzlord", "Poipole", "Naganadel", "Stakataka", "Blacephalon", "Kubfu", "Urshifu", "Regieleki", "Regidrago", "Glastrier", "Spectrier", "Enamorus", "Wo-chien", "Chien-pao", "Ting-lu", "Chi-yu", "Okidogi", "Munkidori", "Fezandipiti", "Ogerpon", "Mewtwo", "Lugia", "Ho-oh", "Kyogre", "Groudon", "Rayquaza", "Dialga", "Palkia", "Giratina", "Reshiram", "Zekrom", "Kyurem", "Xerneas", "Yveltal", "Zygarde", "Cosmog", "Cosmoem", "Solgaleo", "Lunala", "Necrozma", "Zacian", "Zamazenta", "Eternatus", "Calyrex", "Koraidon", "Miraidon", "Terapagos", "Mew", "Celebi", "Jirachi", "Deoxys", "Phione", "Manaphy", "Darkrai", "Arceus", "shaymin", "Victini", "Keldeo", "Meloetta", "Genesect", "Diancie", "Hoopa", "Volcanion", "Megearna", "Marshadow", "Zeraora", "Meltan", "Melmetal", "Zarude"]

NON_LEGENDARY_POKEMON_NAMES = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran-F", "Nidorina", "Nidoqueen", "Nidoran-M", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetchd", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr-Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Dratini", "Dragonair", "Dragonite", "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr", "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou", "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos", "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern", "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown", "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull", "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub", "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom", "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid", "Magby", "Miltank", "Blissey", "Larvitar", "Pupitar", "Tyranitar", "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert", "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple", "Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad", "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull", "Pelipper", "Ralts", "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking", "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass", "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike", "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo", "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava", "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach", "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo", "Feebas", "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Tropius", "Chimecho", "Absol", "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth", "Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Turtwig", "Grotle", "Torterra", "Chimchar", "Monferno", "Infernape", "Piplup", "Prinplup", "Empoleon", "Starly", "Staravia", "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune", "Shinx", "Luxio", "Luxray", "Budew", "Roserade", "Cranidos", "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam-Plant", "Mothim", "Combee", "Vespiquen", "Pachirisu", "Buizel", "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom", "Drifloon", "Drifblim", "Buneary", "Lopunny", "Mismagius", "Honchkrow", "Glameow", "Purugly", "Chingling", "Stunky", "Skuntank", "Bronzor", "Bronzong", "Bonsly", "Mime-Jr", "Happiny", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp", "Munchlax", "Riolu", "Lucario", "Hippopotas", "Hippowdon", "Skorupi", "Drapion", "Croagunk", "Toxicroak", "Carnivine", "Finneon", "Lumineon", "Mantyke", "Snover", "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth", "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z", "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom,Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat", "Watchog", "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear", "Panpour", "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola", "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr", "Tympole", "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede", "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Basculin-Red-Striped", "Sandile", "Krokorok", "Krookodile", "Darumaka", "Darmanitan-Standard", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask", "Cofagrigus", "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark", "Minccino", "Cinccino", "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite", "Vanillish", "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent", "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik", "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic", "Cryogonal", "Shelmet", "Accelgor", "Stunfisk", "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard", "Bisharp", "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous", "Hydreigon", "Larvesta", "Chespin", "Thwackey", "Rillaboom", "Scorbunny", "Raboot", "Cinderace", "Sobble", "Drizzile", "Inteleon", "Skwovet", "Greedent", "Rookidee", "Corvisquire", "Corviknight", "Blipbug", "Dottler", "Orbeetle", "Nickit", "Thievul", "Gossifleur", "Eldegoss", "Wooloo", "Dubwool", "Chewtle", "Drednaw", "Yamper", "Boltund", "Rolycoly", "Carkol", "Coalossal", "Applin", "Flapple", "Appletun", "Silicobra", "Sandaconda", "Cramorant", "Arrokuda", "Barraskewda", "Toxel", "Toxtricity-Amped", "Sizzlipede", "Centiskorch", "Clobbopus", "Grapploct", "Sinistea", "Polteageist", "Hatenna", "Hattrem", "Hatterene", "Impidimp", "Morgrem", "Grimmsnarl", "Obstagoon", "Perrserker", "Cursola", "Sirfetchd", "Mr-Rime", "Runerigus", "Milcery", "Alcremie", "Falinks", "Pincurchin", "Snom", "Frosmoth", "Stonjourner", "Eiscue-Ice", "Indeedee-Male", "Morpeko-Full-Belly", "Cufant", "Copperajah", "Dracozolt", "Arctozolt", "Dracovish", "Dartrix", "Decidueye", "Litten", "Torracat", "Incineroar", "Popplio", "Brionne", "Primarina", "Pikipek", "Trumbeak", "Toucannon", "Yungoos", "Gumshoos", "Grubbin", "Charjabug", "Vikavolt", "Crabrawler", "Crabominable", "Oricorio-Baile", "Cutiefly", "Ribombee", "Rockruff", "Lycanroc-Midday", "Wishiwashi-Solo", "Mareanie", "Toxapex", "Mudbray", "Mudsdale", "Dewpider", "Araquanid", "Fomantis", "Lurantis", "Morelull", "Shiinotic", "Salandit", "Salazzle", "Stufful", "Bewear", "Bounsweet", "Steenee", "Tsareena", "Comfey", "Oranguru", "Passimian", "Wimpod", "Golisopod", "Sandygast", "Palossand", "Pyukumuku", "Type-Null", "Silvally", "Minior-Red-Meteor", "Komala", "Turtonator", "Togedemaru", "Mimikyu-Disguised", "Bruxish", "Drampa", "Dhelmise", "Jangmo-O", "Hakamo-O", "Kommo-O", "Poipole", "Naganadel"]

SHINY_POKEMON_NAMES = LEGENDARY_POKEMON_NAMES + NON_LEGENDARY_POKEMON_NAMES

POKEMON_TEAM = ["Hp", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed"]

TM = ["Tm02", "Tm03", "Tm09", "Tm10", "Tm13", "Tm14", "Tm15", "Tm22", "Tm23", "Tm24", "Tm25", "Tm26", "Tm28", "Tm29", "Tm30", "Tm31", "Tm34", "Tm35", "Tm36", "Tm38", "Tm39", "Tm40", "Tm42", "Tm43", "Tm46", "Tm47", "Tm48", "Tm49", "Tm50", "Tm51", "Tm52", "Tm53", "Tm54", "Tm55", "Tm57", "Tm58", "Tm59", "Tm62", "Tm65", "Tm66", "Tm67", "Tm68", "Tm71", "Tm72", "Tm76", "Tm78", "Tm79", "Tm80", "Tm81", "Tm82", "Tm83", "Tm84", "Tm85", "Tm89", "Tm91", "Tm93", "Tm94", "Tm95", "Tm97", "Tm98", "Tm99"]

approved_users=[]
seller_data = {}
seller_lead = {}
legendary_list = []
non_legendary_list = []
shiny_list = []
tm_list = []
team_list = []
shiny_picture=[]
shiny_caption=[]
legendary_picture=[]
legendary_caption=[]
non_legendary_picture=[]
non_legendary_caption=[]
tm_caption=[]
team_caption=[]
global last_item_name
global sellers_list
# Define the conversation states
ITEM_NAME, NATURE_PAGE, ITEM_DETAILS, POKEMON_IV, MOVESET_PAGE, BOOSTED, BASE_PRICE = range(7)
user_list=[]
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
pokemons["type"] = []
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
def broadcast(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please enter the message you want to broadcast:")
    return BROADCAST_MESSAGE

BROADCAST_MESSAGE = 1

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
    if user_id != chatid:
        context.bot.send_message(chat_id=update.message.chat.id,text="𝑇ℎ𝑖𝑠 𝑐𝑜𝑚𝑚𝑎𝑛𝑑 𝑐𝑎𝑛 𝑜𝑛𝑙𝑦 𝑏𝑒 𝑢𝑠𝑒𝑑 𝑖𝑛 𝑑𝑚 समझा🧐")
        return ConversationHandler.END
    if user_id not in user_list:
        user_list.append(user_id)
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
    if user_id in seller_data:
        update.message.reply_text("please wait till approve/disapprove the last item")
    else:
        message = update.message.reply_text('<blockquote>𝑊𝐻𝐴𝑇 𝑌𝑂𝑈 𝑊𝐴𝑁𝑇 𝑇𝑂 𝑆𝐸𝐿𝐿 𝐼𝑁 𝐼𝐻𝐺 𝐴𝑈𝐶𝑇𝐼𝑂𝑁?</blockquote>\n𝐶ℎ𝑜𝑜𝑠𝑒 𝑓𝑟𝑜𝑚 𝑏𝑒𝑙𝑜𝑤 🎐', reply_markup=reply_markup, parse_mode='HTML')
        context.user_data['message_id'] = message.message_id  # Save the message_id for updating later
        context.user_data["user"] = user

        return ITEM_NAME
def users(update,context):
    usersl="7048431897"
    for user in user_list:
        usersl=f"{usersl},{user}"
    context.bot.send_message(chat_id=update.message.chat.id,text=usersl)
def category(update, context):
    user = update.effective_user
    query = update.callback_query

    callback_data = query.data
    context.user_data['category'] = callback_data

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
    else:
        submission(update, context)
        return 

    context.bot.edit_message_text(chat_id=update.callback_query.message.chat_id,
                                  message_id=context.user_data.get('message_id'),
                                  text=f"<blockquote>{reply_text}</blockquote>",parse_mode="html")

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
                   # Extracting nature and level from the caption
                   nature_index = caption_text.find("Nature: ") + len("Nature: ")
                   lv_index = caption_text.find("Lv. ") + len("Lv. ")
                   types_index = caption_text.find("Types: [") + len("Types: [")

                   # Finding the end of the nature
                   nature_end_index = caption_text.find(" ", nature_index)
                   if nature_end_index == -1:
                       nature_end_index = caption_text.find("\n", nature_index)
                   nature = caption_text[nature_index:nature_end_index]

                   # Finding the end of the level
                   lv_end_index = caption_text.find(" ", lv_index)
                   if lv_end_index == -1:
                       lv_end_index = caption_text.find("\n", lv_index)
                   lv = caption_text[lv_index:lv_end_index]

                   # Finding the end of the types
                   types_end_index = caption_text.find("]", types_index)
                   if types_end_index == -1:
                       types_end_index = caption_text.find("\n", types_index)
                   types = caption_text[types_index:types_end_index]

                   # Save photo file_id
                   photo = update.message.photo[-1]  # Get the largest photo size
                   context.user_data["picture"] = photo.file_id

                   # Save nature and level in user_data
                   context.user_data["nature"] = nature.strip()
                   context.user_data["lv"] = lv.strip()
                   context.user_data["type"] = types.strip()

                   # Forward the message to the submission group
                   context.bot.forward_message(chat_id=SUBMISSION_GROUP_ID, from_chat_id=update.message.chat_id,
                                               message_id=update.message.message_id)
                   update.message.reply_text("<blockquote>𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝐼𝑉/𝐸𝑉 𝑃𝐴𝐺𝐸 𝑂𝐹 𝑌𝑂𝑈𝑅 𝑃𝑂𝐾𝐸𝑀𝑂𝑁</blockquote> 𝐹𝑅𝑂𝑀 @HeXamonbot ",parse_mode="html")
                   return POKEMON_IV
               else:
                   update.message.reply_text("<blockquote>𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 𝐹𝑅𝑂𝑀 @HeXamonbot</blockquote> 𝑜𝑡ℎ𝑒𝑟𝑤𝑖𝑠𝑒 𝑝𝑟𝑜𝑐𝑒𝑠𝑠 𝑤𝑖𝑙𝑙 𝑛𝑜𝑡 𝑤𝑜𝑟𝑘 𝑓𝑜𝑟 𝑠𝑒𝑛𝑑 𝑡𝑜 𝑠𝑢𝑏𝑚𝑖𝑠𝑠𝑖𝑜𝑛",parse_mode="html")
                   return NATURE_PAGE
           else:
               update.message.reply_text("<blockquote>𝑃𝐿𝐸𝐴𝑆𝐸 𝐹𝑂𝑅𝑊𝐴𝑅𝐷 NATURE 𝑃𝐴𝐺𝐸 𝑂𝐹 𝑌𝑂𝑈𝑅 𝑃𝑂𝐾𝐸𝑀𝑂𝑁 </blockquote>𝐹𝑅𝑂𝑀 @HeXamonbot ",parae_mode="html")
               return NATURE_PAGE
        else:
            update.message.reply_text("PLEASE DON'T SEND ONLY PHOTO/DETAILS. <blockquote>FORWARD FULL PAGE FROM @HeXamonbot</blockquote>",parae_mode="html")
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
    seller = context.user_data.get("user")
    boosted = context.user_data.get("boosted")
    moveset_page = context.user_data.get("moveset_page")
    iv_page = context.user_data.get("iv_page")
    nature = context.user_data.get("nature")
    lv = context.user_data.get("lv")
    details = context.user_data.get("details")
    types = context.user_data.get("type")
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
                pokemons["lv"].append(nature) 
                pokemons["type"].append(type) 
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
            return ConversationHandler.END
        else:
            update.message.reply_text(f"<blockquote>OUR ADMINS DECIDE THAT BASE PRICE SHOULD BE MULTIPLE OF 100. BUT YOU TELL ({number_text}) IT IS MULTIPLE OF 100. SO IT WILL BE NOT ACCEPTED BY US.</blockquote>",parse_mode="html")
            return BASE_PRICE
    except ValueError:
        update.message.reply_text("<blockquote>PLEASE WRITE FULL NUMBER OR GIVE IN FORMAT [(number)k]. NO OTHER FORMAT WILL ACCEPT.</blockquote>",parse_mode="html" )
        return BASE_PRICE

def check_message(update, context):
    global rmessage,user_name
    message=update.message

    if update.message.chat.id == AUCTION_GROUP_ID and update. message.reply_to_message and update. message.text.strip() == "." and update. message.from_user.id in approved_users:
        pass
    else:
        return
    number_text = message.reply_to_message.text
    try:
        number = float(number_text[:-1]) * 1000 if number_text[-1].lower() == 'k' else float(number_text)
        if number % 100 == 0:
            pass
        else:
            update.message.reply_text(f"INVALID BID")
            return
    except:
        update.message.reply_text(f"INVALID BID")
        return
    replied_user = message.reply_to_message.from_user
    replied_message = message.reply_to_message.text
    rmessage=number
    user_name=replied_user.first_name
    sent_message = message.reply_text("★")
    time.sleep(1)
    context.bot.edit_message_text(chat_id=sent_message.chat_id, message_id=sent_message.message_id, text="★★")
    time.sleep(1)
    context.bot.edit_message_text(chat_id=sent_message.chat_id, message_id=sent_message.message_id, text="★★★")
    time.sleep(1)

    keyboard = [[InlineKeyboardButton("YES", callback_data=f"confirm_sell_{replied_user.id}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.edit_message_text(chat_id=sent_message.chat_id, message_id=sent_message.message_id,
                                 text=f"<blockquote>Are You Sure To Sell {last_item_name} To <a href='tg://user?id={replied_user.id}'>{replied_user.first_name} {replied_user.last_name} 🍁</a></blockquote>\n<blockquote> For {replied_message} ?</blockquote>", 
                                 reply_markup=reply_markup, 
                                 parse_mode="html")

def button(update: Update, context: CallbackContext):
    global rmessage, user_name, last_item_name
    query = update.callback_query
    if query:
        if query.data.startswith("confirm_sell_"):
            data = query.data.split('_')
            user_id = int(data[2])
            username = user_name
            message = rmessage

            if query.from_user.id in approved_users:
                replied_user = context.bot.get_chat_member(query.message.chat_id, user_id).user.username
                trade_group_link_hidden = "<a href='https://t.me/IGHTRADEGROUP'>𝑇𝑅𝐴𝐷𝐸 𝐺𝑅𝑂𝑈𝑃 </a>"

                context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id,
                                              text=f"<blockquote>🌍 {last_item_name} 𝐻𝑎𝑠 𝐵𝑒𝑒𝑛 𝑆𝑜𝑙𝑑</blockquote>\n\n⛩️𝑆𝑜𝑙𝑑 𝑇𝑜  -- <a href='tg://user?id={user_id}'>{username} </a>\n🍁𝑆𝑜𝑙𝑑 𝐹𝑜𝑟-- {message}\n\n❗ <blockquote>Join {trade_group_link_hidden} To Get Seller Username After Auction</blockquote>",
                                              parse_mode='html')
                bist.append(f"{last_item_name} — <a href='tg://user?id={user_id}'>{username}</a>\nfor : {message}")
            else:
                query.answer(text="🖕", show_alert=True)
        query.answer()
    else:
        # Handle the case where it's not a callback query (e.g., a text message)
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")


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
        # Allow the message if user is approved
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
        types = pokemons["type"][id]
        category = pokemons["category"][id]
        picture = pokemons["picture"][id]
        base_price = pokemons["base"][id]
        message_id = pokemons["msg_id"][id]
        pmessage = f"POKEMON NAME: {item_name}\nLEVEL: {lv}\nNATURE: {nature}\nTYPES: {types}\n\nIVs AND EVs:\n{iv_page}\n\nMOVESETS :\n{moveset_page}\n\nBoosted: {boosted}\nBase Price: {base_price}"
        updated_text = f"POKEMON CATEGORY: {category}\n\n > POKEMON DETAILS:-\n\nNAME: {item_name}\nLEVEL: {lv}\nNATURE: {nature}\nTYPES: {types}\n\n > IV AND EV POINTS:-\n{iv_page}\n\n > MOVESETS:-\n{moveset_page}\n\nBOOSTED: {boosted}\n\nBASE PRICE: {base_price}\n\n > SELLER USERNAME:- {seller_name}\n > SELLER ID:- {seller_id}\n\nIT HAS BEEN {Stats} BY {admin.full_name}({admin_name})"
    if query.data.startswith('tapprove') or query.data.startswith('wrongdisplay') or query.data.startswith('uselessteam') or query.data.startswith('twronginfo') or query.data.startswith('disapprove') or query.data.startswith('tbasehigh'):
        context.bot.send_message(
        chat_id=AUCTION_GROUP_ID,
        text="picture") 
        category = tms["category"][id]
        details = tms["details"][id]
        item_name = tms["item_name"][id]
        base_price = tms["base"][id]
        mid = tms["msg_id"][id]
        seller_id = tms["seller_id"][id]
        seller_name = tms["name"][id]
        tupdated_text = f"{category.upper()} \n > NAME: {item_name}\n\n{category.upper()} DETAILS:\n{details}\n\nBASE PRICE: {base_price}\n\n > SELLER USERNAME: {seller_name}\n > SELLER ID: {seller_id}\n\nIt has been {Stats} by {admin.full_name}({admin.name})"




    if seller_id not in seller_lead:
        seller_lead[seller_id]={}
    if callback_data.startswith('papprove'):
        context.bot.send_message(
        chat_id=seller_id,
        text=f"<blockquote>YOUR {item_name}[LV:{lv} & NATURE:{nature}] HAS BEEN APPROVED FOR NEXT AUCTION.</blockquote>"
    ,parse_mode="html")

    # Send photo to the auction group
        context.bot.send_photo(
        chat_id=AUCTION_GROUP_ID,
        photo=picture,
        caption=f"""
> POKEMON DETAILS:

NAME: {item_name}
LEVEL: {lv}
NATURE: {nature}
TYPE: {types}

> IVS/EVS:
{iv_page}

> MOVESETS:
{moveset_page}

> BOOSTED: {boosted}
> BASE PRICE: {base_price}""",parse_mode="markdown")

    # Edit the original message caption
        context.bot.edit_message_caption(
        chat_id=update.callback_query.message.chat_id,
        message_id=message_id,
        caption=updated_text, parse_mode="markdown")
        if category == "legendary":
            if seller_id in seller_lead:
                if "legendary" in seller_lead[seller_id]:
                    seller_lead[seller_id]["legendary"] += 1
                else:
                    seller_lead[seller_id]["legendary"] = 1  # Default value if not found
            else:
                seller_lead[seller_id]["legendary"] = 1


            legendary_picture.append(picture)
            legendary_caption.append(f"POKEMON DETAILS:\n\n>NAME: {item_name}\nLEVEL: {lv}\nNATURE: {nature}\nTYPE: {types}\n\n > IVS/EVS:\n{iv_page}\n\n > MOVESETS:\n{moveset_page}\n\nBOOSTED: {boosted}\nBASE PRICE: {base_price}")

            legendary_list.append(f"<blockquote>{item_name}({nature})</blockquote> : {seller_name}")
        elif category == "non-legendary":
            if seller_id in seller_lead:
                if "non_legendary" in seller_lead[seller_id]:
                    seller_lead[seller_id]["non_legendary"] += 1
                else:
                    seller_lead[seller_id]["non_legendary"] = 1  # Default value if not found
            else:
                seller_lead[seller_id]["non_legendary"] = 1

            non_legendary_picture.append(picture) 
            non_legendary_caption.append(f"POKEMON DETAILS:\n\n>NAME: {item_name}\nLEVEL: {lv}\nNATURE: {nature}\nTYPE: {types}\n\n > IVS/EVS:\n{iv_page}\n\n > MOVESETS:\n{moveset_page}\n\nBOOSTED: {boosted}\nBASE PRICE: {base_price}") 
            non_legendary_list.append(f"<blockquote>{item_name}({nature}) </blockquote>: {seller_name}")
        elif category == "shiny":
            if seller_id in seller_lead:
                if "shiny" in seller_lead[seller_id]:
                    seller_lead[seller_id]["shiny"] += 1
                else:
                    seller_lead[seller_id]["shiny"] = 1  # Default value if not found
            else:
                seller_lead[seller_id]["shiny"] = 1

            shiny_picture.append(picture)
            shiny_caption.append(f"POKEMON DETAILS:\n\n>NAME: {item_name}\nLEVEL: {lv}\nNATURE: {nature}\nTYPE: {types}\n\n > IVS/EVS:\n{iv_page}\n\n > MOVESETS:\n{moveset_page}\n\nBOOSTED: {boosted}\nBASE PRICE: {base_price}") 

            shiny_list.append(f"<blockquote>{item_name}({nature}) </blockquote>: {seller_name}")

    if callback_data.startswith('tapprove'):
        # Send message to the owne

        # Notify the seller
        context.bot.send_message(chat_id=seller_id, text=f"<blockquote>𝑌𝑜𝑢𝑟 {item_name} 𝐻𝑎𝑠 𝐵𝑒𝑒𝑛 𝑎𝑝𝑝𝑟𝑜𝑣𝑒𝑑.</blockquote>",parse_mode="html")

        # Send auction details to the auction group
        context.bot.send_message(chat_id=AUCTION_GROUP_ID, text=f" > {category.upper()} NAME: {item_name}\n\n{category.upper()} DETAILS:\n{details}\n\n > BASE PRICE: {base_price}",parse_mode="markdown")

    
        context.bot.edit_message_text(
            chat_id=update.callback_query.message.chat_id,
            message_id=mid,
            text=tupdated_text,parse_mode="html"
        )

        if category == "team":
            if seller_id in seller_lead:
                if "team" in seller_lead[seller_id]:
                    seller_lead[seller_id]["team"] += 1
                else:
                    seller_lead[seller_id]["team"] = 1  # Default value if not found
            else:
                seller_lead[seller_id]["team"] = 1

            team_caption.append(f" > {category.upper()} NAME: {item_name}\n\n{category.upper()} DETAILS:\n{details}\n\n > BASE PRICE: {base_price}")
            team_list.append(f"<blockquote>{item_name} Team </blockquote>: {seller_name}")
        elif category == "tm":
            if seller_id in seller_lead:
                if "tm" in seller_lead[seller_id]:
                    seller_lead[seller_id]["tm"] += 1
                else:
                    seller_lead[seller_id]["tm"] = 1  # Default value if not found
            else:
                seller_lead[seller_id]["tm"] = 1

            tm_caption.append(f"{category.upper()} NAME: <blockquote>{item_name}</blockquote>\n\n{category.upper()} DETAILS:\n<blockquote>{details}</blockquote>\n\nBASE PRICE:<blockquote> {base_price}</blockquote>")
            tm_list.append(f"<blockquote>{item_name}</blockquote> : {seller_name}")

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


def next(update, context):
    user_id = update.message.from_user.id
    if user_id in approved_users:
        # Allow the message if user is approved
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
    global next_value_legendary, next_value_non_legendary, next_value_shiny, next_value_tm, next_value_team, last_item_name
    if next_value_legendary is None:
        next_value_legendary = 0
    if next_value_non_legendary is None:
        next_value_non_legendary = 0
    if next_value_shiny is None:
        next_value_shiny = 0
    if next_value_tm is None:
        next_value_tm = 0
    if next_value_team is None:
        next_value_team = 0
    # ... rest of the function remains the same ... 

    # Determine which category to send next based on the current value
    if next_value_legendary < len(legendary_picture):
        # Send legendary data
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=legendary_picture[next_value_legendary],
                               caption=legendary_caption[next_value_legendary], parse_mode="markdown")
        legendary=str(legendary_list[next_value_legendary])
        sp=legendary.split(":",1)
        last_item_name=sp[0]
        next_value_legendary += 1
    elif next_value_non_legendary < len(non_legendary_picture):
        # Send non-legendary data
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=non_legendary_picture[next_value_non_legendary],
                               caption=non_legendary_caption[next_value_non_legendary], parse_mode="markdown")
        legendary=str(non_legendary_list[next_value_non_legendary])
        sp=legendary.split(":",1)
        last_item_name=sp[0]
        next_value_non_legendary += 1
    elif next_value_shiny < len(shiny_picture):
        # Send shiny data
        context.bot.send_photo(chat_id=update.effective_chat.id,
                               photo=shiny_picture[next_value_shiny],
                               caption=shiny_caption[next_value_shiny], parse_mode="markdown")
        legendary=str(shiny_list[next_value_shiny])
        sp=legendary.split(":",1)
        last_item_name=sp[0]
        next_value_shiny += 1
    elif next_value_tm < len(tm_caption):
        # Send TM data
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=tm_caption[next_value_tm], parse_mode="markdown")
        legendary=str(tm_list[next_value_tm])
        sp=legendary.split(":",1)
        last_item_name=sp[0]
        next_value_tm += 1
    elif next_value_team < len(team_caption):
        # Send Team data
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=team_caption[next_value_team], parse_mode="markdown")
        legendary=str(team_list[next_value_team])
        sp=legendary.split(":",1)
        last_item_name=sp[0]
        next_value_team += 1
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="All data sent. Starting from the beginning again.")
def current(update, context):

    if update.message.from_user.id not in approved_users:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return
    total=len(legendary_picture)+len(non_legendary_picture)+len(shiny_picture)+len(tm_caption)+len(team_caption)
    message = f"<blockquote>𝐶𝑢𝑟𝑟𝑒𝑛𝑡 𝑙𝑖𝑠𝑡 𝑜𝑓 𝑃𝑜𝑘𝑒𝑚𝑜𝑛 𝑎𝑛𝑑 𝑡𝑒𝑎𝑚𝑠 </blockquote>:\n\n★ <blockquote>𝐿𝑒𝑔𝑒𝑛𝑑𝑎𝑟𝑦 :</blockquote> {len(legendary_picture)}\n★ <blockquote>𝑁𝑜𝑛-𝑙𝑒𝑔𝑒𝑛𝑑𝑎𝑟𝑦 : {len(non_legendary_picture)}</blockquote>\n★ <blockquote>𝑆ℎ𝑖𝑛𝑦 : {len(shiny_picture)}</blockquote>\n★ <blockquote>𝑇𝑚𝑠 : {len(tm_caption)}</blockquote>\n★ <blockquote>𝑇𝑒𝑎𝑚𝑠 : {len(team_caption)}</blockquote>\n★ <blockquote>𝑇𝑜𝑡𝑎𝑙 : {total}</blockquote>"
    context.bot.send_message(chat_id=update.effective_chat.id, text=f" {message} ",parse_mode="html")

def buyer_command(update, context):
    if update.message.from_user.id not in approved_users:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return

    # Format the list of buyers with Markdown for better readabilit
    blist="<blockquote>HERE IS THE BUYERS LIST</blockquote>"
    for buy in bist:
        blist=f"{blist}\n{buy}"
    context.bot.send_message(chat_id=update.message.chat.id,text=f"{blist}",parse_mode ="html")

def sellers(update, context):

    if update.message.from_user.id in approved_users:
        all_sellers = legendary_list + non_legendary_list + shiny_list + tm_list + team_list
        message_text="HERE IS THE SELLERS LIST"
        for user in all_sellers:
            message_text=f"{message_text}\n{user}"
        context.bot.send_message(chat_id=update.message.chat.id, text=f"<b>{message_text}</b>",parse_mode="html")

    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
def check(update, context):
    user_id = update.message.from_user.id
    if user_id in approved_users:
        # Allow the message if user is approved
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return

    command_parts = update.message.text.split(" ") 
    if len(command_parts) >= 3:  # You need at least 3 parts: command + word1 + word2
        word_to_read = command_parts[1]  
        word_to_reade = int(command_parts[2])  # This is where the error was
        if word_to_read == "legendary":
            ph = legendary_pic[word_to_reade]  # Use the correct variable name
            cap = legendary_cap[word_to_reade]
            context.bot.send_photo(chat_id=update.message.chat.id, photo=ph, caption=cap)
        else:
            update.message.reply_text("I'm only supposed to read value")
    else:
        update.message.reply_text("Please provide two words to read after /read") 

def cancel(update, context):
    update.message.reply_text("DONE YOUR RUNNING COMMAND HAS STOPED.")
    return ConversationHandler.END
def approve_command(update,context):
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

def profile(update,context):
    user = update.effective_user
    seller_id=user.id
    if seller_id not in seller_lead:
        seller_lead[seller_id] = {}
    if "legendary" not in seller_lead[seller_id]:
        seller_lead[seller_id]["legendary"] = 0

    if "non_legendary" not in seller_lead[seller_id]:
        seller_lead[seller_id]["non_legendary"] = 0
    if "shiny" not in seller_lead[seller_id]:
        seller_lead[seller_id]["shiny"] = 0

    if "tm" not in seller_lead[seller_id]:
        seller_lead[seller_id]["tm"] = 0
    if "team" not in seller_lead[seller_id]:
        seller_lead[seller_id]["team"] = 0
    total=seller_lead[user.id]["non_legendary"]+seller_lead[user.id]["legendary"]+seller_lead[user.id]["shiny"]+seller_lead[user.id]["team"]+seller_lead[user.id]["tm"]
    if user.id==OWNER:
        ver="✔️"
        post="🔳OWNER💯"
    elif user.id in approved_users:
        ver="✔️"
        post="🔳Admin📃"
    else:
        ver="❌"
        post="⬛member"
    try:
        photo = context.bot.get_user_profile_photos(update.message.from_user.id, limit=1).photos[0][-1]
    except AttributeError:
        # If user doesn't have a profile photo, use a default
        photo = "AgACAgUAAxkBAAIHpWb3p_ReyXePSv7wsvxeiHKCLHKoAAKZvjEb_8bAV-OkqkL2FtfdAQADAgADcwADNgQ"


    leg=seller_lead[user.id]["legendary"]
    non_leg=seller_lead[user.id]["non_legendary"]
    shiny=seller_lead[user.id]["shiny"]
    tm=seller_lead[user.id]["tm"]
    team=seller_lead[user.id]["team"]
    message=f"Here is Profile Of {user.first_name}\n\n<blockquote>★ » Name: {user.first_name}\n★Username : @{user.username}\n★🆔 ID: {user.id}</blockquote>\n➖➖➖➖➖➖➖➖➖➖➖☆\n┃╸ 🔺 0L : <blockquote>\n{non_leg} </blockquote>\n┃╸ 🔺6L :<blockquote>\n{leg}</blockquote>\n┃╸ 🔺 Shiny : <blockquote>\n{shiny}</blockquote>\n┃╸ 🔺 TMs : <blockquote>\n {tm}</blockquote>\n┃╸ 🔺 Teams : <blockquote>\n{team}</blockquote>\n┃╸🔰 Total :{total}\n★➖➖➖➖➖➖➖➖➖➖☆\n┃╸ ©️ Verified? - {ver}\n┃╸ 💠Status : {post}\n★➖➖➖➖➖➖➖➖➖➖☆ "
    context.bot.send_photo(chat_id=update.message.chat.id, photo=photo, caption=message, parse_mode="html")
def clear(update, context):
    if update.message.from_user.id==OWNER:
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id,text="you want to die 😶‍🌫️😎😎")
        return 
    seller_data .clear()
    legendary_list.clear()
    non_legendary_list.clear()
    shiny_list.clear()
    tm_list.clear()
    team_list.clear()
    shiny_picture.clear()
    shiny_caption.clear()
    legendary_picture.clear()
    legendary_caption.clear()
    non_legendary_picture.clear()
    non_legendary_caption.clear()
    tm_caption.clear()
    team_caption.clear()
    context.bot.send_message(chat_id=update.message.chat.id,text="done ✅ \n cleared all items boss🗿")
    return context.bot.send_message(chat_id=update.message.chat.id, text="working ")

def reset_command(update, context):
    user_id = update.message.from_user.id
    if user_id in approved_users:
        pass
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text="You are not an approved user.")
        return

    global next_value_legendary, next_value_non_legendary, next_value_shiny, next_value_tm, next_value_team, buyers_list
    next_value_legendary = 0
    next_value_non_legendary = 0
    next_value_shiny = 0
    next_value_tm = 0
    next_value_team = 0
    buyers_list="Here is the Buyers List"   
    context.bot.send_message(chat_id=update.message.chat.id,text="all done")
    return
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

updater = Updater("6973255869:AAFZAK9Zt4l_Q8oMSp83QwyDYGsZGQRwbrY", use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(conv_handler)
dispatcher.add_handler(conversation_handler)
submission_pattern = re.compile(r'^disapprove_|^ripnature_|^papprove_|^wrongdisplay_|^tbasehigh_|^uselessteam_|^twronginfo_|^tapprove_|^ripivsevs_|^pbasehigh_|^pwronginfo_|^uselesspoke_|^notindemand_|')
dispatcher.add_handler(CommandHandler('next', next))
dispatcher.add_handler(CommandHandler('reset_next', reset_command))
dispatcher.add_handler(CommandHandler('buyers', buyer_command))
dispatcher.add_handler(CommandHandler('approve', approve_command))
dispatcher.add_handler(CommandHandler('sellers', sellers))
dispatcher.add_handler(CommandHandler('users', users))
dispatcher.add_handler(CommandHandler('current', current))
dispatcher.add_handler(CommandHandler('add_users', add_users))
dispatcher.add_handler(CommandHandler('profile', profile))
dispatcher.add_handler(CommandHandler('clear', clear))
dispatcher.add_handler(CallbackQueryHandler(category, pattern=submission_pattern))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_message))
# Start the bot
updater.start_polling()
updater.idle()
