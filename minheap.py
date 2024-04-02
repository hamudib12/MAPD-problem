import heapq


class MinHeap:
    def __init__(self, key_func):
        self.heap = []
        self.key_func = key_func

    def push(self, item):
        priority = self.key_func(item)
        heapq.heappush(self.heap, (priority, item))

    def __str__(self):
        return ' '.join([str(i) for i in self.heap])

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)[1]
        else:
            raise IndexError("pop from an empty priority queue")

    def is_empty(self):
        return len(self.heap) == 0
