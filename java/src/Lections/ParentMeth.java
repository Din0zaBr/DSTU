package Lections;

public class ParentMeth {
    public static void main(String[] args) {
        ChildMeth ch = new ChildMeth();
        ch.PrintStr();
    }

    public void PrintStr(){
        System.out.println("Parent class");
    }
}

class ChildMeth extends ParentMeth{
    public void PrintStr() {
        super.PrintStr();
        System.out.println("Child class");
    }
}
