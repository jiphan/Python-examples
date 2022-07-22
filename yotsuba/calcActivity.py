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
    hours = timestamp.strftime('%d %H:%M')[:-2]
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
    # print(args)
    expired = set(yotsuba.getArchive(args.board))
    threadQueue = getCurrent()
    allThreads = threadQueue.copy()
    bucket = {}

    while (len(threadQueue) > 0):
        print(threadQueue, allThreads)
        # pull current thread in queue
        cur = yotsuba.getThread(args.board, threadQueue.pop())
        if (not re.search(args.threadRegex, cur[0]['com'])):
            continue

        postSet = set()
        for post in cur:
            # bucket timestamps to 15min intervals
            dt = bucketTime(datetime.fromtimestamp(post['time']))
            bucket[dt] = bucket[dt] + 1 if dt in bucket else 1

            # find backlinks in current
            if post.get('com') and 'quotelink' in post['com']:
                clean = yotsuba.escapeHtml(post['com'])
                link = re.findall(r'(?<=>>)(\d+)', clean)
                postSet.update(map(int, link))

        # add backlink where expired OP, new, not current OP
        threadQueue.update(postSet & expired - allThreads - {cur[0]['no']})
        allThreads.update(threadQueue)

        # time.sleep(1)
        if len(allThreads) > 5:
            break

    # [print(i, ',', str(bucket[i])) for i in sorted(bucket)]
    print()
    cur = int(sorted(bucket)[0][3:5])
    header = []
    line = []
    for i in sorted(bucket):
        # print(i, str(bucket[i]))
        if cur <= int(i[3:5]) <= cur + 2:
            header.append(i[3:])
            line.append(str(bucket[i]))
        else:
            print('\t'.join(header))
            print('\t'.join(line))
            header = [i[3:]]
            line = [str(bucket[i])]
            cur = int(i[3:5])

    print('\t'.join(header))
    print('\t'.join(line))
