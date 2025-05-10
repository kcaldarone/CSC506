import random
import time

def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        leftHalf = arr[:mid]
        rightHalf = arr[mid:]

        mergeSort(leftHalf)
        mergeSort(rightHalf)

        i = j = k = 0

        while i < len(leftHalf) and j < len(rightHalf):
            if leftHalf[i] < rightHalf[j]:
                arr[k] = leftHalf[i]
                i += 1
            else:
                arr[k] = rightHalf[j]
                j += 1
            k += 1

        while i < len(leftHalf):
            arr[k] = leftHalf[i]
            i += 1
            k += 1

        while j < len(rightHalf):
            arr[k] = rightHalf[j]
            j += 1
            k += 1

    return arr

#Comparison Function
def compareSortingAlgorithms():
    patientIds = [random.randint(1, 10000) for _ in range(1000)]

    bubbleSortIds = patientIds.copy()
    mergeSortIds = patientIds.copy()

    startTime = time.time()
    bubbleSort(bubbleSortIds)
    bubbleSortTime = time.time() - startTime

    startTime = time.time()
    mergeSort(mergeSortIds)
    mergeSortTime = time.time() - startTime

    print(f"Bubble Sort Time: {bubbleSortTime:.6f} seconds")
    print(f"Merge Sort Time: {mergeSortTime:.6f} seconds")

compareSortingAlgorithms()