import heapq
from Graf_Matrix import Matrix

def prim(matrix):
    n = len(matrix.matrix)  # Количество вершин
    visited = [False] * n  # Посещённые вершины
    min_heap = []  # Минимальная куча для выбора рёбер с минимальным весом
    mst = []  # Минимальное остовное дерево (список рёбер)

    # Начинаем с вершины 0
    heapq.heappush(min_heap, (0, 0, -1))  # (вес, текущая вершина, предыдущая вершина)

    while min_heap:
        weight, current, prev = heapq.heappop(min_heap)

        if visited[current]:
            continue  # Пропускаем уже посещённые вершины

        visited[current] = True  # Помечаем вершину как посещённую

        if prev != -1:  # Игнорируем начальную вершину
            mst.append((prev, current, weight))  # Добавляем ребро в MST

        # Добавляем все смежные рёбра текущей вершины в кучу
        for neighbor in range(n):
            edge_weight = matrix.matrix[current][neighbor]
            if edge_weight > 0 and not visited[neighbor]:  # Если есть ребро и вершина не посещена
                heapq.heappush(min_heap, (edge_weight, neighbor, current))

    return mst

# Пример использования
matrix = Matrix(4)
matrix.add(1, 2, 2)  # Ребро между вершинами 1 и 2 с весом 2
matrix.add(1, 3, 3)  # Ребро между вершинами 1 и 3 с весом 3
matrix.add(2, 3, 1)  # Ребро между вершинами 2 и 3 с весом 1
matrix.add(2, 4, 1)  # Ребро между вершинами 2 и 4 с весом 1
matrix.add(3, 4, 4)  # Ребро между вершинами 3 и 4 с весом 4

matrix.display()

mst = prim(matrix)
print("Минимальное остовное дерево:", mst)