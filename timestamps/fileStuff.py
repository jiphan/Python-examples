import os
import json
import csv


def loadFolder(folder, callback):
    bucket = {}
    for root, dirs, files in os.walk(folder):
        for filename in files:
            file = '{}/{}'.format(folder, filename)
            print(file)
            break
            with open(file, 'r') as f:
                res = json.load(f)
                callback(res)
    return bucket


def loadTimestamps(folder):
    (_, _, files) = next(os.walk(folder))
    for filename in files:
        file = '{}/{}'.format(folder, filename)
        if (file[-3:] == 'csv'):
            openTimestamp(file)


def openTimestamp(file):
    print(file)
    with open(file, 'r') as f:
        print(csv.reader(f))
        for row in csv.reader(f):
            print(row)


if __name__ == '__main__':
    loadTimestamps('.')
