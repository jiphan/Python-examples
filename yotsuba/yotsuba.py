import requests
import re


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


def getCatalog(board):
    threadList = []
    res = requests.get(
        f'https://a.4cdn.org/{board}/catalog.json'
    )
    if res.status_code != 200:
        return threadList
    for page in res.json():
        for thread in page['threads']:
            threadList.append(thread['no'])

    return threadList


def getCatalogFull(board):
    res = requests.get(
        f'https://a.4cdn.org/{board}/catalog.json'
    )
    if res.status_code != 200:
        return {}
    return res.json()


def getArchive(board):
    res = requests.get(
        f'https://a.4cdn.org/{board}/archive.json'
    )
    return res.json()


def getThread(board, thread):
    postList = []
    res = requests.get(
        f'https://a.4cdn.org/{board}/thread/{thread}.json'
    )
    op = res.json()['posts'][0]
    print(res.status_code, op['no'], op.get('sub', 'none'))
    for post in res.json()['posts']:
        postList.append(post)
    return postList


if __name__ == '__main__':
    pass
