public class main {
    public static void main(String[] args) {
        {
            long l = 1234_564_890L; // Исправлено: не преобразуем в byte
            int x = 0b1000_1100_1010; // остается без изменений
            double m = (byte) 110_987_654_6299.123_34; // остается без изменений
            float f = (float) (l + 10 + ++x - m); // Исправлено: преобразуем в float перед вычислениями
            l = (long) f / 1000; // остается без изменений
            System.out.println(l);
        }
    }
}
