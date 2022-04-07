import re
import requests
import config
import os
script_dir = os.path.dirname(__file__)
args = config.read_yaml(script_dir + '/config.yaml')


def escapeHtml(unsafe):
    # https://stackoverflow.com/a/46328646
    replacements = [
        ('<br>', ' '),
        ('<[^<]+?>', ''),  # remove html tags
        ('&amp;', '&'),
        ('&lt;', '<'),
        ('&gt;', '>'),
        ('&#039;', '\''),
        ('&quot;', '\"')
    ]
    safe = unsafe
    for old, new in replacements:
        safe = re.sub(old, new, safe)
    return safe


def getCatalog():
    threadList = []
    res = requests.get(
        'https://a.4cdn.org/{}/catalog.json'
        .format(args.board)
    )
    if res.status_code != 200:
        return threadList
    for page in res.json():
        for thread in page['threads']:
            if (re.search(args.threadRegex, thread.get('com', ''))):
                threadList.append(thread['no'])
    return threadList


def getCatalogFull():
    res = requests.get(
        'https://a.4cdn.org/{}/catalog.json'
        .format(args.board)
    )
    if res.status_code != 200:
        return {}
    return res.json()


def getArchive():
    res = requests.get(
        'https://a.4cdn.org/{}/archive.json'
        .format(args.board)
    )
    return res.json()


def getThread(thread):
    postList = []
    res = requests.get(
        'https://a.4cdn.org/{}/thread/{}.json'
        .format(args.board, thread)
    )
    op = res.json()['posts'][0]
    print(res.status_code, op.get('sub', 'none'))
    for post in res.json()['posts']:
        postList.append(post)
    return postList


if __name__ == '__main__':
    pass
