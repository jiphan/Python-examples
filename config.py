#!/usr/bin/python
import yaml
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("board", nargs='?', default=None)
parser.add_argument("--recent", default=0)
parser.add_argument("idk", nargs='*', default=None)
args = parser.parse_args()


def read_yaml(path):
    with open(path, "r") as f:
        result = yaml.safe_load(f)
        if args.board:
            result['board'] = args.board
        if args.recent:
            result['recent'] = args.recent
        return result


if __name__ == '__main__':
    res = read_yaml('config.yaml')
    print(res)
