package p4.q1;

import p4.core.AbstractWeightedGraph;
import p4.core.WeightedNode;

public class OrientedGraph<T extends Comparable<T>> extends AbstractWeightedGraph<T> {

    public OrientedGraph() {
        super();
    }

    /**
     * Добавить ребро между вершинами
     *
     * @param from   начальная вершина
     * @param to     конечная вершина
     * @param weight вес ребра
     */
    @Override
    public void addEdge(T from, T to, int weight) {
        nodes.putIfAbsent(from, new WeightedNode<>(from));
        nodes.putIfAbsent(to, new WeightedNode<>(to));
        nodes.get(from).connect(nodes.get(to), weight);
    }


}