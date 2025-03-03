/**
 * Задача заключается в создании сбалансированного дерева из входной коллекции элементов. Сбалансированное дерево должно быть построено таким образом, чтобы на нижнем уровне было как можно больше листовых узлов. Процесс построения дерева включает следующие шаги:
 * Создание трехузловых деревьев:
 *      Каждая пара одноузловых деревьев объединяется в трехузловое дерево с новым корневым узлом +.
 * Объединение трехузловых деревьев:
 *      Каждая пара трехузловых деревьев объединяется в семиузловое дерево.
 * Продолжение объединения:
 *      Процесс продолжается, пока не останется одно дерево. */

package p2.q2;

import p2.core.AbstractTree;
import p2.core.Node;

import java.util.Collection;
import java.util.LinkedList;
import java.util.stream.Collectors;

public class BalancedTree<T extends Comparable<T>> extends AbstractTree<T> {

    public BalancedTree(Collection<T> input) {
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
        var forest = input.stream().map(Node::new).collect(Collectors.toList());

        while (forest.size() > 1) {
            var newForest = new LinkedList<Node<T>>();
            for (int i = 0; i < forest.size(); i += 2) {
                var leftChild = forest.get(i);
                var rightChild = i + 1 < forest.size() ? forest.get(i + 1) : null;
                var value = (T) Character.valueOf('+');
                newForest.add(new Node<>(value, leftChild, rightChild));
            }
            forest = newForest;
        }

        return forest.getFirst();
    }

}