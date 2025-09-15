from string import ascii_uppercase

russian_alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
russian_alphabet_upper = russian_alphabet.upper()
alphabet = ascii_uppercase + russian_alphabet_upper
phrase: list = list(input())
keyword: list = list(input())
row_count, colum_count = int(input()), int(input())

table: list = [[] for _ in range(colum_count)]
array = 0
print(len(phrase))

if len(phrase) > row_count * colum_count:
    print("Фраза не поместится в таблицу")
elif len(phrase) < row_count * colum_count:
    print("В таблице будет присутствовать свободное место")
else:
    for row in range(0, row_count * colum_count, row_count):
        table[array] = phrase[row:(row + 1 * row_count)]
        array += 1

for letter in keyword:
    pass