class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("Pop from an empty stack")

    def is_empty(self):
        return len(self.items) == 0

    def top(self):
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("Top from an empty stack")

    def __str__(self):
        return str(self.items)


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        raise IndexError("Dequeue from an empty queue")

    def is_empty(self):
        return len(self.items) == 0

    def top(self):
        if not self.is_empty():
            return self.items[0]
        raise IndexError("Top from an empty queue")

    def __str__(self):
        return str(self.items)


class StackUsingQueues:
    def __init__(self):
        self.queue1 = Queue()
        self.queue2 = Queue()

    def push(self, item):
        self.queue1.enqueue(item)

    def pop(self):
        if self.queue1.is_empty():
            raise IndexError("Pop from an empty stack")

        # Перемещаем все элементы, кроме последнего, во вторую очередь
        while len(self.queue1.items) > 1:
            self.queue2.enqueue(self.queue1.dequeue())

        # Удаляем последний элемент из первой очереди
        popped_item = self.queue1.dequeue()

        # Меняем местами очереди
        self.queue1, self.queue2 = self.queue2, self.queue1

        return popped_item

    def top(self):
        if self.queue1.is_empty():
            raise IndexError("Top from an empty stack")

        # Перемещаем все элементы, кроме последнего, во вторую очередь
        while len(self.queue1.items) > 1:
            self.queue2.enqueue(self.queue1.dequeue())

        # Получаем последний элемент
        top_item = self.queue1.top()

        # Перемещаем его во вторую очередь
        self.queue2.enqueue(self.queue1.dequeue())

        # Меняем местами очереди
        self.queue1, self.queue2 = self.queue2, self.queue1

        return top_item

    def is_empty(self):
        return self.queue1.is_empty()


def reverse_first_n_elements(queue, n):
    if n > len(queue.items):
        raise ValueError("N is larger than the number of elements in the queue")

    stack = Stack()

    # Перемещаем первые N элементов в стек
    for _ in range(n):
        stack.push(queue.dequeue())

    # Возвращаем элементы из стека обратно в очередь
    while not stack.is_empty():
        queue.enqueue(stack.pop())

    # Перемещаем оставшиеся элементы обратно в очередь
    size = len(queue.items)
    for _ in range(size - n):
        queue.enqueue(queue.dequeue())


def generate_binary_numbers(n):
    queue = Queue()
    result = []

    # Начинаем с первого двоичного числа
    queue.enqueue("1")

    for _ in range(n):
        # Получаем следующее двоичное число
        binary_number = queue.dequeue()
        result.append(binary_number)

        # Генерируем следующие двоичные числа
        queue.enqueue(binary_number + "0")
        queue.enqueue(binary_number + "1")

    return result


# Пример использования очереди
queue = Queue()
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
print("Очередь:", queue)  # [1, 2, 3]
print("Удаляем элемент:", queue.dequeue())  # 1
print("Очередь после удаления:", queue)  # [2, 3]

# Пример использования стека с помощью очереди
stack = StackUsingQueues()
stack.push(1)
stack.push(2)
stack.push(3)
print("Удаляем элемент из стека:", stack.pop())  # 3
print("Верхний элемент стека:", stack.top())  # 2

# Пример реверса первых N элементов очереди
queue_to_reverse = Queue()
for i in range(1, 6):  # Заполняем очередь числами от 1 до 5
    queue_to_reverse.enqueue(i)

print("Очередь до реверса:", queue_to_reverse)  # [1, 2, 3, 4, 5]
reverse_first_n_elements(queue_to_reverse, 3)  # Реверсируем первые 3 элемента
print("Очередь после реверса первых 3 элементов:", queue_to_reverse)  # [3, 2, 1, 4, 5]

# Пример генерации двоичных чисел от 1 до N
n = 5
binary_numbers = generate_binary_numbers(n)
print(f"Двоичные числа от 1 до {n}:", binary_numbers)  # ['1', '10', '11', '100', '101']
