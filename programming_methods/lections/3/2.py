from pathlib import Path
from anytree import Node, RenderTree, findall


# Функция для создания дерева каталогов с ограничением глубины
def build_directory_tree(path, max_depth=1):
    # Создаем корневой узел
    root = Node(str(path))

    # Рекурсивная функция для добавления узлов
    def add_nodes(parent_node, path, current_depth):
        if current_depth > max_depth:
            return  # Прекращаем рекурсию, если достигли максимальной глубины

        try:
            for child in path.iterdir():
                if child.is_dir():  # Проверяем, является ли это каталог
                    child_node = Node(child.name, parent=parent_node)
                    add_nodes(child_node, child, current_depth + 1)  # Рекурсивно добавляем подкаталоги
                elif child.is_file():  # Если это файл, добавляем его как лист
                    Node(child.name, parent=parent_node)
        except PermissionError:
            # Пропускаем каталоги, к которым нет доступа
            print(f"Отказано в доступе: {path}")

    # Начинаем с корневого каталога
    add_nodes(root, path, current_depth=0)
    return root


# Путь к корневому каталогу (например, "C:\\")
root_path = Path("C:\\")

# Создание дерева каталогов с ограничением глубины
root = build_directory_tree(root_path, max_depth=2)

# Визуализация дерева
for pre, fill, node in RenderTree(root):
    print(f"{pre}{node.name}")

# Вывод всех дочерних узлов
for node in root.descendants:
    print(node.name, end=" ")
print()

# Поиск узлов, начинающихся с "mail"
nodes = findall(root, lambda n: n.name.startswith("mail"))
print(nodes)
