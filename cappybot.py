import discord
import os
import random
import requests

from var_dump import var_dump
from discord.ext import commands
from discord.ext.commands import CommandNotFound
from dotenv import load_dotenv
from frogtips import api as frogtips_api
from uuid import UUID
from xml.etree.ElementTree import fromstring, ElementTree
from utils import *

# Global variables
VERSION_NUMBER = "0.8.14"
SHARK_UID = "<@!232598411654725633>"
DOOP_UID = "<@!572963354902134787>"

# Load environment variables from .env file
load_dotenv()

# Set constants from environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Initialise the bot
help_command = commands.DefaultHelpCommand(no_category = 'Misc')
bot = commands.Bot(('?', '!k'), help_command = help_command)



# Catch command not found error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('```ERROR: Command not found - please use the ?help command to find out what commands are supported.```')
        return
    raise error



# About cappybot command
@bot.command(pass_context = True, aliases=['abt'])
async def about(cxt):
    """Displays cappybot's about page"""
    await cxt.send(f"cappybot is a Discord bot tailored specifically for use on the r/ModelM and other Discord servers moderated by {SHARK_UID}. Based on {DOOP_UID}'s clackbot 0.8, this is a successor bot developed by {SHARK_UID} that integrates with Admiral Shark's Keebs website, deskthority wiki and the FCC database to provide keyboard lookup and research capabilities. Other planned features include r/ModelM, r/ModelF and r/MechanicalKeyboards subreddit searching, keyboard ASMR typing playback and some basic community features.")

# Link source repo command
@bot.command(pass_context = True, aliases=['src'])
async def source(cxt):
    """Gives a link to cappybot's GitHub repo"""
    await cxt.send(f'<https://github.com/SharktallicA/cappybot>')

# Display version command
@bot.command(pass_context = True, aliases=['ver'])
async def version(cxt):
    """Displays cappybot's version number"""
    await cxt.send(f'cappybot {VERSION_NUMBER} by {SHARK_UID} (based on clackbot 0.8 by {DOOP_UID})')



