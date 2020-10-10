import discord
import emoji
import os
import random
import requests

from discord.ext import commands
from dotenv import load_dotenv

# Set version number
VERSION_NUMBER = 0.3

# Load environment variables from .env file
load_dotenv()

# Set constants from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot
bot = commands.Bot(command_prefix='!')


# Set up bot commands
@bot.command(name='version')
async def say_version(context):
    """Display clackbot version information."""
    await context.send(f'clackbot {VERSION_NUMBER} © 2020 <@!572963354902134787>')

@bot.command(name='source')
async def say_source_url(context):
    """Display the link to clackbot's source code on GitHub."""
    await context.send('https://github.com/doopqoob/clackbot')

@bot.command(name='follow')
async def join_voice(context):
    """Follow a user into a voice channel."""
    if context.author.voice is None:
        await context.send('You need to be in a voice channel to run that command here (confusing, huh?)')
        return

    channel = context.author.voice.channel
    await channel.connect()


@bot.command(name='leave')
async def leave_voice(context):
    """Leave the currently-joined voice channel."""
    await context.voice_client.disconnect()


@bot.command(name='clack')
async def play_clacking(context):
    """Play a 'clacking' sound into the currently-joined voice channel."""
    # Get list of filenames from 'clacks' directory
    (_,  _, filenames) = next(os.walk('clacks/'))

    # randomize list
    random.shuffle(filenames)

    # set up voice channel
    guild = context.guild
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)

    if voice_client is None:
        await context.send("I need to be in a voice channel to do that. Join the desired voice channel "
                           + "then type !follow in this channel.")
        return

    # set up audio source
    audio_source = discord.FFmpegPCMAudio(f'clacks/{filenames[0]}')

    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)


@bot.command(name='stop')
async def stop_clacking(context):
    """Stop playing the 'clacking' sound."""
    guild = context.guild
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
    if voice_client is None:
        return

    if voice_client.is_playing():
        voice_client.stop()


@bot.command(name='poll')
async def poll(context, *args):
    """Create a poll with up to twenty answers (good lord)."""
    # Check input for common error conditions
    if len(args) == 0:
        await context.send("ERROR: No poll question or answers specified.")
        return

    if len(args) == 1:
        await context.send("ERROR: No answers to poll question specified.")
        return

    # ...and perhaps a not-so-common error condition
    if len(args) > 21:
        await context.send("WHOA! That's just too many answers (maximum 20).")
        return

    # Comb out the input into question and answers (which we treat differently below)
    question = None
    answers = []

    for counter, value in enumerate(args):
        if counter == 0:
            question = value
        else:
            answers.append(value)

    # Start preparing the poll output
    question += "\n----------\n"

    for counter, answer in enumerate(answers):
        char = chr(97 + counter)
        emoji_desc = f':regional_indicator_{char}:'
        question += f'{emoji_desc}: {answer}\n'

    message = await context.send(question)

    # Add reaction emoji for poll answers
    for counter, answer in enumerate(answers):
        char = chr(97 + counter)
        emoji_desc = f':regional_indicator_{char}:'.capitalize()
        emoji_unicode = emoji.emojize(emoji_desc, use_aliases=True)

        await message.add_reaction(emoji_unicode)


@bot.command(name='kbdb')
async def query_kb_db(context, part_num=None):
    """Query SharktasticA's model M keyboard database by part number"""
    # Make sure the user has entered a part number
    if part_num is None:
        await context.send("ERROR: No keyboard part number provided.")
        return

    # These are all the fields we're going to request from the database
    # (and their long names for when we display the data in chat)
    fields_dict = {'pn':            "Part Number",
                   'fru':           "FRU Part Number",
                   'name':          "Full Name",
                   'type':          "Type",
                   'shorthand':     "Shorthand",
                   'nickname':      "Nickname",
                   'model':         "Marketing Name",
                   'oem':           "OEM (Manufacturer)",
                   'switches':      "Switches",
                   'date':          "First Appeared",
                   'keys':          "Key Count",
                   'keycaps':       "Keycap Type",
                   'case':          "Case Colour",
                   'branding':      "Branding",
                   'feet':          "Feet Type",
                   'protocol':      "Protocol",
                   'connection':    "Connection",
                   'layout':        "Layout/Language",
                   'mouse':         "Int. Pointing Device",
                   'notes':         "Notes"}

    # Extract just the field names from fields_dict
    requested_fields = fields_dict.keys()

    # Turn the list of fields into a comma-delimited string:
    fields = ','.join(requested_fields)

    # Build the url
    url = f'https://sharktastica.co.uk/kb_db_req.php?pn={part_num}&dat=JSON&fields={fields}'

    # Query the DB
    result = requests.get(url)

    # Convert JSON into a python data structure
    result = result.json()

    # Extract only the first element of the result
    result = result[0]

    if result['success'] is False:
        await context.send(f"ERROR: Part number {part_num} not found in database.")
        return

    # Take out 'success' -- there's no corresponding key in the fields_dict and no need for it anymore
    del result['success']

    # ---> Build the response <---
    response = f"Here's what I found about part {part_num}:\n"
    for key in result.keys():
        if result[key] is not None:
            response += f'**{fields_dict[key]}:** {result[key]}\n'
    response += ('-' * 10) + '\n'
    response += 'Learn about where this data came from: https://sharktastica.co.uk/about.php#Sources'

    # aaand send it off!
    await context.send(response)


# run the bot
bot.run(DISCORD_TOKEN)