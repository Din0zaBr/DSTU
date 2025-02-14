def find_closest_pair(A, B):
    i, j = 0, 0
    n, m = len(A), len(B)
    closest_pair = (None, None)
    min_diff = float('inf')

    while i < n and j < m:
        diff = abs(A[i] - B[-j])

        if diff < min_diff:
            min_diff = diff
            closest_pair = (A[i], B[-j])

        if A[i] < B[-j]:
            i += 1
        else:
            j -= 1

    return closest_pair


# Пример использования
A: list = sorted([int(el) for el in input("Введите массив данных через пробел:").split()])
B: list = sorted([int(el) for el in input("Введите массив данных через пробел: ").split()])

print(find_closest_pair(A, B))
