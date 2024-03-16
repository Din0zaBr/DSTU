package stepick.Java.Java_from_Zero_to_Junior_plus_Interview_preparation.Java_syntax;

public class Boolean_6_dzu {
    public static void main(String[] args) {
        // что делать в зависимости от погоды и времени суток, булеаны,
        // если день и хорошая погода - гулять, если день и плохая погода - читать книгу
        // и если ночь без учёта погоды - спать
        boolean day = false;
        boolean good_wether = true;
        if (day && good_wether) {
            System.out.println("ГУЛЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯЯять");
        }
        if (day && !good_wether) {
            System.out.println("ЧИТААААААААААААААААААААААААААААААААать книгу");
        }
        if (day == false) {
            System.out.println("СПАААААААААААААААААААААААААать");
        }

    }
}
