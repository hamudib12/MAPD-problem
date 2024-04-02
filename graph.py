# {v1: [(v2,weight)]}
import sys
from minQueue import MinPriorityQueue


class Graph:
    def __init__(self, graph):
        if not graph:
            self.graph = {}
            self.edges = set()
        if graph:
            self.graph = graph
            for vertex in self.graph.keys():
                for neighbor in self.graph[vertex]:
                    self.edges.add((vertex, neighbor[0], neighbor[
                        1]))  # neighbor[0] = neighbor; neighbor[1] = weight => (V1,V2,W) => ((x1,y1), (x2,y2), w)

    def get_vertices(self):
        return list(self.graph.keys())

    def get_edges(self):
        return self.edges

    def get_weight(self, v1, v2):
        for edge in self.edges:
            if (edge[0] == v1 and edge[1] == v2) or (edge[1] == v1 and edge[0] == v2):
                return int(edge[2])
        # neighbors = self.graph[v1]
        # for neighbor in neighbors:
        #     if neighbor[0] == v2:
        #         return neighbor[1]

    def best_neighbor(self, v):  # best = closest
        minQueue = MinPriorityQueue()
        for neighbor in self.graph[v]:
            minQueue.push((neighbor[1], neighbor[0]))
        w, v2 = minQueue.peek()
        best = (v2, w)
        return best

    def vertex_exists(self, v):
        return v in self.get_vertices()

    def edge_exists(self, v1, v2):
        # neighbors = self.graph[v1]
        # for neighbor in neighbors:
        #     if v2 == neighbor[0]:
        #         return True
        # return False
        for edge in self.edges:
            if (edge[0] == v1 and edge[1] == v2) or (edge[1] == v1 and edge[0] == v2):
                return True
        return False

    def mst_weight(self):
        weight = 0
        for edge in self.edges:
            weight += edge[2]
        return weight / 2

    def add_vertex(self, v):
        if not (v in self.get_vertices()):
            self.graph[v] = []

    def add_edge(self, v1, v2, weight):
        if not (self.edge_exists(v1, v2) and self.edge_exists(v2, v1)):
            self.graph[v1].append((v2, weight))
            self.graph[v2].append((v1, weight))
            self.edges.add((v1, v2, weight))
            self.edges.add((v2, v1, weight))

    def delete_edge(self, v1, v2):
        neighbors_v1 = self.graph[v1]
        neighbors_v2 = self.graph[v2]
        for neighbor in neighbors_v1:
            if neighbor[0] == v2:
                w = neighbor[1]
                neighbors_v1.remove(neighbor)
                self.edges.remove((v1, v2, w))
        for neighbor in neighbors_v2:
            if neighbor[0] == v1:
                w = neighbor[1]
                neighbors_v1.remove(neighbor)
                self.edges.remove((v2, v1, w))

    def create_mst(self):
        # create mst.
        if not self.graph:
            return Graph({})
        visited = set()
        start_vertex = self.get_vertices()[0]
        mst = Graph({})
        minQueue = MinPriorityQueue()
        start_vertex_neighbors = self.graph[start_vertex]
        for neighbor in start_vertex_neighbors:
            minQueue.push((neighbor[1], start_vertex, neighbor[0]))

        visited.add(start_vertex)

        while not minQueue.is_empty():
            current_edge = minQueue.pop()
            weight, v1, v2 = current_edge

            if v2 not in visited:
                visited.add(v2)
                mst.add_vertex(v1)
                mst.add_vertex(v2)
                mst.add_edge(v1, v2, weight)

                for neighbor in self.graph[v2]:
                    if neighbor[0] not in visited:
                        minQueue.push((neighbor[1], v2, neighbor[0]))

        return mst
