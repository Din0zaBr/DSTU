package ZeroLaboratory;

public class Solution {
    public static int a = 1;
    public static int b = 3;
    public static int c = 9;
    public static int d = 27;

    public static void main(String[] args) {
        System.out.println("Mesa called Jar Jar Binks, mesa your humble servant!");

        /*
        Дана переменная number.
        Написать программу, которая выводи на экран квадрат этой переменной
         */

        int number = 2;
        int number_square = number * number;
        String number_square_str = Integer.toString(number_square);
        System.out.println(number_square_str);

        /*
        Напишите программу, которая выводит на экран надпись: "May the Force be with you"
         */
        for (int i = 1; i < 11; i++) {
            System.out.println("May the Force be with you");
        }
        String s = "Anakin ";
        System.out.print(s);
/*
        s.append("how are you?");
        s.append("I am");
        s.append("glad");
        s.append("to see you");
        s.append("Your");
*/
        System.out.print("is ");
        System.out.print("a hero");
        System.out.print("!");

        String mol = "Mol";
        String text = "Darth " + mol + "!";
        System.out.println("\n" + text);

        int result = -a + b - c + d;
        System.out.println(result);

        System.out.println(sqr(5));

//        int a = 1;
        double b = 1.5;
        double c = b + 1.5;
        /*
         *        int d = a + 12;
         *        double e = 12.3;
         *        String s = "Luke, " + a;
         */
        String s1 = "Twice ";
//        String s2 = "a";
        String s3 = s1 + "the pride, ";
        String s4 = " the fall.";
        System.out.println(s3 + c + s4);

        print("The power is easy to use!");
        print("The power opens many opportunities!");

        increaseSpeed(700);

        Zam zam = new Zam();
        Dron dron = new Dron();
        zam.spy = dron;
        dron.hunter = zam;

        Jedi jedi1 = new Jedi();
        jedi1.name = "Obi-Wan";
        Jedi jedi2 = new Jedi();
        jedi2.name = "Anakin";
        Jedi jedi3 = new Jedi();
        jedi3.name = "Joda";

        Clone clone1 = new Clone();
        Clone clone2 = new Clone();
        Clone clone3 = new Clone();
        Clone clone4 = new Clone();
        Clone clone5 = new Clone();
        Clone clone6 = new Clone();
        Clone clone7 = new Clone();
        Clone clone8 = new Clone();
        Clone clone9;
        Clone clone10;

        Clone1 clone11 = new Clone1();
        Clone2 clone21 = new Clone2();
        Clone3 clone31 = new Clone3();
        Dias dias = new Dias();

        clone11.owner = dias;
        clone21.owner = dias;
        clone31.owner = dias;

        System.out.println();
        System.out.println(getWeight(888));

        print3("dump");
        print3("cargo");
        System.out.println();
        System.out.println(min(12, 33));
        System.out.println(min(-20, 0));
        System.out.println(min(-10, -20));
    }

    public static int sqr(int a) {
        return a * a;
    }

    public static void print(String s) {
        for (int i = 0; i < 5; i++) {
            System.out.print(s);
        }

    }

    public static void increaseSpeed(int a) {
        a = a + 100;
        System.out.print("\nYour speed is: " + a + " km/h");
    }

    public static class Zam {
        public int kam;
        public int dam;
        public Dron spy;
    }

    public static class Dron {
        public int kam;
        public int dam;
        public Zam hunter;
    }

    public static class Jedi {
        public String name;
    }

    public static class Clone {
    }

    public static class Clone1 {
        public Dias owner;
    }

    public static class Clone2 {
        public Dias owner;
    }

    public static class Clone3 {
        public Dias owner;
    }

    public static class Dias {
    }

    public static double getWeight(int weight) {
        weight = weight / 6;
        return weight;
    }

    public static void print3(String s) {
        System.out.print(s + " " + s + " " + s + " ");
    }

    /*
    Сначала вычисляется условие перед "?" . Если условие истинно, то возвращается значение перед ":" .
    Если условие ложно, то возвращается значение после ":" .
     */
    public static int min(int a, int b) {
        return a < b ? a : b;
    }
}

