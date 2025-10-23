key = int(input())
print(key)
keyword = input().upper()


def unique_ordered(lst):
    return list(dict.fromkeys(lst))


keyword_unique = ''.join(unique_ordered(keyword))

print(keyword_unique)


def encrypt_Ceasar_with_keyword(phrase, key, keyword_unique):
    alp = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    modified_alp = ''
    number = 0
    while len(modified_alp) != key:
        if alp[number] not in keyword_unique:
            modified_alp += alp[number]
            number += 1
        else:
            number += 1
    modified_alp +=

    modified_alp += keyword_unique


encrypt_Ceasar_with_keyword('', key, keyword_unique)
