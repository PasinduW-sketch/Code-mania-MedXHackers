import sys
from sys import stdin
input = stdin.readline

def main():
    import threading
    sys.setrecursionlimit(300000)
    
    MOD = 0
    N, Q = map(int, input().split())
    A = list(map(int, input().split()))
    
    adj = [[] for _ in range(N+1)]
    for _ in range(N-1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # HLD setup rooted at 1
    parent = [0]*(N+1)
    depth = [0]*(N+1)
    sz = [1]*(N+1)
    heavy = [-1]*(N+1)
    head = [0]*(N+1)
    pos = [0]*(N+1)
    pos_end = [0]*(N+1)  # end of subtree in euler order
    order = []
    
    # Iterative DFS for HLD
    stack = [(1, 0, False)]
    while stack:
        v, p, visited = stack.pop()
        if visited:
            max_sz = 0
            for u in adj[v]:
                if u == p: continue
                sz[v] += sz[u]
                if sz[u] > max_sz:
                    max_sz = sz[u]
                    heavy[v] = u
        else:
            parent[v] = p
            order.append(v)
            stack.append((v, p, True))
            for u in adj[v]:
                if u == p:
                    continue
                depth[u] = depth[v] + 1
                stack.append((u, v, False))
    
    # Assign positions
    cur = [0]
    stack2 = [(1, 1)]  # (node, chain_head)
    while stack2:
        v, h = stack2.pop()
        head[v] = h
        pos[v] = cur[0]
        cur[0] += 1
        # push light children first (they go later), heavy child last (processed first)
        children = [u for u in adj[v] if u != parent[v]]
        light = [u for u in children if u != heavy[v]]
        for u in light:
            stack2.append((u, u))
        if heavy[v] != -1:
            stack2.append((heavy[v], h))
    
    # pos_end[v] = pos[v] + sz[v] - 1
    for v in range(1, N+1):
        pos_end[v] = pos[v] + sz[v] - 1
    
    # Segment tree with lazy propagation (range add, range sum)
    size = N
    seg = [0]*(4*N)
    lazy = [0]*(4*N)
    
    # Build with initial values in HLD order
    arr = [0]*(N)
    for v in range(1, N+1):
        arr[pos[v]] = A[v-1]
    
    def build(node, l, r):
        if l == r:
            seg[node] = arr[l]
            return
        m = (l+r)//2
        build(2*node, l, m)
        build(2*node+1, m+1, r)
        seg[node] = seg[2*node] + seg[2*node+1]
    
    build(1, 0, N-1)
    
    def push_down(node, l, r):
        if lazy[node]:
            m = (l+r)//2
            seg[2*node] += lazy[node]*(m-l+1)
            lazy[2*node] += lazy[node]
            seg[2*node+1] += lazy[node]*(r-m)
            lazy[2*node+1] += lazy[node]
            lazy[node] = 0
    
    def range_add(node, l, r, ql, qr, val):
        if qr < l or r < ql:
            return
        if ql <= l and r <= qr:
            seg[node] += val*(r-l+1)
            lazy[node] += val
            return
        push_down(node, l, r)
        m = (l+r)//2
        range_add(2*node, l, m, ql, qr, val)
        range_add(2*node+1, m+1, r, ql, qr, val)
        seg[node] = seg[2*node] + seg[2*node+1]
    
    def range_sum(node, l, r, ql, qr):
        if qr < l or r < ql:
            return 0
        if ql <= l and r <= qr:
            return seg[node]
        push_down(node, l, r)
        m = (l+r)//2
        return range_sum(2*node, l, m, ql, qr) + range_sum(2*node+1, m+1, r, ql, qr)
    
    # LCA using binary lifting
    LOG = 18
    up = [[0]*(N+1) for _ in range(LOG)]
    up[0] = parent[:]
    up[0][1] = 1
    for k in range(1, LOG):
        for v in range(1, N+1):
            up[k][v] = up[k-1][up[k-1][v]]
    
    def lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        diff = depth[u] - depth[v]
        for k in range(LOG):
            if (diff>>k)&1:
                u = up[k][u]
        if u == v:
            return u
        for k in range(LOG-1, -1, -1):
            if up[k][u] != up[k][v]:
                u = up[k][u]
                v = up[k][v]
        return parent[u]
    
    def is_ancestor(u, v):
        # is u ancestor of v in original tree?
        return pos[u] <= pos[v] <= pos_end[u]
    
    def kth_ancestor_on_path(v, r, k):
        # k-th ancestor of v towards r (not needed directly)
        pass
    
    def child_towards(v, target):
        # find child of v on path to target (original root tree)
        # = ancestor of target at depth[v]+1
        diff = depth[target] - depth[v] - 1
        u = target
        for k in range(LOG):
            if (diff>>k)&1:
                u = up[k][u]
        return u
    
    # Subtree add under current root r_cur
    def subtree_add(v, x, r_cur):
        if v == r_cur:
            # entire tree
            range_add(1, 0, N-1, 0, N-1, x)
            return
        if not is_ancestor(v, r_cur):
            # subtree of v in original tree
            range_add(1, 0, N-1, pos[v], pos_end[v], x)
        else:
            # r_cur is in subtree of v
            # subtree under new root = all nodes except subtree of child c of v towards r_cur
            c = child_towards(v, r_cur)
            # add to [0, pos[c]-1] and [pos_end[c]+1, N-1]
            if pos[c] > 0:
                range_add(1, 0, N-1, 0, pos[c]-1, x)
            if pos_end[c] < N-1:
                range_add(1, 0, N-1, pos_end[c]+1, N-1, x)
    
    # Path sum query (root doesn't matter)
    def path_sum(u, v):
        res = 0
        while head[u] != head[v]:
            if depth[head[u]] < depth[head[v]]:
                u, v = v, u
            res += range_sum(1, 0, N-1, pos[head[u]], pos[u])
            u = parent[head[u]]
        if depth[u] > depth[v]:
            u, v = v, u
        res += range_sum(1, 0, N-1, pos[u], pos[v])
        return res
    
    r_cur = 1
    out = []
    for _ in range(Q):
        line = list(map(int, input().split()))
        if line[0] == 1:
            _, v, x = line
            subtree_add(v, x, r_cur)
        elif line[0] == 2:
            _, u, v = line
            out.append(path_sum(u, v))
        else:
            r_cur = line[1]
    
    print('\n'.join(map(str, out)))

main()