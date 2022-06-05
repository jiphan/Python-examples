import tweepy
import traceback
import config
import os
script_dir = os.path.dirname(__file__)
args = config.read_yaml(script_dir + '/config.yaml')

api = tweepy.API(tweepy.OAuth2BearerHandler(args['bearer_token']))
# client = tweepy.Client(args['bearer_token'])
client = tweepy.Client(
    consumer_key=args["consumer_key"],
    consumer_secret=args["consumer_secret"],
    access_token=args["access_token"],
    access_token_secret=args["access_token_secret"]
)


def parse_client(tweets):
    # https://bit.ly/36aRBpA
    media = {m["media_key"]: m for m in tweets.includes['media']}
    user = {u['id']: u for u in tweets.includes['users']}
    # print(user)

    res = {}
    for t in tweets.data:
        try:
            mm = [media[m].url for m in t.data['attachments']['media_keys']]
        except:
            mm = []
        res[t.data['id']] = {
            'text': t.data['text'],
            'created_at': t.data['created_at'],
            'user': user[int(t.data['author_id'])].username,
            'media': mm
        }

    tweet_fallback = lookup_fallback(
        [i for i in res if None in res[i]['media']])
    for i in tweet_fallback:
        res[i]['media'] = tweet_fallback[i]['media']

    return res


def lookup(tweets):
    try:
        res = client.get_tweets(
            tweets,
            expansions=["author_id", "attachments.media_keys",
                        "referenced_tweets.id"],
            media_fields=["preview_image_url", "url"],
            tweet_fields=["created_at"],
            user_auth=True
        )
    except:
        traceback.print_exc()
        res = []

    return parse_client(res)


def parse_api(tweets):
    arr = {}
    for t in tweets:
        data = t._json
        arr[data['id_str']] = {
            'text': data['text'],
            'created_at': data['created_at'],
            'user': data['user']['screen_name'],
            'media': data['extended_entities']['media'][0]['video_info']['variants'][2]['url']
        }
    return arr


def lookup_fallback(tweets):
    try:
        res = api.lookup_statuses(tweets)
    except:
        traceback.print_exc()
        res = []

    return parse_api(res)


def send(tweet):
    try:
        res = client.create_tweet(
            text=tweet
        )
        print(res.data)
        return res
    except:
        traceback.print_exc()


def delete(tweet):
    try:
        res = client.delete_tweet(
            id=tweet
        )
        print(res.data)
    except:
        traceback.print_exc()


def main():
    tweets = [1326355021093498880, 1421626172094492678,
              1505434915856338946, 1531720420478550022,
              1533509004244176896]
    res = lookup(tweets)

    print('results:')
    for i in res:
        # print(res[i])
        print(i, res[i]['media'])

    # t = send('test').data
    # delete(t['id'])


if __name__ == '__main__':
    main()
