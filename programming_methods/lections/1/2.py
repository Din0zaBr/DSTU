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


class QueueUsingStacks:
    def __init__(self):
        self.stack1 = Stack()
        self.stack2 = Stack()

    def enqueue(self, item):
        self.stack1.push(item)

    def dequeue(self):
        if self.stack2.is_empty():
            while not self.stack1.is_empty():
                self.stack2.push(self.stack1.pop())
        if not self.stack2.is_empty():
            return self.stack2.pop()
        raise IndexError("Dequeue from an empty queue")

    def is_empty(self):
        return self.stack1.is_empty() and self.stack2.is_empty()

    def __str__(self):
        return str(self.stack1.items + self.stack2.items[::-1])


def sort_stack(stack):
    sorted_stack = Stack()
    while not stack.is_empty():
        temp = stack.pop()
        while not sorted_stack.is_empty() and sorted_stack.top() > temp:
            stack.push(sorted_stack.pop())
        sorted_stack.push(temp)
    return sorted_stack


class TwoStacks:
    def __init__(self, size):
        self.size = size
        self.arr = [None] * size
        self.top1 = -1
        self.top2 = size

    def push1(self, item):
        if self.top1 + 1 < self.top2:
            self.top1 += 1
            self.arr[self.top1] = item
        else:
            raise IndexError("Stack 1 Overflow")

    def push2(self, item):
        if self.top2 - 1 > self.top1:
            self.top2 -= 1
            self.arr[self.top2] = item
        else:
            raise IndexError("Stack 2 Overflow")

    def pop1(self):
        if self.top1 >= 0:
            item = self.arr[self.top1]
            self.top1 -= 1
            return item
        raise IndexError("Stack 1 Underflow")

    def pop2(self):
        if self.top2 < self.size:
            item = self.arr[self.top2]
            self.top2 += 1
            return item
        raise IndexError("Stack 2 Underflow")

    def is_empty1(self):
        return self.top1 == -1

    def is_empty2(self):
        return self.top2 == self.size


def reverse_string(s):
    stack = Stack()
    for char in s:
        stack.push(char)
    reversed_str = ''
    while not stack.is_empty():
        reversed_str += stack.pop()
    return reversed_str


# Пример использования стека
stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)
print("Стек:", stack)  # [1, 2, 3]
print("Верхний элемент:", stack.top())  # 3
print("Удаляем элемент:", stack.pop())  # 3
print("Стек после удаления:", stack)  # [1, 2]

# Пример использования очереди
queue = QueueUsingStacks()
queue.enqueue(1)
queue.enqueue(2)
queue.enqueue(3)
print("Очередь:", queue)  # [1, 2, 3]
print("Удаляем элемент:", queue.dequeue())  # 1
print("Очередь после удаления:", queue)  # [2, 3]

# Пример сортировки стека
unsorted_stack = Stack()
unsorted_stack.push(3)
unsorted_stack.push(1)
unsorted_stack.push(4)
unsorted_stack.push(2)

print("Несортированный стек:", unsorted_stack)  # [3, 1, 4, 2]
sorted_stack = sort_stack(unsorted_stack)
print("Отсортированный стек:", sorted_stack)  # [1, 2, 3, 4]

# Пример использования двух стеков в массиве
two_stacks = TwoStacks(10)
two_stacks.push1(1)
two_stacks.push1(2)
two_stacks.push2(3)
two_stacks.push2(4)

print("Стек 1:", [two_stacks.arr[i] for i in range(two_stacks.top1 + 1)])  # [1, 2]
print("Стек 2:", [two_stacks.arr[i] for i in range(two_stacks.top2, two_stacks.size)])  # [4, 3]

print("Удаляем из стека 1:", two_stacks.pop1())  # 2
print("Удаляем из стека 2:", two_stacks.pop2())  # 4

# Пример реверса строки
original_string = "Hello, World!"
reversed_str = reverse_string(original_string)
print("Исходная строка:", original_string)  # Hello, World!
print("Реверсированная строка:", reversed_str)  # !dlroW ,olleH
