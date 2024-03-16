package stepick.Java.Java_from_Zero_to_Junior_plus_Interview_preparation.Java_syntax;

import java.util.Scanner;

public class SwitchCase_11 {
    public static void main(String[] args) {
//        Scanner scanner = new Scanner(System.in);
//        System.out.println("Введите число: ");
//        int month = scanner.nextInt();
        int month = 1;
        switch (month) { // switch (...) - какую переменную будем сравнивать
            case 1: // case .. - какое значение ждём и потом пишем определённые действия при этом значении
                System.out.println("January");
                break; // break нужен, так как если month равен 1, то он выведет January
        // и потом будет выводить все оставшиеся месяца пока не встретит break. Т.е. он и дальше будет работать
            case 2:
                System.out.println("February");
                break;
            case 3:
                System.out.println("March");
                break;
            case 4:
                System.out.println("April");
                break;
            case 5:
                System.out.println("May");
                break;
            case 6:
                System.out.println("June");
                break;
            case 7:
                System.out.println("July");
                break;
            case 8:
                System.out.println("August");
                break;
            case 9:
                System.out.println("September");
                break;
            case 10:
                System.out.println("October");
                break;
            case 11:
                System.out.println("November");
                break;
            case 12:
                System.out.println("December");
                break;
            default:
                System.out.println("Unexpected month");
        }
    }
}
