# clackbot

Clackbot is a Discord bot designed for the /r/modelm discord server. It works together with 
[clackbot-qdb-api](https://github.com/doopqoob/clackbot-qdb-api).

## Command Reference

### Clacking
clackbot can, of course, make clacking sounds in a Discord voice channel. Simply do the following:
1. Join a voice channel.
2. type !follow to tell clackbot to follow you into the voice chanel.
3. type !clack to hear the clacking.
4. type !stop to stop the clacking if you've had enough.

### Polls
clackbot can set up a poll for users to vote on. Simply follow this syntax:

    !poll "Your question goes here?" "First answer" "Second answer" "Third answer, etc."

Be sure to quote your question and answers, or each word will be counted separately (with hilarious results).

### Quotes
#### Adding quotes
It's easy to add discord quotes to clackbot. Simply quote a user normally using discord's quote function, then type

    !addquote

and press enter.

#### Retrieving quotes
If you want to retrieve a specific quote from the db, you must know its unique id number. Just type
    
    !quote [id]
    
where _[id]_ is the quote's unique id number. If you don't know the quote's id or just want to retrieve a random quote,
type

    !quote

and press enter.

#### Upvoting and Downvoting
When displaying a quote, clackbot automatically displays voting emoji reatcions. The up arrow is for upvoting, the down 
arrow is for downvoting, and the 0 will zero out your vote for that quote. No matter how many times you appear to be 
able to vote, only the most recent vote is saved. Your most recent vote always overrides any previous vote you've made
on that quote. 

## Running clackbot
### Installing the Requirements

You should install the required pip packages by typing:

    $ pip install -r requirements.txt

You will also need to install _ffmpeg_.

### .env file
clackbot looks for a .env file containing a Discord API token and clackbot API hostname in the format:

    DISCORD_TOKEN=your_token_here
    API_HOST=your_api_host_here

### Running clackbot

Simply run:

    python3 clackbot.py

and clackbot will run, provided you have set the appropriate API token and clackbot API hostname as detailed above.