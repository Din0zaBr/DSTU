package ThirdDotOneLab;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Main {
    public static void main(String[] args) {
        System.out.println(firstQuestion("abcdefghijklmnopqrstuv18340")); // Тестирование строки "abcdefghijklmnopqrstuv18340"
        System.out.println(secondQuestion("{e02fd0e4-00fd-090A-ca30-0d00a0038ba0}")); // Тестирование GUID с скобками
        System.out.println(thirdQuestion("aE:dC:cA:56:76:54")); // Тестирование MAC-адреса
        System.out.println(fourthQuestion("http://www.example.com")); // Тестирование URL
        System.out.println(fifthQuestion("#FFFFFF")); // Тестирование шестнадцатиричного идентификатора цвета в HTML
        System.out.println(sixthQuestion("29/02/2000")); // Тестирование даты в формате dd/mm/yyyy
        System.out.println(seventhQuestion("user@example.com")); // Тестирование E-mail адреса
        System.out.println(eighthQuestion("127.0.0.1")); // Тестирование IP адреса
        System.out.println(ninthQuestion("C00l_Pass")); // Тестирование надежности пароля
        System.out.println(tenthQuestion("123456")); // Тестирование шестизначного числа
        System.out.println(eleventhQuestion("23.78 USD")); // Тестирование цен в USD, RUR, EU
        System.out.println(twelfthQuestion("2 * 9 – 6 × 5")); // Тестирование наличия цифр за которыми не стоит «+»
        System.out.println(thirteenthQuestion("(3 + 5) – 9 × 4")); // Тестирование правильно написанных выражений со скобками
    }

    /**
     * 1. Написать регулярное выражение, определяющее является ли данная строка строкой "abcdefghijklmnopqrstuv18340" или нет.
     */
    public static String firstQuestion(String string) {
        return String.valueOf(Pattern.matches("abcdefghijklmnopqrstuv18340", string.strip()));
    }

    /**
     * 2. Написать регулярное выражение, определяющее является ли данная строка GUID с или без скобок.
     */
    public static String secondQuestion(String string) {
        return String.valueOf(Pattern.matches("^(\\{?[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}}?)$", string.strip()));
    }

    /**
     * 3. Написать регулярное выражение, определяющее является ли заданная строка правильным MAC-адресом.
     */
    public static String thirdQuestion(String string) {
        return String.valueOf(Pattern.matches("^(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", string.strip()));
    }

    /**
     * 4. Написать регулярное выражение, определяющее является ли данная строчка валидным URL адресом.
     */
    public static String fourthQuestion(String string) {
        return String.valueOf(Pattern.matches("^https?://(?:www\\.)?[a-z0-9]{2,}\\.(com|ru)$", string.strip()));
    }

    /**
     * 5. Написать регулярное выражение, определяющее является ли данная строчка шестнадцатиричным идентификатором
     * цвета в HTML.
     */
    public static String fifthQuestion(String string) {
        return String.valueOf(Pattern.matches("^#[0-9a-fA-F]{6}$", string.strip()));
    }

    /**
     * 6. Написать регулярное выражение, определяющее является ли данная строчка датой в формате dd/mm/yyyy.
     */
    public static String sixthQuestion(String string) {
        return String.valueOf(Pattern.matches("^(0[1-9]|1\\d|2[0-8])/(0[1-9]|1[0-2])/((?:1[6-9]|[2-9]\\d)?\\d{2})$" +
                        "|^29/02/(?:(?:1[6-9]|[2-9]\\d)(?:0[48]|[2468][048]|[13579][26])|(?:16|[2468][048]|[3579][26])00)$",
                string.strip()));
    }

    /**
     * 7. Написать регулярное выражение, определяющее является ли данная строчка валидным E-mail адресом согласно RFC
     * под номером 2822.
     */
    public static String seventhQuestion(String string) {
        return String.valueOf(Pattern.matches("^\\w+@\\w+(\\.)?\\w+$", string.strip()));
    }

    /**
     * 8. Составить регулярное выражение, определяющее является ли заданная строка IP адресом, записанным в десятичном виде.
     */
    public static String eighthQuestion(String string) {
        var pattern_str = "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$";
        return String.valueOf(Pattern.matches(pattern_str, string.strip()));
    }

    /**
     * 9. Проверить, надежно ли составлен пароль.
     */
    public static String ninthQuestion(String string) {
        var pattern_str = "^(?=.*[A-Z])(?=.*[a-z])(?=.*\\d)[A-Za-z0-9_]{8,}$";
        return String.valueOf(Pattern.matches(pattern_str, string.strip()));
    }

    /**
     * 10. Проверить является ли заданная строка шестизначным числом, записанным в десятичной системе счисления без
     * нулей в старших разрядах.
     */
    public static String tenthQuestion(String string) {
        var pattern_str = "^[1-9]\\d{5}$";
        return String.valueOf(Pattern.matches(pattern_str, string.strip()));
    }

    /**
     * 11. Есть текст со списками цен. Извлечь из него цены в USD, RUR, EU.
     */
    public static String eleventhQuestion(String string) {
        var pattern_str = "(\\d+(?:\\.\\d+)?)\\s+(USD|RUR|EU)";
        return String.valueOf(Pattern.matches(pattern_str, string.strip()));
    }

    /**
     * 12. Проверить существуют ли в тексте цифры, за которыми не стоит «+».
     */
    public static String twelfthQuestion(String string) {
        var pattern_str = "\\b\\d+\\s*\\+";
        return String.valueOf(Pattern.matches(pattern_str, string.strip()));
    }

    /**
     * 13. Создать запрос для вывода только правильно написанных выражений со скобками
     * (количество открытых и закрытых скобок должно быть одинаково).
     */
    public static String thirteenthQuestion(String string) {
        Pattern pattern = Pattern.compile("((\\([^()]*\\)[^()]*)*)");
        Matcher matcher = pattern.matcher(string);

        if (!matcher.matches()) {
            return String.valueOf(false);
        }

        int openBrackets = 0;
        int closeBrackets = 0;
        for (char c : string.toCharArray()) {
            if (c == '(') {
                openBrackets++;
            } else if (c == ')') {
                closeBrackets++;
            }
        }

        return String.valueOf(openBrackets == closeBrackets);
    }
}
