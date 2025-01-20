/**
 * Снова начните с программы tree.java и постройте дерево из символов, вводимых пользователем.
 * На этот раз должно создаваться полное дерево, то есть дерево, содержащее все возможные узлы на всех уровнях
 * (кроме правого края последнего ряда).
 * Символы должны быть упорядочены сверху вниз и слева направо в каждом ряду.
 * Таким образом, строка ABCDEFGHIJ будет упорядочена в виде
 */

package p2.q3;

import p2.core.AbstractTree;
import p2.core.Node;

import java.util.Collection;
import java.util.List;
import java.util.stream.Collectors;

public class FullBalancedTree<T extends Comparable<T>> extends AbstractTree<T> {

    public FullBalancedTree(Collection<T> input) {
        super(input);
    }

    @Override
    protected Node<T> buildTree(Collection<T> input) {
        var forest = input.stream().map(Node::new).collect(Collectors.toList());
        return buildTreeRecursive(forest, 0);
    }

    private Node<T> buildTreeRecursive(List<Node<T>> symbols, int index) {
        if (index < symbols.size()) {
            int leftIndex = 2 * index + 1; // вычисление индекса для левого потомка
            int rightIndex = 2 * index + 2; // вычисление индекса для правого потомка

            var value = symbols.get(index).getData();
            var leftChild = buildTreeRecursive(symbols, leftIndex);
            var rightChild = buildTreeRecursive(symbols, rightIndex);

            return new Node<>(value, leftChild, rightChild);
        }
        return null;
    }
}