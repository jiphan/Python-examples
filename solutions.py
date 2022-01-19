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


def solution3(A):
    A.sort()
    for i in range(len(A) - 1):
        if i % 2 == 0 and A[i] != A[i + 1]:
            return A[i]
    return A[len(A) - 1]
    pass


def solution4(A):
    if not A:
        return 1
    A.sort()
    for i in range(0, len(A)):
        if A[i] != i + 1:
            return i + 1
    return len(A) + 1


def solution5(A):
    (l, r) = (0, sum(A))
    res = float('inf')
    for i in range(0, len(A) - 1):
        l += A[i]
        r -= A[i]
        res = min(res, abs(l - r))
    return res


def solution6(X, A):
    pos = [-1 for i in range(X)]
    for i in range(len(A)):
        if pos[A[i] - 1] == -1:
            pos[A[i] - 1] = i
    # print(pos)

    ans = -1
    for i in pos:
        if i == -1:
            return -1
        ans = max(ans, i)
    return ans


def main():
    print(solution4([]))


if __name__ == '__main__':
    main()
