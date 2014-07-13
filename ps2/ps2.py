#!/usr/bin/python3

import random
import math

def is_sorted(data, lo=None, hi=None):
    if lo == None:
        lo = 0
    if hi == None:
        hi = len(data)
    
    return all(data[i] >= data[i-1] for i in range(lo + 1, hi))

class SortAlgorithm(object):
    def observable_sort(self, data, statusCallback):
        raise NotImplementedError()

    def sort(self, data):
        return self.observable_sort(data, None)

    def get_sort_state(self, data, stepNumber):
        steps = 0
        state = None
        def capture(data):
            nonlocal steps
            nonlocal state
            steps += 1
            if steps == stepNumber:
                state = tuple(data)

        self.observable_sort(data, capture)
        assert(is_sorted(data))
        return state

class MergeSort(SortAlgorithm):
    @staticmethod
    def _merge(arr, aux, lo, mid, hi):
        assert(is_sorted(arr, lo, mid))
        assert(is_sorted(arr, mid, hi))

        i = lo
        j = mid
        k = lo
        while i < mid and j < hi:
            if arr[i] <= arr[j]:
                aux[k] = arr[i]
                i += 1
            else:
                aux[k] = arr[j]
                j += 1
            k += 1

        while i < mid:
            aux[k] = arr[i]
            k += 1
            i += 1
        
        while j < hi:
            aux[k] = arr[j]
            k += 1
            j += 1

        assert(is_sorted(aux, lo, hi))

class TopDownMergeSort(MergeSort):
    def _sort(self, arr, aux, lo, hi, statusCallback):
        if hi - lo <= 1:
            return

        mid = int(lo + (hi - lo)/2)
        self._sort(aux, arr, lo, mid, statusCallback)
        self._sort(aux, arr, mid, hi, statusCallback)
        self._merge(arr, aux, lo, mid, hi)

        if statusCallback:
            statusCallback(arr)

    def observable_sort(self, data, statusCallback):
        aux = data[:]
        first, second = aux, data

        self._sort(first, second, 0, len(data), statusCallback)

class BottomUpMergeSort(MergeSort):
    def observable_sort(self, data, statusCallback):
        if not data:
            return
        N = len(data)
        aux = [None]*N

        first, second = data, aux
        sz = 1
        while sz < N:
            lo = 0
            while lo < N - sz:
                self._merge(first, second, lo, lo + sz, min(lo+2*sz, N))
                lo += 2*sz

                if statusCallback:
                    statusCallback(data)

            second[lo:N] = first[lo:N]
            first, second = second, first
            sz *= 2

        log2RoundDown = int(math.log(N,2))
        evenTwo = log2RoundDown % 2 == 0
        powerOfTwo = not (N & (N - 1))
        if evenTwo or not is_sorted(data):
            data[:] = aux[:]


def parse_input_string(inStr):
    return list(map(int, inStr.split(" ")))

def format_output(data):
    return " ".join(map(str, data))

def test_sort(sortAlgorithm, N=10, maxLen=1000, seed=None):
    random.seed(seed)

    passed = True
    for _ in range(N):
        data = [random.randint(0, 100) for _ in range(random.randint(0, maxLen))]
        sortAlgorithm.sort(data)
        if not is_sorted(data):
            print("ERROR: Sorting algorithm {} produced bad data ->".format(sortAlgorithm))
            print(len(data))
            print(data)
            print()
            passed = False
    return passed

def p1():
    topDown = TopDownMergeSort()
    test_sort(topDown, 10, 5000)

    p1Str = "75 26 42 35 67 57 62 49 56 61 44 65"
    state = topDown.get_sort_state(parse_input_string(p1Str), 7)
    print("1: Step 7")
    print(format_output(state))

def p2():
    bottomUp = BottomUpMergeSort()
    test_sort(bottomUp, 100, 1000)
    p2Str = "94 50 47 74 85 57 31 28 48 40"
    state = bottomUp.get_sort_state(parse_input_string(p2Str), 7)
    print("2: Step 7")
    print(format_output(state))

def main():
    p1()
    p2()

if __name__ == "__main__":
    main()
