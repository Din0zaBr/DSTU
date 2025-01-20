package p1.q3;

public interface StackOperations<T> {
    void push(T j);

    T pop();

    T peek();

    boolean isEmpty();

    boolean isFull();
}