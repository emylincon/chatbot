import twitter
from selenium import webdriver
import time
import ast
import config


api = twitter.Api(consumer_key=config.consumer_key,
                  consumer_secret=config.consumer_secret,
                  access_token_key=config.access_token,
                  access_token_secret=config.access_token_secret)


def twitter_status_others(user):
    try:
        followers_count = len(api.GetFollowers(screen_name=user))
        friends_count = len(api.GetFriends(screen_name=user))
        return f"{user} have {followers_count} followers and {friends_count} friends following you on twitter"
    except Exception as e:
        return "Due to Twitter Restrictions, You have reached your lookup limit. Try again in 15 minutes"


def twitter_status():
    followers_count = len(api.GetFollowers())
    friends_count = len(api.GetFriends())
    return f"You have {followers_count} followers and {friends_count} friends following you on twitter"


def display_last_tweet(user):
    try:
        status = api.GetUserTimeline(screen_name=user)[0].text
        return status
    except Exception as e:
        return "Due to Twitter Restrictions, You have reached your lookup limit. Try again in 15 minutes"


def last_tweet():
    status = api.GetUserTimeline()[0].text
    return status


def post_tweet(tweet):
    api.PostUpdates(tweet)
    return "Tweet posted"


def display_twitter():
    # chromedriver = "C:\Program Files\chrome driver"
    # driver = webdriver.Chrome(chromedriver)
    driver = webdriver.Chrome(executable_path=r"C:\Program Files\chrome driver\chromedriver.exe")
    query = "https://twitter.com/jamesemyking"
    driver.get(query)
    time.sleep(10)


def twitter_trend():
    results = api.GetTrendsWoeid(woeid=23424975)

    reply = "Top UK Trends in Twitter: "

    for _location in results[:5]:
        location = ast.literal_eval(str(_location))
        reply += ("\n " + str(location["name"]))

    return reply

