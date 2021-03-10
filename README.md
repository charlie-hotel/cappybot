# cappybot
Shark's cappybot is my adaptation of doopqoob's (https://github.com/doopqoob) clackbot with community features removed (temporarily) but added database functionality and tighter integration with my website (https://sharktastica.co.uk) and eventually deskthority wiki.

## Running cappybot

### Installing the Requirements
You should install the required pip packages by typing:

    $ pip3 install -r requirements.txt

You will also need to install _ffmpeg_.

### .env file
cappybot looks for a .env file containing a Discord API token and cappybot API hostname in the format:

    DISCORD_TOKEN=your_token_here
    API_HOST=your_api_host_here

### Running cappybot
Simply run:

    python3 cappybot.py

and cappybot will run, provided you have set the appropriate API token and cappybot API hostname as detailed above.