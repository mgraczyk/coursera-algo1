#!/usr/bin/python

class UnionFind(object):
    def __init__(self, N):
        self._id = list(range(N))

    def union(self, p, q):
        raise NotImplementedError()

    def find(self, p, q):
        raise NotImplementedError()

    def get_ids(self):
        return " ".join(map(str, self._id))

    def do_unions(self, ustr):
        unions = tuple(tuple(map(int, v.split("-"))) for v in ustr.split(" "))
        for vals in unions:
            self.union(*vals)

        for vals in unions:
            assert(self.find(*vals))


class QuickFind(UnionFind):
    def union(self, p, q):
        pId = self._id[p]
        qId = self._id[q]
        for i, val in enumerate(self._id):
            if val == pId:
                self._id[i] = qId

    def find(self, p, q):
        return self._id[p] == self._id[q]

class QuickUnion(UnionFind):
    def __init__(self, N):
        super().__init__(N)
        self._sizes = [1]*N

    def union(self, p, q):
        roots = self._root(p), self._root(q)
        sizes = self._sizes[roots[0]], self._sizes[roots[1]]

        if sizes[1] > sizes[0]:
            # Reverse
            roots = roots[::-1]
            sizes = sizes[::-1]

        self._id[roots[1]] = roots[0]
        self._sizes[roots[0]] += self._sizes[roots[1]]

    def find(self, p, q):
        return self._root(p) == self._root(q)

    def get_sizes(self):
        return " ".join(map(str, self._sizes))

    def _root(self, i):
        while i != self._id[i]:
            i = self._id[i]

        return i

def get_height(arr, i):
    h = 1
    while i != arr[i] and h <= len(arr):
        h += 1
        i = arr[i]

    if h > len(arr):
        return None
    else:
        return h

def get_heights(arrStr):
    arr = tuple(map(int, arrStr.split(" ")))
    return " ".join(map(str, (get_height(arr, i) for i in range(len(arr)))))

def pr1():
    print("Problem 1:")
    uf = QuickFind(10)
    uf.do_unions("6-3 9-7 0-6 8-4 4-0 1-5")
    print(uf.get_ids())
    print()

           
def pr2():
    print("Problem 2:")
    uf = QuickUnion(10)
    uf.do_unions("0-6 7-2 5-2 8-9 6-8 5-4 2-1 2-3 3-0")
    print(uf.get_ids())
    print()

           
def pr3():
    tests = [
        "6 6 8 6 8 4 6 6 6 6",
        "6 1 2 3 7 9 6 7 8 9",
        "3 3 6 5 5 9 5 5 5 0",
        "3 8 9 3 8 5 8 9 3 6",
        "5 5 2 5 5 2 5 0 5 2"]
    print("Problem 3:")
    for test in tests:
        print(get_heights(test))
        print()

if __name__ == "__main__":
    pr1()
    pr2()
    pr3()
