# %% md

# Analiza rozmów na temat szczepionek Covid na Twitterze


# %%

import tweepy
import json
import pandas as pd
import datetime

from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

# %%

consumer_key = 'Rtc2Q6UT6suUSRUZAOrAc7Cvy'
consumer_secret = 'HUB2y0VadL4PiAOvpWEvQAielzZEw2g5DHXwgBy3v2eLtYerJh'
access_token = '1348985626750820355-XxasjfmxmwqkTo4ktct2YKfGy3dIAS'
access_secret = 'UICiTvf4yXd6iZgJ2qp3684zHounvbtz71oDsfPmgJh5u'


# %%

class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        stream = Stream(auth, listener)
        stream.filter(track=hash_tag_list)


class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            # print(data)
            response_parser(data)
            # with open(self.fetched_tweets_filename, 'a') as tf:
            #      tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        print(status)


# functions for preparing list of hast tags
def drop_duplicates(x):
    """
  Function that drops duplicated objects withint the list.
  :Usage: Support function for read_hash_tag_list.
  """
    return list(dict.fromkeys(x))


def read_hash_tag_list(file):
    """
  Function for reading hashtag from the txt file
  and drops duplicated hash tags from the list.
  """
    hash_tag_list = []
    count = 0
    with open(file, "r") as fp:
        for line in fp:
            count += 1
            hash_tag_list.append(line.strip())
    print("before drop_duplicates", len(hash_tag_list))
    hash_tag_list = drop_duplicates(hash_tag_list)
    print("after drop_duplicates", len(hash_tag_list))
    return hash_tag_list


# %%

def write_json(new_data, filename='tweets_id_dates.json'):
    with open(filename, 'w') as f:
        json.dump(new_data, f, indent=4)


def response_parser(data):
    # with open('tweets.json') as json_file:
    #     data = json.load(json_file)
    #
    data = json.loads(data)
    #print("luj")

    if (len(data['entities']['hashtags'])>0) & ( data['user']['location'] is not None) :
        #print("tweet added")

        single_data = {}
        single_data['id'] = data['id']
        single_data['created_at'] = data['created_at']
        csv_list=[data['id'],data['created_at']]

        with open('tweets_id_dates.json') as json_file:
            parsed_tweets = json.load(json_file)
            parsed_tweets.append(single_data)

        with open('luj.csv', 'a') as csv_file:
            csv_file.write(str(data['id']))
            csv_file.write(',')
            csv_file.write(data['created_at'])
            csv_file.write('\n')

        write_json(parsed_tweets)
        #print(datetime.datetime.now().hour)
        now=datetime.datetime.now()
        if (now.hour==21):
            #json.dump(parsed_tweets,"tweets" + str(datetime.datetime.now())+".json")
            write_json(parsed_tweets,filename="tweets" + str(now.day)+"."+str(now.month) + "."+str(now.hour)+".json")

        if (now.hour==10):
            #json.dump(parsed_tweets,"tweets" + str(datetime.datetime.now())+".json")
            write_json(parsed_tweets,filename="tweets" + str(now.day)+"."+str(now.month)+ "."+str(now.hour)+".json")

        if (now.hour==15):
            #json.dump(parsed_tweets,"tweets" + str(datetime.datetime.now())+".json")
            write_json(parsed_tweets,filename="tweets" + str(now.day)+"."+str(now.month)+ "."+str(now.hour)+".json")


# %%

hash_tag_list = read_hash_tag_list("hasztag_list.txt")
print(len(hash_tag_list))

# %%


# hash_tag_list = read_hash_tag_list("/content/hash_tags.txt")
print(hash_tag_list)
fetched_tweets_filename = "tweets.json"


def listen():
    try:
        twitter_streamer = TwitterStreamer()
        auth = OAuthHandler(consumer_key, consumer_secret)
        twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)
    except:
        listen()



listen()