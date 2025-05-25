import random 
import time
from collections import defaultdict
import tracemalloc 
import numpy as np
import math

# — Global Configuration
sizes = [100, 250, 500]  # List sizes to test, can be changed for deeper examiniation, lowered from (100,500,1000) due to long waiting time
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
        pivotIndex = medianOfThreePartition(arr, low, high)
        quickSortInPlace(arr, low, pivotIndex - 1)
        quickSortInPlace(arr, pivotIndex + 1, high)

def medianOfThreePartition(arr, low, high):
    mid = (low + high) // 2
    pivotCandidates = [(arr[low], low), (arr[mid], mid), (arr[high], high)]
    # Sort by value and select the median's index
    _, pivotIndex = sorted(pivotCandidates, key=lambda x: x[0])[1]

    # Move the pivot to the end
    arr[pivotIndex], arr[high] = arr[high], arr[pivotIndex]

    # Standard Lomuto partition
    pivot = arr[high]
    i = low
    for j in range(low, high):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[high] = arr[high], arr[i]
    return i

def timeSortingAlgorithm(sortFunc, arr, inPlace=True):
    arrCopy = arr.copy()
    tracemalloc.start()
    startTime = time.time()
    if inPlace:
        sortFunc(arrCopy)
    else:
        arrCopy = sortFunc(arrCopy)
    endTime = time.time()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return endTime - startTime, peak

# — Main Comparator
#Runs sorting algorithms on different input types and sizes, recording timing data
#UPDATED: New version of compareSorts that also returns space usage
def compareSortsWithSpace():
    algorithms = {
        "Bubble Sort": (bubbleSort, True),
        "Merge Sort": (mergeSort, True),
        "Quick Sort": (quickSortInPlace, False)
    }

    results = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    space_results = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for size in sizes:
        for inputName, generator in inputTypes.items():
            arr = generator(size)
            for algoName, (algoFunc, inPlace) in algorithms.items():
                elapsed, peak = timeSortingAlgorithm(algoFunc, arr, inPlace)
                results[algoName][inputName][size].append(elapsed)
                space_results[algoName][inputName][size].append(peak)

    return results, space_results

# — Multi-Run Comparator with Ranking System 
#Will run the compareSorts() function 100 times and compress the data for better averaging and analysis
#UPDATED: in order to take space results as well
def collectRunsWithSpace(numRuns=50): #lowered run count as it was a lot for my laptop to load
    overallTime = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    overallSpace = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for _ in range(numRuns):
        runTime, runSpace = compareSortsWithSpace()
        for algoName, inputData in runTime.items():
            for inputName, sizeData in inputData.items():
                for size, times in sizeData.items():
                    overallTime[algoName][inputName][size].extend(times)
                    overallSpace[algoName][inputName][size].extend(runSpace[algoName][inputName][size])

    return overallTime, overallSpace

# — NEW Complexity Analysis Function
def analyzeComplexityTrends(timeData, spaceData):
    print("\nEmpirical Complexity Analysis:")
    def fitTrend(xVals, yVals):
        epsilon = 1e-9  #small positive value to avoid log(0)

        #add epsilon to all values to ensure no zero or negative values
        xLog = [math.log(x + epsilon) for x in xVals]
        yVals = [y + epsilon for y in yVals]  #make sure its positive for log
        yLog = [math.log(y) for y in yVals]

        linearFit = np.polyfit(xVals, yVals, 1)
        logFit = np.polyfit(xLog, yVals, 1)
        loglogFit = np.polyfit(xLog, yLog, 1)

        return {
            "Linear Fit (n)": linearFit,
            "Log Fit (log n)": logFit,
            "Log-Log Fit (log n, log y)": loglogFit
        }
    for algoName in timeData:
        print(f"\n→ {algoName} Complexity Trends:")
        for inputName in timeData[algoName]:
            sizesList = []
            avgTimes = []
            avgSpaces = []

            for size in sorted(timeData[algoName][inputName]):
                sizesList.append(size)
                avgTimes.append(np.mean(timeData[algoName][inputName][size]))
                avgSpaces.append(np.mean(spaceData[algoName][inputName][size]))

            print(f"  Input Type: {inputName}")
            timeTrends = fitTrend(sizesList, avgTimes)
            spaceTrends = fitTrend(sizesList, avgSpaces)

            loglogSlopeTime = timeTrends["Log-Log Fit (log n, log y)"][0]
            loglogSlopeSpace = spaceTrends["Log-Log Fit (log n, log y)"][0]

            def interpretSlope(slope):
                if slope < 1.2:
                    return "≈ O(n)"
                elif slope < 1.8:
                    return "≈ O(n log n)"
                else:
                    return "≈ O(n²)"

            timeComplexity = interpretSlope(loglogSlopeTime)
            spaceComplexity = interpretSlope(loglogSlopeSpace)

            print(f"    Estimated Time Complexity: {timeComplexity} (slope: {loglogSlopeTime:.2f})")
            print(f"    Estimated Space Complexity: {spaceComplexity} (slope: {loglogSlopeSpace:.2f})")

# readded and updated the ranking system 
def rankAlgorithmsByTime(timeData):
    print("\nAverage Timings Across Runs:")
    averageResults = {}
    for algoName, inputData in timeData.items():
        averageResults[algoName] = {}
        for inputName, sizeData in inputData.items():
            averageResults[algoName][inputName] = {}
            for size, times in sizeData.items():
                averageResults[algoName][inputName][size] = sum(times) / len(times)

    for algoName, inputData in averageResults.items():
        print(f"\n{algoName} Average Times:")
        for inputName, sizeData in inputData.items():
            for size, avgTime in sizeData.items():
                print(f"  {inputName} list of size {size}: {avgTime:.6f} seconds")

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

    print("\nRanking of Sorting Algorithms by Number of Wins:")

    allAlgorithms = ["Bubble Sort", "Merge Sort", "Quick Sort"]
    for algo in allAlgorithms:
        if algo not in bestAlgoCount:
            bestAlgoCount[algo] = 0

    sortedRanking = sorted(bestAlgoCount.items(), key=lambda x: x[1], reverse=True)
    for rank, (algo, count) in enumerate(sortedRanking, 1):
        print(f"{rank}. {algo} - {count} wins")

# — Main Execution Block
if __name__ == "__main__":
    print("After 50 runs, these are the results: (this may take a moment, please be patient...)\n")
    timeData, spaceData = collectRunsWithSpace()
    analyzeComplexityTrends(timeData, spaceData)
    rankAlgorithmsByTime(timeData)