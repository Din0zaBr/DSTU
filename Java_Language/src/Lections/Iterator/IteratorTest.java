package Lections.Iterator;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;

public class IteratorTest {
    public static void main(String[] args) {
        Integer[] nums = {10, -5, 4, 8,
                -2, -10, 1, 4, 2};
        ArrayList<Integer> numList =
                new ArrayList<>(
                        Arrays.asList(nums));

        Iterator<Integer> numListIter =
                numList.iterator();
        while (numListIter.hasNext()) {
            int n = numListIter.next();
            if (n < 0) {
                numListIter.remove();
            }
        }

        System.out.println(numList);
    }
}
