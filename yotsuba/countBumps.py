import datetime
import time
import yotsuba
import config
import os
script_dir = os.path.dirname(__file__)
args = config.read_yaml(script_dir + '/config.yaml')


def getBumps():
    """returns array of [time since last bump, page]"""
    threadList = []
    for i in yotsuba.getCatalogFull(args.board):
        for j in i['threads']:
            try:
                bump = j['last_replies'][-1]['time']
                if j['bumplimit']:
                    continue
                threadList.append((timeSince(bump), i['page']) or [])
            except:
                continue

    return threadList


def bucketLastBumps(lastBumps):
    timeranges = [1, 5, 10, 15, 30, 60, 120, 240, 480, 960, 1920, 3840]
    count = {}
    for i, _ in lastBumps:
        for j in timeranges:
            if i < datetime.timedelta(0, j * 60):
                if j >= 60 * 2:
                    label = 'under {} hrs'.format(str(j // 60).rjust(2))
                else:
                    label = 'under {} min'.format(str(j).rjust(2))
                if label not in count:
                    count[label] = 1
                else:
                    count[label] += 1
                break
    return count


def convertTime(seconds):
    mn = seconds // 60
    hr = mn // 60
    mn = str(mn % 60).rjust(2, '0')
    return "{}:{}".format(hr, mn)


def timeSince(bump):
    now = datetime.datetime.now().replace(microsecond=0)
    last = datetime.datetime.fromtimestamp(bump)
    diff = now - last
    return diff


def pageRanges(lastBumps):
    """ return map of first bump in each page """
    res = {}
    for i, j in lastBumps:
        if j not in res:
            res[j] = i
    return res


def main():
    arr = getBumps()

    if args.bucket:
        [print('{}: {}'.format(k, v)) for k, v in bucketLastBumps(arr).items()]

    def inlinePrint(pageMap):
        """print results of `pageRanges()` inline"""
        res = '\t'.join(
            convertTime(pageMap[x].seconds) for x in pageMap
            # map(lambda x: convertTime(pageMap[x].seconds))
        )
        if len(pageMap) == 10:
            clean = convertTime(arr[-1][0].seconds)  # needs full bumps
            res += '\t' + clean
        return res

    if args.recent:
        print('\t'.join(map(str, range(1, 12))))  # header
        print(inlinePrint(pageRanges(arr)))
        print()

        recent = int(args.recent)
        [print(i, j) for i, j in arr[-recent:]]

    if args.loop:
        print('\t'.join(map(str, range(1, 12))))  # header
        last = ''
        while True:
            line = inlinePrint(pageRanges(arr))
            timestamp = datetime.datetime.now().strftime('(%H:%M)')
            if timestamp[1:3] == last:
                timestamp = ''
            else:
                last = timestamp[1:3]
            print(line + '\t' + timestamp)
            time.sleep(15 * 60)
            try:
                arr = getBumps()
            except:
                print('connection error probably')


if __name__ == '__main__':
    main()
