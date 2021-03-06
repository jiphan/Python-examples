import re
import time
import subprocess
import yotsuba
import config
import os
script_dir = os.path.dirname(__file__)
args = config.read_yaml(script_dir + '/config.yaml')
postSet = set()


def getPosts(thread):
    postList = []
    res = yotsuba.getThread(args.board, thread)
    for post in res:
        if post['no'] not in postSet and re.search(
            args.postRegex, post.get('com', '')
        ):
            postSet.add(post['no'])
            if 'sub' not in post:
                post['com'] = yotsuba.escapeHtml(post['com'])
                postList.append(post)
    return postList


def main():
    for page in yotsuba.getCatalogFull(args.board):
        for thread in page['threads']:
            if re.search(args.threadRegex, thread.get('com', '')):
                fileList = []
                for post in getPosts(thread['no']):
                    fileList += re.findall(
                        '\S*litter\.catbox\.moe\/\S*', post['com'])
                if fileList != []:
                    print(thread['no'], thread['sub'])
                for file in fileList:
                    print(file, '\t', file.split('/')[-1])
                    folder = '../../dl/catbox'
                    subprocess.run([
                        script_dir + '../../aria2c.exe', file,
                        '-d', script_dir + folder,
                        '-q'
                    ])
                    with open(script_dir + folder + '/log.txt', 'a') as f:
                        f.write(
                            '\n' + file
                        )


if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            print('connection error probably')
        time.sleep(int(args.refresh) * 60)
