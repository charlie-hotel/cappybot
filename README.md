# clackbot

Clackbot is a Discord bot designed for the /r/modelm discord server.

## Command Reference

### Polls
clackbot can set up a poll for users to vote on. Simply follow this syntax:

    !poll "Your question goes here?" "First answer" "Second answer" "Third answer, etc."

Be sure to quote your question and answers, or each word will be counted separately (with hilarious results).

### Clacking
clackbot can, of course, make clacking sounds in a Discord voice channel. Simply do the following:
1. Join a voice channel.
2. type !follow to tell clackbot to follow you into the voice chanel.
3. type !clack to hear the clacking.
4. type !stop to stop the clacking if you've had enough.

## Running clackbot
### Installing the Requirements

You should install the required pip packages by typing:

    $ pip install -r requirements.txt

You will also need to install _ffmpeg_.

### .env file
clackbot looks for a .env file containing a Discord API token in the format:

    DISCORD_TOKEN=your_token_here

### Running clackbot

Simply run:

    python3 clackbot.py

and clackbot will run, provided you have set the appropriate API token as detailed above.