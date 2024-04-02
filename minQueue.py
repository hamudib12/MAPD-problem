import heapq


class MinPriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, element):
        heapq.heappush(self.heap, element)

    def pop(self):
        if not self.is_empty():
            return heapq.heappop(self.heap)
        else:
            raise IndexError("Priority queue is empty")

    def is_empty(self):
        return len(self.heap) == 0

    def peek(self):
        if not self.is_empty():
            return self.heap[0]
        else:
            raise IndexError("Priority queue is empty")
