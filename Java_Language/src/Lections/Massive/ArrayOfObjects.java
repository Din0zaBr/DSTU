package Lections.Massive;

public class ArrayOfObjects {
    public static void main(String[] args) {
        Book[] shelf = new Book[3];
        shelf[0] = new Book("Red");
        shelf[1] = new Book("Green");
        shelf[2] = new Book("Blue");
        System.out.println(shelf[1].title);
    }
}

class Book {
    String title;

    Book(String title) {
        this.title = title;
    }
}