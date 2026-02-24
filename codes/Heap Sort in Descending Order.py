import sys

def heapify(arr, n, i):
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] < arr[smallest]:
        smallest = left
    
    if right < n and arr[right] < arr[smallest]:
        smallest = right
    
    if smallest != i:
        arr[i], arr[smallest] = arr[smallest], arr[i]
        heapify(arr, n, smallest)

def heapSort(arr):
    n = len(arr)
    
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    
    return arr

def main():
    input_data = sys.stdin.buffer.read().split()
    n = int(input_data[0])
    arr = list(map(int, input_data[1:n+1]))
    
    sorted_arr = heapSort(arr)
    
    print(' '.join(map(str, sorted_arr)))

if __name__ == "__main__":
    main()
