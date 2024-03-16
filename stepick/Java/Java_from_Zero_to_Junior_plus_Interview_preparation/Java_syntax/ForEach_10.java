package stepick.Java.Java_from_Zero_to_Junior_plus_Interview_preparation.Java_syntax;

// For each - если не нужны индексы
public class ForEach_10 {
    public static void main(String[] args) {
        String[] students = {
                "Ivan", "Andrew", "Galina", "Sonya", "Arina", "Roma", "Danila", "Kirill", "Milena", "Dima", "Ruslan", "Alexey"
        };
//        for (int i = 0; i < students.length; i++) {
//            System.out.println(students[i]);
//        }
        for (String student : students) { // тип доставаемой переменной, имя : массив откуда достаётся
            System.out.println(student);
        }
    }
}
