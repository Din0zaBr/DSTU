package p1.q3;
// Задание состоит в реализации стека (Stack) на языке Java с использованием двусторонней очереди (Deque)
// и интерфейса для операций со стеком.
// Стек — это структура данных, которая следует принципу LIFO (Last In, First Out),
// то есть последний вошедший элемент будет первым вышедшим.
// В данном задании требуется реализовать основные операции стека,
// такие как вставка (push),
// удаление (pop),
// просмотр верхнего элемента (peek),
// а также проверка на пустоту и полноту.

import java.util.Arrays;

// Создает стек с максимальным размером 10.
//Вставляет несколько элементов в стек и выводит его содержимое.
//Удаляет все элементы из стека и выводит его содержимое.
//Пытается выполнить операцию pop на пустом стеке и обрабатывает исключение.
//Вставляет новые элементы в стек и выводит верхний элемент с помощью операции peek.
//Выводит содержимое стека после операции peek.
class Main {
    public static void main(String[] args) {
        StackOperations<Integer> stack = new DequeStack<>(10);

        int[] elementsToInsert1 = {20, 40, 60, 80};
        System.out.println("Элементы для добавления в стек: " + Arrays.toString(elementsToInsert1));

        for (var element : elementsToInsert1) {
            stack.push(element);
        }

        System.out.println(stack);

        while (!stack.isEmpty()) {
            long value = stack.pop();
            System.out.print(value);
            System.out.print(" ");
        }
        System.out.println("Стек пуст после удаления всех элементов? " + stack.isEmpty());

        System.out.println("Попытка выполнить pop на пустом стеке:");
        try {
            stack.pop();  // Пытаемся выполнить pop на пустом стеке
        } catch (IllegalStateException e) {
            System.out.println("Ошибка: " + e.getMessage());
        }

        stack.push(100);
        stack.push(200);

        System.out.println("Верхний элемент стека (peek): " + stack.peek());

        System.out.println("Состояние стека после peek: " + stack);
    }
}