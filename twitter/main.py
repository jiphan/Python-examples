import tweepy
import config
import os
script_dir = os.path.dirname(__file__)
args = config.read_yaml(script_dir + '/config.yaml')

api = tweepy.API(tweepy.OAuth2BearerHandler(args['bearer_token']))
client = tweepy.Client(args['bearer_token'])
# client = tweepy.Client(
#     consumer_key=args['consumer_key'],
#     consumer_secret=args['consumer_secret'],
#     access_token=args['access_token'],
#     access_token_secret=args['access_token_secret']
# )


def main():
    tweets = [1326355021093498880, 1513653124019494919]
    try:
        res = client.get_tweets(
            tweets,
            expansions=["author_id", "attachments.media_keys",
                        "referenced_tweets.id"],
            media_fields=["preview_image_url", "url"],
            # tweet_fields=["created_at"],
        )

        for t in res.includes['media']:
            print(t.url)
        print()

        for t in res.data:
            print(t.text)
        print()

        print(res)

    except Exception as e:
        print('something happened:', e)


if __name__ == '__main__':
    main()
