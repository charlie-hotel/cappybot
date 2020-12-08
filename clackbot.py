import discord
import emoji
import os
import random
import re
import requests

from discord.ext import commands
from dotenv import load_dotenv
from uuid import UUID

# Set version number
VERSION_NUMBER = "0.5.2"

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

    # Extract only the first element of the result
    result = result[0]

    # Handle situation where no results are returned
    if result['success'] is False:
        message = f"ERROR: Part number {part_num} not found in database.\n"
        message += "Would you like to add it to the database? Just visit\n"
        message += f"https://sharktastica.co.uk/kb_db_sub.php?pn={part_num}"
        await context.send(message)
        return

    # Take out 'success' -- there's no corresponding key in the fields_dict and no need for it anymore
    del result['success']

    # Build the response
    response = f"Here's what I found about part {part_num}:\n"
    for key in result.keys():
        if result[key] is not None:
            response += f'**{fields_dict[key]}:** {result[key]}\n'
    response += ('-' * 10) + '\n'
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

    # Query the DB
    result = requests.get(url)

    # Convert JSON into a python data structure
    result = result.json()

    # Handle situation where no results are returned
    if result[0]['success'] is False:
        message = f'ERROR: Could not find "{query}" in database.'
        await context.send(message)
        return

    # Build the response
    response = f"Here's what I found for _{query}_:\n"

    # Iterate through each keyboard in result.
    for index, kb in enumerate(result):
        response += f"> {index + 1}:\n" \
                    f"> _Part number_: {kb['pn']}\n" \
                    f"> _Name_: {kb['name']}\n" \
                    f"> _Shorthand_: {kb['shorthand']}\n" \
                    f"> _Layout_: {kb['layout']}\n" \
                    f"> _Date First Seen_: {kb['date']}\n" \
                    f"\n"

    response += "You can type `!kbdb [part number]` to find out more!\n"
    await context.send(response)

    response = 'Learn about where this data came from: https://sharktastica.co.uk/about.php#Sources'
    await context.send(response)

    response = 'To learn how to search efficiently, see https://sharktastica.co.uk/kb_db_help.php#SearchingGuide'
    await context.send(response)


@bot.command(name='quote')
async def get_quote(context, *args):
    """Get a quote from the database."""
    # Get quote ID, if any, as first argument
    quote_id = None
    if len(args) == 1:
        quote_id = args[0]

    headers = {'Content-type': 'application/json'}
    response = None
    if quote_id:
        # Validate input as a valid version 4 UUID before continuing
        try:
            UUID(quote_id, version=4)
        except ValueError:
            await context.send("Invalid quote ID")
            return

        # Get quote
        params = {"id": quote_id}
        response = requests.get(f'http://{API_HOST}/getquote', params=params, headers=headers)
    else:
        response = requests.get(f'http://{API_HOST}/getquote', headers=headers)

    if response.status_code == 404:
        await context.send("Quote not found")
        return

    # parse the JSON into a python object
    quote = response.json()

    # assemble the text we're going to send to discord
    quote_text = ""

    for line in quote['quote']:
        quote_text += "> " + line + "\n"

    quote_text += "said by <@!" + str(quote['said_by']['id']) + ">\n"
    quote_text += "added " + quote['added_at'] + " by <@!" + str(quote['added_by']['id']) + ">\n"
    quote_text += "id " + quote['id'] + "\n"
    quote_text += "score: " + str(quote['score'])

    # and send it off!
    message = await context.send(quote_text)

    # make note of the message id to track voting
    params = {"message_id": message.id,
              "quote_id": quote['id']}
    print(params)
    response = requests.get(f'http://{API_HOST}/addvotemessage', params=params, headers=headers)

    if response.status_code != 201:
        print(response.status_code)
        print(response.content)
        await context.send("Something went wrong preparing this quote for voting.")
        return

    # add voting buttons
    emoji_desc = ':up_arrow:'
    emoji_unicode = emoji.emojize(emoji_desc, use_aliases=True)
    await message.add_reaction(emoji_unicode)

    emoji_desc = ':down_arrow:'
    emoji_unicode = emoji.emojize(emoji_desc, use_aliases=True)
    await message.add_reaction(emoji_unicode)

    emoji_desc = ':keycap_0:'
    emoji_unicode = emoji.emojize(emoji_desc, use_aliases=True)
    await message.add_reaction(emoji_unicode)


