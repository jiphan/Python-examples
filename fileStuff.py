import os
import json


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


if __name__ == '__main__':
    loadFolder('./threads')
