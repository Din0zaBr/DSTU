/**
 * Класс, представляющий узел дерева.
 * Реализует интерфейс Comparable для сравнения узлов
 * Использует аннотации Lombok (@Data, @NoArgsConstructor, @AllArgsConstructor)
 * для автоматической генерации геттеров, сеттеров и конструкторов
 */

package p2.core;


import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class Node<T extends Comparable<T>> implements Comparable<Node<T>> {
    private T data;
    private Node<T> leftChild;
    private Node<T> rightChild;

    /**
     * Поле data для хранения значения узла
     * Ссылки на левого (leftChild) и правого (rightChild) потомка
     */
    public Node(T data) {
        this(data, null, null);
    }

    @Override
    public int compareTo(Node<T> other) {
        if (other == null) {
            throw new NullPointerException("Сравниваемый узел не должен быть null.");
        }
        return this.data.compareTo(other.data);
    }
}