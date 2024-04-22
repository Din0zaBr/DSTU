package Lections.Massive;

public class ArrayClass {
    public static void main(String[] args) {
        int[] a = new int[3];
        a[0] = 15;
        a[1] = 12;
        a[2] = -3;

        for (int i = 0; i < a.length; i++) {
            System.out.println(a[i]);
        }

        for (int i : a) {
            System.out.println(i);
        }

        int[][] b = new int[2][2];
        b[0][0] = -1;
        b[0][1] = 1;
        b[1][0] = 1;
        b[1][1] = -1;

        for (int[] ints : b) {
            for (int i : ints) {
                System.out.println(i);
            }
        }

    }
}
