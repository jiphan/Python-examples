import yaml


def read_yaml(path):
    with open(path, "r") as f:
        default = yaml.safe_load(f)
        return default


if __name__ == '__main__':
    res = read_yaml('config.yaml')
    print(res)
