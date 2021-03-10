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

# Set version number
VERSION_NUMBER = "0.8.4"

# Load environment variables from .env file
load_dotenv()

# Set constants from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
API_HOST = os.getenv('API_HOST')

# Initialise the bot
bot = commands.Bot(command_prefix='?')

# Link source repo command
@bot.command(pass_context = True, aliases=['src'])
async def source(cxt):
    """Gives a link to cappybot's GitHub repo"""
    await cxt.send(f'https://github.com/SharktallicA/cappybot')

# Display version command
@bot.command(pass_context = True, aliases=['ver'])
async def version(cxt):
    """Displays cappybot's version number"""
    await cxt.send(f'cappybot {VERSION_NUMBER} by <@!232598411654725633> (based on clackbot 0.8 by <@!572963354902134787>)')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('```Command not found, please use the ?help command to find out what commands are supported.```')
        return
    raise error

# run the bot
bot.run(DISCORD_TOKEN)