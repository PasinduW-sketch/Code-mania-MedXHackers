import sys
sys.setrecursionlimit(300000)

def main():
    input = sys.stdin.buffer.read().split()
    idx = 0
    Q = int(input[idx]); idx += 1
    
    # For each version, store: parent pointer, character, depth (length), and binary ancestors
    # version 0: empty string
    parent = [0]  # parent[i] = parent version of version i
    char = ['']   # char[i] = character added at version i (for version 0, it's empty)
    depth = [0]   # depth[i] = length of string at version i
    
    # Binary lifting table: up[i][j] = 2^j-th ancestor of version i
    LOG = 20
    up = [[0] * LOG]
    
    # Hash values for rolling hash (for LCP binary search)
    BASE = 911382629
    MOD = 10**18 + 9
    pow_base = [1] * (Q + 10)
    for i in range(1, Q + 10):
        pow_base[i] = (pow_base[i-1] * BASE) % MOD
    
    # Hash[i] = hash of string at version i
    hash_val = [0]
    
    output = []
    
    for _ in range(Q):
        op = int(input[idx]); idx += 1
        
        if op == 1:
            # Append: take version v, append character c
            v = int(input[idx]); idx += 1
            c = input[idx].decode(); idx += 1
            
            new_version = len(parent)
            parent.append(v)
            char.append(c)
            depth.append(depth[v] + 1)
            
            # Update binary lifting table
            new_up = [0] * LOG
            new_up[0] = v
            for j in range(1, LOG):
                new_up[j] = up[new_up[j-1]][j-1] if new_up[j-1] < len(up) else 0
            up.append(new_up)
            
            # Update hash
            new_hash = (hash_val[v] * BASE + ord(c)) % MOD
            hash_val.append(new_hash)
            
        elif op == 2:
            # Delete last k characters from version v
            v = int(input[idx]); idx += 1
            k = int(input[idx]); idx += 1
            
            new_version = len(parent)
            # Find ancestor at depth depth[v] - k
            target_depth = depth[v] - k
            curr = v
            for j in range(LOG-1, -1, -1):
                if depth[curr] - (1 << j) >= target_depth:
                    curr = up[curr][j]
            
            parent.append(curr)
            char.append('')  # no new character
            depth.append(depth[curr])
            up.append(up[curr][:])  # copy ancestors
            hash_val.append(hash_val[curr])
            
        elif op == 3:
            # LCP query between versions v1 and v2
            v1 = int(input[idx]); idx += 1
            v2 = int(input[idx]); idx += 1
            
            # Binary search on LCP length
            lo, hi = 0, min(depth[v1], depth[v2])
            ans = 0
            
            while lo <= hi:
                mid = (lo + hi) // 2
                # Get hash of first mid characters of v1 and v2
                h1 = get_hash(v1, mid, up, depth, hash_val, pow_base, BASE, MOD)
                h2 = get_hash(v2, mid, up, depth, hash_val, pow_base, BASE, MOD)
                
                if h1 == h2:
                    ans = mid
                    lo = mid + 1
                else:
                    hi = mid - 1
            
            output.append(ans)
    
    print('\n'.join(map(str, output)))

def get_hash(v, length, up, depth, hash_val, pow_base, BASE, MOD):
    """Get hash of first 'length' characters of version v"""
    if length == 0:
        return 0
    if length == depth[v]:
        return hash_val[v]
    
    # Find ancestor at depth depth[v] - length (node after removing last (depth[v]-length) chars)
    # We want prefix of length 'length', so we need to go up by (depth[v] - length) steps
    steps = depth[v] - length
    curr = v
    for j in range(len(up[0])-1, -1, -1):
        if steps >= (1 << j):
            curr = up[curr][j]
            steps -= (1 << j)
    
    # hash_val[v] = hash_val[curr] * BASE^(depth[v]-depth[curr]) + suffix_hash
    # We need to extract the prefix hash
    # hash_val[v] = hash_prefix * BASE^(len_suffix) + hash_suffix
    # hash_prefix = (hash_val[v] - hash_suffix) / BASE^(len_suffix)
    
    # Actually, let's use a different approach: compute hash from root to curr
    return hash_val[curr]

if __name__ == "__main__":
    main()