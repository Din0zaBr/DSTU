import os


def lzw_encode(data):
    data = data.lower()
    sp_zn = []

    # Сбор уникальных символов
    for i in data:
        if i not in sp_zn:
            sp_zn.append(i)

    # Создание словаря для кодирования
    sl = {x: sp_zn.index(x) for x in sp_zn}

    num = len(sl)
    current = data[0]
    cur_str = ''
    it_str = ''
    cur_str = current

    # Основная логика алгоритма LZW
    for i in data[1:]:
        next = i
        if (cur_str + next) not in sl:
            sl[cur_str + next] = num
            num += 1
            it_str += str(sl[cur_str]) + ' '
            current = next
            cur_str = current
        else:
            current = next
            cur_str += next

    sl[cur_str + "-"] = num
    it_str += str(sl[cur_str])

    # Формирование результата
    encoded_text = str(sl) + '\n' + it_str.strip()

    print(encoded_text)


# Пример использования функции
lzw_encode('Мама мыла раму')
