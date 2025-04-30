import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Tuple


class CyclicCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Циклические коды: кодирование и декодирование")
        self.root.geometry("900x700")

        self.create_widgets()

        # Инициализация переменных
        self.generator_poly = None
        self.code_matrix = None
        self.n = None
        self.k = None

    def create_widgets(self):
        # Notebook для разделения кодирования и декодирования
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Вкладка кодирования
        self.encoding_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.encoding_tab, text="Кодирование")
        self.create_encoding_tab()

        # Вкладка декодирования
        self.decoding_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.decoding_tab, text="Декодирование")
        self.create_decoding_tab()

        # Вкладка информации
        self.info_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.info_tab, text="Информация")
        self.create_info_tab()

    def create_encoding_tab(self):
        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(self.encoding_tab, text="Входные данные")
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Выбор источника данных
        self.input_source = tk.StringVar(value="keyboard")
        ttk.Radiobutton(input_frame, text="Ввод с клавиатуры", variable=self.input_source, value="keyboard").grid(row=0,
                                                                                                                  column=0,
                                                                                                                  sticky=tk.W)
        ttk.Radiobutton(input_frame, text="Загрузить из файла", variable=self.input_source, value="file").grid(row=0,
                                                                                                               column=1,
                                                                                                               sticky=tk.W)

        # Поле для ввода текста
        self.input_text = tk.Text(input_frame, height=5, width=50)
        self.input_text.grid(row=1, column=0, columnspan=2, pady=5)

        # Кнопка загрузки файла
        self.load_file_btn = ttk.Button(input_frame, text="Выбрать файл", command=self.load_file)
        self.load_file_btn.grid(row=2, column=1, sticky=tk.E)

        # Фрейм для параметров кодирования
        params_frame = ttk.LabelFrame(self.encoding_tab, text="Параметры кодирования")
        params_frame.pack(fill=tk.X, padx=5, pady=5)

        # Выбор типа ввода
        self.param_type = tk.StringVar(value="poly")
        ttk.Radiobutton(params_frame, text="Полином", variable=self.param_type, value="poly").grid(row=0, column=0,
                                                                                                   sticky=tk.W)
        ttk.Radiobutton(params_frame, text="Матрица", variable=self.param_type, value="matrix").grid(row=0, column=1,
                                                                                                     sticky=tk.W)

        # Поле для ввода полинома
        ttk.Label(params_frame, text="Порождающий полином (коэффициенты через пробел, старшая степень слева):").grid(
            row=1, column=0, sticky=tk.W)
        self.poly_entry = ttk.Entry(params_frame)
        self.poly_entry.grid(row=1, column=1, sticky=tk.EW)

        # Поле для ввода n
        ttk.Label(params_frame, text="Параметр n (длина кодового слова):").grid(row=2, column=0, sticky=tk.W)
        self.n_entry = ttk.Entry(params_frame)
        self.n_entry.grid(row=2, column=1, sticky=tk.EW)

        # Поле для ввода матрицы (скрыто по умолчанию)
        self.matrix_label = ttk.Label(params_frame,
                                      text="Порождающая матрица (строки через ';', элементы через пробел):")
        self.matrix_label.grid(row=3, column=0, sticky=tk.W)
        self.matrix_entry = ttk.Entry(params_frame)
        self.matrix_entry.grid(row=3, column=1, sticky=tk.EW)

        # Скрываем поля матрицы по умолчанию
        self.matrix_label.grid_remove()
        self.matrix_entry.grid_remove()

        # Привязка изменения типа ввода
        self.param_type.trace_add("write", self.toggle_param_input)

        # Кнопка кодирования
        encode_btn = ttk.Button(self.encoding_tab, text="Закодировать", command=self.encode)
        encode_btn.pack(pady=5)

        # Фрейм для вывода результатов
        output_frame = ttk.LabelFrame(self.encoding_tab, text="Результаты кодирования")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Текст с результатами
        self.encoding_output = tk.Text(output_frame, height=10, state=tk.DISABLED)
        self.encoding_output.pack(fill=tk.BOTH, expand=True)

        # Прокрутка
        scrollbar = ttk.Scrollbar(self.encoding_output)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.encoding_output.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.encoding_output.yview)

    def create_decoding_tab(self):
        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(self.decoding_tab, text="Входные данные")
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Поле для ввода закодированной последовательности
        ttk.Label(input_frame, text="Закодированная последовательность (биты через пробел):").grid(row=0, column=0,
                                                                                                   sticky=tk.W)
        self.encoded_input = ttk.Entry(input_frame)
        self.encoded_input.grid(row=0, column=1, sticky=tk.EW)

        # Фрейм для параметров декодирования
        params_frame = ttk.LabelFrame(self.decoding_tab, text="Параметры декодирования")
        params_frame.pack(fill=tk.X, padx=5, pady=5)

        # Выбор типа ввода
        self.decode_param_type = tk.StringVar(value="poly")
        ttk.Radiobutton(params_frame, text="Полином", variable=self.decode_param_type, value="poly").grid(row=0,
                                                                                                          column=0,
                                                                                                          sticky=tk.W)
        ttk.Radiobutton(params_frame, text="Матрица", variable=self.decode_param_type, value="matrix").grid(row=0,
                                                                                                            column=1,
                                                                                                            sticky=tk.W)

        # Поле для ввода полинома
        ttk.Label(params_frame, text="Порождающий полином (коэффициенты через пробел, старшая степень слева):").grid(
            row=1, column=0, sticky=tk.W)
        self.decode_poly_entry = ttk.Entry(params_frame)
        self.decode_poly_entry.grid(row=1, column=1, sticky=tk.EW)

        # Поле для ввода n
        ttk.Label(params_frame, text="Параметр n (длина кодового слова):").grid(row=2, column=0, sticky=tk.W)
        self.decode_n_entry = ttk.Entry(params_frame)
        self.decode_n_entry.grid(row=2, column=1, sticky=tk.EW)

        # Поле для ввода матрицы (скрыто по умолчанию)
        self.decode_matrix_label = ttk.Label(params_frame,
                                             text="Порождающая матрица (строки через ';', элементы через пробел):")
        self.decode_matrix_label.grid(row=3, column=0, sticky=tk.W)
        self.decode_matrix_entry = ttk.Entry(params_frame)
        self.decode_matrix_entry.grid(row=3, column=1, sticky=tk.EW)

        # Скрываем поля матрицы по умолчанию
        self.decode_matrix_label.grid_remove()
        self.decode_matrix_entry.grid_remove()

        # Привязка изменения типа ввода
        self.decode_param_type.trace_add("write", self.toggle_decode_param_input)

        # Фрейм для ошибок
        error_frame = ttk.LabelFrame(self.decoding_tab, text="Ошибки")
        error_frame.pack(fill=tk.X, padx=5, pady=5)

        # Выбор способа добавления ошибок
        self.error_type = tk.StringVar(value="none")
        ttk.Radiobutton(error_frame, text="Без ошибок", variable=self.error_type, value="none").grid(row=0, column=0,
                                                                                                     sticky=tk.W)
        ttk.Radiobutton(error_frame, text="Случайные ошибки", variable=self.error_type, value="random").grid(row=0,
                                                                                                             column=1,
                                                                                                             sticky=tk.W)
        ttk.Radiobutton(error_frame, text="Ручной ввод ошибок", variable=self.error_type, value="manual").grid(row=0,
                                                                                                               column=2,
                                                                                                               sticky=tk.W)

        # Поле для ввода позиций ошибок
        ttk.Label(error_frame, text="Позиции ошибок (индексы через пробел, начиная с 0):").grid(row=1, column=0,
                                                                                                columnspan=2,
                                                                                                sticky=tk.W)
        self.error_pos_entry = ttk.Entry(error_frame)
        self.error_pos_entry.grid(row=1, column=2, sticky=tk.EW)
        self.error_pos_entry.grid_remove()

        # Привязка изменения типа ошибок
        self.error_type.trace_add("write", self.toggle_error_input)

        # Кнопка декодирования
        decode_btn = ttk.Button(self.decoding_tab, text="Декодировать", command=self.decode)
        decode_btn.pack(pady=5)

        # Фрейм для вывода результатов
        output_frame = ttk.LabelFrame(self.decoding_tab, text="Результаты декодирования")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Текст с результатами
        self.decoding_output = tk.Text(output_frame, height=15, state=tk.DISABLED)
        self.decoding_output.pack(fill=tk.BOTH, expand=True)

        # Прокрутка
        scrollbar = ttk.Scrollbar(self.decoding_output)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.decoding_output.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.decoding_output.yview)

    def create_info_tab(self):
        info_text = """Циклические коды - класс помехоустойчивых кодов, обладающих свойством цикличности.

Кодирование:
1. Полиномиальный метод:
   - Информационное слово представляется как полином m(x)
   - Умножается на x^(n-k)
   - Делится на порождающий полином g(x)
   - Кодовое слово: m(x)*x^(n-k) + остаток от деления

2. Матричный метод:
   - Порождающая матрица строится на основе g(x)
   - Кодовое слово = информационное слово × порождающая матрица

Декодирование (алгоритм Меггита):
1. Вычисление синдрома
2. Поиск ошибки по таблице синдромов
3. Исправление ошибки
4. Циклический сдвиг и повторение

Преобразование полином↔матрица:
- Порождающая матрица строится из циклических сдвигов g(x)
- Полином можно получить из первой строки матрицы
"""
        info_label = tk.Label(self.info_tab, text=info_text, justify=tk.LEFT, anchor=tk.W)
        info_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def toggle_param_input(self, *args):
        if self.param_type.get() == "poly":
            self.poly_entry.grid()
            self.n_entry.grid()
            self.matrix_label.grid_remove()
            self.matrix_entry.grid_remove()
        else:
            self.poly_entry.grid_remove()
            self.n_entry.grid_remove()
            self.matrix_label.grid()
            self.matrix_entry.grid()

    def toggle_decode_param_input(self, *args):
        if self.decode_param_type.get() == "poly":
            self.decode_poly_entry.grid()
            self.decode_n_entry.grid()
            self.decode_matrix_label.grid_remove()
            self.decode_matrix_entry.grid_remove()
        else:
            self.decode_poly_entry.grid_remove()
            self.decode_n_entry.grid_remove()
            self.decode_matrix_label.grid()
            self.decode_matrix_entry.grid()

    def toggle_error_input(self, *args):
        if self.error_type.get() == "manual":
            self.error_pos_entry.grid()
        else:
            self.error_pos_entry.grid_remove()

    def load_file(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.input_text.delete(1.0, tk.END)
                    self.input_text.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def encode(self):
        try:
            # Получаем входные данные
            if self.input_source.get() == "keyboard":
                text = self.input_text.get(1.0, tk.END).strip()
            else:
                # Уже загружено в load_file
                text = self.input_text.get(1.0, tk.END).strip()
                if not text:
                    raise ValueError("Файл не загружен или пуст")

            # Преобразуем текст в бинарную последовательность
            binary_data = ''.join(format(ord(c), '08b') for c in text)

            # Получаем параметры кодирования
            if self.param_type.get() == "poly":
                # Ввод полинома
                poly_str = self.poly_entry.get().strip()
                if not poly_str:
                    raise ValueError("Не введен порождающий полином")

                generator_poly = [int(x) for x in poly_str.split()]
                self.generator_poly = generator_poly

                # Ввод n
                n_str = self.n_entry.get().strip()
                if not n_str:
                    raise ValueError("Не введен параметр n")

                self.n = int(n_str)
                self.k = self.n - (len(generator_poly) - 1)

                # Строим матрицу из полинома
                self.code_matrix = self.poly_to_matrix(generator_poly, self.n)
            else:
                # Ввод матрицы
                matrix_str = self.matrix_entry.get().strip()
                if not matrix_str:
                    raise ValueError("Не введена порождающая матрица")

                # Парсим матрицу
                rows = matrix_str.split(';')
                code_matrix = []
                for row in rows:
                    code_matrix.append([int(x) for x in row.strip().split()])

                self.code_matrix = np.array(code_matrix)
                self.k = len(code_matrix)
                self.n = len(code_matrix[0])

                # Получаем полином из матрицы
                self.generator_poly = self.matrix_to_poly(code_matrix)

            # Кодируем данные
            encoded_poly, encoded_vector = self.encode_data(binary_data)

            # Выводим результаты
            self.encoding_output.config(state=tk.NORMAL)
            self.encoding_output.delete(1.0, tk.END)

            self.encoding_output.insert(tk.END, "Исходный текст:\n")
            self.encoding_output.insert(tk.END, f"{text}\n\n")

            self.encoding_output.insert(tk.END, "Бинарное представление:\n")
            self.encoding_output.insert(tk.END, f"{binary_data}\n\n")

            self.encoding_output.insert(tk.END, "Параметры кода:\n")
            self.encoding_output.insert(tk.END, f"n = {self.n}, k = {self.k}\n\n")

            self.encoding_output.insert(tk.END, "Порождающий полином:\n")
            self.encoding_output.insert(tk.END, f"{self.format_poly(self.generator_poly)}\n\n")

            self.encoding_output.insert(tk.END, "Порождающая матрица:\n")
            for row in self.code_matrix:
                self.encoding_output.insert(tk.END, ' '.join(map(str, row)) + '\n')
            self.encoding_output.insert(tk.END, "\n")

            self.encoding_output.insert(tk.END, "Закодированные данные (полиномиальная форма):\n")
            for poly in encoded_poly:
                self.encoding_output.insert(tk.END, f"{self.format_poly(poly)}\n")
            self.encoding_output.insert(tk.END, "\n")

            self.encoding_output.insert(tk.END, "Закодированные данные (векторная форма):\n")
            for vector in encoded_vector:
                self.encoding_output.insert(tk.END, ' '.join(map(str, vector)) + '\n')

                self.encoding_output.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при кодировании: {e}")

    def decode(self):
        try:
            # Получаем входные данные
            encoded_str = self.encoded_input.get().strip()
            if not encoded_str:
                raise ValueError("Не введена закодированная последовательность")

            encoded_vector = [int(x) for x in encoded_str.split()]

            # Добавляем ошибки, если нужно
            if self.error_type.get() == "random":
                # Случайная ошибка в одном бите
                error_pos = np.random.randint(0, len(encoded_vector))
                encoded_vector[error_pos] ^= 1
            elif self.error_type.get() == "manual":
                error_pos_str = self.error_pos_entry.get().strip()
                if error_pos_str:
                    error_positions = [int(x) for x in error_pos_str.split()]
                    for pos in error_positions:
                        if pos < 0 or pos >= len(encoded_vector):
                            raise ValueError(f"Недопустимая позиция ошибки: {pos}")
                        encoded_vector[pos] ^= 1

            # Получаем параметры декодирования
            if self.decode_param_type.get() == "poly":
                # Ввод полинома
                poly_str = self.decode_poly_entry.get().strip()
                if not poly_str:
                    raise ValueError("Не введен порождающий полином")

                generator_poly = [int(x) for x in poly_str.split()]

                # Ввод n
                n_str = self.decode_n_entry.get().strip()
                if not n_str:
                    raise ValueError("Не введен параметр n")

                n = int(n_str)
                k = n - (len(generator_poly) - 1)

                # Строим матрицу из полинома
                code_matrix = self.poly_to_matrix(generator_poly, n)
            else:
                # Ввод матрицы
                matrix_str = self.decode_matrix_entry.get().strip()
                if not matrix_str:
                    raise ValueError("Не введена порождающая матрица")

                # Парсим матрицу
                rows = matrix_str.split(';')
                code_matrix = []
                for row in rows:
                    code_matrix.append([int(x) for x in row.strip().split()])

                code_matrix = np.array(code_matrix)
                k = len(code_matrix)
                n = len(code_matrix[0])

                # Получаем полином из матрицы
                generator_poly = self.matrix_to_poly(code_matrix)

            # Декодируем данные
            decoded_data, steps = self.decode_data(encoded_vector, generator_poly, n)

            # Выводим результаты
            self.decoding_output.config(state=tk.NORMAL)
            self.decoding_output.delete(1.0, tk.END)

            self.decoding_output.insert(tk.END, "Принятая последовательность (с ошибками):\n")
            self.decoding_output.insert(tk.END, ' '.join(map(str, encoded_vector)) + '\n\n')

            self.decoding_output.insert(tk.END, "Параметры кода:\n")
            self.decoding_output.insert(tk.END, f"n = {n}, k = {k}\n\n")

            self.decoding_output.insert(tk.END, "Порождающий полином:\n")
            self.decoding_output.insert(tk.END, f"{self.format_poly(generator_poly)}\n\n")

            self.decoding_output.insert(tk.END, "Порождающая матрица:\n")
            for row in code_matrix:
                self.decoding_output.insert(tk.END, ' '.join(map(str, row)) + '\n')
            self.decoding_output.insert(tk.END, "\n")

            self.decoding_output.insert(tk.END, "Процесс декодирования:\n")
            for step in steps:
                self.decoding_output.insert(tk.END, step + '\n')
            self.decoding_output.insert(tk.END, "\n")

            self.decoding_output.insert(tk.END, "Декодированные данные:\n")
            self.decoding_output.insert(tk.END, f"{decoded_data}\n")

            self.decoding_output.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при декодировании: {e}")

    def poly_to_matrix(self, poly: List[int], n: int) -> np.ndarray:
        """Преобразует порождающий полином в порождающую матрицу"""
        k = n - (len(poly) - 1)
        matrix = []

        for i in range(k):
            # Создаем строку: x^(k-1-i) * g(x)
            row = [0] * i + poly + [0] * (k - 1 - i)
            # Обрезаем до длины n (младшие степени)
            row = row[:n]
            matrix.append(row)

        return np.array(matrix)

    def matrix_to_poly(self, matrix: np.ndarray) -> List[int]:
        """Извлекает порождающий полином из порождающей матрицы"""
        # Первая строка матрицы - это g(x)
        return list(matrix[0][:len(matrix[0]) - len(matrix) + 1])

    def encode_data(self, binary_data: str) -> Tuple[List[List[int]], List[List[int]]]:
        """Кодирует бинарные данные с использованием циклического кода"""
        # Разбиваем на блоки по k бит
        k = self.k
        blocks = [binary_data[i:i + k] for i in range(0, len(binary_data), k)]

        encoded_poly = []
        encoded_vector = []

        for block in blocks:
            # Дополняем последний блок нулями, если нужно
            if len(block) < k:
                block = block + '0' * (k - len(block))

            # Преобразуем блок в полином
            m = [int(bit) for bit in block]

            # Кодируем полиномиальным методом
            # m(x) * x^(n-k)
            mx = m + [0] * (self.n - self.k)

            # Делим на g(x) и находим остаток
            remainder = self.poly_div(mx, self.generator_poly)

            # Кодовое слово: m(x)*x^(n-k) + remainder
            codeword_poly = mx
            for i in range(len(remainder)):
                codeword_poly[-(i + 1)] = remainder[-(i + 1)]

            encoded_poly.append(codeword_poly)
            encoded_vector.append(codeword_poly)

        return encoded_poly, encoded_vector

    def decode_data(self, encoded_vector: List[int], generator_poly: List[int], n: int) -> Tuple[str, List[str]]:
        """Декодирует данные с использованием алгоритма Меггита"""
        k = n - (len(generator_poly) - 1)
        steps = []

        # Создаем таблицу синдромов для одиночных ошибок
        syndrome_table = {}
        for i in range(n):
            # Создаем вектор ошибки
            error = [0] * n
            error[i] = 1

            # Вычисляем синдром
            syndrome = self.poly_div(error, generator_poly)
            syndrome = syndrome[-(len(generator_poly) - 1):]  # Берем только остаток

            # Сохраняем в таблице
            syndrome_table[tuple(syndrome)] = i

        steps.append("Таблица синдромов для одиночных ошибок:")
        for syn, pos in syndrome_table.items():
            steps.append(f"Синдром: {self.format_poly(list(syn))} -> Ошибка в позиции {pos}")
        steps.append("")

        # Основной цикл декодирования
        received = encoded_vector.copy()
        corrected = received.copy()
        steps.append(f"Начальная принятая последовательность: {self.format_poly(received)}")

        # Вычисляем синдром
        syndrome = self.poly_div(received, generator_poly)
        syndrome = syndrome[-(len(generator_poly) - 1):]  # Берем только остаток
        steps.append(f"Вычисленный синдром: {self.format_poly(syndrome)}")

        # Ищем ошибку
        error_pos = None
        for shift in range(n):
            # Проверяем, есть ли текущий синдром в таблице
            current_syn = tuple(syndrome)
            if current_syn in syndrome_table:
                error_pos = syndrome_table[current_syn]
                steps.append(f"Найденная ошибка после {shift} сдвигов: позиция {error_pos}")
                break

            # Циклический сдвиг вправо
            syndrome = self.poly_shift(syndrome, generator_poly)
            steps.append(f"Сдвиг {shift + 1}: новый синдром {self.format_poly(syndrome)}")

        if error_pos is not None:
            # Исправляем ошибку
            corrected[error_pos] ^= 1
            steps.append(f"Исправленная последовательность: {self.format_poly(corrected)}")
        else:
            steps.append("Ошибка не обнаружена или не может быть исправлена")

        # Удаляем проверочные биты (первые n-k бит)
        decoded_data = ''.join(map(str, corrected[:k]))

        return decoded_data, steps

    def poly_div(self, dividend: List[int], divisor: List[int]) -> List[int]:
        """Деление полиномов в двоичном поле (возвращает остаток)"""
        # Удаляем ведущие нули
        dividend = self.trim_poly(dividend.copy())
        divisor = self.trim_poly(divisor.copy())

        len_diff = len(dividend) - len(divisor)

        if len_diff < 0:
            return dividend  # Остаток равен делимому, если степень делителя больше

        # Основной цикл деления
        for i in range(len_diff + 1):
            if dividend[i] == 1:
                for j in range(len(divisor)):
                    dividend[i + j] ^= divisor[j]

        # Возвращаем остаток
        return self.trim_poly(dividend[-len(divisor) + 1:])

    def poly_shift(self, poly: List[int], generator_poly: List[int]) -> List[int]:
        """Циклический сдвиг полинома вправо с учетом порождающего полинома"""
        # Сохраняем длину синдрома (n-k)
        syn_len = len(generator_poly) - 1
        if len(poly) < syn_len:
            poly = [0] * (syn_len - len(poly)) + poly

        # Сдвигаем вправо
        shifted = [poly[-1]] + poly[:-1]

        # Если старший бит был 1, вычитаем g(x) (сложение в GF(2))
        if poly[-1] == 1:
            for i in range(syn_len):
                shifted[i] ^= generator_poly[i + 1]  # Пропускаем старший коэффициент g(x)

        return shifted

    def trim_poly(self, poly: List[int]) -> List[int]:
        """Удаляет ведущие нули из полинома"""
        while len(poly) > 0 and poly[0] == 0:
            poly = poly[1:]
        return poly if len(poly) > 0 else [0]

    def format_poly(self, poly: List[int]) -> str:
        """Форматирует полином в виде строки"""
        terms = []
        for i, coeff in enumerate(poly):
            if coeff == 1:
                power = len(poly) - 1 - i
                if power == 0:
                    terms.append("1")
                elif power == 1:
                    terms.append("x")
                else:
                    terms.append(f"x^{power}")

        if not terms:
            return "0"

        return " + ".join(terms)


if __name__ == "__main__":
    root = tk.Tk()
    app = CyclicCodeApp(root)
    root.mainloop()