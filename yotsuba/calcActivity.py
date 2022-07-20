from concurrent.futures import thread
from datetime import datetime
import time
import re
import yotsuba
import config
import os
script_dir = os.path.dirname(__file__)
args = config.read_yaml(script_dir + '/config.yaml')


def bucketTime(timestamp):
    hours = timestamp.strftime('%H:%M')[:-2]
    minutes = int(timestamp.strftime('%H:%M')[-2:]) // 15 * 15
    minutes = str(minutes).ljust(2, '0')
    return hours + minutes


def getCurrent():
    res = set()
    for page in yotsuba.getCatalogFull(args.board):
        for thread in page['threads']:
            if re.search(args.threadRegex, thread.get('com', '')):
                res.add(thread['no'])
    return res


if __name__ == '__main__':
    print(args)
    expired = set(yotsuba.getArchive(args.board))
    threadQueue = getCurrent()
    allThreads = getCurrent()
    # allThreads = {getCurrent()}
    bucket = {}

    while (len(threadQueue) > 0):
        print(threadQueue, allThreads)
        # pull current thread in queue
        cur = yotsuba.getThread(args.board, threadQueue.pop())
        if (not re.search(args.threadRegex, cur[0]['com'])):
            continue

        # bucket timestamps to 15min intervals
        for i in cur:
            dt = bucketTime(datetime.fromtimestamp(i['time']))
            bucket[dt] = bucket[dt] + 1 if dt in bucket else 1

        # find backlinks where OP and new
        postSet = set()
        for post in cur:
            if post.get('com') and 'quotelink' in post['com']:
                clean = yotsuba.escapeHtml(post['com'])
                link = re.findall(r'(?<=>>)(\d+)', clean)
                postSet.update(map(int, link))
        threadQueue.update(postSet & expired - allThreads - {cur[0]['no']})
        allThreads.update(threadQueue)
        time.sleep(1)
        if len(allThreads) > 5:
            break

    [print(i, ',', str(bucket[i])) for i in sorted(bucket)]
