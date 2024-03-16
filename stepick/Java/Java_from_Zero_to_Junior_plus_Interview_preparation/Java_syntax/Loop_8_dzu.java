package stepick.Java.Java_from_Zero_to_Junior_plus_Interview_preparation.Java_syntax;

public class Loop_8_dzu {
    // от 1000 до 0 вывести числа, которые делятся на 3 нацело
    public static void main(String[] args) {

        for (int i = 1000; i >= 0; i--) {
            if (i % 3 == 0) {
                System.out.println(i);
            }
        }
    }
}
