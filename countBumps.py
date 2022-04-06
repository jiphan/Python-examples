#!/usr/bin/python
import requests
import datetime
import config
import time


def main():
    args = config.read_yaml('config.yaml')

    def getThreads():
        threadList = []
        res = requests.get(
            'https://a.4cdn.org/{}/catalog.json'
            .format(args.board)
        )
        # print('/{}/ status:'.format(args.board), res.status_code)
        if res.status_code != 200:
            return threadList
        for page in res.json():
            for thread in page['threads']:
                # handle no replies, bumplimit, sticky
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
        arr = []
        for i in threads:
            last = datetime.datetime.fromtimestamp(i['bump'])
            diff = now - last
            arr.append((diff, i['page']))
        return arr

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

    def pageRanges(lastBumps):
        """ return map of first bump in each page """
        res = {}
        for i, j in lastBumps:
            if j not in res:
                res[j] = i
        return res

    def convertTime(seconds):
        mn = seconds // 60
        hr = mn // 60
        mn = str(mn % 60).rjust(2, '0')
        return "{}:{}".format(hr, mn)

    arr = getLastBump(getThreads())

    if args.bucket:
        [print('{}: {}'.format(k, v)) for k, v in bucketLastBumps(arr).items()]

    def inlinePrint(pageMap):
        """print results of `pageRanges()` inline"""
        res = '\t'.join(
            convertTime(pageMap[x].seconds) for x in pageMap
            # map(lambda x: convertTime(pageMap[x].seconds))
        )
        if len(pageMap) == 10:
            clean = convertTime(arr[-1][0].seconds)
            res += '\t' + clean
        return res

    print('\t'.join(map(str, range(1, 12))))  # header
    if args.recent:
        print(inlinePrint(pageRanges(arr)))
        print()

        recent = int(args.recent)
        [print(i, j) for i, j in arr[-recent:]]

    if args.loop:
        last = ''
        while True:
            line = inlinePrint(pageRanges(getLastBump(getThreads())))
            timestamp = datetime.datetime.now().strftime('(%H:%M)')
            if timestamp[1:3] == last:
                timestamp = ''
            else:
                last = timestamp[1:3]
            print(line + '\t' + timestamp)
            time.sleep(15 * 60)


if __name__ == '__main__':
    main()
