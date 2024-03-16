package stepick.Java.Java_from_Zero_to_Junior_plus_Interview_preparation.Java_syntax;

public class IntegerTypes_3 {

    public static void main(String[] args){
        long speed = 300_000;
        long distance = 365 * 24 * 60 * 60 * speed; // приводится к самому большому типу данных, т.е. long.
        // Неявное приведение типа, если меньшее приводится к большему
//      значение большего типа НЕЛЬЗЯ положить в значение меньшего типа
//        System.out.println(distance);

        int a = 5;
        a = a + 1;
        a += 1;
        a += 10;
        a -= 6;
        a++; // оператор инкремента
        a--; // оператор дикремента

        byte b = 127;
        b++; // -128
        System.out.println(b); // произошло переполнение и счёт начнётся с возможного начала [-128, 127]

        byte c = 10;
        c = (byte) (c + 10); // приведение большего типа к меньшему. Явное приведение типа
        c++;
        c++;
        System.out.println(c);
    }
}

