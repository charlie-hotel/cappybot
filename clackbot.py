import os
import discord
import emoji

from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set constants from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Set up bot
bot = commands.Bot(command_prefix='!')


# Set up bot commands
@bot.command(name='follow')
async def join_voice(context):
    """Follow a user into a voice channel"""
    if context.author.voice is None:
        await context.send('You need to be in a voice channel to run that command here (confusing, huh?)')
        return

    channel = context.author.voice.channel
    await channel.connect()


@bot.command(name='leave')
async def leave_voice(context):
    """Leave the currently-joined voice channel"""
    await context.voice_client.disconnect()


@bot.command(name='clack')
async def play_clacking(context):
    """Play a 'clacking' sound into the currently-joined voice channel"""
    guild = context.guild
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
    audio_source = discord.FFmpegPCMAudio('clacking.wav')

    if voice_client is None:
        return

    if not voice_client.is_playing():
        voice_client.play(audio_source, after=None)


@bot.command(name='stop')
async def stop_clacking(context):
    guild = context.guild
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=guild)
    if voice_client is None:
        return

    if voice_client.is_playing():
        voice_client.stop()


@bot.command(name='poll')
async def poll(context, *args):
    """Create a poll with up to twenty-six answers (good lord)"""

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


# run the bot
bot.run(DISCORD_TOKEN)