class Community(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # FROG TIP command
    @commands.command(cxt = True)
    async def frogtip(self, cxt, tip_id=None):
        """Displays a FROG TIP"""
        if tip_id is None:
            tip = frogtips_api.Tips().get_next_tip()
        else:
            tip_id = int(tip_id)
            tip = frogtips_api.Tip(tip_id)

        formatted_tip = tip.get_formatted_tip()
        formatted_tip += '\n'
        formatted_tip += f"<https://frog.tips/#{str(tip.get_id())}>"

        await cxt.send(formatted_tip)



class Researching(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Keyboard documents search command
    @commands.command(pass_context = True)
    async def docs(self, cxt, *args):
        """Searches Admiral Shark's Keebs documents database with given query"""

        # The query is the first argument given
        # (Shark's database takes care of figuring out
        # what query type this is)
        query = args[0]
        result_count = 5

        # Build the URL
        url = f'https://sharktastica.co.uk/documents_req.php?name={query}&dat=JSON&fields=*&c={result_count}'

        # Because the query takes a long time to run,
        # indicate to the user that something is happening.
        await cxt.send(f"Searching Admiral Shark's Keebs for \"{query}\". Just a moment...")

        # display the 'typing' indicator while searching for user's query
        async with cxt.channel.typing():
            # Query the DB
            result = requests.get(url)

            # Convert JSON into a python data structure
            result = result.json()

            # Handle situation where no results are returned
            if result['success'] is False:
                message = f'```ERROR: {result["message"]}```'
                await cxt.send(message)
                return

            # Handle other situation where no results are returned
            if result['hits'] == 0:
                message = f'No results for "{query}" found in Admiral Shark\'s Keebs'
                await cxt.send(message)
                return

            # Build the response
            response = f"Here's what I found for \"{query}\":\n"

            hits = result['hits']

            # Iterate through each keyboard in result.
            for index, doc in enumerate(result['results']):
                hits -= 1
                name = doc['name']
                ed = doc['ed']
                if (ed == None):
                    ed = "1"
                src = doc['src']
                if (src == None):
                    src = "source unknown"
                date = date_2_str(doc['date'])
                ref = doc['ref']
                if (ref == None):
                    ref = "unknown"
                link = doc['link']
                response += f"> **{index + 1}:** " \
                            f" {name}, " \
                            f" Ed. {ed}, " \
                            f" {src}, " \
                            f" {date}, " \
                            f" ref {ref}, " \
                            f" {link} \n" \

            if hits > 0:
                response += f'\nPlus an additional {hits} results.\n\n'

            await cxt.send(response)

    # deskthority wiki search command
    @commands.command(pass_context = True)
    async def dt(self, cxt, query=None):
        """Searches deskthority wiki with given query"""

        # Make sure the user has entered a query
        if query is None:
            await cxt.send("```ERROR: no or invalid query provided.```")
            return

        # Assemble components for a MediaWiki search request
        URL = "https://deskthority.net/wiki/api.php"
        TITLE_PARAMS = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srwhat": "title",
            "srsearch": query,
            "utf8": "",
        }
        TEXT_PARAMS = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srwhat": "text",
            "srsearch": query,
            "utf8": "",
        }

        # Because the query takes a long time to run,
        # indicate to the user that something is happening.
        await cxt.send(f"Searching deskthority wiki for \"{query}\". Just a moment...")

        # display the 'typing' indicator while searching for user's query
        async with cxt.channel.typing():
            # Get title search results
            req_title = requests.get(url=URL, params=TITLE_PARAMS)
            rsts_title = req_title.json()

            # Get text search results
            req_text = requests.get(url=URL, params=TEXT_PARAMS)
            rsts_text = req_text.json()
                
            # Get number of hits
            hits = rsts_title["query"]["searchinfo"]["totalhits"] + rsts_text["query"]["searchinfo"]["totalhits"]

            if hits == 0:
                message = f'No results for "{query}" found in deskthority wiki'
                await cxt.send(message)
                return

            # Output results
            response = ""
            if rsts_title["query"]["searchinfo"]["totalhits"] > 0:
                response = f"Here's the page **title** matches I found for \"{query}\":\n"
                c = 5
                for i, page in enumerate(rsts_title["query"]["search"]):
                    if (c == 0):
                        break
                    c -= 1
                    hits -= 1
                    response += f"> **{i + 1}:** " \
                                f" {page['title']}, " \
                                f" {page['wordcount']} words, " \
                                f" <https://deskthority.net/wiki/{page['title'].replace(' ', '_')}>\n" \
            
            if rsts_text["query"]["searchinfo"]["totalhits"] > 0:
                response += f"Here's the page **text** matches I found for \"{query}\":\n"
                c = 5
                for i, page in enumerate(rsts_text["query"]["search"]):
                    if (c == 0):
                        break
                    c -= 1
                    hits -= 1
                    response += f"> **{i + 1}:** " \
                                f" {page['title']}, " \
                                f" {page['wordcount']} words, " \
                                f" <https://deskthority.net/wiki/{page['title'].replace(' ', '_')}>\n" \

            if hits > 0:
                response += f'\nPlus an additional {hits} results you can see by going to <https://deskthority.net/wiki/index.php?search={query.replace(" ", "+")}&title=Special%3ASearch&fulltext=1>.'
            
            await cxt.send(response)

    # FCC ID search command
    @commands.command(pass_context = True)
    async def fccid(self, cxt, query=None):
        """Searches FCC database for given FCC ID number"""

        # Make sure the user has entered a query
        if query is None:
            await cxt.send("```ERROR: no or invalid query provided.```")
            return

        # Assemble components for a FCC ID database search request
        URL = "https://apps.fcc.gov/OETLabServices/getFCCIDList"
        PARAMS = {
            "fccId": query
        }

        # Because the query takes a long time to run,
        # indicate to the user that something is happening.
        await cxt.send(f"Searching FCC database for \"{query}\". Just a moment...")

        # display the 'typing' indicator while searching for user's query
        async with cxt.channel.typing():
            # Get search results
            req = requests.get(url=URL, params=PARAMS)
            raw = req.content
            
            # Parse raw response into 'objectified' XML tree
            tree = ElementTree(fromstring(raw))
            root = tree.getroot()

            # Count results
            hits = 0
            for child in root:
                hits += 1

            # Check for results
            if hits == 0:
                message = f'No results for "{query}" found in the FCC database'
                await cxt.send(message)
                return

            # Process results
            response = f"Here's what I found for \"{query}\":\n"
            c = 5
            for child in root:
                if (c == 0):
                    break

                c -= 1
                hits -= 1
                response += f"> **{5 - c}:** " \
                            f"{child[4].text}, " \
                            f"{child[6].text}, " \
                            f"{child[5].text}, " \
                            f"{child[1].text}, " \
                            f"<http://fcc.io/{child[4].text}>\n" \
            
            if hits > 0:
                response += f'\nPlus an additional {hits} results.'
            
            await cxt.send(response)

    # FRU number keyboard search command
    @commands.command(pass_context = True)
    async def kbfru(self, cxt, fru_num=None):
        """Queries Admiral Shark's Keebs keyboard database by FRU number"""
        # Make sure the user has entered a FRU number
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
            message = f"FRU number {fru_num} was not found in the database. If you would like to add it to the database, just visit <https://sharktastica.co.uk/kb_db_sub.php?pn={fru_num}>."
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

    # Part number keyboard search command
    @commands.command(pass_context = True, aliases=['kbdb', 'bdb'])
    async def kbpn(self, cxt, part_num=None):
        """Queries Admiral Shark's Keebs keyboard database by part number"""
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
            message = f"Part number {part_num}  was not found in the database. If you would like to add it to the database, just visit <https://sharktastica.co.uk/kb_db_sub.php?pn={part_num}>."
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

    # General keyboard search command
    @commands.command(pass_context = True, aliases=['bsearch'])
    async def kbsearch(self, cxt, *args):
        """Searches Admiral Shark's Keebs keyboard database with given query"""

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
        await cxt.send(f"Searching Admiral Shark's Keebs for \"{query}\". Just a moment...")

        # display the 'typing' indicator while searching for user's query
        async with cxt.channel.typing():
            # Query the DB
            result = requests.get(url)

            # Convert JSON into a python data structure
            result = result.json()

            # Handle situation where no results are returned
            if result['success'] is False:
                message = f'```ERROR: {result["message"]}```'
                await cxt.send(message)
                return

            # Handle other situation where no results are returned
            if result['hits'] == 0:
                message = f'No results for "{query}" found in Admiral Shark\'s Keebs'
                await cxt.send(message)
                return

            # Build the response
            response = f"Here's what I found for \"{query}\":\n"

            hits = result['hits']

            # Iterate through each keyboard in result.
            for index, kb in enumerate(result['results']):
                hits -= 1
                response += f"> **{index + 1}:** " \
                            f" Part number {kb['pn']}, " \
                            f" {kb['name']}, " \
                            f" {kb['shorthand']}, " \
                            f" {kb['layout']}, " \
                            f" {kb['date']}\n" \

            if hits > 0:
                response += f'\nPlus an additional {hits} results.\n\n'

            response += "You can type `?kbpn [part number]` to find out more about a specific keyboard. To learn how to search efficiently, see <https://sharktastica.co.uk/kb_db_help.php#SearchingGuide>. Learn about where this data came from, see <https://sharktastica.co.uk/about.php#Sources>"
            await cxt.send(response)



