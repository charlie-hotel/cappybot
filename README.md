# cappybot
cappybot is a Discord bot tailored specifically for use on the r/ModelM and other Discord servers that I moderate. Based on doopqoob's (https://github.com/doopqoob) clackbot 0.8, this is a successor bot that integrates with my (Admiral Shark's Keebs) website, deskthority wiki and the FCC database to provide keyboard lookup and research capabilities. Other current or planned features include r/ModelM, r/ModelF and r/MechanicalKeyboards subreddit searching, keyboard ASMR typing playback and some basic community features.

## Setting up

### Requirements
cappybot should run on either Windows or Linux after installing Python 3 and several required pip packages. You can automate the installation of these packages by running the following command, or check out the `requirements.txt` file if you want to manually install them. 

    pip3 install -r requirements.txt

On Linux, you will also need to install `ffmpeg`.

### .env file
cappybot looks for a .env file containing a Discord API token in the format:

    DISCORD_TOKEN=your_token_here

### Running
Windows:

    py cappybot.py
Linux:

    python3 cappybot.py

## Commands
cappybot uses '?' as its command prefix with some '!'-prefixed alias commands supported to provide familiarity with the doopqoob's clackbot. 
### Community
* ?frogtip - displays a FROG TIP
### Researching
* ?docs - searches Admiral Shark's Keebs documents database with given query
* ?dt - searches deskthority wiki with given query
* ?fccid - searches FCC database for given FCC ID number
* ?kbfru - queries Admiral Shark's Keebs keyboard database by FRU number
* ?kbpn - queries Admiral Shark's Keebs keyboard database by part number (aliases: ?kbdb, !kbdb)
* ?kbsearch - searches Admiral Shark's Keebs keyboard database with given query (aliases: !kbsearch)
* ?sharks - Searches Admiral Shark's Keebs articles and topics of interest with given query
### Subreddits
* ?rmk - searches the r/MechanicalKeyboards subreddit with given query
* ?rmodelf - searches the r/ModelF subreddit with given query
* ?rmodelm - searches the r/ModelM subreddit with given query
### Misc
* ?about - displays cappybot's about page (aliases: ?abt)
* ?source - gives a link to cappybot's GitHub repo (aliases: ?src)
* ?version - displays cappybot's version number (aliases: ?ver)