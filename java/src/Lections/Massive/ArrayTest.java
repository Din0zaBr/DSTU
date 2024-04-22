package Lections.Massive;

import java.util.Arrays;
import java.util.Random;

public class ArrayTest {
    public static void main(String[] args) {
        Random random = new Random();
        int[] a = new int[10];
        for (int i = 0; i < 10; i++) {
            a[i] = random.nextInt(100);
        }
        System.out.println(Arrays.toString(a));
        Arrays.sort(a);
        System.out.println(Arrays.toString(
                Arrays.copyOf(a, 5)));
    }
}
