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
Simply run:

    python3 cappybot.py

...and cappybot will run provided you have set the appropriate API token as detailed above.

## Commands
cappybot uses '?' as its command prefix. List of current commands:
* ?kbfru - Queries SharktasticA's IBM and co keyboard database by FRU number
* ?kbpn - Queries SharktasticA's IBM and co keyboard database by part number (aliases: ?kbdb, !kbdb)
* ?source - gives a link to cappybot's GitHub repo (aliases: ?src)
* ?version - displays cappybot's version number (aliases: ?ver)