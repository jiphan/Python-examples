#!/usr/bin/env python3


def solution1(N):
    a = format(N, 'b')
    # a = '1001001100'

    print(a)
    a = a.strip('0')
    print(a.split('1'))
    count = 0
    for i in a.split('1'):
        count = max(count, len(i))
    print('count: ', count)
    pass


def solution2(A, K):
    if not A:
        return A
    K %= len(A)
    return A[-K:] + A[:-K]
    pass


def main():
    print(solution2([3, 8, 9, 7, 6], 5))


if __name__ == '__main__':
    main()
