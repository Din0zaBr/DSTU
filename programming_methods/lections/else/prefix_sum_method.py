class PrefixSum:
    def __init__(self, array):
        self.prefix = [0] * (len(array) + 1)
        for i in range(len(array)):
            self.prefix[i + 1] = self.prefix[i] + array[i]

    def query(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]

# Пример использования
array = [1, 2, 3, 4, 5]
prefix_sum = PrefixSum(array)

# Сумма на отрезке от индекса 1 до 3 (включительно)
result = prefix_sum.query(1, 3)
print(result)  # Вывод: 9 (2 + 3 + 4)