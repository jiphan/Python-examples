#!/usr/bin/python
import re
import time
import requests
import yaml
import datetime
from operator import itemgetter


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


def read_yaml(path):
    with open(path, "r") as f:
        return itemgetter(
            'board',
            'threadRegex',
            'postRegex')(yaml.safe_load(f))


def getGeneric(url):
    contentList = []
    res = requests.get(url)
    print(res.text)


def postScan():
    board, threadRegex, postRegex = read_yaml('yotsuba.yaml')
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


def catalogScan():
    board, threadRegex, postRegex = read_yaml('config.yaml')
    board = 'po'

    def getThreads():
        threadList = []
        res = requests.get(
            'https://a.4cdn.org/{}/catalog.json'
            .format(board)
        )
        print('/{}/ status:'.format(board), res.status_code)
        for page in res.json():
            for thread in page['threads']:
                try:
                    bump = thread['last_replies'][-1]['time']
                    if thread['bumplimit']:
                        continue
                except:
                    continue

                threadList.append({
                    'no': thread['no'],
                    'time': thread['time'],
                    'page': page['page'],
                    'bump': bump
                })
        return threadList

    def getLastBump(threads):
        now = datetime.datetime.now().replace(microsecond=0)
        curDiff = datetime.timedelta(0)
        arr = []
        for i in threads:
            last = datetime.datetime.fromtimestamp(i['bump'])
            diff = now - last
            relDiff = diff - curDiff
            curDiff = diff
            # print(i['page'], i['no'], '\t', diff, '\t', relDiff)
            arr.append(diff)
        return arr

    def bucketLastBumps(lastBumps):
        timeranges = [1, 5, 10, 15, 30, 60, 120, 240, 480, 960, 1920, 3840]
        count = {}
        for i in lastBumps:
            for j in timeranges:
                if i < datetime.timedelta(0, j * 60):
                    label = 'under {} hrs'.format(
                        j // 60) if j >= 60 * 2 else 'under {} min'.format(j)
                    if label not in count:
                        count[label] = 1
                    else:
                        count[label] += 1
                    break

    arr = getLastBump(getThreads())
    count = bucketLastBumps(arr)

    [print(k, ':', v) for k, v in count.items()]


if __name__ == '__main__':
    # postScan()
    catalogScan()
