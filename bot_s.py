from telethon import TelegramClient, events, Button
from telethon.tl.types import ReplyKeyboardMarkup, KeyboardButton
from telethon.tl.custom import Message
from config import api_id,api_hash,bot_token
import time
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

#from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
from pymongo import MongoClient
import asyncio
import random
import math
import requests
import json

# MongoDB setup
MONGODB_URL = "mongodb+srv://PokemonMasters:Sarvesh2369@cluster0.qzem0.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO = MongoClient(MONGODB_URL)
db = MONGO['Pokemon-Masters-DB']
col = db['users']

# MongoDB Connection
MONGODB_URL1 = "mongodb+srv://Nintendro:Database@cluster0.yr9jx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
MONGO1 = MongoClient(MONGODB_URL1)

# Select Database and Collection
db1 = MONGO1['database']  # Change 'database' to your actual database name
col1 = db1['move_data']
col2 = db1['pokemon_data']
col3 = db1['training_data']
col4 = db1['rem_pokemon_data']

level = 8

# Create the Telegram bot client
app = TelegramClient('wdvijhv', api_id, api_hash)

#user credentials
battle_state = {}
app.user_states={}
user_state_for_add={}
battle_state={}
battle_stadium={}
waiting_players=[]
#pokemon moves
poke_moves = ['10,000,000 Volt Thunderbolt', 'Absorb', 'Accelerock', 'Acid', 'Acid Armor', 'Acid Downpour', 'Acid Spray', 'Acrobatics', 'Acupressure', 'Aerial Ace', 'Aeroblast', 'After You', 'Agility', 'Air Cutter', 'Air Slash', 'All-Out Pummeling', 'Alluring Voice', 'Ally Switch', 'Amnesia', 'Anchor Shot', 'Ancient Power', 'Apple Acid', 'Aqua Cutter', 'Aqua Jet', 'Aqua Ring', 'Aqua Step', 'Aqua Tail', 'Arm Thrust', 'Armor Cannon', 'Aromatherapy', 'Aromatic Mist', 'Assist', 'Assurance', 'Astonish', 'Astral Barrage', 'Attack Order', 'Attract', 'Aura Sphere', 'Aura Wheel', 'Aurora Beam', 'Aurora Veil', 'Autotomize', 'Avalanche', 'Axe Kick', 'Baby-Doll Eyes', 'Baddy Bad', 'Baneful Bunker', 'Barb Barrage', 'Barrage', 'Barrier', 'Baton Pass', 'Beak Blast', 'Beat Up', 'Behemoth Bash', 'Behemoth Blade', 'Belch', 'Belly Drum', 'Bestow', 'Bide', 'Bind', 'Bite', 'Bitter Blade', 'Bitter Malice', 'Black Hole Eclipse', 'Blast Burn', 'Blaze Kick', 'Blazing Torque', 'Bleakwind Storm', 'Blizzard', 'Block', 'Blood Moon', 'Bloom Doom', 'Blue Flare', 'Body Press', 'Body Slam', 'Bolt Beak', 'Bolt Strike', 'Bone Club', 'Bone Rush', 'Bonemerang', 'Boomburst', 'Bounce', 'Bouncy Bubble', 'Branch Poke', 'Brave Bird', 'Breaking Swipe', 'Breakneck Blitz', 'Brick Break', 'Brine', 'Brutal Swing', 'Bubble', 'Bubble Beam', 'Bug Bite', 'Bug Buzz', 'Bulk Up', 'Bulldoze', 'Bullet Punch', 'Bullet Seed', 'Burn Up', 'Burning Bulwark', 'Burning Jealousy', 'Buzzy Buzz', 'Calm Mind', 'Camouflage', 'Captivate', 'Catastropika', 'Ceaseless Edge', 'Celebrate', 'Charge', 'Charge Beam', 'Charm', 'Chatter', 'Chilling Water', 'Chilly Reception', 'Chip Away', 'Chloroblast', 'Circle Throw', 'Clamp', 'Clanging Scales', 'Clangorous Soul', 'Clangorous Soulblaze', 'Clear Smog', 'Close Combat', 'Coaching', 'Coil', 'Collision Course', 'Combat Torque', 'Comet Punch', 'Comeuppance', 'Confide', 'Confuse Ray', 'Confusion', 'Constrict', 'Continental Crush', 'Conversion', 'Conversion 2', 'Copycat', 'Core Enforcer', 'Corkscrew Crash', 'Corrosive Gas', 'Cosmic Power', 'Cotton Guard', 'Cotton Spore', 'Counter', 'Court Change', 'Covet', 'Crabhammer', 'Crafty Shield', 'Cross Chop', 'Cross Poison', 'Crunch', 'Crush Claw', 'Crush Grip', 'Curse', 'Cut', 'Dark Pulse', 'Dark Void', 'Darkest Lariat', 'Dazzling Gleam', 'Decorate', 'Defend Order', 'Defense Curl', 'Defog', 'Destiny Bond', 'Detect', 'Devastating Drake', 'Diamond Storm', 'Dig', 'Dire Claw', 'Disable', 'Disarming Voice', 'Discharge', 'Dive', 'Dizzy Punch', 'Doodle', 'Doom Desire', 'Double Hit', 'Double Iron Bash', 'Double Kick', 'Double Shock', 'Double Slap', 'Double Team', 'Double-Edge', 'Draco Meteor', 'Dragon Ascent', 'Dragon Breath', 'Dragon Cheer', 'Dragon Claw', 'Dragon Dance', 'Dragon Darts', 'Dragon Energy', 'Dragon Hammer', 'Dragon Pulse', 'Dragon Rage', 'Dragon Rush', 'Dragon Tail', 'Drain Punch', 'Draining Kiss', 'Dream Eater', 'Drill Peck', 'Drill Run', 'Drum Beating', 'Dual Chop', 'Dual Wingbeat', 'Dynamax Cannon', 'Dynamic Punch', 'Earth Power', 'Earthquake', 'Echoed Voice', 'Eerie Impulse', 'Eerie Spell', 'Egg Bomb', 'Electric Terrain', 'Electrify', 'Electro Ball', 'Electro Drift', 'Electro Shot', 'Electroweb', 'Embargo', 'Ember', 'Encore', 'Endeavor', 'Endure', 'Energy Ball', 'Entrainment', 'Eruption', 'Esper Wing', 'Eternabeam', 'Expanding Force', 'Explosion', 'Extrasensory', 'Extreme Evoboost', 'Extreme Speed', 'Facade', 'Fairy Lock', 'Fairy Wind', 'Fake Out', 'Fake Tears', 'False Surrender', 'False Swipe', 'Feather Dance', 'Feint', 'Feint Attack', 'Fell Stinger', 'Fickle Beam', 'Fiery Dance', 'Fiery Wrath', 'Fillet Away', 'Final Gambit', 'Fire Blast', 'Fire Fang', 'Fire Lash', 'Fire Pledge', 'Fire Punch', 'Fire Spin', 'First Impression', 'Fishious Rend', 'Fissure', 'Flail', 'Flame Burst', 'Flame Charge', 'Flame Wheel', 'Flamethrower', 'Flare Blitz', 'Flash', 'Flash Cannon', 'Flatter', 'Fleur Cannon', 'Fling', 'Flip Turn', 'Floaty Fall', 'Floral Healing', 'Flower Shield', 'Flower Trick', 'Fly', 'Flying Press', 'Focus Blast', 'Focus Energy', 'Focus Punch', 'Follow Me', 'Force Palm', 'Foresight', "Forest's Curse", 'Foul Play','Freeze Shock', 'Freeze-Dry', 'Freezing Glare', 'Freezy Frost', 'Frenzy Plant', 'Frost Breath', 'Frustration', 'Fury Attack', 'Fury Cutter', 'Fury Swipes', 'Fusion Bolt', 'Fusion Flare', 'Future Sight', 'G-Max Befuddle', 'G-Max Cannonade', 'G-Max Centiferno', 'G-Max Chi Strike', 'G-Max Cuddle', 'G-Max Depletion', 'G-Max Drum Solo', 'G-Max Finale', 'G-Max Fireball', 'G-Max Foam Burst', 'G-Max Gold Rush', 'G-Max Gravitas', 'G-Max Hydrosnipe', 'G-Max Malodor', 'G-Max Meltdown', 'G-Max One Blow', 'G-Max Rapid Flow', 'G-Max Replenish', 'G-Max Resonance', 'G-Max Sandblast', 'G-Max Smite', 'G-Max Snooze', 'G-Max Steelsurge', 'G-Max Stonesurge', 'G-Max Stun Shock', 'G-Max Sweetness', 'G-Max Tartness', 'G-Max Terror', 'G-Max Vine Lash', 'G-Max Volcalith', 'G-Max Volt Crash', 'G-Max Wildfire', 'G-Max Wind Rage', 'Gastro Acid', 'Gear Grind', 'Gear Up', 'Genesis Supernova', 'Geomancy', 'Giga Drain', 'Giga Impact', 'Gigaton Hammer', 'Gigavolt Havoc', 'Glacial Lance', 'Glaciate', 'Glaive Rush', 'Glare', 'Glitzy Glow', 'Grass Knot', 'Grass Pledge', 'Grass Whistle', 'Grassy Glide', 'Grassy Terrain', 'Grav Apple', 'Gravity', 'Growl', 'Growth', 'Grudge', 'Guard Split', 'Guard Swap', 'Guardian of Alola', 'Guillotine', 'Gunk Shot', 'Gust', 'Gyro Ball', 'Hail', 'Hammer Arm', 'Happy Hour', 'Hard Press', 'Harden', 'Haze', 'Head Charge', 'Head Smash', 'Headbutt', 'Headlong Rush', 'Heal Bell', 'Heal Block', 'Heal Order', 'Heal Pulse', 'Healing Wish', 'Heart Stamp', 'Heart Swap', 'Heat Crash', 'Heat Wave', 'Heavy Slam', 'Helping Hand', 'Hex', 'Hidden Power', 'High Horsepower', 'High Jump Kick', 'Hold Back', 'Hold Hands', 'Hone Claws', 'Horn Attack', 'Horn Drill', 'Horn Leech', 'Howl', 'Hurricane', 'Hydro Cannon', 'Hydro Pump', 'Hydro Steam', 'Hydro Vortex', 'Hyper Beam', 'Hyper Drill', 'Hyper Fang', 'Hyper Voice', 'Hyperspace Fury', 'Hyperspace Hole', 'Hypnosis', 'Ice Ball', 'Ice Beam', 'Ice Burn', 'Ice Fang', 'Ice Hammer', 'Ice Punch', 'Ice Shard', 'Ice Spinner', 'Icicle Crash', 'Icicle Spear', 'Icy Wind', 'Imprison', 'Incinerate', 'Infernal Parade', 'Inferno', 'Inferno Overdrive', 'Infestation', 'Ingrain', 'Instruct', 'Ion Deluge', 'Iron Defense', 'Iron Head', 'Iron Tail', 'Ivy Cudgel', 'Jaw Lock', 'Jet Punch', 'Judgment', 'Jump Kick', 'Jungle Healing', 'Karate Chop', 'Kinesis', "King's Shield", 'Knock Off', 'Kowtow Cleave', "Land's Wrath", 'Laser Focus', 'Lash Out', 'Last Resort', 'Last Respects', 'Lava Plume', 'Leaf Blade', 'Leaf Storm', 'Leaf Tornado', 'Leafage', 'Leech Life', 'Leech Seed', 'Leer', "Let's Snuggle Forever", 'Lick', 'Life Dew', 'Light of Ruin', 'Light Screen', 'Light That Burns the Sky', 'Liquidation', 'Lock-On', 'Lovely Kiss', 'Low Kick', 'Low Sweep', 'Lucky Chant', 'Lumina Crash', 'Lunar Blessing', 'Lunar Dance', 'Lunge', 'Luster Purge', 'Mach Punch', 'Magic Coat', 'Magic Powder', 'Magic Room', 'Magical Leaf', 'Magical Torque', 'Magma Storm', 'Magnet Bomb', 'Magnet Rise', 'Magnetic Flux', 'Magnitude', 'Make It Rain', 'Malicious Moonsault', 'Malignant Chain', 'Mat Block', 'Matcha Gotcha', 'Max Airstream', 'Max Darkness', 'Max Flare', 'Max Flutterby', 'Max Geyser', 'Max Guard', 'Max Hailstorm', 'Max Knuckle', 'Max Lightning', 'Max Mindstorm', 'Max Ooze', 'Max Overgrowth', 'Max Phantasm', 'Max Quake', 'Max Rockfall', 'Max Starfall', 'Max Steelspike', 'Max Strike', 'Max Wyrmwind', 'Me First', 'Mean Look', 'Meditate', 'Mega Drain', 'Mega Kick', 'Mega Punch', 'Megahorn', 'Memento', 'Menacing Moonraze Maelstrom', 'Metal Burst', 'Metal Claw', 'Metal Sound', 'Meteor Assault', 'Meteor Beam', 'Meteor Mash', 'Metronome', 'Mighty Cleave', 'Milk Drink', 'Mimic', 'Mind Blown', 'Mind Reader', 'Minimize', 'Miracle Eye', 'Mirror Coat', 'Mirror Move', 'Mirror Shot', 'Mist', 'Mist Ball', 'Misty Explosion', 'Misty Terrain', 'Moonblast', 'Moongeist Beam', 'Moonlight', 'Morning Sun', 'Mortal Spin', 'Mountain Gale', 'Mud Bomb', 'Mud Shot', 'Mud Sport', 'Mud-Slap', 'Muddy Water', 'Multi-Attack', 'Mystical Fire', 'Mystical Power', 'Nasty Plot', 'Natural Gift', 'Nature Power', "Nature's Madness", 'Needle Arm', 'Never-Ending Nightmare', 'Night Daze','Night Shade', 'Night Slash', 'Nightmare', 'No Retreat', 'Noble Roar', 'Noxious Torque', 'Nuzzle', 'Oblivion Wing', 'Obstruct', 'Oceanic Operetta', 'Octazooka', 'Octolock', 'Odor Sleuth', 'Ominous Wind', 'Order Up', 'Origin Pulse', 'Outrage', 'Overdrive', 'Overheat', 'Pain Split', 'Parabolic Charge', 'Parting Shot', 'Pay Day', 'Payback', 'Peck', 'Perish Song', 'Petal Blizzard', 'Petal Dance', 'Phantom Force', 'Photon Geyser', 'Pika Papow', 'Pin Missile', 'Plasma Fists', 'Play Nice', 'Play Rough', 'Pluck', 'Poison Fang', 'Poison Gas', 'Poison Jab', 'Poison Powder', 'Poison Sting', 'Poison Tail', 'Pollen Puff', 'Poltergeist', 'Population Bomb', 'Pounce', 'Pound', 'Powder', 'Powder Snow', 'Power Gem', 'Power Shift', 'Power Split', 'Power Swap', 'Power Trick', 'Power Trip', 'Power Whip', 'Power-Up Punch', 'Precipice Blades', 'Present', 'Prismatic Laser', 'Protect', 'Psybeam', 'Psyblade', 'Psych Up', 'Psychic', 'Psychic Fangs', 'Psychic Noise', 'Psychic Terrain', 'Psycho Boost', 'Psycho Cut', 'Psycho Shift', 'Psyshield Bash', 'Psyshock', 'Psystrike', 'Psywave', 'Pulverizing Pancake', 'Punishment', 'Purify', 'Pursuit', 'Pyro Ball', 'Quash', 'Quick Attack', 'Quick Guard', 'Quiver Dance', 'Rage', 'Rage Fist', 'Rage Powder', 'Raging Bull', 'Raging Fury', 'Rain Dance', 'Rapid Spin', 'Razor Leaf', 'Razor Shell', 'Razor Wind', 'Recover', 'Recycle', 'Reflect', 'Reflect Type', 'Refresh', 'Relic Song', 'Rest', 'Retaliate', 'Return', 'Revelation Dance', 'Revenge', 'Reversal', 'Revival Blessing', 'Rising Voltage', 'Roar', 'Roar of Time', 'Rock Blast', 'Rock Climb', 'Rock Polish', 'Rock Slide', 'Rock Smash', 'Rock Throw', 'Rock Tomb', 'Rock Wrecker', 'Role Play', 'Rolling Kick', 'Rollout', 'Roost', 'Rototiller', 'Round', 'Ruination', 'Sacred Fire', 'Sacred Sword', 'Safeguard', 'Salt Cure', 'Sand Attack', 'Sand Tomb', 'Sandsear Storm', 'Sandstorm', 'Sappy Seed', 'Savage Spin-Out', 'Scald', 'Scale Shot', 'Scary Face', 'Scorching Sands', 'Scratch', 'Screech', 'Searing Shot', 'Searing Sunraze Smash', 'Secret Power', 'Secret Sword', 'Seed Bomb', 'Seed Flare', 'Seismic Toss', 'Self-Destruct', 'Shadow Ball', 'Shadow Bone', 'Shadow Claw', 'Shadow Force', 'Shadow Punch', 'Shadow Sneak', 'Sharpen', 'Shattered Psyche', 'Shed Tail', 'Sheer Cold', 'Shell Side Arm', 'Shell Smash', 'Shell Trap', 'Shelter', 'Shift Gear', 'Shock Wave', 'Shore Up', 'Signal Beam', 'Silk Trap', 'Silver Wind', 'Simple Beam', 'Sing', 'Sinister Arrow Raid', 'Sizzly Slide', 'Sketch', 'Skill Swap', 'Skitter Smack', 'Skull Bash', 'Sky Attack', 'Sky Drop', 'Sky Uppercut', 'Slack Off', 'Slam', 'Slash', 'Sleep Powder', 'Sleep Talk', 'Sludge', 'Sludge Bomb', 'Sludge Wave', 'Smack Down', 'Smart Strike', 'Smelling Salts', 'Smog', 'Smokescreen', 'Snap Trap', 'Snarl', 'Snatch', 'Snipe Shot', 'Snore', 'Snowscape', 'Soak', 'Soft-Boiled', 'Solar Beam', 'Solar Blade', 'Sonic Boom', 'Soul-Stealing 7-Star Strike', 'Spacial Rend', 'Spark', 'Sparkling Aria', 'Sparkly Swirl', 'Spectral Thief', 'Speed Swap', 'Spicy Extract', 'Spider Web', 'Spike Cannon', 'Spikes', 'Spiky Shield', 'Spin Out', 'Spirit Break', 'Spirit Shackle', 'Spit Up', 'Spite', 'Splash', 'Splintered Stormshards', 'Splishy Splash', 'Spore', 'Spotlight', 'Springtide Storm', 'Stealth Rock', 'Steam Eruption', 'Steamroller', 'Steel Beam', 'Steel Roller', 'Steel Wing', 'Sticky Web', 'Stockpile', 'Stoked Sparksurfer', 'Stomp', 'Stomping Tantrum', 'Stone Axe', 'Stone Edge', 'Stored Power', 'Storm Throw', 'Strange Steam', 'Strength', 'Strength Sap', 'String Shot', 'Struggle', 'Struggle Bug', 'Stuff Cheeks', 'Stun Spore', 'Submission', 'Substitute', 'Subzero Slammer', 'Sucker Punch', 'Sunny Day', 'Sunsteel Strike', 'Super Fang', 'Supercell Slam', 'Superpower', 'Supersonic', 'Supersonic Skystrike', 'Surf', 'Surging Strikes', 'Swagger', 'Swallow', 'Sweet Kiss', 'Sweet Scent', 'Swift', 'Switcheroo', 'Swords Dance', 'Synchronoise', 'Synthesis', 'Syrup Bomb', 'Tachyon Cutter', 'Tackle', 'Tail Glow', 'Tail Slap', 'Tail Whip', 'Tailwind', 'Take Down', 'Take Heart', 'Tar Shot', 'Taunt', 'Tearful Look', 'Teatime', 'Techno Blast', 'Tectonic Rage','Teeter Dance', 'Telekinesis', 'Teleport', 'Temper Flare', 'Tera Blast', 'Tera Starstorm', 'Terrain Pulse', 'Thief', 'Thousand Arrows', 'Thousand Waves', 'Thrash', 'Throat Chop', 'Thunder', 'Thunder Cage', 'Thunder Fang', 'Thunder Punch', 'Thunder Shock', 'Thunder Wave', 'Thunderbolt', 'Thunderclap', 'Thunderous Kick', 'Tickle', 'Tidy Up', 'Topsy-Turvy', 'Torch Song', 'Torment', 'Toxic', 'Toxic Spikes', 'Toxic Thread', 'Trailblaze', 'Transform', 'Tri Attack', 'Trick', 'Trick Room', 'Trick-or-Treat', 'Triple Arrows', 'Triple Axel', 'Triple Dive', 'Triple Kick', 'Trop Kick', 'Trump Card', 'Twin Beam', 'Twineedle', 'Twinkle Tackle', 'Twister', 'U-turn', 'Upper Hand', 'Uproar', 'V-create', 'Vacuum Wave', 'Veevee Volley', 'Venom Drench', 'Venoshock', 'Victory Dance', 'Vine Whip', 'Vise Grip', 'Vital Throw', 'Volt Switch', 'Volt Tackle', 'Wake-Up Slap', 'Water Gun', 'Water Pledge', 'Water Pulse', 'Water Shuriken', 'Water Sport', 'Water Spout', 'Waterfall', 'Wave Crash', 'Weather Ball', 'Whirlpool', 'Whirlwind', 'Wicked Blow', 'Wicked Torque', 'Wide Guard', 'Wild Charge', 'Wildbolt Storm', 'Will-O-Wisp', 'Wing Attack', 'Wish', 'Withdraw', 'Wonder Room', 'Wood Hammer', 'Work Up', 'Worry Seed', 'Wrap', 'Wring Out', 'X-Scissor', 'Yawn', 'Zap Cannon', 'Zen Headbutt', 'Zing Zap', 'Zippy Zap']
spawn = {"locations":{"kanto":{"pallet_town":{},"route_1":{"rattata":{"level":"3-4","spawn_rate":30},"oddish":{"level":"3-4","spawn_rate":30},"pidgey":{"level":"3-4","spawn_rate":40},"bellsprout":{"level":"3-4","spawn_rate":30},"dragonite":{"level":"3-56","spawn_rate":30},"charizard":{"level":"3-15","spawn_rate":30},"moltres":{"level":"3-56","spawn_rate":30},"articuno":{"level":"3-56","spawn_rate":30},"zapdos":{"level":"3-56","spawn_rate":30}}}}}
user_bag_index = {}
pokemon = ["Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran♀", "Nidorina", "Nidoqueen", "Nidoran♂", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales", "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetch’d", "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan", "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon", "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew"]


def test_mongo_connection():
    try:
        # Perform a test query to check if the connection is established
        db.command("ping")
        print("MongoDB connection successful!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
current_indices = {}

type_chart = {
    "normal": {"strengths": [], "weaknesses": ["rock", "steel"], "no_effect": ["ghost"]},
    "fire": {"strengths": ["grass", "ice", "bug", "steel"], "weaknesses": ["fire", "water", "rock", "dragon"], "no_effect": []},
    "water": {"strengths": ["fire", "ground", "rock"], "weaknesses": ["water", "grass", "dragon"], "no_effect": []},
    "grass": {"strengths": ["water", "ground", "rock"], "weaknesses": ["fire", "grass", "poison", "flying", "bug", "dragon", "steel"], "no_effect": []},
    "electric": {"strengths": ["water", "flying"], "weaknesses": ["electric", "grass", "dragon"], "no_effect": ["ground"]},
    "ice": {"strengths": ["grass", "ground", "flying", "dragon"], "weaknesses": ["fire", "water", "ice", "steel"], "no_effect": []},
    "fighting": {"strengths": ["normal", "ice", "rock", "dark", "steel"], "weaknesses": ["poison", "flying", "psychic", "bug", "fairy"], "no_effect": ["ghost"]},
    "poison": {"strengths": ["grass", "fairy"], "weaknesses": ["poison", "rock", "ground", "ghost"], "no_effect": ["steel"]},
    "ground": {"strengths": ["fire", "electric", "poison", "rock", "steel"], "weaknesses": ["grass", "flying", "bug"], "no_effect": []},
    "flying": {"strengths": ["grass", "fighting", "bug"], "weaknesses": ["electric", "rock", "steel"], "no_effect": []},
    "psychic": {"strengths": ["fighting", "poison"], "weaknesses": ["psychic", "steel"], "no_effect": ["dark"]},
    "bug": {"strengths": ["grass", "psychic", "dark"], "weaknesses": ["fire", "fighting", "poison", "flying", "ghost", "steel", "fairy"], "no_effect": []},
    "rock": {"strengths": ["fire", "ice", "flying", "bug"], "weaknesses": ["fighting", "ground", "steel"], "no_effect": []},
    "ghost": {"strengths": ["psychic", "ghost"], "weaknesses": ["dark", "steel"], "no_effect": ["normal"]},
    "dragon": {"strengths": ["dragon"], "weaknesses": ["steel"], "no_effect": ["fairy"]},
    "dark": {"strengths": ["psychic", "ghost"], "weaknesses": ["fighting", "dark", "fairy"], "no_effect": []},
    "steel": {"strengths": ["ice", "rock", "fairy"], "weaknesses": ["fire", "water", "electric", "steel"], "no_effect": []},
    "fairy": {"strengths": ["fighting", "dragon", "dark"], "weaknesses": ["fire", "poison", "steel"], "no_effect": []}
}
async def users(): return[6735548827,5611071586,7503471575,7730460768,1017904439,7946913230,6632519077,1947921832,6669536790,6498879186,7048431897]


#source file_ids
error_image="AgACAgUAAxkBAAIHomeDfoCnF7o3a5k54vHc28acgGLzAAJEwjEbQoaZV4i1LLdR5I66AAgBAAMCAAN4AAceBA"
logo_image="AgACAgUAAxkBAAIH7meEo3fG_pW71jBgpKlTp2s40pEtAAJvwDEb3FFAVzsPv5vliMtPAAgBAAMCAAN4AAceBA"
connect_image="AgACAgUAAxkBAAIIG2eE4bAhOYOZawIEfjoKxfpa47LMAAJrvTEb9LspVBRHlvhLuwfcAAgBAAMCAAN5AAceBA"
version_image="AgACAgUAAxkBAAIKG2eKRXczSDoE-GYIioMVM4x8YwvvAAKqvzEbVAvAVyGmRLTy0pGgAAgBAAMCAAN5AAceBA"
pending_video="BAACAgUAAxkBAAIKeWeLtXUFriwGv5cGqZtKcRw9-ulEAAJSEAACFiDIV6q6kmrlvE3bHgQ"
wifi_1 = "AgACAgUAAxkBAAIsP2fZb56iKDQI3FTQVOo4cc5hC2fOAAJbyjEbn4i5Vveaeo07eVXSAAgBAAMCAAN5AAceBA"
wifi_2="AgACAgUAAxkBAAIsSWfawOdC57NnoCAu8ZV6GOyFtCpwAAIexTEbn4jBVrlKczlSS69lAAgBAAMCAAN5AAceBA"
wifi_3="AgACAgUAAxkBAAIsS2fawQ1YHhYpU4sR5-_xD923a7_5AAIhxTEbn4jBVv9SCq2zn4TrAAgBAAMCAAN5AAceBA"
menu1 = "AgACAgUAAxkBAAIsRWfawJQELg9UWikqXkhXq6NP5AjRAAJfwzEbKPDRVskooBWLDHOvAAgBAAMCAAN5AAceBA"
menu2 = "AgACAgUAAxkBAAIsR2fawLKXaxhzhAUsXq0195oVbiwTAAKTwzEbKPDRVokISb0zSS_XAAgBAAMCAAN5AAceBA"

#Media files
boy_white="AgACAgUAAxkBAAIJ0WeI4nOrtEP5AzO4Evu_p0o5NkE1AAIhzjEbmE55VwSzkNv2eUTWAAgBAAMCAAN5AAceBA"
boy_white_hair="AgACAgUAAxkBAAIJ0meI4nNZvf_WPBxPnsrwXskpoRCTAAIizjEbmE55V1YkqkyGGJdPAAgBAAMCAAN5AAceBA"
boy_light_black="AgACAgUAAxkBAAIJ02eI4nOyb2EQ-jRrviGUci8kV9hkAAIjzjEbmE55V5USnz75OTRcAAgBAAMCAAN5AAceBA"
boy_dark="AgACAgUAAxkBAAIJ1GeI4nN7ucx9AlD1oEjAg4rEGMbIAAIkzjEbmE55V4Q1zWjcBU5NAAgBAAMCAAN5AAceBA"
girl_white="AgACAgUAAxkBAAIJ1WeI4nMtO82NDQ05_ppHveFIlVU0AAInzjEbmE55VzOsDsm5du46AAgBAAMCAAN5AAceBA"
girl_white_hair="AgACAgUAAxkBAAIJ1meI4nNKpnjoewFdy8joIPMrx95lAAIqzjEbmE55V5Sms1pkGTtgAAgBAAMCAAN5AAceBA"
girl_light_black="AgACAgUAAxkBAAIJ12eI4nPnEwtSi5Qc1EjaM8axAQ20AAIuzjEbmE55V4z4sZ8rPHukAAgBAAMCAAN5AAceBA"
girl_dark="AgACAgUAAxkBAAIJ2GeI4nOvbUbg30MywSaUcuJe_7XFAAIvzjEbmE55VzGbscFYZ621AAgBAAMCAAN5AAceBA"

characters = [
    {"name": "boy_white", "url": "AgACAgUAAxkBAAIJ0WeI4nOrtEP5AzO4Evu_p0o5NkE1AAIhzjEbmE55VwSzkNv2eUTWAAgBAAMCAAN5AAceBA"},
    {"name": "boy_white_hair", "url": "AgACAgUAAxkBAAIJ0meI4nNZvf_WPBxPnsrwXskpoRCTAAIizjEbmE55V1YkqkyGGJdPAAgBAAMCAAN5AAceBA"},
    {"name": "boy_light_black", "url": "AgACAgUAAxkBAAIJ02eI4nOyb2EQ-jRrviGUci8kV9hkAAIjzjEbmE55V5USnz75OTRcAAgBAAMCAAN5AAceBA"},
    {"name": "boy_dark", "url": "AgACAgUAAxkBAAIJ1GeI4nN7ucx9AlD1oEjAg4rEGMbIAAIkzjEbmE55V4Q1zWjcBU5NAAgBAAMCAAN5AAceBA"},
    {"name": "girl_white", "url": "AgACAgUAAxkBAAIJ1WeI4nMtO82NDQ05_ppHveFIlVU0AAInzjEbmE55VzOsDsm5du46AAgBAAMCAAN5AAceBA"},
    {"name": "girl_white_hair", "url": "AgACAgUAAxkBAAIJ1meI4nNKpnjoewFdy8joIPMrx95lAAIqzjEbmE55V5Sms1pkGTtgAAgBAAMCAAN5AAceBA"},
    {"name": "girl_light_black", "url": "AgACAgUAAxkBAAIJ12eI4nPnEwtSi5Qc1EjaM8axAQ20AAIuzjEbmE55V4z4sZ8rPHukAAgBAAMCAAN5AAceBA"},
    {"name": "girl_dark", "url": "AgACAgUAAxkBAAIJ2GeI4nOvbUbg30MywSaUcuJe_7XFAAIvzjEbmE55VzGbscFYZ621AAgBAAMCAAN5AAceBA"},
]

PRIVATE_GROUP_ID = -1002388846235 # Example: Private group ID
VIDEO_MESSAGE_ID = 1571

current_spawn = {}

# Start time
StartTime = time.time()

# Command prefixes
prefix = [".", "!", "?", "*", "$", "#", "/"]




def get_pokemon_data(user_data,i):
    try:
        
        party_data = user_data.get("party", {}).get(str(i)) 
        if not party_data:
            print("No pokemon data found in party!")
            return None
        
        pokemon_id_to_find = party_data.get("id")
        if not pokemon_id_to_find:
             print("No pokemon_id in party object!")
             return None
        
        pokemon_data_object = user_data.get("Pokemon", {}) 
        
        for pokemon_name, pokemon_data in pokemon_data_object.items(): 
           if pokemon_data.get("pokemon_id") == pokemon_id_to_find:
                return pokemon_data
            
        print(f"Partner pokemon with ID '{pokemon_id_to_find}' not found in pokemon data.")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON Data")
        return None
    
def fetch_data():
    response = requests.get("https://nintendrolocationapi.onrender.com/locations")
    return response.json()

async def get_spawn(location):
    pokemon_data = spawn["locations"]["kanto"].get(location, {})

    if not pokemon_data:
        return None

    total_spawn_rate = sum(pokemon["spawn_rate"] for pokemon in pokemon_data.values())
    rand = random.randint(1, total_spawn_rate)

    cumulative_rate = 0
    for pokemon, info in pokemon_data.items():
        cumulative_rate += info["spawn_rate"]
        if rand <= cumulative_rate:
            min_level, max_level = map(int, info["level"].split("-"))
            level = random.randint(min_level, max_level)
            return {
                "name": pokemon.capitalize(),
                "level": level,
            }

    return None


class PartnerPokemon:
    def __init__(self, pokemon_name, level):
        self.pokemon_name = pokemon_name
        self.level = level
        self.data = self._fetch_data()

    def _fetch_data(self):
        """ Fetch Pokémon data from MongoDB """
        pokemon_data = col4.find_one({"Basic_Info.Name": self.pokemon_name})
        if pokemon_data:
            print("found!")
            return pokemon_data
        else:
            print(f"⚠️ Pokémon '{self.pokemon_name}' not found in database.")
            return {}
    

    def get_name(self):
        return self.data.get("Basic_Info", {}).get("Name", "Unknown")
    def get_id(self):
        return self.data.get("Basic_Info",{}).get("National_Id", "Unknown")
    def get_type(self):
        return self.data.get("Basic_Info",{}).get("Type", "Unknown")
    def get_abilitites(self):
        return self.data.get("Basic_Info",{}).get("Ability",{})
    def generate_pokemon_id(self):
        timestamp = int(time.time())  # Current timestamp in seconds
        random_number = random.randint(1000, 9999)  # Random number for added uniqueness
        unique_id = f"POKEMON_{timestamp}_{random_number}"
        return unique_id
    def get_category(self):
        return self.data.get("Basic_Info",{}).get("Category", "Unknown")
    def get_description(self):
        return self.data.get("Basic_Info",{}).get("Description", "Unknown")
    def get_nature(self):
        natures = ["Adamant", "Bashful", "Bold", "Brave", "Calm", "Careful", "Docile", "Gentle", "Hardy", 
                   "Hasty", "Impish", "Jolly", "Lax", "Lonely", "Mild", "Modest", "Naughty", "Quiet", 
                   "Quirky", "Rash", "Relaxed", "Sassy", "Serious", "Timid"]
        v = random.choice(natures)
        global nature
        nature = v
        return nature
    def get_level(self):
        return self.level
    def get_ivs(self):
        x=[26,27,28,29,30,31]
        ivs={
            "hp":random.choice  (x),
            "atk":random.choice(x),
            "def":random.choice(x),
            "spa":random.choice(x),
            "spd":random.choice(x),
            "spe":random.choice(x),
        }
        global hp_iv,atk_iv,def_iv,spa_iv,spd_iv,spe_iv 
        hp_iv,atk_iv,def_iv,spa_iv,spd_iv,spe_iv = ivs["hp"],ivs["atk"],ivs["def"],ivs["spa"],ivs["spd"],ivs["spe"]
        return ivs
    def get_evs(self):
        evs={
            "hp":0,
            "atk":0,
            "def":0,
            "spa":0,
            "spd":0,
            "spe":0,
        }
        global hp_ev,atk_ev,def_ev,spa_ev,spd_ev,spe_ev 
        hp_ev,atk_ev,def_ev,spa_ev,spd_ev,spe_ev = evs["hp"],evs["atk"],evs["def"],evs["spa"],evs["spd"],evs["spe"]
        return evs
    def get_moves(self):
        level = self.level
        moves = self.data.get("Moves",{}).get("Level_up_Moves", [])
        x=[
            move for move in moves
            if move.get("level") is not None and int(move["level"]) < level
        ]
        y=x[-4:]
        return y
    def get_stats(self):
        hp_base_stat = self.data.get("Base_Stats",{}).get("Hp","unknown")
        atk_base_stat = self.data.get("Base_Stats",{}).get("Attack","unknown")
        def_base_stat = self.data.get("Base_Stats",{}).get("Defence","unknown")
        spa_base_stat = self.data.get("Base_Stats",{}).get("Sp.Attack","unknown")
        spd_base_stat = self.data.get("Base_Stats",{}).get("Sp.Defence","unknown")
        spe_base_stat = self.data.get("Base_Stats",{}).get("Speed","unknown")
        hp_base_stat = int(hp_base_stat)
        atk_base_stat = int(atk_base_stat)
        def_base_stat = int(def_base_stat)
        spa_base_stat = int(spa_base_stat)
        spd_base_stat = int(spd_base_stat)
        spe_base_stat = int(spe_base_stat)
        level = self.level
        
        hp_stat = math.floor((((2*hp_base_stat+hp_iv+(hp_ev//4) +100) / 100)*level)+10)
        atk_stat = math.floor((((2*atk_base_stat+atk_iv+(atk_ev//4))/100)*level)+5)
        def_stat = math.floor((((2*def_base_stat+def_iv+(def_ev//4))/100)*level)+5)
        spa_stat = math.floor((((2*spa_base_stat+spa_iv+(spa_ev//4))/100)*level)+5)
        spd_stat = math.floor((((2*spd_base_stat+spd_iv+(spd_ev//4))/100)*level)+5)
        spe_stat = math.floor((((2*spe_base_stat+spe_iv+(spe_ev//4))/100)*level)+5)

        nature_modifier={"Adamant":{"hp":1,"atk":1.1,"def":1,"spa":0.9,"spd":1,"spe":1},"Bashful":{"hp":1,"atk":1,"def":1,"spa":1,"spd":1,"spe":1},"Bold":{"hp":1,"atk":0.9,"def":1.1,"spa":1,"spd":1,"spe":1},"Hardy":{"hp":1,"atk":1,"def":1,"spa":1,"spd":1,"spe":1},"Lonely":{"hp":1,"atk":1.1,"def":0.9,"spa":1,"spd":1,"spe":1},"Naughty":{"hp":1,"atk":1,"def":1,"spa":0.9,"spd":1,"spe":1},"Docile":{"hp":1,"atk":1,"def":1,"spa":1,"spd":1,"spe":1},"Hardy":{"hp":1,"atk":1,"def":1.1,"spa":1,"spd":1,"spe":0.9},"Impish":{"hp":1,"atk":1,"def":1.1,"spa":0.9,"spd":1,"spe":1},"Lax":{"hp":1,"atk":1,"def":1.1,"spa":1,"spd":0.9,"spe":1},"Timid":{"hp":1,"atk":0.9,"def":1,"spa":1,"spd":1,"spe":1.1},"Hasty":{"hp":1,"atk":1,"def":0.9,"spa":1,"spd":1,"spe":1.1},"Serious":{"hp":1,"atk":1,"def":1,"spa":1,"spd":1,"spe":1},"Jolly":{"hp":1,"atk":1,"def":1,"spa":0.9,"spd":1,"spe":1.1},"Naive":{"hp":1,"atk":1,"def":1,"spa":1,"spd":0.9,"spe":1.1},"Modest":{"hp":1,"atk":0.9,"def":1,"spa":1.1,"spd":1,"spe":1},"Mild":{"hp":1,"atk":1,"def":0.9,"spa":1.1,"spd":1,"spe":1},"Quiet":{"hp":1,"atk":1,"def":1,"spa":1.1,"spd":1,"spe":0.9},"Rash":{"hp":1,"atk":1,"def":1,"spa":1.1,"spd":0.9,"spe":1},"Calm":{"hp":1,"atk":0.9,"def":1,"spa":1,"spd":1.1,"spe":1},"Hardy":{"hp":1,"atk":1,"def":0.9,"spa":1,"spd":1.1,"spe":1},"Sassy":{"hp":1,"atk":1,"def":1,"spa":1,"spd":1.1,"spe":0.9},"Careful":{"hp":1,"atk":1,"def":1,"spa":0.9,"spd":1.1,"spe":1},"Quirky":{"hp":1,"atk":1,"def":1,"spa":1,"spd":1,"spe":1}}
        hp_modifier = nature_modifier.get(nature,{}).get("hp","")
        atk_modifier = nature_modifier.get(nature,{}).get("atk","")
        def_modifier = nature_modifier.get(nature,{}).get("def","")
        spa_modifier = nature_modifier.get(nature,{}).get("spa","")
        spd_modifier = nature_modifier.get(nature,{}).get("spd","")
        spe_modifier = nature_modifier.get(nature,{}).get("spe","")
        print(hp_stat,atk_stat,def_stat,spa_stat,spd_stat,spe_stat)
        hp_stat = math.floor(hp_stat*hp_modifier)
        atk_stat = math.floor(atk_stat*atk_modifier)
        def_stat = math.floor(def_stat*def_modifier)
        spa_stat = math.floor(spa_stat*spa_modifier)
        spd_stat = math.floor(spd_stat*spd_modifier)
        spe_stat = math.floor(spe_stat*spe_modifier)
        print(hp_stat,atk_stat,def_stat,spa_stat,spd_stat,spe_stat)

        stats = {
            "hp":hp_stat,
            "atk":atk_stat,
            "def":def_stat,
            "spa":spa_stat,
            "spd":spd_stat,
            "spe":spe_stat,
        }
        return stats
    
class Pokemon:
    def __init__(self, pokemon_name, level):
        self.pokemon_name = pokemon_name
        self.level = level
        self.data = self._fetch_data()

    def _fetch_data(self):
        """ Fetch Pokémon data from MongoDB """
        pokemon_data = col2.find_one({"Basic_Info.Name": self.pokemon_name})
        if pokemon_data:
            print("found!")
            return pokemon_data
        else:
            print(f"⚠️ Pokémon '{self.pokemon_name}' not found in database.")
            return {}
    

    def get_name(self):
        return self.data.get("Basic_Info", {}).get("Name", "Unknown")
    def get_id(self):
        return self.data.get("Basic_Info",{}).get("National_Id", "Unknown")
    def get_type(self):
        return self.data.get("Basic_Info",{}).get("Type", "Unknown")
    def get_abilitites(self):
        return self.data.get("Basic_Info",{}).get("Ability",{})
    def generate_pokemon_id(self):
        timestamp = int(time.time())  # Current timestamp in seconds
        random_number = random.randint(1000, 9999)  # Random number for added uniqueness
        unique_id = f"POKEMON_{timestamp}_{random_number}"
        return unique_id
    def get_category(self):
        return self.data.get("Basic_Info",{}).get("Category", "Unknown")
    def get_description(self):
        return self.data.get("Basic_Info",{}).get("Description", "Unknown")
    def get_nature(self):
        natures = ["Adamant", "Bashful", "Bold", "Brave", "Calm", "Careful", "Docile", "Gentle", "Hardy", 
                   "Hasty", "Impish", "Jolly", "Lax", "Lonely", "Mild", "Modest", "Naughty", "Quiet", 
                   "Quirky", "Rash", "Relaxed", "Sassy", "Serious", "Timid"]
        v = random.choice(natures)
        global nature
        nature = v
        return nature
    def get_level(self):
        return self.level
    def get_ivs(self):
        x=[26,27,28,29,30,31]
        ivs={
            "hp":random.choice  (x),
            "atk":random.choice(x),
            "def":random.choice(x),
            "spa":random.choice(x),
            "spd":random.choice(x),
            "spe":random.choice(x),
        }
        global hp_iv,atk_iv,def_iv,spa_iv,spd_iv,spe_iv 
        hp_iv,atk_iv,def_iv,spa_iv,spd_iv,spe_iv = ivs["hp"],ivs["atk"],ivs["def"],ivs["spa"],ivs["spd"],ivs["spe"]
        return ivs
    def get_evs(self):
        evs={
            "hp":0,
            "atk":0,
            "def":0,
            "spa":0,
            "spd":0,
            "spe":0,
        }
        global hp_ev,atk_ev,def_ev,spa_ev,spd_ev,spe_ev 
        hp_ev,atk_ev,def_ev,spa_ev,spd_ev,spe_ev = evs["hp"],evs["atk"],evs["def"],evs["spa"],evs["spd"],evs["spe"]
        return evs
    def get_moves(self):
        level = self.level
        moves = self.data.get("Moves",{}).get("Level_up_Moves", [])
        x=[
            move for move in moves
            if move.get("level") is not None and int(move["level"]) < level
        ]
        y=x[-4:]
        return y
    def get_stats(self):
        hp_base_stat = self.data.get("Base_Stats",{}).get("Hp","unknown")
        atk_base_stat = self.data.get("Base_Stats",{}).get("Attack","unknown")
        def_base_stat = self.data.get("Base_Stats",{}).get("Defence","unknown")
        spa_base_stat = self.data.get("Base_Stats",{}).get("Sp.Attack","unknown")
        spd_base_stat = self.data.get("Base_Stats",{}).get("Sp.Defence","unknown")
        spe_base_stat = self.data.get("Base_Stats",{}).get("Speed","unknown")
        hp_base_stat = int(hp_base_stat)
        atk_base_stat = int(atk_base_stat)
        def_base_stat = int(def_base_stat)
        spa_base_stat = int(spa_base_stat)
        spd_base_stat = int(spd_base_stat)
        spe_base_stat = int(spe_base_stat)
        level = self.level
        
        hp_stat = math.floor(int((((2*hp_base_stat+hp_iv+(hp_ev//4) +100) / 100)*level)+10))
        atk_stat = math.floor((((2*atk_base_stat+atk_iv+(atk_ev//4))/100)*level)+5)
        def_stat = math.floor((((2*def_base_stat+def_iv+(def_ev//4))/100)*level)+5)
        spa_stat = math.floor((((2*spa_base_stat+spa_iv+(spa_ev//4))/100)*level)+5)
        spd_stat = math.floor((((2*spd_base_stat+spd_iv+(spd_ev//4))/100)*level)+5)
        spe_stat = math.floor((((2*spe_base_stat+spe_iv+(spe_ev//4))/100)*level)+5)

        nature_modifier={"Adamant":{"hp":1,"atk":1.1,"def":1,"spa":0.9,"spd":1,"spe":1},"Bashful":{"hp":1,"atk":1,"def":1,"spa":1,"spd":1,"spe":1},"Bold":{"hp":1,"atk":0.9,"def":1.1,"spa":1,"spd":1,"spe":1},"Hardy":{"hp":1,"atk":1,"def":1,"spa":1,"spd":1,"spe":1},"Lonely":{"hp":1,"atk":1.1,"def":0.9,"spa":1,"spd":1,"spe":1},"Naughty":{"hp":1,"atk":1,"def":1,"spa":0.9,"spd":1,"spe":1},"Docile":{"hp":1,"atk":1,"def":1,"spa":1,"spd":1,"spe":1},"Hardy":{"hp":1,"atk":1,"def":1.1,"spa":1,"spd":1,"spe":0.9},"Impish":{"hp":1,"atk":1,"def":1.1,"spa":0.9,"spd":1,"spe":1},"Lax":{"hp":1,"atk":1,"def":1.1,"spa":1,"spd":0.9,"spe":1},"Timid":{"hp":1,"atk":0.9,"def":1,"spa":1,"spd":1,"spe":1.1},"Hasty":{"hp":1,"atk":1,"def":0.9,"spa":1,"spd":1,"spe":1.1},"Serious":{"hp":1,"atk":1,"def":1,"spa":1,"spd":1,"spe":1},"Jolly":{"hp":1,"atk":1,"def":1,"spa":0.9,"spd":1,"spe":1.1},"Naive":{"hp":1,"atk":1,"def":1,"spa":1,"spd":0.9,"spe":1.1},"Modest":{"hp":1,"atk":0.9,"def":1,"spa":1.1,"spd":1,"spe":1},"Mild":{"hp":1,"atk":1,"def":0.9,"spa":1.1,"spd":1,"spe":1},"Quiet":{"hp":1,"atk":1,"def":1,"spa":1.1,"spd":1,"spe":0.9},"Rash":{"hp":1,"atk":1,"def":1,"spa":1.1,"spd":0.9,"spe":1},"Calm":{"hp":1,"atk":0.9,"def":1,"spa":1,"spd":1.1,"spe":1},"Hardy":{"hp":1,"atk":1,"def":0.9,"spa":1,"spd":1.1,"spe":1},"Sassy":{"hp":1,"atk":1,"def":1,"spa":1,"spd":1.1,"spe":0.9},"Careful":{"hp":1,"atk":1,"def":1,"spa":0.9,"spd":1.1,"spe":1},"Quirky":{"hp":1,"atk":1,"def":1,"spa":1,"spd":1,"spe":1}}
        hp_modifier = int(nature_modifier.get(nature,{}).get("hp",""))
        atk_modifier = nature_modifier.get(nature,{}).get("atk","")
        def_modifier = nature_modifier.get(nature,{}).get("def","")
        spa_modifier = nature_modifier.get(nature,{}).get("spa","")
        spd_modifier = nature_modifier.get(nature,{}).get("spd","")
        spe_modifier = nature_modifier.get(nature,{}).get("spe","")
        print(hp_stat,atk_stat,def_stat,spa_stat,spd_stat,spe_stat)
        hp_stat = math.floor(hp_stat*hp_modifier)
        print(type(hp_stat))
        atk_stat = math.floor(atk_stat*atk_modifier)
        def_stat = math.floor(def_stat*def_modifier)
        spa_stat = math.floor(spa_stat*spa_modifier)
        spd_stat = math.floor(spd_stat*spd_modifier)
        spe_stat = math.floor(spe_stat*spe_modifier)
        print(hp_stat,atk_stat,def_stat,spa_stat,spd_stat,spe_stat)

        stats = {
            "hp":hp_stat,
            "atk":atk_stat,
            "def":def_stat,
            "spa":spa_stat,
            "spd":spd_stat,
            "spe":spe_stat,
        }
        return stats

# Function to get readable time
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

# Command handler: /ping
@app.on(events.NewMessage(pattern="/ping"))
async def ping(event):
    user_list=await users()
    user_id=event.sender_id
    if user_id in user_list:
      start_time = time.time()
      end_time = time.time()
      ping_time = round((end_time - start_time) * 1000, 3)
      uptime = get_readable_time(int(time.time() - StartTime))
      await event.reply(f"Pong⋙ {ping_time}ms\nBot Is Online Since⋙ {uptime}")
    else:
      await event.reply("__**You are not an authorised user**__")

# Command handler: /start
@app.on(events.NewMessage(pattern="/start"))
async def start(event):
  
  await event.reply("__**Welcome to the bot\nNothing here to mention**__")


# Command handler: /register
@app.on(events.NewMessage(pattern="/register"))
#group
async def log_in(event):
   user_list = await users()
   user_id = event.sender_id
   if user_id in user_list:
      if event.is_group:
         await app.send_file(event.chat.id,file=error_image,caption="__**Try the operation again in private!**__",buttons=[
            [Button.url("Log In", "https://t.me/Pokemon_Masters_Game_Bot?start=start_chat")]
         ])
      elif event.is_private:
        
        check_whether_existing_user = col.find_one({"user_id": user_id},{"Registration": 1})

        if check_whether_existing_user and "Registration" in check_whether_existing_user:
            print(f"User found in database: {check_whether_existing_user}")  # Log DB result
            await event.reply("__**You are already registered!**__")
        else:
            raw_user = {
                "user_id": user_id
            }
                # Inserting the user data into the database
            col.insert_one(raw_user)
            print("User not found in database, added user")  # Log DB result
            x=await app.send_message(event.chat.id,"__**Your Raw Data has been created in the database!**__")
            await x.delete()
            x1=await app.send_file(event.chat.id,file=logo_image,caption="__**Preparing to start game**__")
            await asyncio.sleep(1.5)
            x2=await x1.edit("__**Getting Started**__")
            await asyncio.sleep(1.5)
            x3=await x2.edit("__**Getting things ready**__")
            await asyncio.sleep(1.5)
            x4=await x3.edit("__**Getting things ready just for you**__")
            await asyncio.sleep(1.5)
            x5=await x4.edit("__**Just sit back and relax everything will be done automatically\nJust for you**__")
            await asyncio.sleep(1.5)
            x6=await x5.edit("__**Retrieving necessary user data from the database**__")
            await asyncio.sleep(1.5)
            x7=await x6.edit("__**Requesting permission for creation of new user data to the server**__")
            await asyncio.sleep(1.5)
            x8=await x7.edit("__**Access approved , waiting for response from the server**__")
            await asyncio.sleep(1.5)
            x9=await x8.edit("__**Searching for your raw data in the database**__") 
            await asyncio.sleep(1.5)
            x10=await x9.edit("__**Please hold on while we are collecting new user creation credentials data from the server\nNote: This might take from few seconds to a minute or two! **__")
            y=random.randint(1,2)
            print(y)
            await asyncio.sleep(y)
            await x10.delete()
            await app.send_file(event.chat.id,file=,caption="__**Tell us more about yourself**__")
                            # Ask for trainer's name
            global msg
            msg = await event.reply("__**Tell us what you want to be called as**__",buttons=[
                [Button.inline("Note!",data="n1")]
            ])

            app.user_states[event.sender_id] = {
        "stage": "awaiting_name",
        "message_id": msg.id
    }
            

   else:
      await event.reply("__**You are not an authorised user!**__")

@app.on(events.NewMessage)
async def handle_message(event):
    # Get the user state
    user_state = app.user_states.get(event.sender_id)

    if user_state:
        # Check if the message is a reply to the tracked message
        if event.message.reply_to_msg_id == user_state["message_id"]:
            # Handle based on the current stage
            if user_state["stage"] == "awaiting_name":
                 
                # Get the user's name
                global name
                name = event.message.text
                if name.startswith('/'):
                    await event.reply("__**Invalid name exiting registration process**__")
                    await msg.delete()
                    app.user_states.pop(event.sender_id, None)
                    col.delete_one({"user_id": event.sender_id})
                    return
                print(name)
                # Update the state to "awaiting_passcode"
                await msg.delete()
                global msg1
                msg1 = await event.reply("__**Kindly enter a valid passcode address which is not used already**__",buttons=[
                [Button.inline("Note!",data="n3")]
                ])
                user_state["stage"] = "awaiting_passcode"
                user_state["message_id"] = msg1.id

            elif user_state["stage"] == "awaiting_passcode":
                # Get the user's passcode
                global passcode
                passcode = event.message.text
                print(passcode)
                await msg1.delete()
                # Clear the user's state
                app.user_states.pop(event.sender_id, None)
                
                col.update_one({"user_id": event.sender_id}, {"$set": {"name": name, "passcode": passcode}})
                m1=await event.reply("__**Saving your data to the server, please wait**__")
                r=random.randint(1,50)
                m2=await m1.edit(f"__**Saving your data to the server, please wait {r}%**__")
                await asyncio.sleep(1)
                r=random.randint(51,99)
                m3=await m2.edit(f"__**Saving your data to the server, please wait {r}%**__")
                await asyncio.sleep(1)
                m4=await m3.edit("__**Saving your data to the server, please wait %**__")
                await m4.delete()
                
                await event.respond(
        file="AgACAgUAAxkBAAIJ0WeI4nOrtEP5AzO4Evu_p0o5NkE1AAIhzjEbmE55VwSzkNv2eUTWAAgBAAMCAAN5AAceBA",
        buttons=[
            Button.inline("Previous", data="prev"),
            Button.inline("Select", data="select"),
            Button.inline("Next", data="next"),
        ]
    )

@app.on(events.NewMessage(pattern="/delete"))
#to delete all documents in the db
async def delete(event):
    col.delete_many({})
    await event.reply("__**All documents have been deleted!**__")


@app.on(events.NewMessage(pattern="/launch"))
async def launch(event):
    if event.is_group:
        await app.send_file(event.chat.id,file=error_image,caption="__**Try the operation again in private!**__",buttons=[
            [Button.url("Log In", "https://t.me/Pokemon_Masters_Game_Bot?start=start_chat")]
         ])
    elif event.is_private:
        check_whether_existing_user = col.find_one({"user_id": event.sender_id},{"Registration": 1})
        if check_whether_existing_user and "Registration" in check_whether_existing_user:
            check_partner=col.find_one({"user_id": event.sender_id},{"partner": 1})
            if check_partner and "partner" in check_partner:
                r=random.randint(1,5)
                r1=random.randint(6,10)
                r2=random.randint(11,15)
                r3=random.randint(16,20)
                r4=random.randint(21,25)
                r5=random.randint(26,30)
                x=await app.send_file(event.chat.id,file=logo_image,caption=f"__**Loading necessary data!{r}%**__")
                await x.edit(f"__**Loading necessary data! {r1}%**__")
                await x.edit(f"__**Loading necessary data! {r2}%**__")
                await x.edit(f"__**Loading necessary data! {r3}%**__")
                await x.edit(f"__**Loading necessary data! {r4}%**__")
                await x.edit(f"__**Loading necessary data! {r5}%**__")
                r6=random.randint(31,35)
                r7=random.randint(36,40)
                r8=random.randint(41,45)
                r9=random.randint(46,50)
                r10=random.randint(51,55)
                await x.edit(f"__**Connecting with server {r6}%**__")
                await x.edit(f"__**Connecting with server {r7}%**__")
                await x.edit(f"__**Connecting with server {r8}%**__")
                await x.edit(f"__**Connecting with server {r9}%**__")
                await x.edit(f"__**Connecting with server {r10}%**__")
                r11=random.randint(56,60)
                r12=random.randint(61,65)
                r13=random.randint(66,70)
                r14=random.randint(71,75)
                r15=random.randint(76,80)
                await x.edit(f"__**Checking user credentials{r11}%**__")
                await x.edit(f"__**Checking user credentials{r12}%**__")
                await x.edit(f"__**Checking user credentials{r13}%**__")
                await x.edit(f"__**Checking user credentials{r14}%**__")
                await x.edit(f"__**Checking user credentials{r15}%**__")
                r16=random.randint(81,85)
                r17=random.randint(86,90)
                r18=random.randint(91,95)
                r19=random.randint(96,100)
                await x.edit(f"__**Logging in ...{r16}%**__")
                await x.edit(f"__**Logging in ...{r17}%**__")
                await x.edit(f"__**Logging in ...{r18}%**__")
                await x.edit(f"__**Logging in ...{r19}%**__")
                await x.delete()
            else:
                r=random.randint(1,5)
                r1=random.randint(6,10)
                r2=random.randint(11,15)
                r3=random.randint(16,20)
                r4=random.randint(21,25)
                r5=random.randint(26,30)
                x=await app.send_file(event.chat.id,file=logo_image,caption=f"__**Loading necessary data!{r}%**__")
                await x.edit(f"__**Loading necessary data! {r1}%**__")
                await x.edit(f"__**Loading necessary data! {r2}%**__")
                await x.edit(f"__**Loading necessary data! {r3}%**__")
                await x.edit(f"__**Loading necessary data! {r4}%**__")
                await x.edit(f"__**Loading necessary data! {r5}%**__")
                r6=random.randint(31,35)
                r7=random.randint(36,40)
                r8=random.randint(41,45)
                r9=random.randint(46,50)
                r10=random.randint(51,55)
                await x.edit(f"__**Connecting with server {r6}%**__")
                await x.edit(f"__**Connecting with server {r7}%**__")
                await x.edit(f"__**Connecting with server {r8}%**__")
                await x.edit(f"__**Connecting with server {r9}%**__")
                await x.edit(f"__**Connecting with server {r10}%**__")
                r11=random.randint(56,60)
                r12=random.randint(61,65)
                r13=random.randint(66,70)
                r14=random.randint(71,75)
                r15=random.randint(76,80)
                await x.edit(f"__**Checking user credentials{r11}%**__")
                await x.edit(f"__**Checking user credentials{r12}%**__")
                await x.edit(f"__**Checking user credentials{r13}%**__")
                await x.edit(f"__**Checking user credentials{r14}%**__")
                await x.edit(f"__**Checking user credentials{r15}%**__")
                r16=random.randint(81,85)
                r17=random.randint(86,90)
                r18=random.randint(91,95)
                r19=random.randint(96,100)
                await x.edit(f"__**Logging in ...{r16}%**__")
                await x.edit(f"__**Logging in ...{r17}%**__")
                await x.edit(f"__**Logging in ...{r18}%**__")
                await x.edit(f"__**Logging in ...{r19}%**__")
                await x.delete()
                await app.send_file(event.chat.id,file=version_image,buttons=[
                    [Button.inline("Bulbasaur",data="pb"),Button.inline("Charmander",data="pc"),Button.inline("Squirtle",data="ps")],
                    [Button.inline("Pikachu",data="pp"),Button.inline("Eevee",data="pe")],
                ])
        else:
            await app.send_message(event.chat.id,"__**No save data detected \n You may fix the problem by using /register or contact Support Team**__")

#/walk command
@app.on(events.NewMessage(pattern="/walk"))
async def walk(event):
    if event.is_group:
        user_list = await users()
        user_id = event.sender_id
        if user_id in user_list:
            await app.send_file(event.chat.id,file=error_image,caption="__**Try the operation again in private!**__",buttons=[
            [Button.url("Log In", "https://t.me/Pokemon_Masters_Game_Bot?start=start_chat")]
         ])
        else:
            await event.reply("__**You are not an authorized user**__")
    elif event.is_private:
        
        user_id = event.sender_id

        # If user is already in battle, prevent walking
        if user_id in battle_state and battle_state[user_id]["status"] == "in_battle":
            await event.respond(f"You are in the middle of a battle with {battle_state[user_id]['pokemon']}! Use the buttons to continue.")
            return

        location = "route_1"
        wild_pokemon = await get_spawn(location)

        if not wild_pokemon:
            await event.respond("No Pokémon appeared.")
            return

        msg = f"Oh! You encountered a wild {wild_pokemon['name']} (Level {wild_pokemon['level']})"

        buttons = [
            [Button.inline("⚔ Fight", f"fight|{wild_pokemon['name']}")],
            [Button.inline("📖 Pokédex", b"pokedex")]
        ]

        # Store new battle data, removing old battle
        battle_state[user_id] = {
            "status": "encounter",
            "pokemon": wild_pokemon["name"],
            "level": wild_pokemon["level"],
            "type": "wild"
        }

        await event.respond(msg, buttons=buttons)
        
    
@app.on(events.NewMessage(pattern="/bag"))
async def bag(event):
    user_id = event.sender_id

    # Fetch pokeball and pokecoins from MongoDB
    item = col.find_one({"active_user_id": user_id}, {"_id": 0, "pokeball": 1, "pokecoins": 1})

    if item:
        # Extract values, default to 0 if not found
        pokeball = item.get("pokeball", 0)
        pokecoins = item.get("pokecoins", 0)

        # Format the message
        response = f"🎒 **Your Bag**\n🟠 Pokeballs: {pokeball}\n💰 Pokecoins: {pokecoins}"

        await event.reply(response)  # Send the formatted message
    else:
        await event.reply("🎒 Your bag is empty!")

@app.on(events.NewMessage(pattern="/set"))
async def v(event):
    user_id = event.sender_id
    user_data = col.find_one({"active_user_id": user_id}, {"party": 1})

    if user_data and "party" in user_data:
        team1 = user_data["party"]  # Copy party Pokémon to team1
        col.update_one({"active_user_id": user_id}, {"$set": {"team1": team1}})

        await event.reply("Your party Pokémon have been added to team1!")
    else:
        await event.reply("You have no Pokémon in your party!")



@app.on(events.NewMessage(pattern="/add"))
async def add(event):
    user_id = event.sender_id
    if user_id in user_state_for_add:  # Ignore if already in process
        return  
    user_state_for_add[user_id] = {"awaiting_name": True} 
    await event.reply("Enter a valid Kanto Pokémon Name")

@app.on(events.NewMessage)
async def add_handle(event):
    user_id = event.sender_id
    text = event.text.strip().capitalize()  # Convert input to uppercase for case insensitivity

    if text == "/ADD" or text == "/add":  # Ignore repeated "/add"
        return  

    if user_id in user_state_for_add:
        state = user_state_for_add[user_id]

        # Step 1: Get Pokémon Name
        if state.get("awaiting_name"):
            if text in pokemon:
                state["pokemon_name"] = text  # Store Pokémon name
                state["awaiting_name"] = False
                state["awaiting_level"] = True  # Now ask for level
                await event.reply(f"Pokémon {text} accepted.\nNow enter the level (1 - 100).")
            else:
                await event.reply("Invalid Pokémon name! Please enter a valid Kanto Pokémon.")

        # Step 2: Get Level
        elif state.get("awaiting_level"):
            if text.isdigit():
                level = int(text)
                if 1 <= level <= 100:
                    state["pokemon_level"] = level  # Store level
                    global pokemon_name
                    pokemon_name = state["pokemon_name"]
                    del user_state_for_add[user_id]  # Remove user state after completion

                    # Print both values
                    x = await event.reply(f"Pokémon: {pokemon_name}\nLevel: {level}")
                    await asyncio.sleep(1)
                    y = await x.edit("Communicating with the server")
                    eevee = Pokemon(pokemon_name,level)
                    name = eevee.get_name()
                    global v_g,v_u
                    v_g = pokemon_name
                    
                    id = eevee.get_id()
                    pokemon_id = eevee.generate_pokemon_id()
                    v_u = pokemon_id
                    type = eevee.get_type()
                    type_data=type.split(" ")
                    type1=type_data[0]
                    type2=type_data[1] if len(type_data)>1 else None
                    abilities = eevee.get_abilitites()
                    category = eevee.get_category()
                    description = eevee.get_description()
                    nature = eevee.get_nature()
                    iv = eevee.get_ivs()
                    ev = eevee.get_evs()
                    moves = eevee.get_moves()
                    stats = eevee.get_stats()
                    global z456
                    z456 = await y.edit(f"__**Name - {name}\nId - {pokemon_id}\nType 1 - {type1}\nType 2 - {type2}\nAbility - {abilities}\nCategory - {category}\nDescription - {description}\nNature - {nature}\nIVs - {iv}\nEVs - {ev}\nStats - {stats}\nMoves - {moves}__**",buttons = [
    [Button.inline("Confirm", data=b"co_data"), Button.inline("Retry", data=b"r_data")],  # First row
    [Button.inline("Cancel", data=b"ca_data")]  # Second row
])
                    global t_data
                    t_data = {
           "name": pokemon_name,
           "id":id,
           "level":level,
           "pokemon_id":pokemon_id,
           "type1":type1,
           "type2":type2,
           "ability":abilities,
           "category":category,
           "description":description,
           "nature":nature,
           "level":5,
           "iv":iv,
           "ev":ev,
           "moves":moves,
           "stats":stats
       }
                    
                    



                else:
                    await event.reply("Invalid level! Enter a number between 1 and 100.")
            else:
                await event.reply("Please enter a valid numeric level (1 - 100).")

#menu handler
@app.on(events.NewMessage(pattern="/menu"))
async def menu(event):
    user_id = event.sender_id
    x = await event.reply("Communicating...")
    await asyncio.sleep(1)
    await x.delete()
    if user_id in waiting_players:
       await event.respond("Your Matchup is already in progress or you are currently battling...")
    await event.respond(file = menu1,buttons=[[Button.inline("Pokemon",data=b"m_poe")],[Button.inline("Options",data=b"m_op")]])

@app.on(events.CallbackQuery)
async def menu_callback(event):
    user_id = event.sender_id 
    if event.data == b"m_op" and event.is_private:
        await event.edit(file = menu2,buttons = [[Button.inline("Battle Stadium",b"m_bs")]])
    elif event.data == b"m_poe":
        await event.edit(buttons=[
    [Button.inline("Party", data=b"m_pa")],
    [Button.inline("Manage Teams", data=b"m_mt")]
])

    elif event.data == b"m_mt" and event.is_private:
        user_id = event.sender_id
        document = col.find_one({"active_user_id": user_id})
        print(document)  # Fetch the full document
        if not document or "Active Team" not in document:
            col.update_one(
                {"active_user_id": user_id},
                {"$set": {
                    "Active Team": None,
                    "team1": [],
                    "team2": [],
                    "team3": [],
                    "team4": [],
                    "team5": [],
                    "team6": []
                }},
                # Ensures the document is created if it doesn't exist
            )
            await event.respond("done")
            
        else:
            x = col.find_one({"active_user_id":user_id},{"Active Team":1})
            x = x.get("Active Team", "")
            if x is None :
                print("yes")
                await event.delete()
                await event.respond("No active team",buttons = [[Button.inline("Team1",data=b"t1"),Button.inline("Team2",data=b"t2")],[Button.inline("Team3",data=b"t3"),Button.inline("Team4",data=b"t4")],[Button.inline("Team5",data=b"t5"),Button.inline("Team6",data=b"t6")],[Button.inline("Edit Team",data=b"et")]])

    

    elif event.data == b"m_bs" and event.is_private:
        await event.edit(file = wifi_1, buttons = [[Button.inline("Casual Battles",b"wf_c")]])
        battle_stadium[user_id]={}
    elif event.data == b"wf_c" and event.is_private:
        await event.edit(file = wifi_2, buttons = [[Button.inline("Single Battles",b"wf_s")]])
        battle_stadium[user_id]["wifi_format"] = "Casual Battles"
    elif event.data == b"wf_s" and event.is_private:
        await event.answer("Communicating. Please stand by...",alert=True)
        battle_stadium[user_id]["battle_format"] = "Single Battles"
        print(battle_stadium)
        if battle_stadium[user_id]["wifi_format"] == "Casual Battles":
            
            image = Image.open("D:\\python\\Pokemon-Masters-Nintendro-AAC\\wifi2.jpg").convert("RGBA")
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("verdana",120)
            font1 = ImageFont.truetype("verdana",90)
            draw.text((70,75),"Casual Battles",font = font, fill = "white")
            draw.text((70,250),"Single Battles",font = font, fill = "white")
            draw.text((1030,1850),"Choose the method to matchup...",font = font1, fill = "white")
            image.save("D:\\python\\Pokemon-Masters-Nintendro-AAC\\wifie.jpg",format="PNG")
            await event.edit(text="D:\\python\\Pokemon-Masters-Nintendro-AAC\\wifie.jpg",buttons=[[Button.inline("Random",data=b"random")],[Button.inline("Link Code",data=b"link_code")]])
    elif event.data == b"random":
        await event.answer("Communicating. Please stand by...",alert=True)
        battle_stadium[user_id]["mode"] = {}
        battle_stadium[user_id]["mode"]["random"] = {"random":"yes","started":"no"}
        waiting_players.append(user_id)
        image = Image.open("D:\\python\\Pokemon-Masters-Nintendro-AAC\\wifi2.jpg").convert("RGBA")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("verdana",120)
        font1 = ImageFont.truetype("verdana",90)
        draw.text((70,75),"Casual Battles",font = font, fill = "white")
        draw.text((70,250),"Single Battles",font = font, fill = "white")
        draw.text((1030,1850),"Searching for an opposing Trainer...",font = font1, fill = "white")
        image.save("D:\\python\\Pokemon-Masters-Nintendro-AAC\\wifie.jpg",format="PNG")
        await event.edit(text="D:\\python\\Pokemon-Masters-Nintendro-AAC\\wifie.jpg")
        await event.delete()
        if len(waiting_players) >=2:
            global player1,player2
            player1,player2=random.sample(waiting_players,2)
            waiting_players.remove(player1)
            waiting_players.remove(player2)
            image = Image.open("D:\\python\\Pokemon-Masters-Nintendro-AAC\\wifi2.jpg").convert("RGBA")
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype("verdana",120)
            font1 = ImageFont.truetype("verdana",90)
            draw.text((70,75),"Casual Battles",font = font, fill = "white")
            draw.text((70,250),"Single Battles",font = font, fill = "white")
            draw.text((1030,1850),"An opposing Trainer has been found!",font = font1, fill = "white")
            image.save("D:\\python\\Pokemon-Masters-Nintendro-AAC\\wifie.jpg",format="PNG")
            yv=await app.send_file(event.chat.id,file="D:\\python\\Pokemon-Masters-Nintendro-AAC\\wifie.jpg")
            try:
                await yv.delete()
            except Exception as e:
                print(f"Error deleting event: {e}")
            await asyncio.sleep(3) 
            global p1_msg,p2_msg   
            p1_msg = await app.send_message(player1, f"A battle against againt {player2} is about to start!")
            p2_msg =await app.send_message(player2, f"A battle against againt {player1} is about to start!")
            await asyncio.sleep(1)
            await p1_msg.edit("Communicating...")
            await p2_msg.edit("Communicating...")
            c_p1= col.find_one({"active_user_id":player1},{"Active Team":1})
            c_p1=c_p1.get("Active Team","")
            d_p1= col.find_one({"active_user_id":player1},{c_p1:1})
            d_p1=d_p1.get(c_p1,{})
            print(d_p1)
            c_p2= col.find_one({"active_user_id":player2},{"Active Team":1})
            c_p2=c_p2.get("Active Team","")
            d_p2= col.find_one({"active_user_id":player2\
                },{c_p2:1})
            d_p2=d_p2.get(c_p2,{})
            print(d_p2)
            print("player1",player1)
            print("player2",player2)
            cv=battle_stadium[player1]["mode"]["random"]["team"] = {}
            vc=battle_stadium[player2]["mode"]["random"]["team"] = {}
            cv.update(d_p1)
            vc.update(d_p2)
            print(battle_stadium)
            p1_team = battle_stadium[player1]["mode"]["random"]["team"]
            p2_team = battle_stadium[player2]["mode"]["random"]["team"]
            team_list1 = []
            team_list2 = []
            for x in p1_team:
                x = x.split("_")
                x = x[0]
                team_list1.append(x)
            for y in p2_team:
                y = y.split("_")
                y = y[0]
                team_list2.append(y)
            print(team_list1,team_list2)
            global p1_team_str,p2_team_str
            p1_team_str = "\n".join(team_list1)
            p2_team_str = "\n".join(team_list2)
            
            await p1_msg.edit(f"Your Team\n{p1_team_str}\n\nOpposing Team\n{p2_team_str}",buttons=[[Button.inline("Back",data=b"backzy")]])
            await p2_msg.edit(f"Your Team\n{p2_team_str}\n\nOpposing Team\n{p1_team_str}",buttons=[[Button.inline("Back",data=b"backzy")]])

            print("Final",battle_stadium)
    elif event.data == b"backzy":
        try:
            if user_id == player1:  
                
                p_buttons = [[Button.inline(pokemon, data="x")] for pokemon in team_list1]
                print("see it",pokemon)
                await p1_msg.delete()
                await event.respond(p1_team_str,buttons= [p_buttons[i : i + 2] for i in range(0, len(p_buttons), 2)])
                print(user_id,player1)
            if user_id == player2:
                await p2_msg.edit(p2_team_str)
                print(user_id,player2)
        except Exception as e:
            await event.respond(str(e))


    



@app.on(events.CallbackQuery)
async def query_handler(event):
   if event.data==b"n1":
      await event.answer("Reply to the message with your unique name", alert=True)
   elif event.data==b"n3":
      await event.answer("Reply to the message with your passcode which is not registered already", alert=True)
   
   elif event.data == b"r_data":  
         eevee = Pokemon(pokemon_name,level)
         name = eevee.get_name()
         global v_g
         v_g = name
         
         id = eevee.get_id()
         global pokemon_id
         pokemon_id = eevee.generate_pokemon_id()
         global v_u
         v_u = pokemon_id
         type = eevee.get_type()
         type_data=type.split(" ")
         type1=type_data[0]
         type2=type_data[1] if len(type_data)>1 else None
         abilities = eevee.get_abilitites()
         category = eevee.get_category()
         description = eevee.get_description()
         nature = eevee.get_nature()
         iv = eevee.get_ivs()
         ev = eevee.get_evs()
         moves = eevee.get_moves()
         stats = eevee.get_stats()
         y56 = await z456.edit("Communicating with server")
         v345 = await y56.edit(f"__**Name - {name}\nId - {pokemon_id}\nType 1 - {type1}\nType 2 - {type2}\nAbility - {abilities}\nCategory - {category}\nDescription - {description}\nNature - {nature}\nIVs - {iv}\nEVs - {ev}\nStats - {stats}\nMoves - {moves}__**",buttons = [
    [Button.inline("Confirm", data=b"co_data"), Button.inline("Retry", data=b"r_data")],  # First row
    [Button.inline("Cancel", data=b"ca_data")]  # Second row
])
         global t_data
         t_data = {
           "name": v_g,
           "id":id,
           "level":level,
           "pokemon_id":pokemon_id,
           "type1":type1,
           "type2":type2,
           "ability":abilities,
           "category":category,
           "description":description,
           "nature":nature,
           "level":5,
           "iv":iv,
           "ev":ev,
           "moves":moves,
           "stats":stats
       }
   elif event.data == b"co_data":
       user_id = event.sender_id
       # Fetch the user's current party
       user_data = col.find_one({"active_user_id": user_id}, {"party": 1})

    # Get existing party data (default to empty dict if not found
       if user_data is  None:
            await event.respond("user is not registered")
            return
       party = user_data.get("party", {})

    # Always store the Pokémon in "Pokemon" object
       col.update_one(
        {"active_user_id": user_id},
        {"$set": {f"Pokemon.{v_g}_{v_u}": t_data}}  # Always store Pokémon data
    )

    # Check if party already has 6 Pokémon
       if len(party) < 6:
        # Add new Pokémon to the party
           party[f"{v_g}_{v_u}"] = {"name": t_data["name"], "id": t_data["pokemon_id"]}

        # Update the database with new party data
           col.update_one(
            {"active_user_id": user_id},
            {"$set": {"party": party}}
            
        )
           await event.delete()
           await event.respond("Added")
       else:
        # Notify that the party is full but Pokémon is still stored
           await event.delete()
           await event.respond("Added")
           await event.reply("Your party is full! The Pokémon has been stored but won't be in your active party.")

   elif event.data == b"ca_data":
    await event.delete()
    await event.respond("Cancellation Complete")

@app.on(events.CallbackQuery) 
async def character_navigation(event): 
   user_id = event.sender_id 
   if user_id not in current_indices: 
      current_indices[user_id] = 0
       
   if event.data == b"prev": 
        current_indices[user_id] = (current_indices[user_id] - 1) % len(characters) 
        index = current_indices[user_id] 
        global ch
        ch=await event.edit( file=characters[index]["url"], buttons=[ Button.inline("Previous", data="prev"), Button.inline("Select", data="select"), Button.inline("Next", data="next"), ] )
   elif event.data == b"next": 
        current_indices[user_id] = (current_indices[user_id] + 1) % len(characters) 
        index = current_indices[user_id] 
        ch=await event.edit( file=characters[index]["url"], buttons=[ Button.inline("Previous", data="prev"), Button.inline("Select", data="select"), Button.inline("Next", data="next"), ] )  
   elif event.data == b"select":
        index = current_indices[user_id]
        selected_character = characters[index]["name"]
        await save_to_db(user_id, selected_character)
        message = await event.get_message()
        await message.delete()
        k=await app.send_message(user_id,"__**Collecting your raw information from the bot's temporary cache**__")
        await asyncio.sleep(2)
        k1= await k.edit("__**Gathering your raw data**__")
        await asyncio.sleep(2)
        k2= await k1.edit("__**Transfering your data to the server**__")
        await asyncio.sleep(2)
        k3 = await k2.edit("__**Registering new user by creating user save data**__")
        await asyncio.sleep(2)
        k4 = await k3.edit("__**Creating personalised user cache with the server!\nPlease hold on!\nNote: This process might take from few seconds to a minute or two!**__")
        r = random.randint(1,2)
        await asyncio.sleep(r)
        k5=await k4.edit("__**Personal save data has been created!\nUse /launch to launch the game!**__")
   elif event.data==b"pb":
       await event.delete()
       bulbasaur = PartnerPokemon("Partner Bulbasaur",5)
       name = bulbasaur.get_name()
       id = bulbasaur.get_id()
       pokemon_id = bulbasaur.generate_pokemon_id()
       type = bulbasaur.get_type()
       type_data=type.split(" ")
       type1=type_data[0]
       type2=type_data[1] if len(type_data)>1 else None
       abilities = bulbasaur.get_abilitites()
       category = bulbasaur.get_category()
       description = bulbasaur.get_description()
       nature = bulbasaur.get_nature()
       iv = bulbasaur.get_ivs()
       ev = bulbasaur.get_evs()
       moves = bulbasaur.get_moves()
       stats = bulbasaur.get_stats()
       data = {"Pokemon":{"Bulbasaur":{
           "name": "Bulbasaur (Partner)",
           "id":id,
           "level":"5",
           "pokemon_id":pokemon_id,
           "type1":type1,
           "type2":type2,
           "ability":abilities,
           "category":category,
           "description":description,
           "nature":nature,
           "level":5,
           "iv":iv,
           "ev":ev,
           "moves":moves,
           "stats":stats
       }}}
       col.update_one({"user_id":user_id},{"$set": data})
       col.update_one({"user_id":user_id},{"$set": {"partner":"bulbasaur"}})
       await event.respond(f"{name}\n{id}\n{type}\n{abilities}\n{category}\n{description}\n{nature}\n{iv}\n{ev}\n{moves}\n{stats}")
       video_message = await app.get_messages(PRIVATE_GROUP_ID,ids=VIDEO_MESSAGE_ID)
       await app.send_message(event.sender_id,video_message,buttons=[Button.inline("----->", data="n2")])
   elif event.data==b"pc":
       await event.delete()
       charmander = PartnerPokemon("Partner Charmander",5)
       name = charmander.get_name()
       id = charmander.get_id()
       pokemon_id = charmander.generate_pokemon_id()
       type = charmander.get_type()
       type_data=type.split(" ")
       type1=type_data[0]
       type2=type_data[1] if len(type_data)>1 else None
       abilities = charmander.get_abilitites()
       category = charmander.get_category()
       description = charmander.get_description()
       nature = charmander.get_nature()
       iv = charmander.get_ivs()
       ev = charmander.get_evs()
       moves = charmander.get_moves()
       stats = charmander.get_stats()
       data = {"Pokemon":{"Charmander":{
           "name": "Charmander (Partner)",
           "id":id,
           "level":"5",
           "pokemon_id":pokemon_id,
           "type1":type1,
           "type2":type2,
           "ability":abilities,
           "category":category,
           "description":description,
           "nature":nature,
           "level":5,
           "iv":iv,
           "ev":ev,
           "moves":moves,
           "stats":stats
       }}}
       col.update_one({"user_id":user_id},{"$set": data})
       col.update_one({"user_id":user_id},{"$set": {"partner":"charmander"}})
       await event.respond(f"{name}\n{id}\n{type}\n{abilities}\n{category}\n{description}\n{nature}\n{iv}\n{ev}\n{moves}\n{stats}")
       video_message = await app.get_messages(PRIVATE_GROUP_ID,ids=VIDEO_MESSAGE_ID)
       await app.send_message(event.sender_id,video_message,buttons=[Button.inline("----->", data="n2")])
   elif event.data==b"ps":
       await event.delete()
       squirtle = PartnerPokemon("Partner Squirtle",5)
       name = squirtle.get_name()
       id = squirtle.get_id()
       pokemon_id = squirtle.generate_pokemon_id()
       type = squirtle.get_type()
       type_data=type.split(" ")
       type1=type_data[0]
       type2=type_data[1] if len(type_data)>1 else None
       abilities = squirtle.get_abilitites()
       category = squirtle.get_category()
       description = squirtle.get_description()
       nature = squirtle.get_nature()
       iv = squirtle.get_ivs()
       ev = squirtle.get_evs()
       moves = squirtle.get_moves()
       stats = squirtle.get_stats()
       data = {"Pokemon":{"Squirtle":{
           "name": "Squirtle (Partner)",
           "id":id,
           "level":"5",
           "pokemon_id":pokemon_id,
           "type1":type1,
           "type2":type2,
           "ability":abilities,
           "category":category,
           "description":description,
           "nature":nature,
           "level":5,
           "iv":iv,
           "ev":ev,
           "moves":moves,
           "stats":stats
       }}}
       col.update_one({"user_id":user_id},{"$set": data})
       col.update_one({"user_id":user_id},{"$set": {"partner":"squirtle"}})
       await event.respond(f"{name}\n{id}\n{type}\n{abilities}\n{category}\n{description}\n{nature}\n{iv}\n{ev}\n{moves}\n{stats}")
       video_message = await app.get_messages(PRIVATE_GROUP_ID,ids=VIDEO_MESSAGE_ID)
       await app.send_message(event.sender_id,video_message,buttons=[Button.inline("----->", data="n2")])

   elif event.data==b"pp":
       await event.delete()
       pikachu = PartnerPokemon("Partner Pikachu",5)
       name = pikachu.get_name()
       id = pikachu.get_id()
       pokemon_id = pikachu.generate_pokemon_id()
       type = pikachu.get_type()
       type_data=type.split(" ")
       type1=type_data[0]
       type2=type_data[1] if len(type_data)>1 else None
       abilities = pikachu.get_abilitites()
       category = pikachu.get_category()
       description = pikachu.get_description()
       nature = pikachu.get_nature()
       iv = pikachu.get_ivs()
       ev = pikachu.get_evs()
       moves = pikachu.get_moves()
       stats = pikachu.get_stats()
       data = {"Pokemon":{"Pikachu":{
           "name": "Pikachu (Partner)",
           "id":id,
           "level":"5",
           "pokemon_id":pokemon_id,
           "type1":type1,
           "type2":type2,
           "ability":abilities,
           "category":category,
           "description":description,
           "nature":nature,
           "level":5,
           "iv":iv,
           "ev":ev,
           "moves":moves,
           "stats":stats
       }}}
       try:
           col.update_one({"user_id":user_id},{"$set": data})
           col.update_one({"user_id":user_id},{"$set": {"partner":"pikachu"}})
           await event.respond(f"{name}\n{id}\n{type}\n{abilities}\n{category}\n{description}\n{nature}\n{iv}\n{ev}\n{moves}\n{stats}")
           video_message = await app.get_messages(PRIVATE_GROUP_ID,ids=VIDEO_MESSAGE_ID)
           await app.send_message(event.sender_id,video_message,buttons=[Button.inline("----->", data="n2")])
       except Exception as e:
           print(e)  
       
   elif event.data==b"pe":
       await event.delete()
       eevee = PartnerPokemon("Partner Eevee",5)
       name = eevee.get_name()
       id = eevee.get_id()
       pokemon_id = eevee.generate_pokemon_id()
       type = eevee.get_type()
       type_data=type.split(" ")
       type1=type_data[0]
       type2=type_data[1] if len(type_data)>1 else None
       abilities = eevee.get_abilitites()
       category = eevee.get_category()
       description = eevee.get_description()
       nature = eevee.get_nature()
       iv = eevee.get_ivs()
       ev = eevee.get_evs()
       moves = eevee.get_moves()
       stats = eevee.get_stats()
       data = {"Pokemon":{"Eevee":{
           "name": "Eevee (Partner)",
           "id":id,
           "level":"5",
           "pokemon_id":pokemon_id,
           "type1":type1,
           "type2":type2,
           "ability":abilities,
           "category":category,
           "description":description,
           "nature":nature,
           "level":5,
           "iv":iv,
           "ev":ev,
           "moves":moves,
           "stats":stats
       }}}
       col.update_one({"user_id":user_id},{"$set": data})
       col.update_one({"user_id":user_id},{"$set": {"partner":"eevee"}})
       await event.respond(f"{name}\n{id}\n{type}\n{abilities}\n{category}\n{description}\n{nature}\n{iv}\n{ev}\n{moves}\n{stats}")
       video_message = await app.get_messages(PRIVATE_GROUP_ID,ids=VIDEO_MESSAGE_ID)
       await app.send_message(event.sender_id,video_message,buttons=[Button.inline("----->", data="n2")])
   elif event.data==b"n2":
       await event.delete()
       await app.send_message(event.sender_id,"TEXT YET TO BE ADDED")
       result = col.find_one(
    {"user_id": user_id},  # Filter by user_id
    {"partner": 1, "_id": 0}  # Retrieve only the 'partner' field
)

       # Extract the 'partner' value
       y = result.get("partner") if result else None
       y = y.capitalize()
       print(y)
       pokemon = col.find_one({"user_id": user_id}, {f"Pokemon.{y}.name": 1})
       x_id = col.find_one({"user_id": user_id}, {f"Pokemon.{y}.pokemon_id": 1})
       pc = col.update_one({"user_id":user_id}, {"$set": {"pokecoins":10000,"pokeball":100}})
       
# Extracting the values from the query results
       pokemon_name = pokemon.get("Pokemon", {}).get(y, {}).get("name", "Unknown")
       pokemon_id = x_id.get("Pokemon", {}).get(y, {}).get("pokemon_id", "Unknown")

# Updating only the 'party' field
       col.update_one(
    {"user_id": user_id},  # Match the user by ID
    {
        "$set": {
            "party": {
                "1": {
                    "name": pokemon_name,
                    "id": pokemon_id
                }
            }
        }
    }
)

       

   

      

async def save_to_db(user_id, selected_character):
    # Ensure col is your MongoDB collection instance
    col.update_one(
        {"user_id": user_id},  # Match the user by ID
        {"$set": {"selected_character": selected_character,"Registration":"done","active_user_id":user_id}}
    )


app.start(bot_token=bot_token)

print("Bot is running...")

# Run the bot until it is disconnected
app.run_until_disconnected()