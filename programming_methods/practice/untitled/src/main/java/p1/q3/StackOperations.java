package p1.q3;
// Этот интерфейс определяет основные операции стека:

//push(T j): Вставка элемента на вершину стека.
//pop(): Удаление элемента с вершины стека.
//peek(): Получение верхнего элемента стека без его удаления.
//isEmpty(): Проверка, пуст ли стек.
//isFull(): Проверка, полон ли стек.
public interface StackOperations<T> {
    void push(T j);

    T pop();

    T peek();

    boolean isEmpty();

    boolean isFull();
}