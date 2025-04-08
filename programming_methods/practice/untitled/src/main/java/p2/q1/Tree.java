/**
 * Задание №1.
 * Реализует задание №1: создание двоичного дерева из цепочки символов.
 * Принимает коллекцию символов на вход
 * Строит дерево методом buildTree()
 * Создает листовые узлы для входных символов
 * Использует символ '+' как значение для родительских узлов
 * Гарантирует наличие двух потомков у каждого внутреннего узла
 * Обратите внимание: созданное дерево не является деревом поиска;
 * в нем не существует быстрого способа найти заданный узел.
 */


package p2.q1;

import p2.core.AbstractTree;
import p2.core.Node;

import java.util.Collection;
import java.util.LinkedList;
import java.util.stream.Collectors;

public class Tree<T extends Comparable<T>> extends AbstractTree<T> {

    public Tree(Collection<T> input) {
        super(input);
    }

    /**
     * Данный конструктор принимает коллекцию элементов, по которой можно итерироваться и собирает дерево.
     *
     * @param input итерируемая коллекция, где элементы поддерживают сравнение.
     */
    @Override
    @SuppressWarnings("unchecked")
    protected Node<T> buildTree(Collection<T> input) {
        // Каждый элемент из входной коллекции преобразуется в узел (Node) и добавляется в список forest
        var forest = input.stream().map(Node::new).collect(Collectors.toList());
        // Этот список будет использоваться для хранения промежуточных узлов дерева.
        var newForest = new LinkedList<Node<T>>();
        // Пока в списке forest есть элементы, выполняются следующие шаги:
        // Выбор левого потомка:
        //      Если newForest пуст, левый потомок берется из forest.
        //      Если newForest не пуст, левый потомок берется из newForest.
        // Выбор правого потомка:
        //      Правый потомок всегда берется из forest.
        // Создание родительского узла:
        //      Создается новый узел со значением + и двумя потомками (leftChild и rightChild).
        //      Новый узел добавляется в newForest.
        while (!forest.isEmpty()) {
            var leftChild = newForest.isEmpty() ? forest.removeFirst() : newForest.removeFirst();
            var rightChild = forest.removeFirst();
            var value = (T) Character.valueOf('+');
            newForest.add(new Node<>(value, leftChild, rightChild));
//            System.out.println(newForest);

        }

        return newForest.getFirst();
    }
}