from Graf_Matrix import Matrix

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))  # Родительская вершина для каждой вершины
        self.rank = [1] * n  # Ранг (глубина) дерева для каждой вершины

    def find(self, u):
        # Находим корень дерева, к которому принадлежит вершина u
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])  # Сжатие пути
        return self.parent[u]

    def union(self, u, v):
        # Объединяем два дерева
        root_u = self.find(u)
        root_v = self.find(v)

        if root_u != root_v:
            # Присоединяем дерево с меньшим рангом к дереву с большим рангом
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            elif self.rank[root_u] < self.rank[root_v]:
                self.parent[root_u] = root_v
            else:
                self.parent[root_v] = root_u
                self.rank[root_u] += 1

def kruskal(matrix):
    n = len(matrix.matrix)  # Количество вершин
    edges = []  # Список всех рёбер

    # Собираем все рёбра из матрицы смежности
    for i in range(n):
        for j in range(i + 1, n):  # Чтобы не дублировать рёбра
            if matrix.matrix[i][j] > 0:
                edges.append((matrix.matrix[i][j], i, j))  # (вес, вершина1, вершина2)

    # Сортируем рёбра по весу
    edges.sort()

    uf = UnionFind(n)  # Структура Union-Find для проверки циклов
    mst = []  # Минимальное остовное дерево (список рёбер)

    for weight, u, v in edges:
        if uf.find(u) != uf.find(v):  # Если рёбра не образуют цикл
            uf.union(u, v)  # Объединяем множества
            mst.append((u, v, weight))  # Добавляем ребро в MST

    return mst

# Пример использования
matrix = Matrix(4)
matrix.add(1, 2, 2)  # Ребро между вершинами 1 и 2 с весом 2
matrix.add(1, 3, 3)  # Ребро между вершинами 1 и 3 с весом 3
matrix.add(2, 3, 1)  # Ребро между вершинами 2 и 3 с весом 1
matrix.add(2, 4, 1)  # Ребро между вершинами 2 и 4 с весом 1
matrix.add(3, 4, 4)  # Ребро между вершинами 3 и 4 с весом 4

matrix.display()

mst = kruskal(matrix)
print("Минимальное остовное дерево:", mst)