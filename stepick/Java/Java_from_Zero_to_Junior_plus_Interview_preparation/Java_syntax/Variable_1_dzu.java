package stepick.Java.Java_from_Zero_to_Junior_plus_Interview_preparation.Java_syntax;

public class Variable_1_dzu {
    public static void main(String[] args) {
        int days = 10000;
        int weeks = days / 7;
        int months = days / 30;
        int years = days / 365;
        int leftDays = days - weeks * 7;
        System.out.println(weeks);
        System.out.println(months);
        System.out.println(years);
        System.out.println(leftDays);
    }
}
