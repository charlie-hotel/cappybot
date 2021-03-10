import discord
import emoji
import os
import random
import requests

from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv
from frogtips import api as frogtips_api
from uuid import UUID

# Global variables
VERSION_NUMBER = "0.8.5"
SHARK_UID = "<@!232598411654725633>"
DOOP_UID = "<@!572963354902134787"

# Load environment variables from .env file
load_dotenv()

# Set constants from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
API_HOST = os.getenv('API_HOST')

# Initialise the bot
bot = commands.Bot(('?', '!k'))



# Catch command not found error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('```ERROR: Command not found - please use the ?help command to find out what commands are supported.```')
        return
    raise error



# Link source repo command
@bot.command(pass_context = True, aliases=['src'])
async def source(cxt):
    """Gives a link to cappybot's GitHub repo"""
    await cxt.send(f'https://github.com/SharktallicA/cappybot')

# Display version command
@bot.command(pass_context = True, aliases=['ver'])
async def version(cxt):
    """Displays cappybot's version number"""
    await cxt.send(f'cappybot {VERSION_NUMBER} by {SHARK_UID} (based on clackbot 0.8 by {DOOP_UID})')


@bot.command(pass_context = True)
async def kbfru(cxt, fru_num=None):
    """Queries SharktasticA's IBM and co keyboard database by FRU number"""
    # Make sure the user has entered a part number
    if fru_num is None:
        await cxt.send("```ERROR: no or invalid FRU number provided.```")
        return

    # These are all the fields we're going to request from the database
    # (and their long names for when we display the data in chat)
    fields_dict = {'pn': "Part Number",
                   'fru': "FRU Number",
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
    url = f'https://sharktastica.co.uk/kb_db_req.php?fru={fru_num}&dat=JSON&fields={fields}'

    # Query the DB
    result = requests.get(url)

    # Convert JSON into a python data structure
    result = result.json()

    # Handle situation where no results are returned
    if result['hits'] == 0:
        message = f"FRU number {fru_num} not found in database.\n"
        message += "Would you like to add it to the database? Just visit\n"
        message += f"<https://sharktastica.co.uk/kb_db_sub.php?pn={fru_num}>"
        await cxt.send(message)
        return

    # Build the response
    response = f"Here's what I found about FRU {fru_num}:\n\n"
    for kb in result['results']:
        link = kb.pop('link', None)
        for key in kb.keys():
            if kb[key] is not None:
                response += f'**{fields_dict[key]}:** {kb[key]}\n'
        if link is not None:
            response += f'\n**Permalink:** <{link}>\n'
    response += '\n'
    response += 'Learn about where this data came from: <https://sharktastica.co.uk/about.php#Sources>'

    # aaand send it off!
    await cxt.send(response)

@bot.command(pass_context = True, aliases=['kbdb', 'bdb'])
async def kbpn(cxt, part_num=None):
    """Queries SharktasticA's IBM and co keyboard database by part number"""
    # Make sure the user has entered a part number
    if part_num is None:
        await cxt.send("```ERROR: no or invalid part number provided.```")
        return

    # These are all the fields we're going to request from the database
    # (and their long names for when we display the data in chat)
    fields_dict = {'pn': "Part Number",
                   'fru': "FRU Number",
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
        message = f"Part number {part_num} not found in database.\n"
        message += "Would you like to add it to the database? Just visit\n"
        message += f"<https://sharktastica.co.uk/kb_db_sub.php?pn={part_num}>"
        await cxt.send(message)
        return

    # Build the response
    response = f"Here's what I found about P/N {part_num}:\n\n"
    for kb in result['results']:
        link = kb.pop('link', None)
        for key in kb.keys():
            if kb[key] is not None:
                response += f'**{fields_dict[key]}:** {kb[key]}\n'
        if link is not None:
            response += f'\n**Permalink:** <{link}>\n'
    response += '\n'
    response += 'Learn about where this data came from: <https://sharktastica.co.uk/about.php#Sources>'

    # aaand send it off!
    await cxt.send(response)



# run the bot
bot.run(DISCORD_TOKEN)