# Определение структуры узла дерева
def create_node(key):
    return {
        'key': key,  # информационное поле
        'service': None,  # служебное поле
        'right': None,  # указатель на правое поддерево
        'left': None  # указатель на левое поддерево
    }


# Создание дерева согласно структуре
d1 = create_node('d1')
d2 = create_node('d2')
d3 = create_node('d3')
d4 = create_node('d4')
d5 = create_node('d5')
d6 = create_node('d6')

# Связывание узлов в дерево
d1['left'] = d2
d1['right'] = d3
d2['left'] = d4
d2['right'] = d5
d3['left'] = d6
print(d1)


# Функция для вывода структуры дерева
def print_tree(node, level=0):
    if node:
        # Выводим текущий узел с отступом
        print('  ' * level + str(node['key']))

        # Рекурсивно обходим левого потомка
        if node['left']:
            print('  ' * level + 'L---')
            print_tree(node['left'], level + 1)

        # Рекурсивно обходим правого потомка
        if node['right']:
            print('  ' * level + 'R---')
            print_tree(node['right'], level + 1)


print("Структура бинарного дерева:")
print_tree(d1)
