import sys
from math import ceil, log2
input = sys.stdin.readline

def main():
    N, Q = map(int, input().split())
    A = list(map(int, input().split()))
    
    #
    size = 1 << ceil(log2(N)) if N > 1 else 1
    tree = [(0, 0)] * (2 * size)
    
    def merge(a, b):
        ca, na = a
        cb, nb = b
        if ca == cb:
            return (ca, na + nb)
        if na >= nb:
            return (ca, na - nb)
        return (cb, nb - na)
    
    def build(pos, val):
        tree[size + pos] = (val, 1)
    
    def update_tree():
        for i in range(size - 1, 0, -1):
            tree[i] = merge(tree[2*i], tree[2*i+1])
    
    def point_update(pos, val):
        pos += size
        tree[pos] = (val, 1)
        pos >>= 1
        while pos >= 1:
            tree[pos] = merge(tree[2*pos], tree[2*pos+1])
            pos >>= 1
    
    def query(l, r):
        res = (0, 0)
        l += size
        r += size + 1
        while l < r:
            if l & 1:
                res = merge(res, tree[l])
                l += 1
            if r & 1:
                r -= 1
                res = merge(res, tree[r])
            l >>= 1
            r >>= 1
        return res
    
    for i in range(N):
        build(i, A[i])
    update_tree()
    
    out = []
    for _ in range(Q):
        line = list(map(int, input().split()))
        if line[0] == 1:
            _, i, x = line
            i -= 1
            A[i] = x
            point_update(i, x)
        else:
            _, L, R = line
            L -= 1; R -= 1
            length = R - L + 1
            candidate, _ = query(L, R)
           
            count = 0
            for j in range(L, R + 1):
                if A[j] == candidate:
                    count += 1
            if count * 2 > length:
                out.append(candidate)
            else:
                out.append(-1)
    
    print('\n'.join(map(str, out)))

main()