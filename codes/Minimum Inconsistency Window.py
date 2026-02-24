import sys
import heapq
input = sys.stdin.readline

def solve():
    N = int(input())
    logs = []
    for _ in range(N):
        L = int(input())
        arr = list(map(int, input().split()))
        logs.append(arr)
    
    # Initialize min-heap with first element from each log
    heap = []
    current_max = 0
    for i in range(N):
        val = logs[i][0]
        heapq.heappush(heap, (val, i, 0))  # (value, log_index, element_index)
        current_max = max(current_max, val)
    
    min_window = float('inf')
    
    while True:
        current_min, log_idx, elem_idx = heapq.heappop(heap)
        min_window = min(min_window, current_max - current_min)
        
        # Move pointer in the same log
        if elem_idx + 1 < len(logs[log_idx]):
            next_val = logs[log_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, log_idx, elem_idx + 1))
            current_max = max(current_max, next_val)
        else:
            break  # Reached the end of one log, cannot cover all logs anymore
    
    print(min_window)

if __name__ == "__main__":
    solve()