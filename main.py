import datetime
import openai
import tweepy
from datetime import date

#Retrieve keys.txt from other file
all_keys = open("keys.txt", 'r').read().splitlines()
# CAREFUL! When running from crontab; mention full path from the cronjob working directory.
# full path in Debian VM would be /home/asaussier99/scripts/on_this_day_bot/keys.txt

twitter_api_key = all_keys[0]
twitter_api_key_secret = all_keys[1]
twitter_bearer_token = all_keys[2]
twitter_access_token = all_keys[3]
twitter_access_token_secret = all_keys[4]
openai_api_key = all_keys[5]


# Connect to twitter and chatGPT apis
openai.api_key = openai_api_key

twitter_v2_client = tweepy.Client(
    bearer_token=twitter_bearer_token,
    consumer_key=twitter_api_key,
    consumer_secret=twitter_api_key_secret,
    access_token=twitter_access_token,
    access_token_secret=twitter_access_token_secret,
    return_type="Response",
    wait_on_rate_limit=False
)

today = date.today().strftime("%B %d")

request = "Tell me about an interesting event that happened on " + today + " in the past"\
          ". Format the response to optimize engagement for a twitter post. " \
          "Spell the full date. "

def get_chatgpt_response():
    # Send request to chat gpt
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=request,
        temperature=0.6,
        max_tokens=500
    )
    return response


# Need to parse response to retrieve exactly the chatgpt text completion
chatgpt_response = get_chatgpt_response().choices[0].text

#Publish tweet
tweet = twitter_v2_client.create_tweet(text=chatgpt_response)
print("Tweet sent: " + chatgpt_response)
print("Time sent: " + str(datetime.datetime.now()))




#To do: set up a CRON job in the tmux shell to have this run once a day. Remove while loop.
