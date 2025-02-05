package p1.q3;

import p1.q2.Deque;

class DequeStack<T> implements StackOperations<T> {
    private final Deque<T> deque;

    // Инициализирует стек с заданным максимальным размером.
    public DequeStack(int size) {
        deque = new Deque<>(size);
    }

    //  Вставляет элемент на вершину стека.
    @Override
    public void push(T j) {
        if (isFull()) {
            throw new IllegalStateException("Стек полон. Невозможно добавить элемент: " + j);
        }
        deque.insertRight(j);
    }

    // Удаляет элемент с вершины стека.
    @Override
    public T pop() {
        if (!isEmpty()) {
            return deque.removeRight();
        }
        throw new IllegalStateException("Стек пуст. Невозможно выполнить операцию pop.");
    }

    // Возвращает верхний элемент стека без его удаления.
    @Override
    public T peek() {
        if (!isEmpty()) {
            var value = deque.removeRight();
            deque.insertRight(value);
            return value;
        }
        throw new IllegalStateException("Стек пуст. Невозможно выполнить операцию peek.");
    }

    @Override
    public boolean isEmpty() {
        return deque.isEmpty();
    }

    @Override
    public boolean isFull() {
        return deque.isFull();
    }

    @Override
    public String toString() {
        return deque.toString();
    }
}