import random 
import time
from collections import defaultdict
import tracemalloc #added for timeSortingAlgorithm optimization

# — Global Configuration
sizes = [100, 500, 1000]  # List sizes to test, can be changed for deeper examiniation
inputTypes = { #list generator is up here now! easier for access
    "Random": lambda size: [random.randint(0, 10000) for _ in range(size)],
    "Sorted": lambda size: list(range(size)),
    "Reversed": lambda size: list(range(size, 0, -1))
}

# — Sorting Algorithms 
#Implements Bubble Sort: simple but inefficient (O(n^2) time complexity)
#OPTIMIZIATION: Add a swapped flag to terminate early if no swaps occur in a pass (best-case O(n)):
def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

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
#OPTIMIZATION: Utilized In-Place Quick Sort in order to reduce memory use and allow fairer timing:
def quickSortInPlace(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_index = partition(arr, low, high)
        quickSortInPlace(arr, low, pivot_index - 1)
        quickSortInPlace(arr, pivot_index + 1, high)

def partition(arr, low, high):
    pivot = arr[high]
    i = low
    for j in range(low, high):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[high] = arr[high], arr[i]
    return i

# — Timing Helper
#Measures how long a sorting function takes on a copy of the input array
#OPTIMIZATION: To examine space complexity empirically, I utilized tracemalloc
def timeSortingAlgorithm(sortFunc, arr, inPlace=True):
    arrCopy = arr.copy()
    tracemalloc.start()
    start_time = time.time()
    if inPlace:
        sortFunc(arrCopy)
    else:
        arrCopy = sortFunc(arrCopy)
    end_time = time.time()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return end_time - start_time, peak

# — Main Comparator
#Runs sorting algorithms on different input types and sizes, recording timing data
def compareSorts():
    algorithms = {
        "Bubble Sort": (bubbleSort, True),
        "Merge Sort": (mergeSort, True),
        "Quick Sort": (quickSortInPlace, False)
    }

    results = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for size in sizes:
        for inputName, generator in inputTypes.items():
            arr = generator(size)
            for algoName, (algoFunc, inPlace) in algorithms.items():
                elapsed, _ = timeSortingAlgorithm(algoFunc, arr, inPlace)
                results[algoName][inputName][size].append(elapsed)

    return results

# NEW FUNCTION!
# — Multi-Run Comparator with Ranking System 
#Will run the compareSorts() function 100 times and compress the data for better averaging and analysis
def collectAndCompareRuns(numRuns=100):
    overallResults = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for _ in range(numRuns):
        runResults = compareSorts()
        for algoName, inputData in runResults.items():
            for inputName, sizeData in inputData.items():
                for size, times in sizeData.items():
                    overallResults[algoName][inputName][size].extend(times)

    # Compute average timings
    averageResults = {}
    for algoName, inputData in overallResults.items():
        averageResults[algoName] = {}
        for inputName, sizeData in inputData.items():
            averageResults[algoName][inputName] = {}
            for size, times in sizeData.items():
                averageResults[algoName][inputName][size] = sum(times) / len(times)

    # Print average timings
    for algoName, inputData in averageResults.items():
        print(f"\n{algoName} Average Times:")
        for inputName, sizeData in inputData.items():
            for size, avgTime in sizeData.items():
                print(f"  {inputName} list of size {size}: {avgTime:.6f} seconds")

    # Find best algorithms by input type and size
    print("\nSummary of Best Algorithms by Input Type and Size:")
    summary_messages = []
    bestAlgoCount = defaultdict(int)

    for inputType in inputTypes:
        for size in sizes:
            bestAlgo = None
            bestTime = float('inf')
            for algoName in averageResults:
                avgTime = averageResults[algoName].get(inputType, {}).get(size)
                if avgTime is not None and avgTime < bestTime:
                    bestTime = avgTime
                    bestAlgo = algoName
            if bestAlgo:
                bestAlgoCount[bestAlgo] += 1
                summary_messages.append(
                    f"For {inputType} lists of size {size}, the best algorithm on average is: {bestAlgo} ({bestTime:.6f} seconds)"
                )

    for msg in summary_messages:
        print(msg)

    # Final ranking system
    print("\nRanking of Sorting Algorithms by Number of Wins:")

    # Make sure every algorithm is represented, even if they have 0 wins
    allAlgorithms = ["Bubble Sort", "Merge Sort", "Quick Sort"]
    for algo in allAlgorithms:
        if algo not in bestAlgoCount:
            bestAlgoCount[algo] = 0  # Initialize with 0 wins if missing

    # Sort the algorithms based on the number of wins
    sortedRanking = sorted(bestAlgoCount.items(), key=lambda x: x[1], reverse=True)

    # Print the sorted ranking
    for rank, (algo, count) in enumerate(sortedRanking, 1):
        print(f"{rank}. {algo} - {count} wins")

#Runs the comparator when the script is executed
if __name__ == "__main__":
    print("After 100 runs, these are the results: (this may take a moment, please be patient...)\n")
    collectAndCompareRuns()