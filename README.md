# cappybot
Shark's cappybot is my adaptation of doopqoob's (https://github.com/doopqoob) clackbot with community features removed (temporarily) but eventually featuring additional database functionality and tighter integration with my website (https://sharktastica.co.uk) and deskthority wiki.

## Setting up

### Requirements
cappybot should run on either Windows or Linux fine after installing the required pip packages: 

    pip3 install -r requirements.txt

On Linux, you will also need to install `ffmpeg`.

### .env file
cappybot looks for a .env file containing a Discord API token in the format:

    DISCORD_TOKEN=your_token_here

### Running cappybot
Windows:

    py cappybot.py
Linux:

    python3 cappybot.py

## Commands
cappybot uses '?' as its command prefix.
### Searching
* ?docs - Searches Admiral Shark's Keebs documents database with given query
* ?dt - Searches deskthority wiki with given query
* ?fccid - Searches FCC database for given FCC ID number
* ?kbfru - Queries Admiral Shark's Keebs keyboard database by FRU number
* ?kbpn - Queries Admiral Shark's Keebs keyboard database by part number (aliases: ?kbdb, !kbdb)
* ?kbsearch - Searches Admiral Shark's Keebs keyboard database with given query (aliases: !kbsearch)
### Misc
* ?source - gives a link to cappybot's GitHub repo (aliases: ?src)
* ?version - displays cappybot's version number (aliases: ?ver)