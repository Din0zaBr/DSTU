package stepick.Java.Java_from_Zero_to_Junior_plus_Interview_preparation.Java_syntax;

// создать массив целых чисел размером 100 и присвоить значение (проинициализировать) его элелементам от 100 до 200
// потом при помощи for each вывести данные в консоль
public class ForEach_10_dzu {
    public static void main(String[] args) {
        int[] digits = new int[101];
        for (int i = 0; i < digits.length; i++) {
            digits[i] = i + 100;
        }
        for (Integer digit : digits) { // тип доставаемой переменной, имя : массив откуда достаётся
            System.out.println(digit);
        }
    }
}
