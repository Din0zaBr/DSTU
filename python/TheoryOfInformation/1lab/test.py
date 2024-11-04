import ast
from bisect import bisect_left


def z_Haffman(content, it):
    try:
        ver = []
        sp_zn = []
        content = content.lower()

        # Подсчет частоты символов
        for i in content:
            if i not in sp_zn:
                ver.append(1)
                sp_zn.append(i)
            else:
                ind = sp_zn.index(i)
                ver[ind] += 1

        dl = len(content)
        ver = [x / dl for x in ver]

        # Сортировка по убыванию частоты
        for i in range(len(ver) - 1):
            for j in range(i + 1, len(sp_zn)):
                if ver[i] < ver[j]:
                    ver[i], ver[j] = ver[j], ver[i]
                    sp_zn[i], sp_zn[j] = sp_zn[j], sp_zn[i]

        k = len(sp_zn)
        sl = {}

        # Построение кодов Хаффмана
        for i in range(k - 1):
            summ = ver[-1] + ver[-2]
            ver = ver[:(len(ver) - 2)]
            ver.reverse()
            ind = bisect_left(ver, summ)
            ver.insert(ind, summ)
            ver.reverse()

            for char in sp_zn[-1]:
                sl[char] = sl.get(char, '') + '0'
            for char in sp_zn[-2]:
                sl[char] = sl.get(char, '') + '1'

            st = sp_zn[-1] + sp_zn[-2]
            sp_zn = sp_zn[:(len(sp_zn) - 2)]
            sp_zn.reverse()
            sp_zn.insert(ind, st)
            sp_zn.reverse()

        # Обратное преобразование кодов
        for k in sl.keys():
            sl[k] = sl[k][::-1]

        answer = str(sl) + "n"
        for i in content:
            answer += sl[i]

        fname = "file" + str(it) + ".txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(answer)

        return answer  # Возвращаем результат для дальнейшего использования

    except Exception as e:
        print(f"Произошла ошибка при открытии файла: {str(e)}")
        return None


def d_Haffman(content, it):
    try:
        sl, stroka = content.split('n')
        sl = ast.literal_eval(sl)
        sl1 = {value: key for key, value in sl.items()}
        answer = ''
        current = ''

        # Декодирование
        for i in stroka:
            current += i
            if current in sl1:
                answer += sl1[current]
                current = ''

        fname = "file" + str(it) + ".txt"
        with open(fname, "w", encoding="utf-8") as f:
            f.write(answer)

        return answer  # Возвращаем результат для дальнейшего использования

    except Exception as e:
        print(f"Введён неверный формат зашифрованного текста: {str(e)}")
        return None


# Пример использования функций
content_to_encode = "Мама мыла раму"
it_counter = 1

encoded_result = z_Haffman(content_to_encode, it_counter)
print("Закодированный результат:n", encoded_result)

# Для декодирования нужно будет передать закодированный текст в правильном формате
if encoded_result:
    decoded_result = d_Haffman(encoded_result, it_counter)
    print("Декодированный результат:n", decoded_result)

'''
{'у': '0110', 'р': '0111', 'л': '0100', 'ы': '0101', ' ': '00', 'а': '10', 'м': '11'}
111011100011010101001000011110110110
'''


def lz77_encode(text, window_size=20):
    """
    Кодирует текст с использованием алгоритма LZ77.
    """
    encoded = []
    i = 0
    while i < len(text):
        match_length = 0
        match_offset = 0
        lookahead_buffer = text[i:i + window_size]  # Окно просмотра вперед
        search_buffer = text[max(0, i - window_size):i]  # Окно поиска
        for j in range(len(search_buffer)):
            length = 0
            while (length < len(lookahead_buffer) and
                   j + length < len(search_buffer) and
                   search_buffer[j + length] == lookahead_buffer[length]):
                length += 1
            if length > match_length:
                match_length = length
                match_offset = len(search_buffer) - j
        if match_length > 0:
            encoded.append((match_offset, match_length, lookahead_buffer[match_length]))
            i += match_length + 1
        else:
            encoded.append((0, 0, text[i]))
            i += 1
    return encoded


print(lz77_encode("Мама мыла раму"))
