import sys

sys.setrecursionlimit(10**6)

class Node:
    def __init__(self, ch=None, end=False):
        self.ch = ch
        self.children = {}
        self.end_count = 0 if end else 0
        self.version = 0

class PersistentTrie:
    def __init__(self):
        self.roots = [Node()]
        self.version_cnt = 0
    
    def new_node(self, ch=None, end=False):
        return Node(ch, end)
    
    def append(self, prev_ver, c):
        self.version_cnt += 1
        root = self.roots[prev_ver]
        cur = root
        
        for i in range(26):
            ch_idx = ord(c) - ord('a') if i == 0 else -1
            new_node = self.new_node()
            
            if ch_idx >= 0 and chr(ch_idx + ord('a')) == c:
                new_node.children[ch_idx] = cur.children.get(ch_idx, self.new_node())
                new_node.end_count = cur.end_count + 1
            else:
                new_node.end_count = cur.end_count
                new_node.children = cur.children.copy()
            
            cur = new_node
        
        self.roots.append(cur)
        return self.version_cnt
    
    def delete(self, prev_ver, k):
        self.version_cnt += 1
        root = self.roots[prev_ver]
        cur = root
        
        new_node = self.new_node()
        new_node.end_count = cur.end_count - k
        new_node.children = cur.children.copy()
        
        self.roots.append(new_node)
        return self.version_cnt
    
    def lcp(self, ver1, ver2):
        root1 = self.roots[ver1]
        root2 = self.roots[ver2]
        
        if root1.end_count == 0 or root2.end_count == 0:
            return 0
        
        def dfs(node1, node2, depth):
            if node1.end_count == 0 or node2.end_count == 0:
                return depth
            
            for i in range(26):
                child1 = node1.children.get(i)
                child2 = node2.children.get(i)
                
                if child1 and child2:
                    if dfs(child1, child2, depth + 1) == depth:
                        return depth
            return depth
        
        return dfs(root1, root2, 0)

def main():
    input = sys.stdin.read
    data = input().split()
    
    idx = 0
    Q = int(data[idx]); idx += 1
    
    trie = PersistentTrie()
    outputs = []
    
    for q in range(Q):
        tp = int(data[idx]); idx += 1
        
        if tp == 1:
            v = int(data[idx]); idx += 1
            c = data[idx]; idx += 1
            new_ver = trie.append(v, c)
        elif tp == 2:
            v = int(data[idx]); idx += 1
            k = int(data[idx]); idx += 1
            new_ver = trie.delete(v, k)
        else:
            v1 = int(data[idx]); idx += 1
            v2 = int(data[idx]); idx += 1
            lcp_len = trie.lcp(v1, v2)
            outputs.append(str(lcp_len))
    
    print('\n'.join(outputs))

if __name__ == "__main__":
    main()
