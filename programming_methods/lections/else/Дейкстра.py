import heapq
from Graf_Matrix import Matrix


def dijkstra(matrix, start):
    n = len(matrix.matrix)  # Количество вершин в matrix
    distances = [float(
        'infinity')] * n  #  массив, хранящий минимальные расстояния от начальной вершины до всех остальных вершин
    distances[start - 1] = 0
    priority_queue = [(0, start)]  # это список кортежей, где каждый кортеж содержит расстояние и номер вершины.
    # Изначально в очередь добавляется стартовая вершина с расстоянием 0.

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(
            priority_queue)  # Пока очередь не пуста, извлекается вершина с минимальным расстоянием.

        if current_distance > distances[current_vertex - 1]:
            continue

        for neighbor in range(1,
                              n + 1):  # Для каждой соседней вершины вычисляется новое расстояние через текущую вершину.
            weight = matrix.get(current_vertex, neighbor)
            if weight > 0:
                distance = current_distance + weight
                if distance < distances[neighbor - 1]:
                    # Если новое расстояние меньше текущего минимального расстояния до соседней вершины,
                    # обновите его и добавьте соседнюю вершину в очередь с новым расстоянием.
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

    distances = dijkstra(matrix, 1)
    print("Расстояния до вершин:")
    print(distances)
