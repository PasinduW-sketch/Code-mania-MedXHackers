import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    num_elements = int(input_data[0])
    num_queries = int(input_data[1])
    
    basis_table = [[0] * 30 for _ in range(num_elements + 1)]
    position_table = [[0] * 30 for _ in range(num_elements + 1)]
    
 
    for i in range(1, num_elements + 1):
        current_value = int(input_data[1 + i])
        basis_table[i] = basis_table[i - 1][:]
        position_table[i] = position_table[i - 1][:]
        current_pos = i
        
        for bit in range(29, -1, -1):
            if (current_value >> bit) & 1:
                if not basis_table[i][bit]:
                    basis_table[i][bit] = current_value
                    position_table[i][bit] = current_pos
                    break
                
                if position_table[i][bit] < current_pos:
                    current_pos, position_table[i][bit] = position_table[i][bit], current_pos
                    current_value, basis_table[i][bit] = basis_table[i][bit], current_value
                
                current_value ^= basis_table[i][bit]
    
    data_pointer = num_elements + 2
    results = []
    
    for _ in range(num_queries):
        left_bound = int(input_data[data_pointer])
        right_bound = int(input_data[data_pointer + 1])
        data_pointer += 2
        
        
        max_xor = 0
        for bit in range(29, -1, -1):
            if position_table[right_bound][bit] >= left_bound:
                
                if (max_xor ^ basis_table[right_bound][bit]) > max_xor:
                    max_xor ^= basis_table[right_bound][bit]
        
        results.append(str(max_xor))
    
  
    print('\n'.join(results))

if __name__ == '__main__':
    solve()
