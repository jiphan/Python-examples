import os
import csv
import subprocess


def main(folder):
    timestamps = ''
    karaoke = ''
    (_, _, files) = next(os.walk(folder))
    for filename in files:
        ext = filename[-3:]
        print(filename, ext)
        if (ext == 'csv'):
            timestamps = filename
        if (ext == 'm4a'):
            karaoke = filename
    print(karaoke, timestamps)
    return

    arr = [';FFMETADATA1']
    last_timestamp = 0
    last_title = 'Intro'
    for row in csv.reader(open(timestamps, 'r')):
        cur_title = row[0]
        cur_time = row[1].split(':')
        if len(cur_time) == 3:
            hr = int(cur_time[0]) * 60 * 60
            mn = int(cur_time[1]) * 60
            sc = int(cur_time[2].split('.')[0])
            cur_time = hr + mn + sc

        if cur_title == 'setlist':  # header
            continue
        arr += [
            '[CHAPTER]',
            'TIMEBASE=1/1',
            f'START={last_timestamp}',
            f'END={cur_time}',
            f'title={last_title}'
        ]
        last_timestamp = cur_time
        last_title = cur_title

    arr += [
        '[CHAPTER]',
        'TIMEBASE=1/1',
        f'START={last_timestamp}',
        f'END={cur_time}',
        f'title={last_title}'
    ]
    timestamps = timestamps.replace('csv', 'ffmetadata')

    # open(filename, 'w').writelines('\n'.join(arr))
    # subprocess.run('ls')
    # subprocess.run(f'ffmpeg -i {INPUT} -i {filename} -map_metadata 1 -codec copy output.m4a')


if __name__ == '__main__':
    main('.')
