#!/usr/bin/python
import re
import time
import requests
import config


def escapeHtml(unsafe):
    # https://stackoverflow.com/a/46328646
    replacements = [
        ('<br>', ' '),
        ('<[^<]+?>', ''),
        ('&amp;', '&'),
        ('&lt;', '<'),
        ('&gt;', '>'),
        ('&#039;', '\''),
        ('&quot;', '\"')
    ]
    safe = unsafe
    for old, new in replacements:
        safe = re.sub(old, new, safe)
    return safe


def main():
    args = config.read_yaml('config.yaml')
    postSet = set()

    def getThreads():
        threadList = []
        res = requests.get(
            'https://a.4cdn.org/{}/catalog.json'
            .format(args.board)
        )
        for page in res.json():
            for thread in page['threads']:
                if (re.search(args.threadRegex, thread.get('com', ''))):
                    threadList.append(thread['no'])
        return threadList

    def getPosts(thread):
        postList = []
        res = requests.get(
            'https://a.4cdn.org/{}/thread/{}.json'
            .format(args.board, thread)
        )
        for post in res.json()['posts']:
            if (post['no'] not in postSet and re.search(
                args.postRegex,
                post.get('com', '')
            )):
                postSet.add(post['no'])
                post['com'] = escapeHtml(post['com'])
                postList.append(post)
        return postList

    def scan():
        postList = []
        for thread in getThreads():
            postList += getPosts(thread)
        # print(list(map(lambda i: i['com'], postList)))

        if len(postList) > 0:
            print('\n' + time.strftime("%H:%M:%S", time.localtime()))
            for post in postList:
                if re.search(args.threadRegex, post['com']):
                    print('\n{}: {}'.format(post['no'], post.get('sub', '')))
                else:
                    print('{}: {}'.format(post['no'], post['com']))

    while True:
        scan()
        time.sleep(5 * 60)


if __name__ == '__main__':
    main()
