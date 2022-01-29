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


def getGeneric(url):
    contentList = []
    res = requests.get(url)
    print(res.text)


def main():
    c = config.read_yaml('config.yaml')
    board, threadRegex, postRegex = c['board'], c['threadRegex'], c['postRegex']
    postSet = set()

    def getThreads():
        threadList = []
        res = requests.get(
            'https://a.4cdn.org/{}/catalog.json'
            .format(board)
        )
        for page in res.json():
            for thread in page['threads']:
                if (re.search(threadRegex, thread.get('com', ''))):
                    threadList.append(thread['no'])
        return threadList

    def getPosts(thread):
        postList = []
        res = requests.get(
            'https://a.4cdn.org/{}/thread/{}.json'
            .format(board, thread)
        )
        for post in res.json()['posts']:
            if (post['no'] not in postSet and re.search(
                postRegex,
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
                if re.search(threadRegex, post['com']):
                    print('\n{}: {}'.format(post['no'], post.get('sub', '')))
                else:
                    print('{}: {}'.format(post['no'], post['com']))

    while True:
        scan()
        time.sleep(5 * 60)


if __name__ == '__main__':
    main()
