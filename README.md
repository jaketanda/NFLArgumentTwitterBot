# NFL Argument Twitter Bot
A bot to have civil discussions with heated NFL fans on Twitter.

If you use this bot, it will probably be banned for spam... :(
    But hey, it's pretty funny while it lasts

## How it works

This bot listens for posts by Twitter accounts determined in `twitterIds.json`. Usually, I would have it listen for sports media accounts like @NFL, or @PFF. To see the id of a Twitter account use [this tool](https://tweeterid.com/). Simply add that ID to the `twitterIds.json` file to start listening for tweets from that account

If ANY of their posts contain a player name in `players.json`, then the bot will respond with a phrase from `phrases.json`, replacing `PLAYERNAME` with the player's actual name.

If someone responds to our bot, the bot will wait a little bit, and then respond to the user with a response from `responses.json`

Add whatever phrases and replies to the json, and have fun!

Note: I made this when I was pretty new to Python3, so it might not work and it might suck. I'm working on a new version of this, so hopefully that should work better. Until then... this.

Also note: This bot was made for fun and not to cause serious harm or trouble with anyone it interacts with. Don't be too mean to these passionate fans on Twitter :)