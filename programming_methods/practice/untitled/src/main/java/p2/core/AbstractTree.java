/**
 * Абстрактный класс, представляющий дерево.
 * Содержит корневой узел дерева (root)
 * Определяет абстрактный метод buildTree, который должен быть реализован в наследниках
 * Реализует метод toString() для визуализации дерева в консоли
 * Использует стеки для обхода дерева по уровням при выводе
 * Форматирует вывод с правильным отступом и разделителями между узлами
 * <p>
 * Лес — это набор деревьев.
 * Дерево (Tree):
 *      Структура данных, состоящая из узлов, связанных рёбрами. Каждый узел (кроме корневого) имеет ровно одного родителя, и каждый узел может иметь ноль или более дочерних узлов.
 * Узел (Node):
 *      Основной элемент дерева, который содержит данные и ссылки на своих дочерних узлов.
 * Корневой узел (Root Node):
 *      Верхний узел дерева, который не имеет родителя. Это начальная точка дерева.
 * Листовой узел (Leaf Node):
 *      Узел, который не имеет дочерних узлов. Это конечные узлы дерева.
 * Родительский узел (Parent Node):
 *      Узел, который имеет один или более дочерних узлов.
 * Дочерний узел (Child Node):
 *      Узел, который имеет родительский узел.
 * Поддерево (Subtree):
 *      Часть дерева, состоящая из узла и всех его потомков.
 * Глубина узла (Depth of a Node):
 *      Количество рёбер от корневого узла до данного узла. Глубина корневого узла равна 0.
 * Высота дерева (Height of a Tree):
 *      Максимальная глубина любого листового узла. Высота дерева с одним узлом равна 0.
 * Уровень (Level):
 *      Уровень узла определяется его глубиной. Корневой узел находится на уровне 0, его дочерние узлы — на уровне 1 и так далее.
 * Рёбра (Edges):
 *      Связи между узлами дерева. Каждое ребро соединяет родительский узел с дочерним.
 * Бинарное дерево (Binary Tree):
 *      Дерево, в котором каждый узел имеет не более двух дочерних узлов.
 * Двоичное дерево поиска (Binary Search Tree, BST):
 *      Бинарное дерево, в котором для каждого узла выполняется следующее условие: все узлы в левом поддереве имеют значения меньше, чем узел, а все узлы в правом поддереве — больше.
 * Сбалансированное дерево (Balanced Tree):
 *      Дерево, в котором высота всех поддеревьев отличается не более чем на одну единицу. Примеры сбалансированных деревьев: AVL-дерево, красно-чёрное дерево.
 * Полное бинарное дерево (Full Binary Tree):
 *      Бинарное дерево, в котором каждый узел имеет либо 0, либо 2 дочерних узла.
 * Полное дерево (Complete Tree):
 *      Дерево, в котором все уровни, кроме последнего, полностью заполнены, а узлы на последнем уровне заполнены слева направо.
 * Префиксный обход (Preorder Traversal):
 *      Обход дерева, при котором сначала посещается корневой узел, затем левое поддерево, а затем правое поддерево.
 * Инфиксный обход (Inorder Traversal):
 *      Обход дерева, при котором сначала посещается левое поддерево, затем корневой узел, а затем правое поддерево.
 * Постфиксный обход (Postorder Traversal):
 *      Обход дерева, при котором сначала посещается левое поддерево, затем правое поддерево, а затем корневой узел.
 * Уровневый обход (Level Order Traversal):
 *      Обход дерева, при котором узлы посещаются уровень за уровнем, слева направо.
 */

package p2.core;


import lombok.AllArgsConstructor;
import lombok.NoArgsConstructor;

import java.util.Collection;
import java.util.Stack;

// Эти аннотации автоматически генерируют конструкторы без аргументов и с аргументами для класса.
@NoArgsConstructor
@AllArgsConstructor
public abstract class AbstractTree<T extends Comparable<T>> {
    protected Node<T> root;

    public AbstractTree(Collection<T> input) {
        this.root = buildTree(input);
    }

    protected abstract Node<T> buildTree(Collection<T> input);

    /**
     * Метод для вывода дерева в консоль.
     *
     * @return возвращает строковый вид дерева, как указано в задании.
     */
    @Override
    public String toString() {
        var result = new StringBuilder();
        var globalStack = new Stack<Node<T>>(); // глобальный стек для обхода дерева
        var nBlanks = 32;
        var isRowEmpty = false;

        globalStack.push(root);

        result.append(".....................................\n");

        // Пока в текущем ряду есть элементы для отображения
        while (!isRowEmpty) {
            var localStack = new Stack<Node<T>>(); // локальный стек для текущего ряда
            isRowEmpty = true;

            result.append(" ".repeat(nBlanks));

            // Обрабатываем текущий уровень
            while (!globalStack.isEmpty()) {
                var node = globalStack.pop();

                if (node != null) {
                    // Добавляем данные текущего узла
                    result.append(node.getData());

                    // Добавляем дочерние элементы в локальный стек
                    localStack.push(node.getLeftChild());
                    localStack.push(node.getRightChild());

                    // Если хотя бы один дочерний элемент есть, ряд не пустой
                    if (node.getLeftChild() != null || node.getRightChild() != null) {
                        isRowEmpty = false;
                    }
                } else {
                    // Если узел пустой, добавляем placeholders
                    result.append("--");
                    localStack.push(null);
                    localStack.push(null);
                }

                result.append(" ".repeat(nBlanks * 2 - 2));
            }

            result.append('\n');
            nBlanks /= 2;

            // Переносим элементы из локального стека обратно в глобальный
            while (!localStack.isEmpty()) {
                globalStack.push(localStack.pop());
            }
        }

        result.append("......................................................\n");

        return result.toString().trim();
    }

}