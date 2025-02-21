/**
 * Создайте класс Deque по описанию деков (двусторонних очередей).
 * Класс должен содержать методы insertLeft(), insertRight(), removeLeft(), removeRight(), isEmpty() и isFull().
 * Также в нем должна быть реализована поддержка циклического переноса индексов, по аналогии с очередями.
 */

package p1.q2;

public class Deque<T> {
    private final int maxSize;
    private final T[] dequeArray;
    private int front;
    private int rear;
    private int nItems;

    @SuppressWarnings("unchecked")
    public Deque(int s) {
        maxSize = s;
        dequeArray = (T[]) new Object[maxSize];
        front = 0;
        rear = -1;
        nItems = 0;
    }

    /**
     * Вставка элемента в конец дека. Если дек полон, будет перезаписан старый элемент.
     */
    public void insertRight(T value) {
        if (isFull()) {
            // Если дек полон, передвигаем front для перезаписи элемента
            front = (front + 1) % maxSize; // Сдвигаем front вперед, чтобы освободить место
        }

        // Вставляем элемент в конец дека
        rear = (rear + 1) % maxSize; // Циклический переход
        dequeArray[rear] = value;

        if (nItems < maxSize) {
            nItems++; // Увеличиваем количество элементов, если дек не полон
        }
    }

    /**
     * Вставка элемента в начало дека. Если дек полон, будет перезаписан старый элемент.
     */
    public void insertLeft(T value) {
        if (isFull()) {
            // Если дек полон, передвигаем rear для перезаписи элемента
            rear = (rear - 1 + maxSize) % maxSize; // Сдвигаем rear назад, чтобы освободить место
        }

        // Вставляем элемент в начало дека
        front = (front - 1 + maxSize) % maxSize; // Циклический переход
        dequeArray[front] = value;

        if (nItems < maxSize) {
            nItems++; // Увеличиваем количество элементов, если дек не полон
        }
    }

    /**
     * Удаляет элемент из конца дека.
     */
    public T removeRight() {
        if (isEmpty()) {
            throw new IllegalStateException("Дек пустой");
        }
        T temp = dequeArray[rear];
        rear = (rear - 1 + maxSize) % maxSize;
        nItems--;
        return temp;
    }

    /**
     * Удаляет элемент из начала дека.
     */
    public T removeLeft() {
        if (isEmpty()) {
            throw new IllegalStateException("Дек пустой");
        }
        T temp = dequeArray[front];
        front = (front + 1) % maxSize;
        nItems--;
        return temp;
    }

    /**
     * Проверяет, пуст ли дек.
     */
    public boolean isEmpty() {
        return nItems == 0;
    }

    /**
     * Проверяет, заполнен ли дек.
     */
    public boolean isFull() {
        return nItems == maxSize;
    }

    /**
     * Возвращает строковое представление содержимого дека.
     */
    @Override
    public String toString() {
        if (isEmpty()) {
            return "[]";
        }

        StringBuilder sb = new StringBuilder();

        int count = 0;
        int current = front;

        while (count < nItems) {
            sb.append(dequeArray[current]).append(" ");
            current = (current + 1) % maxSize; // Циклический переход
            count++;
        }

        return sb.toString().trim();
    }
}