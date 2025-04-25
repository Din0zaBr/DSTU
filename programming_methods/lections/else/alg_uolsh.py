from Graf_Matrix_Uolsh import Matrix

def floyd_warshall(matrix):
    n = matrix.len_matix()
    # Создаем матрицу расстояний, инициализируем её значениями из матрицы смежности
    distances = [[matrix.get(i + 1, j + 1) for j in range(n)] for i in range(n)]

    # Основной цикл алгоритма Флойда — Уоршелла
    for k in range(n):
        for i in range(n):
            for j in range(n):
                # Обновляем расстояние, если найден более короткий путь
                distances[i][j] = min(distances[i][j], distances[i][k] + distances[k][j])

    return distances

if __name__ == "__main__":
    matrix = Matrix(4)
    matrix.add(1, 2, 3)
    matrix.add(1, 3, 8)
    matrix.add(1, 4, 2)
    matrix.add(2, 3, 1)
    matrix.add(2, 4, 7)
    matrix.add(3, 4, 1)

    print("Матрица смежности:")
    matrix.display()

    distances = floyd_warshall(matrix)

    print("Матрица кратчайших расстояний:")
    for row in distances:
        print(row)
