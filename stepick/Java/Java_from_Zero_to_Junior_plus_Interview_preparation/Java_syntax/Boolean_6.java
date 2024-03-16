package stepick.Java.Java_from_Zero_to_Junior_plus_Interview_preparation.Java_syntax;

public class Boolean_6 {

    public static void main(String[] args) {
        int temp = 30;
        boolean hot = temp >= 25;
        boolean cold = temp <= 22;
        // также есть >=, <=, == и != аналогично Python
        int time = 23;
        boolean isNight = time > 22 || time < 6;
        // || - или, && - и, ! - не,
        if (hot && !isNight) {
            System.out.println("Кондиционер включён");
        } else if (cold) {
            System.out.println("Кондиционер выключен");
        } else {
            System.out.println("Кондиционер ничего не делает");
        }

    }

}
