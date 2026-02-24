import sys
input = sys.stdin.readline

class DSU:
    def __init__(self, n):
        self.par = list(range(n + 1))
        self.size = [1] * (n + 1)
        self.stack = []
    
    def find(self, x):
        while x != self.par[x]:
            x = self.par[x]
        return x
    
    def union(self, a, b):
        a = self.find(a)
        b = self.find(b)
        if a == b:
            self.stack.append((-1, -1, -1, -1))
            return
        if self.size[a] < self.size[b]:
            a, b = b, a
        self.stack.append((b, self.par[b], a, self.size[a]))
        self.par[b] = a
        self.size[a] += self.size[b]
    
    def rollback(self):
        b, par_b, a, size_a = self.stack.pop()
        if b == -1:
            return
        self.par[b] = par_b
        self.size[a] = size_a

def solve():
    n, q = map(int, input().split())
    ops = []
    edge_time = dict()
    
    queries = []
    
    for i in range(q):
        tmp = list(map(int, input().split()))
        if tmp[0] == 1:
            u, v = tmp[1], tmp[2]
            if u > v: u, v = v, u
            edge_time[(u,v)] = i
            ops.append(('add', u, v))
        elif tmp[0] == 2:
            u, v = tmp[1], tmp[2]
            if u > v: u, v = v, u
            start = edge_time.pop((u,v))
            ops.append(('remove', u, v, start, i))
        else:
            u, v = tmp[1], tmp[2]
            ops.append(('query', u, v, len(queries)))
            queries.append(None)
    
    # Add remaining edges as having "infinite" end time
    for (u,v), start in edge_time.items():
        ops.append(('remove', u, v, start, q))
    
    # Segment tree based approach
    st_size = 1
    while st_size < q:
        st_size <<= 1
    seg = [[] for _ in range(2*st_size)]
    
    def add_edge(seg_l, seg_r, u, v, l, r, idx=1, tl=0, tr=st_size):
        if r <= tl or tr <= l:
            return
        if l <= tl and tr <= r:
            seg[idx].append((u,v))
            return
        tm = (tl+tr)//2
        add_edge(seg_l, seg_r, u, v, l, r, idx*2, tl, tm)
        add_edge(seg_l, seg_r, u, v, l, r, idx*2+1, tm, tr)
    
    for op in ops:
        if op[0]=='remove':
            u,v,start,end = op[1], op[2], op[3], op[4]
            add_edge(start, end, u, v, start, end)
    
    dsu = DSU(n)
    ans = [None]*len(queries)
    
    def dfs(idx, l, r):
        for u,v in seg[idx]:
            dsu.union(u,v)
        if r - l == 1:
            if l < len(ops) and ops[l][0]=='query':
                _, u, v, q_idx = ops[l]
                ans[q_idx] = 'YES' if dsu.find(u)==dsu.find(v) else 'NO'
        else:
            m = (l+r)//2
            dfs(idx*2, l, m)
            dfs(idx*2+1, m, r)
        for _ in seg[idx]:
            dsu.rollback()
    
    dfs(1, 0, st_size)
    print('\n'.join(ans))

if __name__ == "__main__":
    solve()