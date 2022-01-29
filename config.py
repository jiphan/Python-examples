#!/usr/bin/python
import yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("board", nargs='?', default=None)
parser.add_argument("--recent")
parser.add_argument("--threadRegex")
parser.add_argument("--postRegex")
parser.add_argument("idk", nargs='*', default=None)
args = parser.parse_args()


def read_yaml(path):
    with open(path, "r") as f:
        result = yaml.safe_load(f)
        args.board = args.board or result['board']
        args.threadRegex = args.threadRegex or result['threadRegex']
        args.postRegex = args.postRegex or result['postRegex']
        return args


if __name__ == '__main__':
    res = read_yaml('config.yaml')
    print(res)
