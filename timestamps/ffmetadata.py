import os
import csv
import subprocess


def main(folder):
    timestamps = ''
    karaoke = ''

    # find files
    (_, _, files) = next(os.walk(folder))
    for filename in files:
        ext = filename[-3:]
        if (ext == 'csv'):
            timestamps = filename
        if (ext == 'mp4'):
            karaoke = filename

    # add chapters from timestamp.csv
    arr = []
    last_timestamp = 0
    last_title = 'Intro'
    print('reading: ', timestamps)
    for row in csv.reader(open(timestamps, 'r')):
        # format: time, title
        cur_time = row[0].split(':')
        cur_title = row[1].strip()
        if len(cur_time) == 3:
            hr = int(cur_time[0]) * 60 * 60
            mn = int(cur_time[1]) * 60
            sc = int(cur_time[2].split('.')[0])
            cur_time = hr + mn + sc
        elif len(cur_time) == 2:
            mn = int(cur_time[0]) * 60
            sc = int(cur_time[1].split('.')[0])
            cur_time = mn + sc

        if cur_title in ['setlist', 'title']:  # header
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

    # extract existing ffmetadata from karaoke.mp4
    subprocess.run([
        'ffmpeg',
        '-i', karaoke,          # file 0
        '-f', 'ffmetadata',     # export ffmetadata
        f'{karaoke}.txt'        # output filename
    ])

    # add chapters to ffmetadata
    timestamps = f'{karaoke}.txt'
    try:
        open(timestamps, 'a').writelines('\n'.join(arr))
        print(f'wrote: {timestamps}')
    except:
        print(f'failed to write: {timestamps}')

    # write updated ffmetadata to karaoke.m4a
    subprocess.run([
        'ffmpeg',
        '-i', karaoke,          # file 0
        '-i', timestamps,       # file 1
        '-map_metadata', '1',   # use metadata from file 1
        '-vn',                  # no video
        '-acodec', 'copy',      # copy audio
        f'{karaoke}.m4a'        # output filename
    ])


if __name__ == '__main__':
    main('.')
