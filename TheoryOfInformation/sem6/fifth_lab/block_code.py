import customtkinter as ctk
import numpy as np
import random
from tkinter import messagebox
from helpers import text_to_binary, binary_to_text


class BlockCodeModule:
    def __init__(self, parent):
        self.parent = parent
        self.n = 7  # Общее количество бит в кодовом слове (по умолчанию 7)
        self.k = 4  # Количество информационных бит (по умолчанию 4)
        self.H_matrix = None  # Проверочная матрица
        self.G_matrix = None  # Порождающая матрица
        self.error_correction_capability = 1  # Начальное количество исправляемых ошибок

    def create_widgets(self, parent_frame):
        # Создание основного фрейма
        self.main_frame = ctk.CTkFrame(parent_frame)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Фрейм для ввода параметров
        self.params_frame = ctk.CTkFrame(self.main_frame)
        self.params_frame.pack(fill="x", padx=10, pady=10)

        # Параметры кода
        self.params_label = ctk.CTkLabel(self.params_frame, text="Параметры кода:",
                                         font=ctk.CTkFont(weight="bold", size=14))
        self.params_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # n
        self.n_label = ctk.CTkLabel(self.params_frame, text="n (длина кодового слова):",
                                    font=ctk.CTkFont(size=12))
        self.n_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.n_entry = ctk.CTkEntry(self.params_frame, width=60)
        self.n_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.n_entry.insert(0, str(self.n))

        # k
        self.k_label = ctk.CTkLabel(self.params_frame, text="k (кол-во информационных бит):",
                                    font=ctk.CTkFont(size=12))
        self.k_label.grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.k_entry = ctk.CTkEntry(self.params_frame, width=60)
        self.k_entry.grid(row=1, column=3, padx=10, pady=5, sticky="w")
        self.k_entry.insert(0, str(self.k))

        # Кнопка для генерации или ввода матрицы
        self.matrix_button = ctk.CTkButton(self.params_frame, text="Сгенерировать матрицу",
                                           command=self.generate_matrix, fg_color="#2E86C1", hover_color="#1A5276")
        self.matrix_button.grid(row=1, column=4, padx=10, pady=5)

        # Информация о корректирующей способности
        self.info_label = ctk.CTkLabel(self.params_frame,
                                       text=f"Текущая корректирующая способность: {self.error_correction_capability} ошибок",
                                       font=ctk.CTkFont(size=12))
        self.info_label.grid(row=2, column=0, columnspan=5, padx=10, pady=5, sticky="w")

        # Фрейм для ввода текста
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(fill="x", padx=10, pady=10)

        # Заголовок для ввода текста
        self.input_label = ctk.CTkLabel(self.input_frame, text="Исходный текст:",
                                        font=ctk.CTkFont(weight="bold", size=14))
        self.input_label.pack(padx=10, pady=5, anchor="w")

        # Текстовое поле для ввода
        self.input_text = ctk.CTkTextbox(self.input_frame, height=100)
        self.input_text.pack(fill="x", padx=10, pady=5)

        # Кнопки для загрузки текста из файла и очистки
        self.buttons_frame = ctk.CTkFrame(self.input_frame)
        self.buttons_frame.pack(fill="x", padx=10, pady=5)

        self.load_button = ctk.CTkButton(self.buttons_frame, text="Загрузить из файла",
                                         command=self.load_text)
        self.load_button.pack(side="left", padx=5)

        self.clear_button = ctk.CTkButton(self.buttons_frame, text="Очистить",
                                          command=lambda: self.input_text.delete("1.0", "end"))
        self.clear_button.pack(side="left", padx=5)

        # Фрейм для операций кодирования
        self.operation_frame = ctk.CTkFrame(self.main_frame)
        self.operation_frame.pack(fill="x", padx=10, pady=10)

        # Кнопка для кодирования
        self.encode_button = ctk.CTkButton(self.operation_frame, text="Кодировать",
                                           command=self.encode_text)
        self.encode_button.pack(side="left", padx=10, pady=10)

        # Кнопка для внесения ошибок
        self.noise_button = ctk.CTkButton(self.operation_frame, text="Внести ошибки",
                                          command=self.add_noise)
        self.noise_button.pack(side="left", padx=10, pady=10)

        # Кнопка для декодирования
        self.decode_button = ctk.CTkButton(self.operation_frame, text="Декодировать",
                                           command=self.decode_text)
        self.decode_button.pack(side="left", padx=10, pady=10)

        # Адаптивная кнопка для увеличения корректирующей способности
        self.adapt_button = ctk.CTkButton(self.operation_frame, text="Адаптировать код",
                                          command=self.adapt_code, state="disabled")
        self.adapt_button.pack(side="left", padx=10, pady=10)

        # Основной фрейм для матриц и результатов
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Фрейм для отображения матриц слева
        self.matrix_display_frame = ctk.CTkFrame(self.content_frame)
        self.matrix_display_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.matrix_label = ctk.CTkLabel(self.matrix_display_frame, text="Матрицы кода:",
                                         font=ctk.CTkFont(weight="bold", size=14))
        self.matrix_label.pack(padx=10, pady=5, anchor="w")

        self.matrix_text = ctk.CTkTextbox(self.matrix_display_frame, height=200)
        self.matrix_text.pack(fill="both", expand=True, padx=10, pady=5)

        # Фрейм для отображения результатов справа
        self.result_frame = ctk.CTkFrame(self.content_frame)
        self.result_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # Заголовок для результатов
        self.result_label = ctk.CTkLabel(self.result_frame, text="Результаты:",
                                         font=ctk.CTkFont(weight="bold", size=14))
        self.result_label.pack(padx=10, pady=5, anchor="w")

        # Текстовое поле для вывода результатов
        self.result_text = ctk.CTkTextbox(self.result_frame, height=250)
        self.result_text.pack(fill="both", expand=True, padx=10, pady=5)

        # Настройка веса колонок для корректного распределения пространства
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

    def load_text(self):
        text = self.parent.load_text_from_file()
        if text:
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", text)

    def generate_matrix(self):
        try:
            self.n = int(self.n_entry.get())
            self.k = int(self.k_entry.get())

            if self.n <= self.k:
                messagebox.showerror("Ошибка", "n должно быть больше k")
                return

            if 2 ** (self.n - self.k) < 2 * self.n + 1:
                self.result_text.insert("end",
                                        "\nПредупреждение: при данных параметрах (n, k) не гарантируется исправление 2 ошибок.\n")

            # Для обеспечения исправления 2 ошибок, минимальное расстояние должно быть 5
            # Будем генерировать матрицу до тех пор, пока min_distance не достигнет нужного значения
            max_attempts = 10
            for attempt in range(max_attempts):
                # Генерируем порождающую матрицу G
                # Сначала создаем единичную матрицу k x k
                I_k = np.eye(self.k, dtype=int)

                # Затем создаем случайную матрицу k x (n-k)
                P = np.random.randint(0, 2, size=(self.k, self.n - self.k))

                # Объединяем их, чтобы получить G в систематической форме [I_k | P]
                self.G_matrix = np.hstack((I_k, P))

                # Генерируем проверочную матрицу H
                # Создаем матрицу P^T
                P_t = P.T

                # Создаем единичную матрицу (n-k) x (n-k)
                I_nk = np.eye(self.n - self.k, dtype=int)

                # Объединяем их, чтобы получить H в систематической форме [P^T | I_(n-k)]
                self.H_matrix = np.hstack((P_t, I_nk))

                # Определяем корректирующую способность кода
                min_d = self.calculate_min_distance()
                self.error_correction_capability = (min_d - 1) // 2

                # Проверяем, достигли ли мы требуемого минимального расстояния для исправления двух ошибок
                if self.error_correction_capability >= 2:
                    break

            # Обновляем информацию о корректирующей способности
            self.info_label.configure(
                text=f"Текущая корректирующая способность: {self.error_correction_capability} ошибок")

            # Формируем строковое представление матриц для более наглядного отображения
            G_str = "Порождающая матрица G:\n"
            H_str = "Проверочная матрица H:\n"

            # Форматируем матрицу G
            for row in self.G_matrix:
                G_str += ' '.join(map(str, row)) + '\n'

            # Форматируем матрицу H
            for row in self.H_matrix:
                H_str += ' '.join(map(str, row)) + '\n'

            # Вывод матриц в текстовое поле
            self.matrix_text.delete("1.0", "end")
            self.matrix_text.insert("1.0", G_str + "\n")
            self.matrix_text.insert("end", H_str)

            messagebox.showinfo("Успех", f"Матрицы блочного кода ({self.n}, {self.k}) успешно сгенерированы")

        except ValueError:
            messagebox.showerror("Ошибка", "Параметры должны быть целыми числами")

    def calculate_min_distance(self):
        """
        Вычисляет минимальное расстояние Хэмминга для кода
        """
        if self.k <= 15:
            all_messages = [format(i, f'0{self.k}b') for i in range(2 ** self.k)]
            codewords = []

            for msg in all_messages:
                msg_bits = np.array([int(bit) for bit in msg])
                codeword = np.remainder(np.dot(msg_bits, self.G_matrix), 2)
                codewords.append(codeword)

            min_weight = float('inf')
            for codeword in codewords:
                weight = np.sum(codeword)
                if 0 < weight < min_weight:
                    min_weight = weight

            return min_weight if min_weight != float('inf') else 0
        else:
            # Для больших k используем аппроксимацию
            return max(3, self.n - self.k)

    def encode_text(self):
        if self.G_matrix is None:
            messagebox.showerror("Ошибка", "Сначала сгенерируйте матрицу кода")
            return

        # Получаем текст из поля ввода
        input_text = self.input_text.get("1.0", "end-1c")
        if not input_text:
            messagebox.showerror("Ошибка", "Введите текст для кодирования")
            return

        # Преобразуем текст в двоичную последовательность
        binary_data = text_to_binary(input_text)

        # Выводим результат
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "Исходный текст:\n")
        self.result_text.insert("end", input_text + "\n\n")
        self.result_text.insert("end", "Бинарное представление:\n")
        self.result_text.insert("end", binary_data + "\n\n")

        # Показываем посимвольное кодирование для отладки
        self.result_text.insert("end", "Посимвольное бинарное представление:\n")
        for char in input_text:
            binary_char = format(ord(char), '08b')
            self.result_text.insert("end", f"{char} -> {binary_char}\n")
        self.result_text.insert("end", "\n")

        # Делим двоичную последовательность на блоки по k бит
        # Если длина последовательности не кратна k, дополняем нулями
        if len(binary_data) % self.k != 0:
            padding = self.k - (len(binary_data) % self.k)
            self.result_text.insert("end",
                                    f"Добавлено {padding} нулей для выравнивания до размера блока k={self.k}\n\n")
            binary_data += '0' * padding

        # Кодируем каждый блок
        encoded_data = ""
        self.result_text.insert("end", "Процесс кодирования по блокам:\n")

        for i in range(0, len(binary_data), self.k):
            block = binary_data[i:i + self.k]

            # Преобразуем блок в массив бит
            block_bits = np.array([int(bit) for bit in block])

            # Умножаем на порождающую матрицу по модулю 2
            codeword = np.remainder(np.dot(block_bits, self.G_matrix), 2)

            encoded_block = ''.join(map(str, codeword))
            encoded_data += encoded_block

            self.result_text.insert("end", f"Блок {i // self.k + 1}: {block} -> {encoded_block}\n")

        self.parent.encoded_text = encoded_data
        self.result_text.insert("end", "\nЗакодированные данные:\n")
        self.result_text.insert("end", encoded_data)

    def add_noise(self):
        if not self.parent.encoded_text:
            messagebox.showerror("Ошибка", "Сначала закодируйте текст")
            return False

        encoded_data = self.parent.encoded_text
        noisy_data = ""
        self.result_text.insert("end", "\n\nПроцесс внесения ошибок по блокам:\n")

        for i in range(0, len(encoded_data), self.n):
            block = encoded_data[i:i + self.n]
            if len(block) < self.n:
                block = block + '0' * (self.n - len(block))

            # Выбираем 2 разные случайные позиции для внесения ошибок
            # Для маленьких блоков уменьшаем количество ошибок до 1
            num_errors = 2 if len(block) >= 3 else 1
            error_positions = random.sample(range(len(block)), num_errors)

            # Вносим ошибки (инвертируем биты)
            block_list = list(block)
            for pos in error_positions:
                block_list[pos] = '1' if block_list[pos] == '0' else '0'

            noisy_block = ''.join(block_list)
            noisy_data += noisy_block

            # Выводим информацию о внесенных ошибках
            self.result_text.insert("end",
                                    f"Блок {i // self.n + 1}: {block} -> {noisy_block}, ошибки в позициях: {error_positions}\n")

        self.parent.noisy_text = noisy_data

        # Итоговый результат
        self.result_text.insert("end", "\nДанные с внесенными ошибками (обычно 2 ошибки на блок):\n")
        self.result_text.insert("end", noisy_data)

        return True

    def decode_text(self):
        if not self.parent.noisy_text:
            messagebox.showerror("Ошибка", "Сначала внесите ошибки в закодированный текст")
            return

        if self.H_matrix is None:
            messagebox.showerror("Ошибка", "Матрица кода не сгенерирована")
            return

        noisy_data = self.parent.noisy_text

        decoded_data = ""
        error_blocks = 0

        self.result_text.insert("end", "\n\nПроцесс декодирования по блокам:\n")

        for i in range(0, len(noisy_data), self.n):
            block = noisy_data[i:i + self.n]
            if len(block) < self.n:  # Если последний блок неполный, дополняем его нулями
                self.result_text.insert("end", f"Последний блок неполный, дополняем нулями: {block} -> ")
                block = block + '0' * (self.n - len(block))
                self.result_text.insert("end", f"{block}\n")

            received_vector = np.array([int(bit) for bit in block])
            syndrome = np.remainder(np.dot(received_vector, self.H_matrix.T), 2)
            syndrome_str = ''.join(map(str, syndrome))

            # Если синдром не нулевой, пытаемся исправить ошибки
            if np.any(syndrome):
                self.result_text.insert("end",
                                        f"Блок {i // self.n + 1}: {block}, синдром: {syndrome_str} - Обнаружена ошибка, ")

                error_syndromes = {}

                # Пытаемся исправить ошибки в зависимости от нашей корректирующей способности
                correctable = False
                error_pos = []

                for pos in range(self.n):
                    error_vector = np.zeros(self.n, dtype=int)
                    error_vector[pos] = 1
                    error_syndrome = np.remainder(np.dot(error_vector, self.H_matrix.T), 2)
                    error_syndromes[tuple(error_syndrome)] = (error_vector, [pos])

                if self.error_correction_capability >= 2:
                    for pos1 in range(self.n):
                        for pos2 in range(pos1 + 1, self.n):
                            error_vector = np.zeros(self.n, dtype=int)
                            error_vector[pos1] = 1
                            error_vector[pos2] = 1
                            error_syndrome = np.remainder(np.dot(error_vector, self.H_matrix.T), 2)
                            error_syndromes[tuple(error_syndrome)] = (error_vector, [pos1, pos2])

                # Если синдром соответствует одному из известных векторов ошибок
                if tuple(syndrome) in error_syndromes:
                    error_vector, error_pos = error_syndromes[tuple(syndrome)]
                    corrected_vector = np.remainder(received_vector + error_vector, 2)
                    correctable = True

                    self.result_text.insert("end", f"исправлены ошибки в позициях {error_pos}\n")
                else:
                    error_blocks += 1
                    corrected_vector = received_vector

                    self.result_text.insert("end", f"невозможно исправить\n")

                if self.k <= len(corrected_vector):
                    info_bits = corrected_vector[:self.k]
                else:
                    info_bits = corrected_vector
            else:
                # Если синдром нулевой
                self.result_text.insert("end",
                                        f"Блок {i // self.n + 1}: {block}, синдром: {syndrome_str} - Ошибок не обнаружено\n")

                if self.k <= len(received_vector):
                    info_bits = received_vector[:self.k]
                else:
                    info_bits = received_vector

            decoded_block = ''.join(map(str, info_bits))
            decoded_data += decoded_block

            info_bits_str = ''.join(map(str, info_bits))
            self.result_text.insert("end", f"Извлеченные информационные биты: {info_bits_str}\n")

        if error_blocks > 0:
            self.adapt_button.configure(state="normal")
        else:
            self.adapt_button.configure(state="disabled")

        # Сохраняем декодированные данные
        self.parent.decoded_text = decoded_data

        # Выводим результат
        self.result_text.insert("end", "\nДекодированные данные (информационные биты):\n")
        self.result_text.insert("end", decoded_data)

        # Сохраняем оригинальный двоичный текст перед кодированием
        # для сравнения с декодированным результатом
        original_binary = None
        try:
            input_text = self.input_text.get("1.0", "end-1c")
            if input_text:
                original_binary = text_to_binary(input_text)
                self.result_text.insert("end", f"\n\nОригинальный бинарный текст ({len(original_binary)} бит):\n")
                self.result_text.insert("end", original_binary)
        except:
            pass

        # Преобразуем двоичные данные обратно в текст
        try:
            # Обрезаем возможные лишние биты в конце для корректного преобразования
            # Если известна оригинальная длина бинарных данных, используем её
            if original_binary and len(original_binary) <= len(decoded_data):
                self.result_text.insert("end",
                                        f"\n\nОбрезаем декодированные данные до исходной длины: {len(decoded_data)} -> {len(original_binary)} бит\n")
                decoded_data = decoded_data[:len(original_binary)]

            # Строка должна быть кратна 8 для преобразования в ASCII
            padding = 8 - (len(decoded_data) % 8) if len(decoded_data) % 8 != 0 else 0
            if padding > 0:
                self.result_text.insert("end",
                                        f"Добавляем {padding} нулей в конец для выравнивания до размера байта (8 бит)\n")
                decoded_data = decoded_data + '0' * padding

            self.result_text.insert("end", f"\nДекодированные данные после корректировки ({len(decoded_data)} бит):\n")
            self.result_text.insert("end", decoded_data)

            # Анализируем полученный результат
            if original_binary and len(original_binary) <= len(decoded_data):
                # Сравниваем оригинальные данные с декодированными
                errors = sum(1 for a, b in zip(original_binary, decoded_data) if a != b)
                error_rate = errors / len(original_binary)
                self.result_text.insert("end",
                                        f"\n\nСравнение с исходными данными: {errors} ошибок из {len(original_binary)} бит ({error_rate:.2%} ошибок)\n")

            decoded_text = binary_to_text(decoded_data)
            self.result_text.insert("end", "\n\nДекодированный текст:\n")
            self.result_text.insert("end", decoded_text)

            # Проверяем корректирующую способность кода
            if self.error_correction_capability < 2:
                self.adapt_button.configure(state="normal")

            # Проверяем успешность декодирования, сравнивая с исходным текстом
            input_text = self.input_text.get("1.0", "end-1c")
            if input_text and input_text != decoded_text:
                messagebox.showwarning("Ошибка декодирования",
                                       f"Декодированный текст не совпадает с исходным.\n"
                                       f"Текущая корректирующая способность кода: {self.error_correction_capability} ошибок.\n"
                                       f"Рекомендуется адаптировать параметры кода для исправления ошибок.")
                self.adapt_button.configure(state="normal")
                return False

            return error_blocks == 0  # Возвращаем True, если все блоки декодированы успешно
        except Exception as e:
            self.result_text.insert("end", f"\n\nНе удалось преобразовать двоичные данные в текст: {str(e)}")
            return False

    def adapt_code(self):
        # Увеличиваем параметры кода для исправления большего числа ошибок
        old_n = self.n
        old_k = self.k

        # Необходимое количество проверочных бит для исправления 2 ошибок
        # По формуле 2^(n-k) >= n+1
        # Увеличиваем n при сохранении k (уменьшаем скорость кода R = k/n)
        while 2 ** (self.n - self.k) < self.n + 1:
            self.n += 1

        # Для надежности добавляем еще немного избыточности
        self.n += 1

        # Обновляем поля ввода
        self.n_entry.delete(0, "end")
        self.n_entry.insert(0, str(self.n))

        self.result_text.insert("end",
                                f"\n\nАдаптация кода: параметры изменены с ({old_n}, {old_k}) на ({self.n}, {self.k})\n")

        # Получаем исходный текст из поля ввода для повторного кодирования
        input_text = self.input_text.get("1.0", "end-1c")
        if not input_text:
            messagebox.showerror("Ошибка", "Отсутствует исходный текст для адаптации")
            return

        # Пытаемся генерировать матрицу с требуемой корректирующей способностью
        max_attempts = 10
        success = False

        for attempt in range(max_attempts):
            I_k = np.eye(self.k, dtype=int)

            # Затем создаем случайную матрицу k x (n-k)
            P = np.random.randint(0, 2, size=(self.k, self.n - self.k))

            # Объединяем их, чтобы получить G в систематической форме [I_k | P]
            self.G_matrix = np.hstack((I_k, P))

            P_t = P.T

            # Создаем единичную матрицу (n-k) x (n-k)
            I_nk = np.eye(self.n - self.k, dtype=int)

            # Объединяем их, чтобы получить H в систематической форме [P^T | I_(n-k)]
            self.H_matrix = np.hstack((P_t, I_nk))

            # Определяем корректирующую способность кода
            min_d = self.calculate_min_distance()
            self.error_correction_capability = (min_d - 1) // 2

            # Проверяем, достигли ли мы требуемой корректирующей способности
            if self.error_correction_capability >= 2:
                success = True
                break

        if not success:
            old_n = self.n
            self.n += 2
            self.n_entry.delete(0, "end")
            self.n_entry.insert(0, str(self.n))

            self.result_text.insert("end",
                                    f"Не удалось создать код с корректирующей способностью 2, увеличиваем n до {self.n}\n")

            # Повторно генерируем матрицу
            self.generate_matrix()

        # Обновляем информацию о корректирующей способности
        self.info_label.configure(text=f"Текущая корректирующая способность: {self.error_correction_capability} ошибок")

        # Выводим матрицы в текстовое поле
        self.matrix_text.delete("1.0", "end")

        # Форматируем и выводим порождающую матрицу G
        G_str = "Порождающая матрица G:\n"
        for row in self.G_matrix:
            G_str += ' '.join(map(str, row)) + '\n'

        # Форматируем и выводим проверочную матрицу H
        H_str = "\nПроверочная матрица H:\n"
        for row in self.H_matrix:
            H_str += ' '.join(map(str, row)) + '\n'

        # Выводим обе матрицы в интерфейс
        self.matrix_text.insert("1.0", G_str + H_str)

        messagebox.showinfo("Адаптация",
                            f"Код адаптирован для исправления 2 ошибок.\nПараметры изменены с ({old_n}, {old_k}) на ({self.n}, {self.k}).")
        self.encode_text()
        self.add_noise()
        success = self.decode_text()

        if not success and self.n < 20:  # Ограничиваем n, чтобы избежать бесконечного цикла
            self.result_text.insert("end", "\n\nДекодирование после адаптации не успешно. Повторяем адаптацию...\n")
            self.adapt_code()  # Рекурсивно пытаемся адаптировать код дальше
            return
