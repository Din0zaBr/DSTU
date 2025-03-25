class Matrix:
    def __init__(self, len_matrix):
        # Инициализация матрицы смежности с бесконечными значениями
        self.matrix = [[float('inf') if i != j else 0 for j in range(len_matrix)] for i in range(len_matrix)]

    def add(self, i, j, len_dug):
        # Добавление ребра с весом len_dug
        self.matrix[i - 1][j - 1] = len_dug

    def get(self, i, j):
        # Получение веса ребра между вершинами i и j
        return self.matrix[i - 1][j - 1]

    def len_matix(self):
        # Возвращает количество вершин в графе
        return len(self.matrix)

    def display(self):
        # Вывод матрицы смежности
        for row in self.matrix:
            print(row)