@bot.command(name='delquote')
async def del_quote(context, *args):
    """Delete a quote from the database."""
    # Get quote ID, if any, as first argument
    quote_id = None
    if len(args) == 1:
        quote_id = args[0]

    if not quote_id:
        await context.send("You must provide a quote ID.")
        return

    # Validate input as a valid version 4 UUID before continuing
    try:
        UUID(quote_id, version=4)
    except ValueError:
        await context.send("Invalid quote ID")
        return

    # Get quote
    params = {"id": quote_id}
    headers = {'Content-type': 'application/json'}
    response = requests.get(f'http://{API_HOST}/getquote', params=params, headers=headers)

    print(response.json())

    quote = response.json()

    if 'added_by' not in quote:
        await context.send("Invalid quote ID")
        return

    # Make sure the user is authorized to delete the quote
    # print(context.author.top_role.name)
    if context.author.top_role.name != "Keyboard Lords":
        if quote['added_by']['id'] != context.author.id and quote['said_by']['id'] != context.author.id:
            await context.send("Only the person who submitted the quote, the person named in the quote, " +
                               f"or an administrator may delete quote {quote_id}")
            return

    # Delete the quote
    response = requests.get(f'http://{API_HOST}/delquote', params=params, headers=headers)

    if response.status_code == 200:
        await context.send("Successfully deleted quote " + quote_id)
        return
    else:
        await context.send("Something went wrong deleting quote " + quote_id)
        return


# Add a quote with !addquote
@bot.event
async def on_message(message):
    """Examine messages to see whether they meet the syntax for adding a quote"""

    # If the following isn't run, then this event sucks up all commands and doesn't let them run (thanks, discord.py?)
    await bot.process_commands(message)

    # TODO: there has to be a way to do this whole match-and-find-repeated-subsequences thing with one operation instead
    # of all the lines that follow
    match = re.match(r'^(>\s.+\n)<@!(\d+)>\s+!addquote$', message.content, re.DOTALL)

    if not match:
        return

    # match group 0 is the quote content, match group 1 is the user being quoted
    raw_quote = match.groups()[0]
    quoted_user_id = int(match.groups()[1])

    # split up the raw quote by linefeed
    split_quote = raw_quote.split('\n')

    # remove the last item if it is an empty string
    if split_quote[-1] == "":
        split_quote.pop()

    # Build the quote object we will submit to the database
    quote = {}
    quote['added_by'] = {}
    quote['added_by']['id'] = message.author.id
    quote['added_by']['handle'] = message.author.name
    quote['added_by']['discriminator'] = int(message.author.discriminator)

    quoted_user = bot.get_user(quoted_user_id)
    quote['said_by'] = {}
    quote['said_by']['id'] = quoted_user.id
    quote['said_by']['handle'] = quoted_user.name
    quote['said_by']['discriminator'] = int(quoted_user.discriminator)

    quote['quote'] = []
    for line in split_quote:
        quote['quote'].append(line[2:])

    # Submit to the database
    headers = {'Content-type': 'application/json'}
    response = requests.post(f'http://{API_HOST}/addquote', json=quote, headers=headers)

    # Did the quote get added successfully?
    if response.status_code != 201:
        await message.channel.send("Something went wrong adding your quote.")
        return

    response = response.json()

    # Is the response a valid uuid?
    try:
        UUID(response['id'], version=4)
    except ValueError:
        # If not, failure.
        await message.channel.send("Something went wrong adding your quote.")
        return

    rebuilt_quote = ""
    # if so, success!
    for line in quote['quote']:
        rebuilt_quote += '> ' + line + '\n'

    rebuilt_quote += "said by <@!" + str(quote['said_by']['id']) + ">\n"
    rebuilt_quote += "added by <@!" + str(quote['added_by']['id']) + ">\n"
    rebuilt_quote += "id " + response['id'] + "\n"
    rebuilt_quote += "score: 0"

    quote_message = await message.channel.send(rebuilt_quote)

    # make note of the message id to track voting
    params = {"message_id": quote_message.id,
              "quote_id": response['id']}
    print(params)
    response = requests.get(f'http://{API_HOST}/addvotemessage', params=params, headers=headers)

    if response.status_code != 201:
        print(response.status_code)
        print(response.content)
        await message.channel.send("Something went wrong preparing this quote for voting.")
        return

    # add voting buttons
    emoji_desc = ':up_arrow:'
    emoji_unicode = emoji.emojize(emoji_desc, use_aliases=True)
    await quote_message.add_reaction(emoji_unicode)

    emoji_desc = ':down_arrow:'
    emoji_unicode = emoji.emojize(emoji_desc, use_aliases=True)
    await quote_message.add_reaction(emoji_unicode)

    emoji_desc = ':keycap_0:'
    emoji_unicode = emoji.emojize(emoji_desc, use_aliases=True)
    await quote_message.add_reaction(emoji_unicode)

    return


@bot.event
async def on_raw_reaction_add(payload):
    """Called when a discord user adds a reaction to a message"""

    # If it's the bot adding a reaction, igonre it
    if payload.member.id == bot.user.id:
        return

    # Convert emoji into something pronounceable
    emoji_name = emoji.demojize(str(payload.emoji))
    print(emoji_name)

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
        print(f"error recording vote for {ballot['voter_id']['handle']} ({ballot['voter_id']['id']})")
        print(response.content)

    return


# run the bot
bot.run(DISCORD_TOKEN)
