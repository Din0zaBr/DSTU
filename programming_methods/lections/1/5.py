from collections import deque, defaultdict


class Graph:
    def __init__(self):
        self.adjacency_list = defaultdict(list)

    def add_edge(self, u, v, directed=False):
        self.adjacency_list[u].append(v)
        if not directed:
            self.adjacency_list[v].append(u)

    def bfs(self, start):
        visited = set()
        queue = deque([start])
        result = []

        while queue:
            vertex = queue.popleft()
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                queue.extend(neighbor for neighbor in self.adjacency_list[vertex] if neighbor not in visited)

        return result

    def dfs(self, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)
        result = [start]

        for neighbor in self.adjacency_list[start]:
            if neighbor not in visited:
                result.extend(self.dfs(neighbor, visited))

        return result

    def is_tree(self):
        visited = set()

        def dfs(vertex, parent):
            visited.add(vertex)
            for neighbor in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    if not dfs(neighbor, vertex):
                        return False
                elif parent != neighbor:
                    return False
            return True

        # Start DFS from any vertex, here we take the first vertex in the adjacency list
        start_vertex = next(iter(self.adjacency_list))
        if not dfs(start_vertex, None):
            return False

        # Check if all vertices are visited (i.e., the graph is connected)
        return len(visited) == len(self.adjacency_list)

    def count_edges(self):
        return sum(len(neighbors) for neighbors in self.adjacency_list.values()) // 2  # For undirected graph

    def shortest_path(self, start, end):
        queue = deque([(start, [start])])
        visited = set()

        while queue:
            vertex, path = queue.popleft()
            if vertex == end:
                return path
            visited.add(vertex)

            for neighbor in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        return None  # If there is no path


# Пример использования
if __name__ == "__main__":
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(1, 3)
    g.add_edge(2, 4)
    g.add_edge(3, 5)
    g.add_edge(4, 5, directed=True)  # Пример направленного ребра

    print("BFS:", g.bfs(1))
    print("DFS:", g.dfs(1))
    print("Is tree:", g.is_tree())
    print("Number of edges:", g.count_edges())
    print("Shortest path from 1 to 5:", g.shortest_path(1, 5))