class Subreddits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Search r/MechanicalKeyboards command
    @commands.command(pass_context = True)
    async def rmk(self, cxt, query=None):
        """Searches the r/MechanicalKeyboards subreddit with given query"""

        # Make sure the user has entered a query
        if query is None:
            await cxt.send("```ERROR: no or invalid query provided.```")
            return

        # Assemble components for a subreddit search request
        URL = "https://www.reddit.com/r/mechanicalkeyboards/search.json"
        PARAMS = {
            "include_over_18": "off",
            "restrict_sr": "on",
            "q": query
        }
        HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"}

        # Because the query takes a long time to run,
        # indicate to the user that something is happening.
        await cxt.send(f"Searching r/MechanicalKeyboards for \"{query}\". Just a moment...")

        # display the 'typing' indicator while searching for user's query
        async with cxt.channel.typing():
            # Get search results
            req = requests.get(url=URL, params=PARAMS, headers=HEADERS)
            rsts = req.json()
                
            # Get number of hits
            hits = rsts["data"]["dist"]

            if hits == 0:
                message = f'No results for "{query}" found in r/MechanicalKeyboards'
                await cxt.send(message)
                return

            # Output results
            response = f"Here's the results I found for \"{query}\":\n"
            c = 5
            for i, post in enumerate(rsts["data"]["children"]):
                # "t3" = subreddit link, which is what we want
                if (post['kind'] != "t3"):
                    continue 
                if (c == 0):
                    break
                c -= 1
                hits -= 1
                response += f"> **{i + 1}:** " \
                            f" \"{post['data']['title']}\" " \
                            f" by u/{post['data']['author']}, " \
                            f" <https://www.reddit.com{post['data']['permalink']}>\n" \
            
            if hits > 0:
                response += f'\nPlus an additional {hits} results you can see by going to <https://www.reddit.com/r/mechanicalkeyboards/search?q={query.replace(" ", "+")}&restrict_sr=1&include_over_18=off>.'
            
            await cxt.send(response)

    # Search r/ModelF command
    @commands.command(pass_context = True)
    async def rmodelf(self, cxt, query=None):
        """Searches the r/ModelF subreddit with given query"""

        # Make sure the user has entered a query
        if query is None:
            await cxt.send("```ERROR: no or invalid query provided.```")
            return

        # Assemble components for a subreddit search request
        URL = "https://www.reddit.com/r/modelf/search.json"
        PARAMS = {
            "include_over_18": "off",
            "restrict_sr": "on",
            "q": query
        }
        HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"}

        # Because the query takes a long time to run,
        # indicate to the user that something is happening.
        await cxt.send(f"Searching r/ModelF for \"{query}\". Just a moment...")

        # display the 'typing' indicator while searching for user's query
        async with cxt.channel.typing():
            # Get search results
            req = requests.get(url=URL, params=PARAMS, headers=HEADERS)
            rsts = req.json()
                
            # Get number of hits
            hits = rsts["data"]["dist"]

            if hits == 0:
                message = f'No results for "{query}" found in r/ModelF'
                await cxt.send(message)
                return

            # Output results
            response = f"Here's the results I found for \"{query}\":\n"
            c = 5
            for i, post in enumerate(rsts["data"]["children"]):
                # "t3" = subreddit link, which is what we want
                if (post['kind'] != "t3"):
                    continue 
                if (c == 0):
                    break
                c -= 1
                hits -= 1
                response += f"> **{i + 1}:** " \
                            f" \"{post['data']['title']}\" " \
                            f" by u/{post['data']['author']}, " \
                            f" <https://www.reddit.com{post['data']['permalink']}>\n" \
            
            if hits > 0:
                response += f'\nPlus an additional {hits} results you can see by going to <https://www.reddit.com/r/modelf/search?q={query.replace(" ", "+")}&restrict_sr=1&include_over_18=off>.'
            
            await cxt.send(response)

    # Search r/ModelM command
    @commands.command(pass_context = True)
    async def rmodelm(self, cxt, query=None):
        """Searches the r/ModelM subreddit with given query"""

        # Make sure the user has entered a query
        if query is None:
            await cxt.send("```ERROR: no or invalid query provided.```")
            return

        # Assemble components for a subreddit search request
        URL = "https://www.reddit.com/r/modelm/search.json"
        PARAMS = {
            "include_over_18": "off",
            "restrict_sr": "on",
            "q": query
        }
        HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0"}

        # Because the query takes a long time to run,
        # indicate to the user that something is happening.
        await cxt.send(f"Searching r/ModelM for \"{query}\". Just a moment...")

        # display the 'typing' indicator while searching for user's query
        async with cxt.channel.typing():
            # Get search results
            req = requests.get(url=URL, params=PARAMS, headers=HEADERS)
            rsts = req.json()
                
            # Get number of hits
            hits = rsts["data"]["dist"]

            if hits == 0:
                message = f'No results for "{query}" found in r/ModelM'
                await cxt.send(message)
                return

            # Output results
            response = f"Here's the results I found for \"{query}\":\n"
            c = 5
            for i, post in enumerate(rsts["data"]["children"]):
                # "t3" = subreddit link, which is what we want
                if (post['kind'] != "t3"):
                    continue 
                if (c == 0):
                    break
                c -= 1
                hits -= 1
                response += f"> **{i + 1}:** " \
                            f" \"{post['data']['title']}\" " \
                            f" by u/{post['data']['author']}, " \
                            f" <https://www.reddit.com{post['data']['permalink']}>\n" \
            
            if hits > 0:
                response += f'\nPlus an additional {hits} results you can see by going to <https://www.reddit.com/r/modelm/search?q={query.replace(" ", "+")}&restrict_sr=1&include_over_18=off>.'
            
            await cxt.send(response)



# Add cogs to bot
bot.add_cog(Community(bot))
bot.add_cog(Researching(bot))
bot.add_cog(Subreddits(bot))

# Run the bot
bot.run(DISCORD_TOKEN)