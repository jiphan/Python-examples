import tweepy
import twitter
import traceback


def parse_tweet(response):
    print(response.errors)
    user = {u['id']: u for u in response.includes['users']}
    try:
        media = {m["media_key"]: m for m in response.includes['media']}
        mm = [media[m].url for m in response.data['attachments']['media_keys']]
        if None in mm:
            fallback = twitter.lookup_fallback([response.data['id']])
            mm = fallback[str(response.data['id'])]
    except:
        mm = []

    return {
        'id': response.data['id'],
        'text': response.data['text'],
        'created_at': response.data['created_at'],
        'user': user[int(response.data['author_id'])].username,
        'media': mm,
        'rules': list(map(lambda i: i.id, response.matching_rules)),
    }


class stream_parse(tweepy.StreamingClient):
    def on_connect(self):
        print('connect OK')

    def on_tweet(self, tweet):
        if 'testpost' in tweet.text:
            self.disconnect()

    def on_response(self, response):
        res = parse_tweet(response)
        print(res['id'], res['user'], res['created_at'])
        print(res['text'])
        [print(i) for i in res['media']]


def init(streaming_client):
    streaming_client.filter(
        expansions=["author_id",
                    "attachments.media_keys",
                    "referenced_tweets.id"],
        media_fields=["preview_image_url", "url"],
        tweet_fields=["created_at"],
        threaded=True
    )


def main():
    streaming_client = stream_parse(twitter.args['bearer_token'])
    try:
        init(streaming_client)
    except:
        print('already connected')

    while(True):
        text = input('>')
        try:
            if 'init' in text:
                init(streaming_client)
            if 'exit' in text:
                streaming_client.disconnect()
            if 'status' in text:
                print(streaming_client.running)
            if 'view' in text:
                arr = streaming_client.get_rules()
                [print(i.id, i.value) for i in arr.data]
            if 'del' in text:
                res = streaming_client.delete_rules(text.split(' ')[1:])
                print(res.meta['summary'])
            if 'add' in text:
                res = streaming_client.add_rules(
                    tweepy.StreamRule(value=text[4:]),
                    dry_run=False
                )
                print(res.meta['summary'])
        except:
            traceback.print_exc()


if __name__ == '__main__':
    main()
