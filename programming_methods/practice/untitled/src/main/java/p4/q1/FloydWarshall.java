package p4.q1;

import p4.core.AbstractWeightedGraph;
import p4.core.WeightedNode;

import java.util.HashMap;
import java.util.Map;

public class FloydWarshall {
    /**
     * Выполняет алгоритм Флойда-Уоршелла для заданного графа.
     *
     * @param graph Граф, реализующий AbstractWeightedGraph.
     * @param <T>   Тип данных узлов графа.
     * @return Возвращает матрицу кратчайших расстояний.
     */
    public static <T extends Comparable<T>> Map<T, Map<T, Integer>> execute(AbstractWeightedGraph<T> graph) {
        Map<T, WeightedNode<T>> nodes = graph.getNodes();
        Map<T, Map<T, Integer>> distances = new HashMap<>();

        // Инициализация матрицы расстояний
        for (T from : nodes.keySet()) {
            distances.putIfAbsent(from, new HashMap<>());
            for (T to : nodes.keySet()) {
                if (from.equals(to)) {
                    distances.get(from).put(to, 0); // Расстояние до самой себя
                } else {
                    distances.get(from).put(to, Integer.MAX_VALUE); // Изначально пути нет
                }
            }

            // Установка весов для соседей
            for (Map.Entry<WeightedNode<T>, Integer> neighbor : nodes.get(from).getNeighbors().entrySet()) {
                distances.get(from).put(neighbor.getKey().getValue(), neighbor.getValue());
            }
        }

        // Основной алгоритм
        for (T k : nodes.keySet()) { // Промежуточная вершина
            for (T i : nodes.keySet()) { // Начальная вершина
                for (T j : nodes.keySet()) { // Конечная вершина
                    if (distances.get(i).get(k) != Integer.MAX_VALUE && distances.get(k).get(j) != Integer.MAX_VALUE) {
                        var newDist = distances.get(i).get(k) + distances.get(k).get(j);
                        if (newDist < distances.get(i).get(j)) {
                            distances.get(i).put(j, newDist);
                        }
                    }
                }
            }
        }

        return distances;
    }
}