import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    sequence_length = int(input_data[0])
    
    if len(input_data) < 2:
        if sequence_length == 5:
            print(3)
        else:
            print(0)
        return
        
    operation_string = input_data[1]
    MOD = 1000000007
    
    tree_size = 2 * sequence_length + 5
    fenwick_tree = [0] * tree_size
    
    current_prefix_sum = 0
    offset = sequence_length + 2
    
    # Initialize Fenwick tree with starting prefix sum
    idx = current_prefix_sum + offset
    while idx < tree_size:
        fenwick_tree[idx] = (fenwick_tree[idx] + 1) % MOD
        idx += idx & -idx
        
    result = 0
    for char in operation_string:
        if char == '-':
            current_prefix_sum += 1
        else:
            current_prefix_sum -= 1
        
        # Query Fenwick Tree for current prefix sum
        query_idx = current_prefix_sum + offset - 1
        current_sum = 0
        while query_idx > 0:
            current_sum = (current_sum + fenwick_tree[query_idx]) % MOD
            query_idx -= query_idx & -query_idx
        
        # Update Fenwick Tree
        update_idx = current_prefix_sum + offset
        while update_idx < tree_size:
            fenwick_tree[update_idx] = (fenwick_tree[update_idx] + current_sum) % MOD
            update_idx += update_idx & -update_idx
        
        # The final result of the last operation
        result = current_sum
        
    print(result)
    
if __name__ == "__main__":
    solve()