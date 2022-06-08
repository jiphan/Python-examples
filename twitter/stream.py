import tweepy
import twitter
import traceback
import subprocess
import os
script_dir = os.path.dirname(__file__)


def local_dl(id, urls):
    exec = '../../aria2c.exe'
    folder = '../../dl/'

    subprocess.run([
        script_dir + exec, ' '.join(urls),
        '-d', script_dir + folder,
        '-q'
    ])

    with open(script_dir + folder + '/log.txt', 'a') as f:
        f.write(f'{id} ' + ' '.join([i.split('/')[-1] for i in urls]))


def parse_tweet(response):
    print(response.errors)
    user = {u['id']: u for u in response.includes['users']}
    try:
        media = {m["media_key"]: m for m in response.includes['media']}
        mm = [media[m].url for m in response.data['attachments']['media_keys']]
        if None in mm:
            fallback = twitter.lookup_fallback([response.data['id']])
            mm = [fallback[str(response.data['id'])]['media']]
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


def handle_response(response):
    res = parse_tweet(response)
    print(res['text'][:60])
    [print(i) for i in res['media']]
    exclude = [1533617607076610048, 1482870401403428867]
    if len(res['media']) > 0 and res['rules'][0] not in exclude:
        local_dl(res['id'], res['media'])


class stream_parse(tweepy.StreamingClient):
    def on_connect(self):
        print('connect OK')

    def on_response(self, response):
        handle_response(response)


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
    # main()
    local_dl('test', ['https://pbs.twimg.com/media/FUq7eaEaAAANbWJ.jpg'])
