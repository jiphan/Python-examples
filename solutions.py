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


def solution7(N, S):
    open = [[1 for i in range(3)] for i in range(N)]

    for i in S.split():
        row = int(i[:-1])
        seat = i[-1]

        rowIndex = -1
        semiClosed = False
        if seat in ('A', 'B', 'C'):
            rowIndex = 0
        elif seat in ('E', 'F'):
            rowIndex = 1
        elif seat in ('H', 'J', 'K'):
            rowIndex = 2
        elif seat in ('D', 'G'):  # middle aisle logic
            rowIndex = 1
        else:
            print('seat out of range')

        if open[row - 1][rowIndex] > 0:
            if semiClosed:
                open[row - 1][rowIndex] -= 0.5
            else:
                open[row - 1][rowIndex] = 0

    openSections = 0
    for i in open:
        for j in i:
            if j > 0:
                openSections += 1

    return openSections


# pure recursion
def fibb1(N):
    if N == 1 or N == 2:
        return 1
    else:
        return fibb1(N - 1) + fibb1(N - 2)  # subproblem


# memoization
def fibb2(N):
    dp = [0] * (N + 1)

    def memo(N):
        if dp[N]:
            return dp[N]
        elif N == 1 or 2:
            result = 1
        else:
            result = memo(N - 1) + memo(N - 2)  # subproblem
        dp[N] = result  # memoize
        # print(dp)
        return dp[N]

    return memo(N)


# bottom up
def fibb3(N):
    dp = [0] * (N + 1)
    dp[1] = 1
    dp[2] = 1

    for i in range(3, N + 1):
        dp[i] = dp[i - 1] + dp[i - 2]  # subproblem

    return dp[N]


# BST core
def treeSum(root):
    if root is None:
        return 0
    else:
        left = treeSum(root.left)
        right = treeSum(root.right)
        return root.data + left + right


if __name__ == '__main__':
    print(fibb2(2))
