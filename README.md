# cappybot
Shark's cappybot is my adaptation of doopqoob's (https://github.com/doopqoob) clackbot with community features removed (temporarily) but eventually featuring additional database functionality and tighter integration with my website (https://sharktastica.co.uk) and deskthority wiki.

## Setting up

### Installing the Requirements
You should install the required pip packages by typing:

    $ pip3 install -r requirements.txt

You will also need to install _ffmpeg_.

### .env file
cappybot looks for a .env file containing a Discord API token in the format:

    DISCORD_TOKEN=your_token_here

### Running cappybot
Windows:

    py cappybot.py
Linux:

    python3 cappybot.py

## Commands
cappybot uses '?' as its command prefix. List of current commands:
* ?dt - Searches deskthority wiki with given query
* ?kbfru - Queries Admiral Shark's Keebs keyboard database by FRU number
* ?kbpn - Queries Admiral Shark's Keebs keyboard database by part number (aliases: ?kbdb, !kbdb)
* ?kbsearch - Searches Admiral Shark's Keebs keyboard database with given query (aliases: !kbsearch)
* ?source - gives a link to cappybot's GitHub repo (aliases: ?src)
* ?version - displays cappybot's version number (aliases: ?ver)