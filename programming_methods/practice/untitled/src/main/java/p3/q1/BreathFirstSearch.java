/*
Поиск в ширину (BFS) — это алгоритм для обхода или поиска в графах.
Он начинает с корневой вершины и исследует все соседние вершины.
Затем он переходит к вершинам, которые находятся на следующем уровне глубины, и так далее.
BFS использует очередь для отслеживания вершин, которые нужно посетить.

Минимальное остовное дерево (MST) — это подграф,
который соединяет все вершины вместе, без циклов, с минимальной возможной суммой весов рёбер.
MST часто используется в задачах оптимизации сетей, таких как минимизация стоимости кабельной сети.
 */


package p3.q1;

import p3.core.AbstractUnweightedGraph;
import p3.core.UnweightedNode;

import java.util.*;

public class BreathFirstSearch {

    /**
     * BFS для построения минимального остовного дерева.
     * Использует очередь для обхода вершин.
     * Сохраняет рёбра в виде списка пар вершин.
     * Возвращает минимальное остовное дерево (хотя для невзвешенного графа это просто остовное дерево)
     * 1. Инициализация.
     * Проверяется, существует ли граф и стартовая вершина.
     * Создаются структуры данных для хранения результата, посещённых вершин и очереди.
     * 2. Основной цикл BFS.
     * Начинается с стартовой вершины.
     * Для каждой вершины исследуются её соседи.
     * Если сосед не посещён, он добавляется в очередь и результат.
     * 3. Возврат результата.
     * Возвращается список рёбер, представляющих минимальное остовное дерево.
     *
     * @param startValue стартовая вершина.
     * @param graph      объект графа.
     * @param <T>        тип данных вершин.
     * @return минимальное остовное дерево как список рёбер.
     */
    public static <T extends Comparable<T>> List<List<UnweightedNode<T>>> execute(T startValue, AbstractUnweightedGraph<T> graph) {
        if (graph == null || graph.getVertex(startValue) == null) {
            throw new IllegalArgumentException("Graph is null or start vertex not found: " + startValue);
        }

        UnweightedNode<T> startNode = graph.getVertex(startValue);

        List<List<UnweightedNode<T>>> result = new LinkedList<>(); // Хранение рёбер
        Set<UnweightedNode<T>> visited = new HashSet<>();
        Queue<UnweightedNode<T>> queue = new LinkedList<>();

        visited.add(startNode);
        queue.add(startNode);

        while (!queue.isEmpty()) {
            UnweightedNode<T> current = queue.poll();

            for (UnweightedNode<T> neighbor : current.getNeighbors()) {
                if (!visited.contains(neighbor)) {
                    visited.add(neighbor);

                    // Сохраняем ребро как пару вершин
                    result.add(List.of(current, neighbor));

                    queue.add(neighbor);
                }
            }
        }

        return result;
    }
}