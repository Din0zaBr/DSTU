class CustomArray:
    def __init__(self):
        self.array = []

    def insert(self, index, value):
        if index < 0 or index > len(self.array):
            raise IndexError("Index out of bounds")
        self.array.insert(index, value)

    def get(self, index):
        if index < 0 or index >= len(self.array):
            raise IndexError("Index out of bounds")
        return self.array[index]

    def delete(self, index):
        if index < 0 or index >= len(self.array):
            raise IndexError("Index out of bounds")
        self.array.pop(index)

    def size(self):
        return len(self.array)

    def __repr__(self):  # покажет текущий массив (для интерпретатора)
        return repr(self.array)


def second_minimum(arr):
    if arr.size() < 2:
        return None  # Второго минимального элемента нет

    first_min = float('inf')
    second_min = float('inf')

    for i in range(arr.size()):
        num = arr.get(i)
        if num < first_min:
            first_min, second_min = num, first_min
        elif first_min < num < second_min:
            second_min = num

    return second_min if second_min != float('inf') else None


def first_non_repeating(arr):
    frequency = {}
    for i in range(arr.size()):
        num = arr.get(i)
        if num in frequency:
            frequency[num] += 1
        else:
            frequency[num] = 1

    non_repeating = []
    for i in range(arr.size()):
        num = arr.get(i)
        if frequency[num] == 1:
            non_repeating.append(num)
            if len(non_repeating) == 2:
                break

    return non_repeating


def merge_sorted_arrays(arr1, arr2):
    merged = CustomArray()
    i, j = 0, 0

    while i < arr1.size() and j < arr2.size():
        if arr1.get(i) < arr2.get(j):
            merged.insert(merged.size(), arr1.get(i))
            i += 1
        else:
            merged.insert(merged.size(), arr2.get(j))
            j += 1

    while i < arr1.size():
        merged.insert(merged.size(), arr1.get(i))
        i += 1

    while j < arr2.size():
        merged.insert(merged.size(), arr2.get(j))
        j += 1

    return merged


def rearrange_positive_negative(arr):
    left, right = 0, arr.size() - 1

    while left <= right:
        if arr.get(left) < 0 < arr.get(right):
            arr.insert(left, arr.get(right))
            arr.delete(left + 1)
            arr.delete(right)
            left += 1
            right -= 1
        elif arr.get(left) > 0:
            left += 1
        elif arr.get(right) < 0:
            right -= 1
        else:
            left += 1
            right -= 1

    return arr


arr0 = CustomArray()
arr0.insert(0, 4)
arr0.insert(1, 6)
arr0.insert(2, 2)
arr0.insert(3, 6)
arr0.insert(4, 7)
arr0.insert(5, 2)
print(first_non_repeating(arr0))

arr = CustomArray()
arr.insert(0, 1)
arr.insert(1, -1)
arr.insert(2, 3)

rearranged_arr = rearrange_positive_negative(arr)
print(rearranged_arr)

arr1 = CustomArray()
arr1.insert(0, 1)
arr1.insert(1, 3)
arr1.insert(2, 5)

arr2 = CustomArray()
arr2.insert(0, 2)
arr2.insert(1, 4)
arr2.insert(2, 6)

merged_arr = merge_sorted_arrays(arr1, arr2)
print(merged_arr)

arr3 = CustomArray()
arr3.insert(0, 3)
arr3.insert(1, 1)
arr3.insert(2, 4)
arr3.insert(3, 1)
arr3.insert(4, 5)
arr3.insert(5, 9)
arr3.insert(6, 2)
arr3.insert(7, 6)
arr3.insert(8, 5)
arr3.insert(9, 3)
arr3.insert(10, 5)
print(second_minimum(arr))
