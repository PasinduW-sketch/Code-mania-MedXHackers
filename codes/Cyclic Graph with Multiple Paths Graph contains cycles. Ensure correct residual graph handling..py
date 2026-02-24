from collections import deque
import sys

class MaxFlow:
    def __init__(self, n):
        self.n = n
        self.adj = [[] for _ in range(n + 1)]
        self.cap = {}
    
    def add_edge(self, u, v, c):
        # Add forward edge
        self.adj[u].append(v)
        self.adj[v].append(u)  # Add reverse edge for residual graph
        self.cap[(u, v)] = self.cap.get((u, v), 0) + c
        self.cap[(v, u)] = self.cap.get((v, u), 0)  # Initialize reverse capacity to 0
    
    def bfs(self, s, t, parent):
        visited = [False] * (self.n + 1)
        queue = deque([s])
        visited[s] = True
        
        while queue:
            u = queue.popleft()
            
            for v in self.adj[u]:
                if not visited[v] and self.cap.get((u, v), 0) > 0:
                    visited[v] = True
                    parent[v] = u
                    if v == t:
                        return True
                    queue.append(v)
        
        return False
    
    def ford_fulkerson(self, s, t):
        parent = [-1] * (self.n + 1)
        max_flow = 0
        
        while self.bfs(s, t, parent):
            # Find the minimum capacity along the path
            path_flow = float('inf')
            v = t
            while v != s:
                u = parent[v]
                path_flow = min(path_flow, self.cap[(u, v)])
                v = u
            
            # Update residual capacities
            v = t
            while v != s:
                u = parent[v]
                self.cap[(u, v)] -= path_flow
                self.cap[(v, u)] += path_flow
                v = u
            
            max_flow += path_flow
            parent = [-1] * (self.n + 1)
        
        return max_flow
    
    def dinic_bfs(self, s, t, level):
        queue = deque([s])
        level[s] = 0
        
        while queue:
            u = queue.popleft()
            
            for v in self.adj[u]:
                if level[v] == -1 and self.cap.get((u, v), 0) > 0:
                    level[v] = level[u] + 1
                    queue.append(v)
        
        return level[t] != -1
    
    def dinic_dfs(self, u, t, flow, level, ptr):
        if u == t:
            return flow
        
        for i in range(ptr[u], len(self.adj[u])):
            v = self.adj[u][i]
            if level[v] == level[u] + 1 and self.cap.get((u, v), 0) > 0:
                pushed = self.dinic_dfs(v, t, min(flow, self.cap[(u, v)]), level, ptr)
                if pushed > 0:
                    self.cap[(u, v)] -= pushed
                    self.cap[(v, u)] += pushed
                    return pushed
            ptr[u] += 1
        
        return 0
    
    def dinic(self, s, t):
        max_flow = 0
        level = [-1] * (self.n + 1)
        
        while self.dinic_bfs(s, t, level):
            ptr = [0] * (self.n + 1)
            while True:
                pushed = self.dinic_dfs(s, t, float('inf'), level, ptr)
                if pushed == 0:
                    break
                max_flow += pushed
            level = [-1] * (self.n + 1)
        
        return max_flow

def main():
    input = sys.stdin.read().split()
    idx = 0
    
    n = int(input[idx]); idx += 1
    m = int(input[idx]); idx += 1
    
    mf = MaxFlow(n)
    
    for _ in range(m):
        u = int(input[idx]); idx += 1
        v = int(input[idx]); idx += 1
        c = int(input[idx]); idx += 1
        mf.add_edge(u, v, c)
    
    s = int(input[idx]); idx += 1
    t = int(input[idx]); idx += 1
    
    # Using Dinic's algorithm for better performance
    result = mf.dinic(s, t)
    print(result)

if __name__ == "__main__":
    main()