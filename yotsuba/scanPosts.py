#!/usr/bin/python
import re
import time
import yotsuba
postSet = set()


def getPosts(thread):
    postList = []
    res = yotsuba.getThread(thread)
    for post in res:
        if (post['no'] not in postSet and re.search(
            yotsuba.args.postRegex,
            post.get('com', '')
        )):
            postSet.add(post['no'])
            post['com'] = yotsuba.escapeHtml(post['com'])
            postList.append(post)
    return postList


def scan():
    postList = []
    for thread in yotsuba.getCatalog():
        postList += getPosts(thread)
    # print(list(map(lambda i: i['com'], postList)))

    if len(postList) > 0:
        print('\n' + time.strftime("%H:%M:%S", time.localtime()))
        for post in postList:
            if re.search(yotsuba.args.threadRegex, post['com']):
                print('\n{}: {}'.format(post['no'], post.get('sub', '')))
            else:
                print('{}: {}'.format(post['no'], post['com']))


if __name__ == '__main__':
    while True:
        scan()
        time.sleep(int(yotsuba.args.refresh) * 60)
