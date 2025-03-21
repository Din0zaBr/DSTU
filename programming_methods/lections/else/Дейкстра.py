import heapq
from Graf_Matrix import Matrix

def dijkstra(matrix, start):
    n = matrix.len_matix()
    distances = [float('infinity')] * n
    distances[start - 1] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex - 1]:
            continue

        for neighbor in range(1, n + 1):
            weight = matrix.get(current_vertex, neighbor)
            if weight > 0:
                distance = current_distance + weight
                if distance < distances[neighbor - 1]:
                    distances[neighbor - 1] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))

    return distances

if __name__ == "__main__":
    matrix = Matrix(4)
    matrix.add(1, 2, 1)
    matrix.add(1, 3, 4)
    matrix.add(2, 3, 2)
    matrix.add(2, 4, 5)
    matrix.add(3, 4, 1)

    print("Матрица смежности:")
    matrix.display()

    start_vertex = 1
    shortest_paths = dijkstra(matrix, start_vertex)

    print(f"Кратчайшие пути от вершины {start_vertex}:")
    for i in range(len(shortest_paths)):
        print(f"Вершина {i + 1}: {shortest_paths[i]}")