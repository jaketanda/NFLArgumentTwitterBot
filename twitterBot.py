import tweepy
import time
import json
import random
from keys import keys
from tweepy import Stream
from tweepy.streaming import StreamListener

statusList = []

class StdOutListener(StreamListener):
    def on_status(self, status):
        try:
            status.retweeted_status
            return True
        except:
            with open('twitterIds.json') as json_file:
                data = json.load(json_file)
                    
                if str(status.user.id) in data['twitterIds']:
                    print(f"Adding tweet by {status.user.name} to statusList")
                    statusList.append(status)
        return True

    def on_error(self, status):
        return False

def doesReply(pctChance):
    if (pctChance > random.randint(0,99)):
        return True
    return False

def createApi():
    CONSUMER_KEY = keys['consumer_key']
    CONSUMER_SECRET = keys['consumer_secret']
    ACCESS_TOKEN = keys['access_token']
    ACCESS_TOKEN_SECRET = keys['access_token_secret']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")

    return api

def createStream(api, stream):
    with open('twitterIds.json') as json_file:
        data = json.load(json_file)
        twitterHandlesStr = ""
        for p in data['twitterIds']:
            twitterHandlesStr += p + ","

        twitterHandlesStr = twitterHandlesStr[:-1]

    stream.filter(follow=[twitterHandlesStr], is_async=True, stall_warnings=True)

def check_mentions(api, since_id):
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
    
        if (doesReply(80)):
            time.sleep(60)
            print(f"Replying to {tweet.user.name}")

            with open('replies.json') as reply_file:
                replies = json.load(reply_file)["replies"]
                api.update_status(
                    status=f"@{tweet.user.screen_name} " + replies[random.randint(0, len(replies)-1)],
                    in_reply_to_status_id=tweet.id,
                )

    return new_since_id

def checkNewTweets(api):
    for status in statusList:
        with open('players.json') as json_players:
            playerNames = json.load(json_players)["players"]

            for playerName in playerNames:
                if playerName.lower() in status.text.lower():
                    if doesReply(30):
                        time.sleep(60)                
                        print(f"Commenting on post by {status.user.name}")

                        with open('phrases.json') as phrases_json:
                            phrases = json.load(phrases_json)["phrases"]
                            api.update_status(
                                status=f"@{status.user.screen_name} " + phrases[random.randint(0, len(phrases)-1)].replace("PLAYERNAME", playerName),
                                in_reply_to_status_id=status.id,
                            )
                        
                        time.sleep(30)

                    break

    statusList.clear()

def main():
    api = createApi()
    stream = Stream(auth=api.auth, listener=StdOutListener())
    createStream(api, stream)
    while True:
        sinceIdFile = open(r"Id.txt", "r")
        sinceId = int(sinceIdFile.read())
        sinceIdFile.close()
        sinceId = check_mentions(api, sinceId)
        sinceIdFile = open(r"Id.txt", "w")
        sinceIdFile.write(str(sinceId))
        sinceIdFile.close()
        checkNewTweets(api)
        time.sleep(60)

main()

