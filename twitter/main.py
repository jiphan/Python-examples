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

        return [
            list(map(lambda x: x.text, res.data)),
            list(map(lambda x: x.url, res.includes['media']))
        ]
    except:
        traceback.print_exc()
        return []


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
    tweets = [1326355021093498880, 1514110244578029569]
    print(lookup(tweets))
    # t = send('test').data
    # delete(t['id'])


if __name__ == '__main__':
    main()
