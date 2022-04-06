import yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("board", nargs='?', default=None)
parser.add_argument("--recent")
parser.add_argument("--threadRegex")
parser.add_argument("--postRegex")
parser.add_argument("--refresh")
parser.add_argument("--bucket", dest='bucket', action='store_true')
parser.add_argument("--loop", dest='loop', action='store_true')
parser.add_argument("idk", nargs='*', default=None)
args = parser.parse_args()


def read_yaml(path):
    with open(path, "r") as f:
        default = yaml.safe_load(f)
        args.board = args.board or default['board']
        args.threadRegex = args.threadRegex or default['threadRegex']
        args.postRegex = args.postRegex or default['postRegex']
        args.refresh = args.refresh or default['refresh']
        return args


if __name__ == '__main__':
    res = read_yaml('config.yaml')
    print(res)
