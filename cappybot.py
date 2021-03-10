import discord
import emoji
import os
import random
import requests

from discord.ext import commands
from dotenv import load_dotenv
from frogtips import api as frogtips_api
from uuid import UUID

# Set version number
VERSION_NUMBER = "0.8.1"

# Load environment variables from .env file
load_dotenv()

# Set constants from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
API_HOST = os.getenv('API_HOST')

# Set up bot
bot = commands.Bot(command_prefix='!')


# Set up bot commands
@bot.command(name='version')
async def say_version(context):
    """Display cappybot version information."""
    await context.send(f'cappybot {VERSION_NUMBER} 2021 <@!232598411654725633>')


@bot.command(name='source')
async def say_source_url(context):
    """Display the link to cappybot's source code on GitHub."""
    await context.send('https://github.com/SharktallicA/cappybot')


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
    (_, _, filenames) = next(os.walk('clacks/'))

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


@bot.command(name='frogtip')
async def frog_tip(context, tip_id=None):
    """Display a FROG Tip"""
    if tip_id is None:
        tip = frogtips_api.Tips().get_next_tip()
    else:
        tip_id = int(tip_id)
        tip = frogtips_api.Tip(tip_id)

    formatted_tip = tip.get_formatted_tip()
    formatted_tip += '\n'
    formatted_tip += "https://frog.tips/#" + str(tip.get_id())

    await context.send(formatted_tip)


@bot.command(name='kbdb')
async def query_kb_db(context, part_num=None):
    """Query SharktasticA's IBM keyboard database by part number"""
    # Make sure the user has entered a part number
    if part_num is None:
        await context.send("ERROR: No keyboard part number provided.")
        return

    # These are all the fields we're going to request from the database
    # (and their long names for when we display the data in chat)
    fields_dict = {'pn': "Part Number",
                   'fru': "FRU Part Number",
                   'name': "Full Name",
                   'type': "Type",
                   'shorthand': "Shorthand",
                   'nickname': "Nickname",
                   'model': "Marketing Name",
                   'oem': "OEM (Manufacturer)",
                   'switches': "Switches",
                   'date': "First Appeared",
                   'keys': "Key Count",
                   'formfactor': "Form Factor",
                   'keycaps': "Keycap Type",
                   'case': "Case Colour",
                   'branding': "Branding",
                   'feet': "Feet Type",
                   'protocol': "Protocol",
                   'connection': "Connection",
                   'cable': "Cable",
                   'layout': "Layout/Language",
                   'mouse': "Int. Pointing Device",
                   'price': "Price",
                   'notes': "Notes"}

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

    # Handle situation where no results are returned
    if result['hits'] == 0:
        message = f"ERROR: Part number {part_num} not found in database.\n"
        message += "Would you like to add it to the database? Just visit\n"
        message += f"https://sharktastica.co.uk/kb_db_sub.php?pn={part_num}"
        await context.send(message)
        return


    # Build the response
    response = f"Here's what I found about part {part_num}:\n\n"
    for kb in result['results']:
        link = kb.pop('link', None)
        for key in kb.keys():
            if kb[key] is not None:
                response += f'**{fields_dict[key]}:** {kb[key]}\n'
        if link is not None:
            response += f'\n**Permalink:** <{link}>\n'
    response += '\n'
    response += 'Learn about where this data came from: https://sharktastica.co.uk/about.php#Sources'

    # aaand send it off!
    await context.send(response)


@bot.command(name='kbsearch')
async def search_kb_db(context, *args):
    """Search SharktasticA's IBM keyboard database."""

    # The query is the first argument given
    # (Shark's database takes care of figuring out
    # what query type this is)
    query = args[0]
    result_count = 5

    # Build the URL
    url = f'https://sharktastica.co.uk/kb_db_req.php?q={query}&c={result_count}' \
          f'&dat=JSON&fields=pn,name,shorthand,layout,date'

    # Because the query takes a long time to run,
    # indicate to the user that something is happening.
    await context.send(f"Searching for _{query}_. Just a moment...")

    # display the 'typing' indicator while searching for user's query
    async with context.channel.typing():
        # Query the DB
        result = requests.get(url)

        # Convert JSON into a python data structure
        result = result.json()

        # Handle situation where no results are returned
        if result['success'] is False:
            message = f'ERROR: {result["message"]}'
            await context.send(message)
            return

        # Handle other situation where no results are returned
        if result['hits'] == 0:
            message = f'ERROR: No results for _{query}_ in database.'
            await context.send(message)
            return

        # Build the response
        response = f"Here's what I found for _{query}_:\n"

        hits = result['hits']

        # Iterate through each keyboard in result.
        for index, kb in enumerate(result['results']):
            hits -= 1
            response += f"> {index + 1}:\n" \
                        f"> _Part number_: {kb['pn']}\n" \
                        f"> _Name_: {kb['name']}\n" \
                        f"> _Shorthand_: {kb['shorthand']}\n" \
                        f"> _Layout_: {kb['layout']}\n" \
                        f"> _Date First Seen_: {kb['date']}\n" \
                        f"\n"

        if hits > 0:
            response += f'Plus an additional {hits} results.\n\n'

        response += "You can type `!kbdb [part number]` to find out more about a specific keyboard.\n"
        await context.send(response)

        response = 'To learn how to search efficiently, see https://sharktastica.co.uk/kb_db_help.php#SearchingGuide'
        await context.send(response)

        response = 'Learn about where this data came from: https://sharktastica.co.uk/about.php#Sources'
        await context.send(response)

@bot.event
async def on_raw_reaction_add(payload):
    """Called when a discord user adds a reaction to a message"""

    # If it's the bot adding a reaction, igonre it
    if payload.member.id == bot.user.id:
        return

    # Convert emoji into something pronounceable
    emoji_name = emoji.demojize(str(payload.emoji))

    # If it's not an upvote, a downvote, or a 0 vote, ignore it
    allowed_emoji = [':up_arrow:', ':down_arrow:', ':keycap_0:']
    if emoji_name not in allowed_emoji:
        return

    # Build the ballot
    ballot = {"message_id": payload.message_id,
              "voter_id": {
                  "id": payload.member.id,
                  "handle": payload.member.display_name,
                  "discriminator": int(payload.member.discriminator)}}

    # Determine the vote
    if emoji_name == ':up_arrow:':
        ballot['vote'] = 1
    elif emoji_name == ':down_arrow:':
        ballot['vote'] = -1
    elif emoji_name == ':keycap_0:':
        ballot['vote'] = 0

    # Submit to the database
    headers = {'Content-type': 'application/json'}
    response = requests.post(f'http://{API_HOST}/vote', json=ballot, headers=headers)

    if response.status_code != 201:
        # TODO: respond with real error message
        print(f"error recording vote for {ballot['voter_id']['handle']} ({ballot['voter_id']['id']})")
        print(response.content)
    return


# run the bot
bot.run(DISCORD_TOKEN)
