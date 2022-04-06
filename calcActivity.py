from datetime import datetime
import time
import re
import yotsuba
bucket = {}


def getBacklinks(thread):
    postSet = set()
    res = yotsuba.getThread(thread)
    bucketThread(res, bucket)
    op = res[0]
    if (not re.search(yotsuba.args.threadRegex, op['com'])):
        print('skipping')
        return postSet
    for post in res:
        if post.get('com') and 'quotelink' in post['com']:
            clean = yotsuba.escapeHtml(post['com'])
            link = re.findall(r'(?<=>>)(\d+)', clean)
            postSet.update(map(int, link))
    return postSet


def getRelatedThreads(threadList):
    arr = set(yotsuba.getArchive())
    threadQueue = set()
    threadQueue.add(threadList[0])
    while (len(threadQueue) > 0):
        # print(threadQueue)
        cur = threadQueue.pop()
        curLinks = getBacklinks(cur)
        if len(curLinks) == 0:
            print('removing')
            threadList.remove(cur)
        next = arr & curLinks
        for i in next:
            if i not in threadList:
                threadQueue.add(i)
                threadList.append(i)
        time.sleep(1)

        if len(threadList) > 5:
            break
    return threadList


def bucketThread(data, bucket):
    for i in data:
        dt = datetime.fromtimestamp(i['time'])
        q = int(dt.strftime('%H:%M')[-2:]) // 15 * 15
        dt = dt.strftime('%H:%M')[:-2] + str(q).ljust(2, '0')
        bucket[dt] = 1 if dt not in bucket else bucket[dt] + 1


if __name__ == '__main__':
    print(yotsuba.args)
    q = yotsuba.getCatalog()
    q = getRelatedThreads(q)
    [print(i, str(bucket[i])) for i in sorted(bucket)]
