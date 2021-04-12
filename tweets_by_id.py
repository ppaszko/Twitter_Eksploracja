import requests
import json
import TwitterAPI
import datetime

consumer_key = 'Rtc2Q6UT6suUSRUZAOrAc7Cvy'
consumer_secret = 'HUB2y0VadL4PiAOvpWEvQAielzZEw2g5DHXwgBy3v2eLtYerJh'
access_token = '1348985626750820355-XxasjfmxmwqkTo4ktct2YKfGy3dIAS'
access_secret = 'UICiTvf4yXd6iZgJ2qp3684zHounvbtz71oDsfPmgJh5u'

# --header
# 'authorization: OAuth oauth_consumer_key="CONSUMER_API_KEY", oauth_nonce="OAUTH_NONCE", oauth_signature="OAUTH_SIGNATURE", oauth_signature_method="HMAC-SHA1", oauth_timestamp="OAUTH_TIMESTAMP", oauth_token="ACCESS_TOKEN", oauth_version="1.0"' \
#  \
api=TwitterAPI.TwitterAPI(consumer_key,consumer_secret,access_token,access_secret)
# r = api.request('statuses/show/:%d' % 1375538713233518595)
#
#
# resp=api.request("statuses/show/:1375538713233518595&tweet.fields=context_annotations")
# print(resp.text)

today=datetime.datetime.now(datetime.timezone.utc)


def write_json(new_data, filename='new_parsed_tweets.json'):
    with open(filename, 'w') as f:
        json.dump(new_data, f, indent=4)

def tweet_by_id():
    with open('tweets_id_dates_closed.json') as json_file:
        collected_tweets = json.load(json_file)

    for tweet in collected_tweets:
        id=tweet["id"]
        tweet_date=tweet['created_at']
        if (abs((datetime.datetime.strptime(tweet_date, '%a %b %d %H:%M:%S %z %Y')-today).days )<5) & (abs((datetime.datetime.strptime(tweet_date, '%a %b %d %H:%M:%S %z %Y')-today).days )>2):
            print(tweet['created_at'])
            data = (api.request('statuses/show/:%d' % id)).text
            data=json.loads(data)
            #print(tweet)
            #print(collected_tweets[:3])
            collected_tweets.pop(0)
            #print(collected_tweets[:3])
            write_json(collected_tweets, filename='parsed_tweets.json')

            # i=
            #print(data)
            try:
                if data['entities']['hashtags']:
                    # print("tweet {}", format(i))
                    # i+=1
                    single_data = {}
                    single_data['id'] = data['id']
                    single_data['created_at'] = data['created_at']
                    single_data['text'] = data['text']
                    single_data['geo'] = data['geo']
                    single_data['coordinates'] = data['coordinates']

                    if data['place']:
                        single_data['place_name'] = data['place']['name']
                        single_data['place_full_name'] = data['place']['full_name']
                        single_data['place_country'] = data['place']['country_code']
                        if data['place']['bounding_box']:
                            single_data['place_coordinates'] = data['place']['bounding_box']['coordinates'][0]
                        else:
                            single_data['place_coordinates'] = None
                    else:
                        single_data['place_name'] = None
                        single_data['place_full_name'] = None
                        single_data['place_country'] = None
                        single_data['place_coordinates'] = None
                    # single_data['place'] = data['place']
                    # single_data['filter_level'] = data['filter_level']
                    single_data['lang'] = data['lang']
                    #single_data['quote_count'] = data['quote_count']
                    #single_data['reply_count'] = data['reply_count']
                    single_data['retweet_count'] = data['retweet_count']
                    single_data['favorite_count'] = data['favorite_count']
                    single_data['user_id'] = data['user']['id']
                    single_data['user_name'] = data['user']['name']
                    single_data['user_description'] = data['user']['description']
                    single_data['user_location'] = data['user']['location']
                    single_data['user_created_at'] = data['user']['created_at']
                    single_data['user_followers_count'] = data['user']['followers_count']
                    single_data['user_friends_count'] = data['user']['friends_count']
                    single_data['user_favourites_count'] = data['user']['favourites_count']
                    single_data['user_statuses_count'] = data['user']['statuses_count']
                    hashtags_list = []
                    for hashtag in data['entities']['hashtags']:
                        hashtags_list.append(hashtag['text'])

                    single_data['hashtags_list'] = hashtags_list

                    with open('new_parsed_tweets.json') as json_file:
                        parsed_tweets = json.load(json_file)
                        parsed_tweets.append(single_data)

                    write_json(parsed_tweets)
            except:
                pass

while True:
    try:
        tweet_by_id()
    except:
        tweet_by_id()
