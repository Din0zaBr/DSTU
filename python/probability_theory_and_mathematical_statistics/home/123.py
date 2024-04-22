"""
Этот файл создан для того, чтобы:
 1. Подсчитать кол-во повторений каждого элемента в списке и вывести его на экран
 2. Подсчитать количество уникальных элементов в списке
"""

from collections import Counter

from python.probability_theory_and_mathematical_statistics.home import count_seconds_from_file

Data = count_seconds_from_file()
print(f"Список секунд: {Data}")

# Создаем словарь с количеством повторений каждого элемента
counter = Counter(Data)

# Выводим количество повторений каждого элемента
for element, count in counter.items():
    print(f"Элемент: {element}, количество повторений: {count}")
Data = set(count_seconds_from_file())
print(len(Data))
