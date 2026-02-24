import sys

def selectionSort(arr):
    """
    Sorts array in descending order using Selection Sort.
    Finds the maximum element in the unsorted portion and swaps it to the front.
    """
    n = len(arr)
    
    for i in range(n):
        # Find the index of the maximum element in the unsorted portion
        max_idx = i
        for j in range(i + 1, n):
            if arr[j] > arr[max_idx]:
                max_idx = j
        
        # Swap the found maximum with the first element of unsorted portion
        arr[i], arr[max_idx] = arr[max_idx], arr[i]
    
    return arr

def main():
    input_data = sys.stdin.buffer.read().split()
    n = int(input_data[0])
    arr = list(map(int, input_data[1:n+1]))
    
    sorted_arr = selectionSort(arr)
    
    print(' '.join(map(str, sorted_arr)))

if __name__ == "__main__":
    main()
