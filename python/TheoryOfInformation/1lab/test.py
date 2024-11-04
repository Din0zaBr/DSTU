import heapq
import collections


# Создаем узел дерева
class Node:
    def __init__(self, freq, char=None):
        self.freq = freq
        self.char = char
        self.left = None
        self.right = None


# Функция для построения дерева Хаффмана
def build_huffman_tree(stream):
    freq = collections.defaultdict(int)
    # Подсчитываем частоту символов в потоке данных
    for char in stream:
        freq[char] += 1
    heap = []
    # Создаем кучу из узлов дерева
    for char, char_freq in freq.items():
        heapq.heappush(heap, (char_freq, Node(char_freq, char)))
    # Строим дерево Хаффмана
    while len(heap) > 1:
        freq1, node1 = heapq.heappop(heap)
        freq2, node2 = heapq.heappop(heap)
        merged_node = Node(freq1 + freq2)
        merged_node.left = node1
        merged_node.right = node2
        heapq.heappush(heap, (freq1 + freq2, merged_node))
    # Возвращаем корень дерева
    _, root = heapq.heappop(heap)
    return root


stream = "hello world"
tree = build_huffman_tree(stream)


# Функция для кодирования символов
def encode(char, node):
    if char in node.char:
        return ""
    if char in node.left.char:
        return "0" + encode(char, node.left)
    else:
        return "1" + encode(char, node.right)


# Кодируем каждый символ
code = ""
for char in stream:
    code += encode(char, tree)
print("Encoded code:", code)
