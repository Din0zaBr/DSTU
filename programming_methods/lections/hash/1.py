class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]  # Создаем список списков

    def _hash(self, key):
        # Простая хеш-функция: сумма ASCII-кодов символов ключа по модулю size
        return sum(ord(c) for c in str(key)) % self.size

    def insert(self, key, value):
        hash_key = self._hash(key)
        bucket = self.table[hash_key]

        # Проверяем, нет ли уже такого ключа в цепочке
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)  # Обновляем значение, если ключ существует
                return
        bucket.append((key, value))  # Добавляем новую пару ключ-значение

    def get(self, key):
        hash_key = self._hash(key)
        bucket = self.table[hash_key]

        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(key)

    def delete(self, key):
        hash_key = self._hash(key)
        bucket = self.table[hash_key]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return
        raise KeyError(key)

    def __str__(self):
        return str(self.table)


# Пример использования
ht = HashTable()
ht.insert("apple", 10)
ht.insert("orange", 20)
ht.insert("banana", 30)
ht.insert("apple", 15)  # Обновляем значение для "apple"

print(ht)  # Выводим всю таблицу
print(ht.get("orange"))  # 20
ht.delete("orange")
print(ht.get("orange"))  # KeyError


class ResizableHashTable(HashTable):
    def __init__(self, initial_size=10, load_factor=0.7):
        super().__init__(initial_size)
        self.load_factor = load_factor
        self.count = 0

    def insert(self, key, value):
        if self.count / self.size > self.load_factor:
            self._resize()
        super().insert(key, value)
        self.count += 1

    def _resize(self):
        new_size = self.size * 2
        new_table = [[] for _ in range(new_size)]

        old_table = self.table
        self.table = new_table
        self.size = new_size
        self.count = 0

        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)


# Пример использования
rht = ResizableHashTable(5, 0.6)
for i in range(10):
    rht.insert(f"key{i}", i)
    print(f"Inserted key{i}, size: {rht.size}, count: {rht.count}")
