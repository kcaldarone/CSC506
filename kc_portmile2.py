import random 
import time

# — Sorting Algorithms 
#Implements Bubble Sort: simple but inefficient (O(n^2) time complexity)
def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

#Implements Merge Sort: an efficient divide-and-conquer algorithm (O(n log n) time complexity)
def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left = arr[:mid]
        right = arr[mid:]

        mergeSort(left)
        mergeSort(right)

        i = j = k = 0

        #Merge the sorted halves
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        #Copy any remaining elements
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

#Implements Quick Sort: another efficient divide-and-conquer algorithm (average O(n log n), worst O(n^2))
def quickSort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return quickSort(left) + middle + quickSort(right)

# — Input Generators
#Generates a list of random integers (testing performance on unsorted data)
def generateRandomList(size):
    return [random.randint(0, 10000) for _ in range(size)]

#Generates a pre-sorted list (testing best-case or special performance)
def generateSortedList(size):
    return list(range(size))

#Generates a list sorted in reverse order (testing worst-case scenarios for some algorithms)
def generateReversedList(size):
    return list(range(size, 0, -1))

# — Timing Helper
#Measures how long a sorting function takes on a copy of the input array
def timeSortingAlgorithm(sortFunc, arr, inPlace=True):
    arrCopy = arr.copy()  #Prevents modification of original array
    start = time.time()
    if inPlace:
        sortFunc(arrCopy)  #Sorts in-place
    else:
        sortFunc(arrCopy)  #Sorts and returns a new list (quickSort)
    end = time.time()
    return end - start

# — Main Comparator
#Runs sorting algorithms on different input types and sizes, recording timing data
def compareSorts():
    sizes = [100, 500, 1000]  #List sizes to test (can be increased for deeper analysis)
    inputTypes = {
        "Random": generateRandomList,
        "Sorted": generateSortedList,
        "Reversed": generateReversedList
    }
    algorithms = {
        "Bubble Sort": (bubbleSort, True),
        "Merge Sort": (mergeSort, True),
        "Quick Sort": (quickSort, False)  #QuickSort returns a new list, not in-place
    }

    for size in sizes:
        print(f"\n--- List Size: {size} ---")
        for inputName, generator in inputTypes.items():
            arr = generator(size)
            print(f"\nInput Type: {inputName}")
            for algoName, (algoFunc, inPlace) in algorithms.items():
                elapsed = timeSortingAlgorithm(algoFunc, arr, inPlace)
                print(f"{algoName}: {elapsed:.6f} seconds")

#Runs the comparator when the script is executed
if __name__ == "__main__":
    compareSorts()