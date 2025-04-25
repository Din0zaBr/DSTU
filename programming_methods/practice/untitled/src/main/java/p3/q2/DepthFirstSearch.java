/*
Поиск в глубину (DFS) — это алгоритм для обхода или поиска в графах,
который исследует как можно дальше по каждому пути перед возвратом.
DFS использует стек (или рекурсию) для отслеживания вершин, которые нужно посетить.
 */

package p3.q2;

import p3.core.AbstractUnweightedGraph;
import p3.core.UnweightedNode;

import java.util.*;

public class DepthFirstSearch {

    /**
     * Выполняет обход в глубину (DFS) от заданной вершины.
     * Использует рекурсию для обхода вершин.
     * Возвращает путь обхода в виде списка вершин.
     * 1. Инициализация:
     * Проверяется, существует ли граф и стартовая вершина.
     * Создаются структуры данных для хранения пути и посещённых вершин.
     * 2. Рекурсивный метод DFS:
     * Начинается с стартовой вершины.
     * Для каждой вершины исследуются её соседи.
     * Если сосед не посещён, вызывается рекурсивный метод для его обхода.
     * 3. Возврат результата:
     * Возвращается путь обхода в виде списка вершин.
     *
     * @param startValue стартовое значение вершины.
     * @param graph      объект графа.
     * @param <T>        тип значения вершины.
     * @return список, представляющий путь обхода.
     */
    public static <T extends Comparable<T>> List<T> execute(T startValue, AbstractUnweightedGraph<T> graph) {
        if (graph == null || graph.getVertex(startValue) == null) {
            throw new IllegalArgumentException("Graph is null or start vertex not found: " + startValue);
        }

        List<T> path = new ArrayList<>();
        Set<UnweightedNode<T>> visited = new HashSet<>();
        UnweightedNode<T> startNode = graph.getVertex(startValue);

        dfsRecursive(startNode, visited, path);

        return path;
    }

    /**
     * Рекурсивный метод для выполнения DFS.
     *
     * @param current текущая вершина.
     * @param visited множество посещённых вершин.
     * @param path    путь обхода.
     * @param <T>     тип значения вершины.
     */
    private static <T extends Comparable<T>> void dfsRecursive(UnweightedNode<T> current, Set<UnweightedNode<T>> visited, List<T> path) {
        visited.add(current);
        path.add(current.getValue());

        for (UnweightedNode<T> neighbor : current.getNeighbors()) {
            if (!visited.contains(neighbor)) {
                dfsRecursive(neighbor, visited, path);
            }
        }
    }
}