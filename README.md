# cappybot
cappybot is a Discord bot tailored specifically for use on the r/ModelM and other Discord servers that I moderate. Based on doopqoob's (https://github.com/doopqoob) clackbot 0.8, this is a successor bot that integrates with my (Admiral Shark's Keebs) website, deskthority wiki and the FCC database to provide keyboard lookup and research capabilities. Other current or planned features include r/ModelM, r/ModelF and r/MechanicalKeyboards subreddit searching, keyboard ASMR typing playback and some basic community features.

## Setting up

### Requirements
cappybot should run on either Windows or Linux after installing Python 3, ffmpeg, and several required `pip` packages. You can automate the installation of these latter packages by running the following command, or check out the `requirements.txt` file if you want to manually install them. 

    pip3 install -r requirements.txt

### Environment
cappybot looks for the file `.env` in the local directory to get two environment variables; a Discord API token and the location of the `ffmpeg.exe` binary if you're running cappybot on Windows. You will need to create this `.env` file using the following template:

    DISCORD_TOKEN=your_token_here
    FFMPEG_WIN=your_token_here

If you're running cappybot on Linux, you can leave out the `FFMPEG_WIN` line.

### Running
Windows:

    py cappybot.py
Linux:

    python3 cappybot.py

## Commands
cappybot uses '?' as its command prefix with some '!'-prefixed alias commands supported to provide familiarity with the doopqoob's clackbot. 
### Community
* ?clack - tells cappybot to play a random buckling springs typing sample
* ?frogtip - displays a FROG TIP
* ?join - calls cappybot to your current voice channel (aliases: ?cloak, ?follow)
* ?leave - Tells cappybot to leave whatever voice channel it is in (aliases: ?decloak)
* ?stop - tells cappybot to stop playing the current typing sample
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