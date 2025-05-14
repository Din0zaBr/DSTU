import customtkinter as ctk
import numpy as np
import random
from tkinter import messagebox
from helpers import text_to_binary, binary_to_text


class ConvolutionalCodeModule:
    CHANNEL_INFO = {
        "ДСК": {
            "name": "Двоичный симметричный канал (ДСК)",
            "characteristics": [
                "Ошибки 0<->1 с вероятностью p",
                "Симметричный канал",
                "C = 1 + p*log2(p) + (1-p)*log2(1-p)"
            ],
            "diagram": [
                "  0 --p--> 1",
                "  1 --p--> 0"
            ],
            "recommendations": [
                "Симметричные полиномы"
            ]
        },
        "ДСКС": {
            "name": "Двоичный симметричный канал со стираниями (ДСКС)",
            "characteristics": [
                "Ошибки 0<->1 с p, стирания с q",
                "C = 1 - q + (1-p-q)*log2((1-p-q)/(1-q)) + p*log2(p/(1-q))"
            ],
            "diagram": [
                "  0 --p--> 1",
                "  0 --q--> e",
                "  1 --p--> 0",
                "  1 --q--> e"
            ],
            "recommendations": [
                "Больше полиномов при больших q",
                "Стирания проще исправлять"
            ]
        },
        "Z-канал": {
            "name": "Z-канал (асимметричный)",
            "characteristics": [
                "1->0 с вероятностью p, 0 не искажается",
                "C = log2(1 + (1-p)*p^(p/(1-p)))"
            ],
            "diagram": [
                "  1 --p--> 0",
                "  0 --1--> 0"
            ],
            "recommendations": [
            ]
        }
    }

    GENERAL_INFO = [
        "Сверточные коды эффективны при последовательной передаче данных",
        "Длина ограничения определяет память кода и сложность декодирования",
        "Количество полиномов влияет на скорость кода и его избыточность",
        "Скорость кода R = 1/n, где n - количество полиномов",
        "Для надежной передачи скорость кода должна быть меньше пропускной способности канала"
    ]

    INITIAL_STEPS = [
        "Введите исходный текст или загрузите его из файла",
        "Настройте параметры кода (длина ограничения, количество и значения полиномов)",
        "Нажмите 'Кодировать' для получения сверточного кода"
    ]

    def __init__(self, parent):
        self.parent = parent
        self.constraint_length = 3
        self.rate = 1 / 2
        self.generator_polynomials = ["111", "101"]
        self.num_polynomials = 2
        self.registers = None
        self.error_probability = 0.05
        self.erasure_probability = 0.03
        self.channel_type = "ДСК"

    def create_widgets(self, parent_frame):
        # Создание основного фрейма
        self.main_frame = ctk.CTkFrame(parent_frame)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Создаем вкладки
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Добавляем вкладки
        self.tabview.add("Кодирование")
        self.tabview.add("Канал")
        self.tabview.add("Декодирование")
        self.tabview.add("Анализ")

        # === Вкладка Кодирование ===
        encode_frame = self.tabview.tab("Кодирование")
        
        # Карточка с параметрами кода
        code_params_card = ctk.CTkFrame(encode_frame)
        code_params_card.pack(fill="x", padx=10, pady=5)
        
        # Заголовок карточки
        ctk.CTkLabel(code_params_card, text="Параметры сверточного кода",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(padx=10, pady=5)

        # Сетка параметров
        params_grid = ctk.CTkFrame(code_params_card)
        params_grid.pack(fill="x", padx=10, pady=5)

        # Длина ограничения
        ctk.CTkLabel(params_grid, text="Длина ограничения:").grid(row=0, column=0, padx=5, pady=5)
        self.constraint_entry = ctk.CTkEntry(params_grid, width=60)
        self.constraint_entry.grid(row=0, column=1, padx=5, pady=5)
        self.constraint_entry.insert(0, str(self.constraint_length))
        
        ctk.CTkButton(params_grid, text="Обновить",
                     command=self.update_constraint_length).grid(row=0, column=2, padx=5, pady=5)

        # Количество полиномов
        ctk.CTkLabel(params_grid, text="Количество полиномов:").grid(row=1, column=0, padx=5, pady=5)
        self.num_poly_entry = ctk.CTkEntry(params_grid, width=60)
        self.num_poly_entry.grid(row=1, column=1, padx=5, pady=5)
        self.num_poly_entry.insert(0, str(self.num_polynomials))
        
        ctk.CTkButton(params_grid, text="Обновить",
                     command=self.update_polynomials_count).grid(row=1, column=2, padx=5, pady=5)

        # Карточка с полиномами
        poly_card = ctk.CTkFrame(encode_frame)
        poly_card.pack(fill="x", padx=10, pady=5)
        
        # Заголовок и кнопка редактирования
        poly_header = ctk.CTkFrame(poly_card)
        poly_header.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(poly_header, text="Полиномы генератора",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(side="left", padx=5)
        
        ctk.CTkButton(poly_header, text="Редактировать",
                     command=self.open_polynomials_window).pack(side="right", padx=5)

        # Сводка полиномов
        self.poly_summary = ctk.CTkTextbox(poly_card, height=60)
        self.poly_summary.pack(fill="x", padx=10, pady=5)
        self.update_polynomials_summary()

        # Карточка ввода текста
        input_card = ctk.CTkFrame(encode_frame)
        input_card.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(input_card, text="Исходный текст",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(padx=10, pady=5)
        
        self.input_text = ctk.CTkTextbox(input_card, height=100)
        self.input_text.pack(fill="x", padx=10, pady=5)
        
        # Кнопки управления текстом
        input_buttons = ctk.CTkFrame(input_card)
        input_buttons.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(input_buttons, text="Загрузить из файла",
                     command=self.load_text).pack(side="left", padx=5)
        
        ctk.CTkButton(input_buttons, text="Очистить",
                     command=lambda: self.input_text.delete("1.0", "end")).pack(side="left", padx=5)
        
        ctk.CTkButton(input_buttons, text="Кодировать",
                     command=self.encode_text).pack(side="right", padx=5)

        # === Вкладка Канал ===
        channel_frame = self.tabview.tab("Канал")
        
        # Карточка параметров канала
        channel_params_card = ctk.CTkFrame(channel_frame)
        channel_params_card.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(channel_params_card, text="Параметры канала",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(padx=10, pady=5)

        # Тип канала
        channel_type_frame = ctk.CTkFrame(channel_params_card)
        channel_type_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(channel_type_frame, text="Тип канала:").pack(side="left", padx=5)
        
        self.channel_type_var = ctk.StringVar(value=self.channel_type)
        self.channel_type_combo = ctk.CTkComboBox(channel_type_frame,
                                                 values=["ДСК", "ДСКС", "Z-канал"],
                                                 variable=self.channel_type_var,
                                                 command=self.on_channel_changed)
        self.channel_type_combo.pack(side="left", padx=5)

        # Вероятности
        prob_frame = ctk.CTkFrame(channel_params_card)
        prob_frame.pack(fill="x", padx=10, pady=5)
        
        # Вероятность ошибки
        ctk.CTkLabel(prob_frame, text="Вероятность ошибки (p):").grid(row=0, column=0, padx=5, pady=5)
        self.error_entry = ctk.CTkEntry(prob_frame, width=60)
        self.error_entry.grid(row=0, column=1, padx=5, pady=5)
        self.error_entry.insert(0, str(self.error_probability))

        # Вероятность стирания
        ctk.CTkLabel(prob_frame, text="Вероятность стирания (q):").grid(row=1, column=0, padx=5, pady=5)
        self.erasure_entry = ctk.CTkEntry(prob_frame, width=60)
        self.erasure_entry.grid(row=1, column=1, padx=5, pady=5)
        self.erasure_entry.insert(0, str(self.erasure_probability))

        # Кнопка внесения ошибок
        ctk.CTkButton(channel_params_card, text="Внести ошибки/стирания",
                     command=self.add_noise).pack(padx=10, pady=10)

        # === Вкладка Декодирование ===
        decode_frame = self.tabview.tab("Декодирование")
        
        # Карточка декодирования
        decode_card = ctk.CTkFrame(decode_frame)
        decode_card.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(decode_card, text="Декодирование",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(padx=10, pady=5)
        
        ctk.CTkButton(decode_card, text="Декодировать",
                     command=self.decode_text).pack(padx=10, pady=10)

        # === Вкладка Анализ ===
        analysis_frame = self.tabview.tab("Анализ")
        
        # Карточка анализа
        analysis_card = ctk.CTkFrame(analysis_frame)
        analysis_card.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(analysis_card, text="Анализ канала",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(padx=10, pady=5)
        
        ctk.CTkButton(analysis_card, text="Рассчитать пропускную способность",
                     command=self.calculate_capacity).pack(padx=10, pady=10)

        # === Общее текстовое поле для результатов ===
        self.result_text = ctk.CTkTextbox(self.main_frame, height=200)
        self.result_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Настройка интерфейса в зависимости от типа канала
        self.on_channel_changed(self.channel_type)

    def create_polynomial_entries(self):
        # Очищаем существующие поля ввода
        for entry in self.poly_entries:
            entry.destroy()
        self.poly_entries = []

        # Удаляем предыдущий контейнер, если он существует
        for widget in self.poly_frame.winfo_children():
            widget.destroy()

        # Если полиномов слишком много, используем компактный режим отображения
        compact_mode = self.num_polynomials > 8

        # Добавляем информационную строку
        info_text = f"Всего полиномов: {self.num_polynomials}, длина полинома: {self.constraint_length} бит"
        info_label = ctk.CTkLabel(self.poly_frame, text=info_text, font=ctk.CTkFont(size=10))
        info_label.pack(fill="x", padx=10, pady=(5, 0), anchor="w")

        # Создаем компактный контейнер с прокруткой и ограниченной высотой
        container_height = 90 if compact_mode else 100
        poly_container = ctk.CTkScrollableFrame(self.poly_frame, height=container_height)
        poly_container.pack(fill="x", padx=10, pady=2)

        # Определяем оптимальное количество полиномов в строке в зависимости от их количества
        if compact_mode:
            polynomials_per_row = 5  # Очень компактное отображение при большом количестве
        elif self.num_polynomials <= 3:
            polynomials_per_row = self.num_polynomials
        elif self.num_polynomials <= 6:
            polynomials_per_row = 3
        else:
            polynomials_per_row = 4

        # Создаем сетку для размещения полиномов
        row_frames = []

        # Создаем фреймы для каждой строки
        row_count = (self.num_polynomials + polynomials_per_row - 1) // polynomials_per_row
        for i in range(row_count):
            row_frame = ctk.CTkFrame(poly_container)
            row_frame.pack(fill="x", padx=2, pady=2)
            row_frames.append(row_frame)

        # Заполняем строки полиномами
        for i in range(self.num_polynomials):
            row_index = i // polynomials_per_row
            col_index = i % polynomials_per_row

            # Создаем компактный фрейм для каждого полинома
            poly_entry_frame = ctk.CTkFrame(row_frames[row_index])
            poly_entry_frame.grid(row=0, column=col_index, padx=2, pady=2, sticky="w")

            # Максимально компактная метка
            label_width = 20 if compact_mode else 25
            font_size = 9 if compact_mode else 10
            poly_label = ctk.CTkLabel(poly_entry_frame, text=f"П{i + 1}:", width=label_width,
                                      font=ctk.CTkFont(size=font_size))
            poly_label.pack(side="left", padx=1)

            # Компактное поле ввода с шириной в зависимости от количества полиномов
            if compact_mode:
                entry_width = 70
            elif polynomials_per_row <= 3:
                entry_width = 120
            else:
                entry_width = 90

            poly_entry = ctk.CTkEntry(poly_entry_frame, width=entry_width, font=ctk.CTkFont(size=font_size + 1))
            poly_entry.pack(side="left", padx=1)

            # Заполняем поле существующим значением из списка полиномов
            if i < len(self.generator_polynomials):
                poly_entry.insert(0, self.generator_polynomials[i])

            self.poly_entries.append(poly_entry)

        # Добавляем нижнюю панель управления с кнопками
        controls_frame = ctk.CTkFrame(self.poly_frame)
        controls_frame.pack(fill="x", padx=10, pady=5)


        # Если есть рекомендуемые полиномы, добавляем кнопку их применения
        if self.constraint_length <= 5:
            suggestions = self.get_polynomial_suggestions(self.constraint_length)
            if suggestions and len(suggestions) > 0:
                apply_button = ctk.CTkButton(controls_frame, text="Применить рекомендуемые",
                                             width=160, height=25,
                                             command=lambda: self._apply_recommended_polynomials(suggestions))
                apply_button.pack(side="left", padx=5)

        # Добавляем кнопку применения для всех полиномов одинакового значения
        if self.num_polynomials > 2:
            same_poly_button = ctk.CTkButton(controls_frame, text="Одинаковые полиномы",
                                             width=140, height=25,
                                             command=self._apply_same_polynomial)
            same_poly_button.pack(side="left", padx=5)

    def _apply_recommended_polynomials(self, suggestions):
        """Применяет рекомендуемые полиномы"""
        # Используем только необходимое количество полиномов
        recommended = suggestions[:self.num_polynomials]

        # Если рекомендаций меньше, чем нужно полиномов, дублируем их
        while len(recommended) < self.num_polynomials:
            recommended.append(suggestions[0])

        # Обновляем список полиномов
        self.generator_polynomials = recommended.copy()

        # Получаем числовое представление полиномов
        numeric_polys = self.binary_polys_to_numeric()

        # Выводим информацию
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "Применены рекомендуемые полиномы:\n")
        for i, poly in enumerate(recommended):
            self.result_text.insert("end", f"Полином {i + 1}: {poly} (двоичный) / {numeric_polys[i]} (индексы)\n")

        # Обновляем сводку полиномов
        self.update_polynomials_summary()

    def _apply_same_polynomial(self):
        """Применяет первый полином ко всем полиномам"""
        if not self.generator_polynomials or len(self.generator_polynomials) == 0:
            messagebox.showerror("Ошибка", "Нет доступных полиномов")
            return

        # Берем первый полином и применяем его ко всем остальным
        first_poly = self.generator_polynomials[0]
        self.generator_polynomials = [first_poly] * self.num_polynomials

        # Получаем числовое представление полиномов
        numeric_polys = self.binary_polys_to_numeric()

        # Выводим информацию
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "Применен одинаковый полином ко всем позициям:\n")
        for i, poly in enumerate(self.generator_polynomials):
            self.result_text.insert("end", f"Полином {i + 1}: {poly} (двоичный) / {numeric_polys[i]} (индексы)\n")

        # Обновляем сводку полиномов
        self.update_polynomials_summary()

    def get_polynomial_suggestions(self, constraint_length):
        """Возвращает список эффективных полиномов для заданной длины ограничения"""
        # Словарь эффективных полиномов для разных длин ограничения
        # Источник: учебные материалы по теории кодирования
        suggestions = {
            2: ["11"],
            3: ["111", "101"],
            4: ["1111", "1101", "1011"],
            5: ["11111", "10101", "11001", "10011"]
        }

        return suggestions.get(constraint_length, [])

    def update_polynomials_count(self):
        try:
            # Получаем новое количество полиномов
            new_count = int(self.num_poly_entry.get())
            if new_count < 1:
                messagebox.showerror("Ошибка", "Количество полиномов должно быть не менее 1")
                return

            # Ограничение на максимальное количество полиномов для удобства использования
            if new_count > 10:
                response = messagebox.askquestion("Предупреждение",
                                                  f"Вы выбрали {new_count} полиномов. Большое количество полиномов может снизить скорость кода и усложнить интерфейс. Продолжить?")
                if response != 'yes':
                    return

            # Обновляем количество полиномов
            self.num_polynomials = new_count

            # Получаем текущую длину ограничения
            try:
                constraint_length = int(self.constraint_entry.get())
                if constraint_length < 2:
                    constraint_length = 3  # Устанавливаем значение по умолчанию
                    self.constraint_entry.delete(0, "end")
                    self.constraint_entry.insert(0, str(constraint_length))
                    self.constraint_length = constraint_length
            except ValueError:
                constraint_length = 3  # Устанавливаем значение по умолчанию
                self.constraint_entry.delete(0, "end")
                self.constraint_entry.insert(0, str(constraint_length))
                self.constraint_length = constraint_length

            # Создаем новые полиномы по умолчанию, полностью удаляя предыдущие
            self.generator_polynomials = []
            for i in range(new_count):
                # Создаем полином по умолчанию с соответствующей длиной ограничения
                # Используем шаблон 1...1 (первый и последний бит = 1)
                default_poly = '1' + '0' * (constraint_length - 2) + '1'
                self.generator_polynomials.append(default_poly)

            # Обновляем скорость кода
            self.rate = 1 / self.num_polynomials

            # Обновляем заголовок с информацией о количестве полиномов
            self.poly_label.configure(text=f"Полиномы генератора ({self.num_polynomials}):")

            # Обновляем сводку о полиномах
            self.update_polynomials_summary()

            # Очищаем текстовое поле для результатов
            self.result_text.delete("1.0", "end")

            # Обновляем информацию
            self.result_text.insert("1.0", "=== Обновление параметров сверточного кода ===\n")
            self.result_text.insert("end", f"Количество полиномов обновлено: {self.num_polynomials}\n")
            self.result_text.insert("end", f"Длина ограничения: {self.constraint_length}\n")
            self.result_text.insert("end", f"Скорость кода: 1/{self.num_polynomials}\n")
            self.result_text.insert("end", f"Предыдущие полиномы удалены, созданы новые полиномы по умолчанию.\n")

            # Выводим информацию о полиномах
            self.result_text.insert("end", "\nНовые полиномы генератора:\n")
            for i, poly in enumerate(self.generator_polynomials):
                self.result_text.insert("end", f"Полином {i + 1}: {poly}\n")

            # Информация о влиянии скорости кода на кодирование
            self.result_text.insert("end", f"\nВлияние скорости кода на кодирование:\n")
            self.result_text.insert("end",
                                    f"- Скорость 1/{self.num_polynomials} означает, что каждый исходный бит преобразуется в {self.num_polynomials} кодовых битов\n")
            self.result_text.insert("end",
                                    f"- Более низкая скорость (больше полиномов) повышает избыточность и помехоустойчивость кода\n")
            self.result_text.insert("end",
                                    f"- Более высокая скорость (меньше полиномов) снижает избыточность, но ухудшает помехоустойчивость\n")

            # Проверяем полиномы для безопасности
            self._validate_polynomials()

        except ValueError:
            messagebox.showerror("Ошибка", "Количество полиномов должно быть целым числом")

    def on_channel_changed(self, channel_type):
        """Обработка изменения типа канала"""
        self.channel_type = channel_type
        self._update_erasure_field()
        self._update_error_field()
        self._display_channel_info()

    def _update_erasure_field(self):
        """Обновление поля вероятности стирания"""
        if self.channel_type == "ДСКС":
            self.erasure_entry.configure(state="normal")
        else:
            self.erasure_entry.configure(state="disabled")
            self.erasure_entry.delete(0, "end")
            self.erasure_entry.insert(0, "0")
            self.erasure_probability = 0

    def _update_error_field(self):
        """Обновление поля вероятности ошибки"""
        if not self.error_entry.get():
            self.error_entry.delete(0, "end")
            self.error_entry.insert(0, str(self.error_probability))

    def _display_channel_info(self):
        """Отображение информации о канале"""
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", f"=== Выбран канал: {self.channel_type} ===\n\n")

        info = self.CHANNEL_INFO[self.channel_type]
        
        # Вывод основной информации о канале
        self.result_text.insert("end", f"{info['name']}\n\n")
        
        # Характеристики
        self._insert_section("Характеристики:", info['characteristics'])
        
        # Схема канала
        self.result_text.insert("end", "Схема канала:\n")
        for line in info['diagram']:
            self.result_text.insert("end", f"{line}\n")
        self.result_text.insert("end", "\n")
        
        # Рекомендации
        self._insert_section("Рекомендации для кодирования:", info['recommendations'])
        
        # Общая информация
        self._insert_section("=== Общая информация о сверточных кодах ===", self.GENERAL_INFO)
        
        # Шаги
        self.result_text.insert("end", "\nДля начала работы:\n")
        for i, step in enumerate(self.INITIAL_STEPS, 1):
            self.result_text.insert("end", f"{i}. {step}\n")

    def _insert_section(self, title, items):
        """Вспомогательный метод для вставки секции с заголовком и списком"""
        self.result_text.insert("end", f"{title}\n")
        for item in items:
            self.result_text.insert("end", f"- {item}\n")
        self.result_text.insert("end", "\n")

    def load_text(self):
        text = self.parent.load_text_from_file()
        if text:
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", text)

    def encode_text(self):
        # Получаем входной текст
        input_text = self.input_text.get("1.0", "end").strip()
        if not input_text:
            messagebox.showerror("Ошибка", "Введите текст для кодирования")
            return

        # Очищаем результаты
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "=== Сверточное кодирование ===\n")

        try:
            # Проверяем параметры
            if not self._validate_polynomials():
                messagebox.showerror("Ошибка", "Некорректные полиномы генератора")
                return

            # Проверяем длину ограничения
            try:
                self.constraint_length = int(self.constraint_entry.get())
                if self.constraint_length < 2:
                    messagebox.showerror("Ошибка", "Длина ограничения должна быть не менее 2")
                    return
            except ValueError:
                messagebox.showerror("Ошибка", "Длина ограничения должна быть целым числом")
                return

            # Проверяем, что полиномы соответствуют длине ограничения
            for poly in self.generator_polynomials:
                if len(poly) != self.constraint_length:
                    messagebox.showerror("Ошибка",
                                         f"Длина полинома {poly} не соответствует длине ограничения ({self.constraint_length})")
                    return
                if not all(bit in '01' for bit in poly):
                    messagebox.showerror("Ошибка", f"Полином {poly} должен состоять только из 0 и 1")
                    return

            # Преобразуем текст в двоичное представление
            binary_data = text_to_binary(input_text)
            if not binary_data:
                messagebox.showerror("Ошибка", "Не удалось преобразовать текст в двоичный код")
                return

            # Выводим базовую информацию о кодировании
            self.result_text.insert("end", f"Тип канала: {self.channel_type}\n")
            self.result_text.insert("end", f"Длина ограничения: {self.constraint_length}\n")
            self.result_text.insert("end", f"Количество полиномов: {len(self.generator_polynomials)}\n")

            # Рассчитываем и отображаем скорость кода
            code_rate = 1 / len(self.generator_polynomials)
            self.result_text.insert("end",
                                    f"Скорость кода: R = 1/{len(self.generator_polynomials)} = {code_rate:.4f}\n")

            # Получаем параметры канала
            p = float(self.error_entry.get())
            if self.channel_type == "ДСКС":
                q = float(self.erasure_entry.get())
            else:
                q = 0

            # Расчёт пропускной способности через новую функцию
            channel_capacity = self.get_channel_capacity(p, q, self.channel_type)

            # Сравнение скорости кода и пропускной способности
            self.result_text.insert("end", f"\nАнализ кода для канала {self.channel_type}:\n")
            self.result_text.insert("end", f"- Пропускная способность канала: C ≈ {channel_capacity:.4f} бит/символ\n")

            if code_rate <= channel_capacity:
                self.result_text.insert("end", f"✅ Скорость кода ({code_rate:.4f}) не превышает пропускную способность ({channel_capacity:.4f})\n")
                self.result_text.insert("end", "   Согласно теореме Шеннона, возможно построение кода с произвольно малой вероятностью ошибки\n")
            else:
                self.result_text.insert("end", f"⚠️ Скорость кода ({code_rate:.4f}) превышает пропускную способность ({channel_capacity:.4f})\n")
                self.result_text.insert("end", "   Согласно теореме Шеннона, надежная передача невозможна\n")

                # Рекомендации по улучшению
                required_polys = max(2, int(np.ceil(1 / channel_capacity)))
                if required_polys > len(self.generator_polynomials):
                    self.result_text.insert("end", f"   Рекомендуется использовать не менее {required_polys} полиномов для надежной передачи\n")

            # Кодируем данные
            encoded_data = self.convolutional_encode(binary_data)

            # Сохраняем закодированные данные
            self.parent.input_text = input_text
            self.parent.encoded_text = encoded_data

            # Базовая статистика кодирования
            input_bits = len(binary_data)
            output_bits = len(encoded_data)
            redundancy_ratio = (output_bits - input_bits) / input_bits if input_bits > 0 else 0

            self.result_text.insert("end", f"\nСтатистика кодирования:\n")
            self.result_text.insert("end", f"- Длина исходных данных: {input_bits} бит\n")
            self.result_text.insert("end", f"- Длина закодированных данных: {output_bits} бит\n")
            self.result_text.insert("end",
                                    f"- Избыточность кода: {redundancy_ratio:.2f} ({redundancy_ratio * 100:.0f}%)\n")

            # Анализ влияния кода на защиту от ошибок
            error_correction_level = "Низкая"
            if len(self.generator_polynomials) >= 3 and self.constraint_length >= 4:
                error_correction_level = "Высокая"
            elif len(self.generator_polynomials) >= 2 and self.constraint_length >= 3:
                error_correction_level = "Средняя"

            self.result_text.insert("end", f"- Способность исправления ошибок: {error_correction_level}\n")

            # Выводим часть закодированных данных
            if len(encoded_data) > 100:
                self.result_text.insert("end", "\nПервые 50 символов закодированных данных:\n")
                self.result_text.insert("end", encoded_data[:50] + "\n")
                self.result_text.insert("end", "Последние 50 символов закодированных данных:\n")
                self.result_text.insert("end", encoded_data[-50:] + "\n")
            else:
                self.result_text.insert("end", "\nЗакодированные данные:\n")
                self.result_text.insert("end", encoded_data + "\n")

            # Рекомендации в зависимости от типа канала
            self.result_text.insert("end", f"\nРекомендации для канала {self.channel_type}:\n")

            if self.channel_type == "ДСК":
                self.result_text.insert("end", "- ДСК хорошо работает с симметричными кодами\n")
                self.result_text.insert("end",
                                        "- Увеличение количества полиномов улучшает корректирующую способность кода\n")
            elif self.channel_type == "ДСКС":
                self.result_text.insert("end",
                                        "- В ДСКС стирания лучше обрабатываются, чем ошибки, так как известны позиции стираний\n")
                self.result_text.insert("end", "- Рекомендуется использовать коды с большим расстоянием Хэмминга\n")
            elif self.channel_type == "Z-канал":
                self.result_text.insert("end",
                                        "- Z-канал имеет асимметричные ошибки (только 1->0), это можно использовать для оптимизации\n")
                self.result_text.insert("end",
                                        "- Полиномы с большим количеством единиц помогают лучше защититься от ошибок типа 1->0\n")

            # Следующий шаг
            self.result_text.insert("end",
                                    "\n✓ Кодирование успешно завершено. Теперь вы можете нажать 'Внести ошибки/стирания' для моделирования канала.\n")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при кодировании: {str(e)}")

    def convolutional_encode(self, binary_data):
        """Сверточное кодирование по алгоритму из второй лабораторной работы"""
        # Преобразуем полиномы генератора в числовой формат для алгоритма из второй лабы
        numeric_polynomials = self.binary_polys_to_numeric()

        # Добавляем обработку начального и конечного состояний для улучшения кодирования
        # Добавляем constraint_length-1 нулей в конец для очистки регистров
        padded_data = binary_data + '0' * (self.constraint_length - 1)

        # Сохраняем текущее содержимое результатов
        current_results = self.result_text.get("1.0", "end")

        # Добавляем вывод информации о кодировании
        self.result_text.insert("end", "\n=== Детали сверточного кодирования ===\n")
        self.result_text.insert("end", f"Количество полиномов: {len(numeric_polynomials)}\n")
        for i, poly in enumerate(numeric_polynomials):
            self.result_text.insert("end", f"Полином {i + 1}: {poly} (индексы регистров)\n")

        encoded_data = ""
        max_register = max(max(p) for p in numeric_polynomials)
        registers = [0] * (max_register + 1)

        self.result_text.insert("end", "\nПример кодирования первых нескольких битов:\n")

        # Покажем пример кодирования первых нескольких битов для наглядности
        example_bits = min(8, len(padded_data))

        # Создаем таблицу для отображения процесса кодирования
        self.result_text.insert("end", "Бит | Регистр | Выходные биты\n")
        self.result_text.insert("end", "-" * 40 + "\n")

        for i, bit in enumerate(padded_data):
            # Сдвигаем регистр и добавляем новый бит
            registers.insert(0, int(bit))
            registers.pop()

            # Выходные биты для этого входного бита
            output_bits = []

            # Вычисляем выходные биты для каждого полинома
            for poly in numeric_polynomials:
                xor = 0
                for idx in poly:
                    xor ^= registers[idx]
                output_bits.append(str(xor))
                encoded_data += str(xor)

            # Показываем пример для первых нескольких битов
            if i < example_bits:
                reg_str = ''.join(str(r) for r in registers[:max_register + 1])
                out_str = ''.join(output_bits)
                self.result_text.insert("end", f" {bit}  | {reg_str} | {out_str}\n")

        return encoded_data

    def binary_polys_to_numeric(self):
        """Преобразует полиномы из двоичного формата в числовой формат индексов"""
        numeric_polynomials = []
        for poly in self.generator_polynomials:
            indices = [i for i, bit in enumerate(poly) if bit == '1']
            numeric_polynomials.append(indices)
        return numeric_polynomials

    def numeric_poly_to_binary(self, numeric_poly, length):
        """Преобразует полином из числового формата индексов в двоичный формат"""
        binary_poly = ['0'] * length
        for idx in numeric_poly:
            if 0 <= idx < length:
                binary_poly[idx] = '1'
        return ''.join(binary_poly)

    def add_noise(self):
        if not self.parent.encoded_text:
            messagebox.showerror("Ошибка", "Сначала закодируйте текст")
            return

        try:
            # Получаем параметры канала
            try:
                self.error_probability = float(self.error_entry.get())
            except ValueError:
                # Устанавливаем значение по умолчанию
                self.error_probability = 0.05
                self.error_entry.delete(0, "end")
                self.error_entry.insert(0, str(self.error_probability))

            if self.channel_type == "ДСКС":
                try:
                    self.erasure_probability = float(self.erasure_entry.get())
                except ValueError:
                    # Устанавливаем значение по умолчанию
                    self.erasure_probability = 0.03
                    self.erasure_entry.delete(0, "end")
                    self.erasure_entry.insert(0, str(self.erasure_probability))
            else:
                self.erasure_probability = 0
                self.erasure_entry.delete(0, "end")
                self.erasure_entry.insert(0, "0")

            # Проверка корректности вероятностей
            if self.error_probability < 0 or self.error_probability > 1:
                messagebox.showerror("Ошибка", "Вероятность ошибки должна быть в диапазоне [0, 1]")
                return

            if self.erasure_probability < 0 or self.erasure_probability > 1:
                messagebox.showerror("Ошибка", "Вероятность стирания должна быть в диапазоне [0, 1]")
                return

            if self.error_probability + self.erasure_probability > 1:
                messagebox.showerror("Ошибка", "Сумма вероятностей ошибки и стирания не может превышать 1")
                return

            # Получаем закодированные данные
            encoded_data = self.parent.encoded_text

            noisy_data = ""
            error_count = 0
            erasure_count = 0
            bits_processed = 0

            zero_to_one_count = 0
            one_to_zero_count = 0
            zeros_count = 0
            ones_count = 0

            # Детальная статистика для Z-канала
            z_channel_error_count = 0
            z_channel_ones_count = 0

            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", "=== Моделирование канала связи ===\n")
            self.result_text.insert("end", f"Тип канала: {self.channel_type}\n")
            self.result_text.insert("end", f"Параметры канала:\n")
            self.result_text.insert("end", f"- Вероятность ошибки (p): {self.error_probability}\n")

            if self.channel_type == "ДСКС":
                self.result_text.insert("end", f"- Вероятность стирания (q): {self.erasure_probability}\n")

            for bit in encoded_data:
                bits_processed += 1
                r = random.random()

                if bit == '0':
                    zeros_count += 1
                elif bit == '1':
                    ones_count += 1
                    if self.channel_type == "Z-канал":
                        z_channel_ones_count += 1

                if self.channel_type == "ДСК":
                    # ДСК
                    if r < self.error_probability:
                        new_bit = '1' if bit == '0' else '0'
                        noisy_data += new_bit
                        error_count += 1

                        # ошибки
                        if bit == '0':
                            zero_to_one_count += 1
                        else:
                            one_to_zero_count += 1
                    else:
                        noisy_data += bit

                elif self.channel_type == "ДСКС":
                    # ДСКС
                    if r < self.error_probability:
                        new_bit = '1' if bit == '0' else '0'
                        noisy_data += new_bit
                        error_count += 1

                        # Подсчет типов ошибок
                        if bit == '0':
                            zero_to_one_count += 1
                        else:
                            one_to_zero_count += 1
                    elif r < self.error_probability + self.erasure_probability:
                        noisy_data += '!'  # Обозначаем стирание символом '!'
                        erasure_count += 1
                    else:
                        noisy_data += bit

                elif self.channel_type == "Z-канал":
                    # Z-канал: 0->0 всегда, 1->0 с вероятностью p
                    if bit == '1' and r < self.error_probability:
                        noisy_data += '0'
                        error_count += 1
                        one_to_zero_count += 1
                        z_channel_error_count += 1
                    else:
                        noisy_data += bit

            total_bits = bits_processed
            # Сохраняем фактические вероятности как атрибуты класса
            self.error_prob = error_count / total_bits if total_bits > 0 else 0
            self.erasure_prob = erasure_count / total_bits if total_bits > 0 else 0

            z_prob = 0
            if self.channel_type == "Z-канал" and z_channel_ones_count > 0:
                z_prob = z_channel_error_count / z_channel_ones_count

            # Сохраняем данные с ошибками
            self.parent.noisy_text = noisy_data

            self.result_text.insert("end", "\n\n=== Статистика внесения ошибок ===\n")

            if total_bits > 100:
                self.result_text.insert("end", "Первые 50 бит закодированных данных:\n")
                self.result_text.insert("end", encoded_data[:50] + "\n")
                self.result_text.insert("end", "Первые 50 бит данных с ошибками:\n")
                self.result_text.insert("end", noisy_data[:50] + "\n")
            else:
                self.result_text.insert("end", "Закодированные данные:\n")
                self.result_text.insert("end", encoded_data + "\n")
                self.result_text.insert("end", "Данные с ошибками:\n")
                self.result_text.insert("end", noisy_data + "\n")

            self.result_text.insert("end", f"\nРаспределение исходных битов:\n")
            self.result_text.insert("end", f"- Нули: {zeros_count} ({zeros_count / total_bits:.4f})\n")
            self.result_text.insert("end", f"- Единицы: {ones_count} ({ones_count / total_bits:.4f})\n")

            self.result_text.insert("end", f"\nСтатистика канала:\n")
            self.result_text.insert("end", f"- Общее количество битов: {total_bits}\n")
            self.result_text.insert("end", f"- Количество ошибок: {error_count}\n")
            self.result_text.insert("end", f"- Фактическая вероятность ошибки: {self.error_prob:.6f}\n")

            if error_count > 0:
                self.result_text.insert("end", f"\nТипы битовых ошибок:\n")
                zero_to_one_ratio = zero_to_one_count / error_count if error_count > 0 else 0
                one_to_zero_ratio = one_to_zero_count / error_count if error_count > 0 else 0

                self.result_text.insert("end", f"- 0->1: {zero_to_one_count} ({zero_to_one_ratio:.4f})\n")
                self.result_text.insert("end", f"- 1->0: {one_to_zero_count} ({one_to_zero_ratio:.4f})\n")

            if self.channel_type == "ДСКС":
                self.result_text.insert("end", f"- Количество стираний: {erasure_count}\n")
                self.result_text.insert("end", f"- Фактическая вероятность стирания: {self.erasure_prob:.6f}\n")

            if self.channel_type == "Z-канал":
                self.result_text.insert("end", f"- Количество единиц в исходных данных: {z_channel_ones_count}\n")
                self.result_text.insert("end", f"- Количество ошибок типа 1->0: {z_channel_error_count}\n")
                self.result_text.insert("end", f"- Вероятность ошибки при передаче '1': {z_prob:.6f}\n")

            self.result_text.insert("end",
                                    "\n✓ Ошибки и стирания внесены. Теперь вы можете нажать 'Декодировать' для восстановления данных.\n")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при внесении ошибок: {str(e)}")

    def decode_text(self):
        if not self.parent.noisy_text:
            messagebox.showerror("Ошибка", "Сначала внесите ошибки в закодированный текст")
            return

        # Получаем данные с ошибками/стираниями
        noisy_data = self.parent.noisy_text

        if '!' in noisy_data:
            noisy_data = noisy_data.replace('!', '0')
        numeric_polynomials = self.binary_polys_to_numeric()


        try:
            decoded_data = self.viterbi_decode(noisy_data, numeric_polynomials)

            if len(decoded_data) >= self.constraint_length - 1:
                decoded_data = decoded_data[:-self.constraint_length + 1]

            self.parent.decoded_text = decoded_data

            self.result_text.insert("end", "\n\nДекодированные данные:\n")
            self.result_text.insert("end", decoded_data)

            self.result_text.insert("end", f"\n\nИнформация о декодировании:\n")
            self.result_text.insert("end", f"Количество полиномов: {len(numeric_polynomials)}\n")
            self.result_text.insert("end", f"Использован метод декодирования: алгоритм Витерби\n")

            try:
                decoded_text = binary_to_text(decoded_data)
                self.result_text.insert("end", "\n\nДекодированный текст:\n")
                self.result_text.insert("end", decoded_text)
            except Exception as e:
                self.result_text.insert("end", f"\n\nНе удалось преобразовать двоичные данные в текст: {str(e)}")

        except Exception as e:
            messagebox.showerror("Ошибка декодирования", f"Ошибка при декодировании: {str(e)}")

    def viterbi_decode(self, encoded_bits, polynomials):
        """Декодирует последовательность с помощью алгоритма Витерби."""
        if not encoded_bits:
            return ''

        n_outputs = len(polynomials)
        if len(encoded_bits) % n_outputs != 0:
            raise ValueError("Некорректная длина закодированной последовательности")

        max_register = max(max(p) for p in polynomials)
        n_states = 2 ** max_register
        states = [format(i, f'0{max_register}b') for i in range(n_states)]

        # Вывод в интерфейс информации о декодировании Витерби
        self.result_text.insert("end", "\n=== Декодирование алгоритмом Витерби ===\n")
        self.result_text.insert("end", f"Количество состояний: {n_states}\n")
        self.result_text.insert("end", f"Длина закодированной последовательности: {len(encoded_bits)} бит\n")
        self.result_text.insert("end", f"Количество шагов: {len(encoded_bits) // n_outputs}\n")

        path_metrics = {s: float('inf') for s in states}
        path_metrics['0' * max_register] = 0
        paths = {s: [] for s in states}

        for i in range(0, len(encoded_bits), n_outputs):
            current_bits = encoded_bits[i:i + n_outputs]
            new_metrics = {s: float('inf') for s in states}
            new_paths = {s: [] for s in states}

            for state in states:
                if path_metrics[state] == float('inf'):
                    continue

                for input_bit in ['0', '1']:
                    next_state = (input_bit + state)[:-1]
                    tmp_registers = list(map(int, (input_bit + state)))
                    expected = []
                    for poly in polynomials:
                        xor = 0
                        for idx in poly:
                            xor ^= tmp_registers[idx]
                        expected.append(str(xor))
                    expected_str = ''.join(expected)

                    metric = sum(c1 != c2 for c1, c2 in zip(current_bits, expected_str))
                    total_metric = path_metrics[state] + metric

                    if total_metric < new_metrics[next_state]:
                        new_metrics[next_state] = total_metric
                        new_paths[next_state] = paths[state] + [input_bit]

            path_metrics, paths = new_metrics, new_paths

        final_state = min(path_metrics, key=path_metrics.get)
        self.result_text.insert("end", f"\nФинальная метрика: {path_metrics[final_state]:.1f}\n")

        return ''.join(paths[final_state])

    def calculate_capacity(self):
        try:
            # Проверяем, были ли внесены ошибки
            if not hasattr(self, 'error_prob') or not hasattr(self, 'erasure_prob'):
                messagebox.showerror("Ошибка", "Сначала внесите ошибки в закодированный текст")
                return

            # Используем фактические вероятности из add_noise
            p = self.error_prob
            q = self.erasure_prob if self.channel_type == "ДСКС" else 0

            # Используем универсальную функцию для всех каналов
            capacity_dsk = self.get_channel_capacity(p, 0, "ДСК")
            capacity_dsks = self.get_channel_capacity(p, q, "ДСКС")
            capacity_z = self.get_channel_capacity(p, 0, "Z-канал")

            # Выводим результаты
            self.result_text.insert("end", "\n\n=== Результаты расчета пропускной способности ===\n")
            self.result_text.insert("end", f"Фактическая вероятность ошибки (p): {p:.6f}\n")
            if self.channel_type == "ДСКС":
                self.result_text.insert("end", f"Фактическая вероятность стирания (q): {q:.6f}\n")

            self.result_text.insert("end", "\nПропускная способность каналов:\n")
            self.result_text.insert("end", f"1. Двоичный симметричный канал (ДСК): {capacity_dsk:.4f} бит/символ\n")
            self.result_text.insert("end", f"2. Двоичный симметричный канал со стираниями (ДСКС): {capacity_dsks:.4f} бит/символ\n")
            self.result_text.insert("end", f"3. Z-канал: {capacity_z:.4f} бит/символ\n")

            # Выводим текущую пропускную способность канала
            current_capacity = self.get_channel_capacity(p, q, self.channel_type)
            self.result_text.insert("end", f"\nТекущая пропускная способность ({self.channel_type}): {current_capacity:.4f} бит/символ\n")

            # Вставляем только корректные формулы
            self.result_text.insert("end", "\nФормулы пропускной способности:\n")
            self.result_text.insert("end", "ДСК:      C = 1 + p*log2(p) + (1-p)*log2(1-p)\n")
            self.result_text.insert("end", "ДСКС:     C = 1 - q + (1-p-q)*log2((1-p-q)/(1-q)) + p*log2(p/(1-q))\n")
            self.result_text.insert("end", "Z-канал:  C = log2(1 + (1-p)*p^(p/(1-p)))\n")

        except ValueError as e:
            messagebox.showerror("Ошибка", f"Ошибка в параметрах: {str(e)}")

    def update_constraint_length(self):
        try:
            # Получаем новое значение длины ограничения
            new_constraint_length = int(self.constraint_entry.get())

            if new_constraint_length < 2:
                messagebox.showerror("Ошибка", "Длина ограничения должна быть не менее 2")
                return

            # Обновляем длину ограничения
            self.constraint_length = new_constraint_length

            # Создаем новые полиномы по умолчанию, полностью удаляя предыдущие
            self.generator_polynomials = []
            for i in range(self.num_polynomials):
                # Создаем полином по умолчанию с соответствующей длиной ограничения
                # Используем шаблон 1...1 (первый и последний бит = 1)
                default_poly = '1' + '0' * (self.constraint_length - 2) + '1'
                self.generator_polynomials.append(default_poly)

            # Обновляем сводку о полиномах
            self.update_polynomials_summary()

            # Очищаем текстовое поле для результатов
            self.result_text.delete("1.0", "end")

            # Обновляем информацию
            self.result_text.insert("1.0", "=== Обновление параметров сверточного кода ===\n")
            self.result_text.insert("end", f"Длина ограничения обновлена: {self.constraint_length}\n")
            self.result_text.insert("end", f"Все полиномы пересозданы под новую длину ограничения.\n")

            # Предложение эффективных полиномов для новой длины
            suggestions = self.get_polynomial_suggestions(self.constraint_length)
            if suggestions:
                self.result_text.insert("end",
                                        f"\nРекомендуемые полиномы для длины ограничения {self.constraint_length}:\n")
                for i, poly in enumerate(suggestions):
                    self.result_text.insert("end", f"- {poly}\n")

            # Выводим информацию о полиномах
            self.result_text.insert("end", "\nНовые полиномы генератора:\n")
            for i, poly in enumerate(self.generator_polynomials):
                self.result_text.insert("end", f"Полином {i + 1}: {poly}\n")

            # Информация о влиянии длины ограничения на кодирование
            self.result_text.insert("end", f"\nВлияние длины ограничения на кодирование:\n")
            self.result_text.insert("end",
                                    f"- Более длинное ограничение увеличивает избыточность и помехоустойчивость кода\n")
            self.result_text.insert("end",
                                    f"- Более короткое ограничение снижает избыточность, но ухудшает помехоустойчивость\n")

            # Проверяем полиномы для безопасности
            self._validate_polynomials()

        except ValueError:
            messagebox.showerror("Ошибка", "Длина ограничения должна быть целым числом")

    def _validate_polynomials(self):
        """Проверяет и исправляет полиномы, если их длина не соответствует constraint_length"""
        valid_polynomials = []
        has_changes = False

        # Если список полиномов пуст или меньше, чем num_polynomials, добавим недостающие
        while len(self.generator_polynomials) < self.num_polynomials:
            default_poly = '1' + '0' * (self.constraint_length - 2) + '1'
            self.generator_polynomials.append(default_poly)
            has_changes = True

        # Обрезаем лишние полиномы, если их больше, чем num_polynomials
        if len(self.generator_polynomials) > self.num_polynomials:
            self.generator_polynomials = self.generator_polynomials[:self.num_polynomials]
            has_changes = True

        for i, poly in enumerate(self.generator_polynomials):
            # Проверяем, не является ли полином в числовом формате (список индексов)
            if isinstance(poly, list):
                # Преобразуем числовой формат в двоичный
                binary_poly = self.numeric_poly_to_binary(poly, self.constraint_length)
                valid_polynomials.append(binary_poly)
                has_changes = True
                continue

            # Проверяем длину полинома
            if len(poly) != self.constraint_length:
                # Создаем новый полином правильной длины
                new_poly = '1' + '0' * (self.constraint_length - 2) + '1'
                valid_polynomials.append(new_poly)
                has_changes = True
            # Проверяем состав полинома (только 0 и 1)
            elif not all(bit in '01' for bit in poly):
                # Заменяем недопустимые символы на 0
                new_poly = ''.join(['0' if bit not in '01' else bit for bit in poly])
                # Еще проверяем первый и последний бит
                if new_poly[0] != '1' or new_poly[-1] != '1':
                    new_poly = '1' + new_poly[1:-1] + '1'
                valid_polynomials.append(new_poly)
                has_changes = True
            # Проверяем, что первый и последний биты равны 1
            elif poly[0] != '1' or poly[-1] != '1':
                new_poly = '1' + poly[1:-1] + '1'
                valid_polynomials.append(new_poly)
                has_changes = True
            else:
                valid_polynomials.append(poly)

        # Обновляем список полиномов, если были изменения
        if has_changes:
            self.generator_polynomials = valid_polynomials
            self.update_polynomials_summary()
            return True

        return True  # Всегда возвращаем True, так как мы исправили все проблемы

    def toggle_poly_frame(self):
        """Сворачивает или разворачивает фрейм с полиномами"""
        if self.poly_expanded:
            self.poly_frame.pack_forget()
            self.toggle_poly_button.configure(text="Развернуть")
            self.poly_expanded = False
        else:
            self.poly_frame.pack(fill="x", padx=10, pady=(0, 10))
            self.toggle_poly_button.configure(text="Свернуть")
            self.poly_expanded = True

    def open_polynomials_window(self):
        """Открывает отдельное окно для редактирования полиномов"""
        # Создаем новое окно
        poly_window = ctk.CTkToplevel(self.parent)
        poly_window.title("Настройка полиномов генератора")
        poly_window.geometry("600x400")
        poly_window.grab_set()

        # Заголовок
        header_frame = ctk.CTkFrame(poly_window)
        header_frame.pack(fill="x", padx=10, pady=10)

        header_label = ctk.CTkLabel(header_frame, text=f"Полиномы генератора ({self.num_polynomials})",
                                    font=ctk.CTkFont(size=16, weight="bold"))
        header_label.pack(side="left", padx=10, pady=10)

        # Информационная строка
        info_text = f"Всего полиномов: {self.num_polynomials}, длина полинома: {self.constraint_length} бит"
        info_label = ctk.CTkLabel(poly_window, text=info_text, font=ctk.CTkFont(size=12))
        info_label.pack(fill="x", padx=10, pady=0, anchor="w")

        # Фрейм для полиномов с прокруткой
        poly_frame = ctk.CTkScrollableFrame(poly_window, height=250)
        poly_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Создаем поля ввода для полиномов
        poly_entries = []

        # Определяем оптимальное количество полиномов в строке
        polynomials_per_row = min(3, self.num_polynomials)

        # Создаем сетку для размещения полиномов
        row_frames = []

        # Создаем фреймы для каждой строки
        row_count = (self.num_polynomials + polynomials_per_row - 1) // polynomials_per_row
        for i in range(row_count):
            row_frame = ctk.CTkFrame(poly_frame)
            row_frame.pack(fill="x", padx=5, pady=5)
            row_frames.append(row_frame)

        # Заполняем строки полиномами
        for i in range(self.num_polynomials):
            row_index = i // polynomials_per_row
            col_index = i % polynomials_per_row

            # Создаем фрейм для полинома
            entry_frame = ctk.CTkFrame(row_frames[row_index])
            entry_frame.grid(row=0, column=col_index, padx=5, pady=5, sticky="w")

            # Метка
            label = ctk.CTkLabel(entry_frame, text=f"Полином {i + 1}:", width=80)
            label.pack(side="left", padx=5)

            # Поле ввода
            entry = ctk.CTkEntry(entry_frame, width=150)
            entry.pack(side="left", padx=5)

            # Заполняем поле существующим значением
            if i < len(self.generator_polynomials):
                entry.insert(0, self.generator_polynomials[i])

            poly_entries.append(entry)

        # Фрейм для кнопок
        button_frame = ctk.CTkFrame(poly_window)
        button_frame.pack(fill="x", padx=10, pady=10)

        # Кнопка для применения рекомендуемых полиномов
        if self.constraint_length <= 5:
            suggestions = self.get_polynomial_suggestions(self.constraint_length)
            if suggestions and len(suggestions) > 0:
                recommend_button = ctk.CTkButton(button_frame, text="Применить рекомендуемые",
                                                 command=lambda: self._apply_recommended_to_entries(suggestions,
                                                                                                    poly_entries))
                recommend_button.pack(side="left", padx=10, pady=10)

        # Кнопка для применения одинаковых полиномов
        same_poly_button = ctk.CTkButton(button_frame, text="Одинаковые полиномы",
                                         command=lambda: self._apply_same_to_entries(poly_entries))
        same_poly_button.pack(side="left", padx=10, pady=10)

        # Кнопки OK и Отмена
        cancel_button = ctk.CTkButton(button_frame, text="Отмена",
                                      command=poly_window.destroy)
        cancel_button.pack(side="right", padx=10, pady=10)

        ok_button = ctk.CTkButton(button_frame, text="Применить",
                                  command=lambda: self._apply_polynomials_from_window(poly_entries, poly_window))
        ok_button.pack(side="right", padx=10, pady=10)

    def _apply_recommended_to_entries(self, suggestions, entries):
        """Применяет рекомендуемые полиномы к полям ввода"""
        # Используем только необходимое количество полиномов
        recommended = suggestions[:self.num_polynomials]

        # Если рекомендаций меньше, чем нужно полиномов, дублируем их
        while len(recommended) < self.num_polynomials:
            recommended.append(suggestions[0])

        # Получаем числовое представление полиномов для отображения
        numeric_polys = []
        for poly in recommended:
            indices = [i for i, bit in enumerate(poly) if bit == '1']
            numeric_polys.append(indices)

        # Обновляем поля ввода
        for i, poly in enumerate(recommended):
            if i < len(entries):
                entries[i].delete(0, "end")
                # Показываем двоичный формат в полях ввода
                entries[i].insert(0, poly)

    def _apply_same_to_entries(self, entries):
        """Применяет одинаковый полином ко всем полям ввода"""
        if not entries or len(entries) == 0:
            return

        # Используем значение из первого поля ввода
        first_poly = entries[0].get()

        # Проверяем, в каком формате введен полином
        if ',' in first_poly:
            try:
                # Пробуем разобрать как список индексов
                indices = [int(idx.strip()) for idx in first_poly.split(',')]
                # Проверяем валидность индексов
                if any(idx < 0 or idx >= self.constraint_length for idx in indices):
                    messagebox.showerror("Ошибка",
                                         f"Индексы должны быть в диапазоне от 0 до {self.constraint_length - 1}")
                    return

                # Создаем двоичный полином
                binary_poly = self.numeric_poly_to_binary(indices, self.constraint_length)

                # Применяем это значение ко всем полям
                for entry in entries:
                    entry.delete(0, "end")
                    entry.insert(0, binary_poly)
            except ValueError:
                messagebox.showerror("Ошибка", "Некорректный формат числовых индексов")
                return
        else:
            # Проверяем корректность двоичного полинома
            if len(first_poly) != self.constraint_length or not all(bit in '01' for bit in first_poly):
                messagebox.showerror("Ошибка", f"Полином должен состоять из {self.constraint_length} бит (0 или 1)")
                return

            # Применяем это значение ко всем полям
            for entry in entries:
                entry.delete(0, "end")
                entry.insert(0, first_poly)

    def _apply_polynomials_from_window(self, entries, window):
        """Применяет полиномы из отдельного окна"""
        # Собираем значения из полей ввода
        polynomials = []
        for entry in entries:
            poly_input = entry.get().strip()

            # Проверяем, является ли ввод числовым форматом (через запятую)
            if ',' in poly_input:
                try:
                    # Пробуем разобрать как список индексов
                    indices = [int(idx.strip()) for idx in poly_input.split(',')]
                    # Проверяем валидность индексов
                    if any(idx < 0 or idx >= self.constraint_length for idx in indices):
                        messagebox.showerror("Ошибка",
                                             f"Индексы должны быть в диапазоне от 0 до {self.constraint_length - 1}")
                        return

                    # Создаем двоичный полином из индексов
                    binary_poly = self.numeric_poly_to_binary(indices, self.constraint_length)
                    polynomials.append(binary_poly)
                except ValueError:
                    messagebox.showerror("Ошибка", "Некорректный формат числовых индексов")
                    return
            else:
                # Проверяем корректность двоичного полинома
                if len(poly_input) != self.constraint_length:
                    messagebox.showerror("Ошибка",
                                         f"Длина полиномов должна соответствовать длине ограничения ({self.constraint_length})")
                    return

                if not all(bit in '01' for bit in poly_input):
                    messagebox.showerror("Ошибка", "Полиномы должны быть записаны в двоичном виде (только 0 и 1)")
                    return

                polynomials.append(poly_input)

        # Обновляем список полиномов
        self.generator_polynomials = polynomials

        # Закрываем окно
        window.destroy()

        # Обновляем информацию в основном окне
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "Полиномы генератора обновлены:\n")

        # Выводим полиномы в двух форматах (двоичном и числовом)
        numeric_polys = self.binary_polys_to_numeric()
        for i, poly in enumerate(self.generator_polynomials):
            self.result_text.insert("end", f"Полином {i + 1}: {poly} (двоичный) / {numeric_polys[i]} (индексы)\n")

        # Обновляем метку с количеством полиномов и сводку полиномов
        self.poly_label.configure(text=f"Полиномы генератора ({self.num_polynomials}):")
        self.update_polynomials_summary()

    def update_polynomials_summary(self):
        """Обновляет текстовое поле с информацией о текущих полиномах"""
        self.poly_summary.configure(state="normal")
        self.poly_summary.delete("1.0", "end")

        # Получаем числовое представление полиномов
        numeric_polys = self.binary_polys_to_numeric()

        # Добавляем информацию о полиномах
        if len(self.generator_polynomials) <= 6:
            # Показываем все полиномы, если их не слишком много
            for i, poly in enumerate(self.generator_polynomials):
                # Показываем оба формата для каждого полинома
                self.poly_summary.insert("end", f"Полином {i + 1}: {poly} / {numeric_polys[i]}  ")
                # Добавляем перенос строки после каждого второго полинома
                if (i + 1) % 2 == 0 and i < len(self.generator_polynomials) - 1:
                    self.poly_summary.insert("end", "\n")
        else:
            # Показываем только первые и последние полиномы
            for i in range(3):
                if i < len(self.generator_polynomials):
                    self.poly_summary.insert("end",
                                             f"Полином {i + 1}: {self.generator_polynomials[i]} / {numeric_polys[i]}  ")
                    if i == 1:
                        self.poly_summary.insert("end", "\n")

            self.poly_summary.insert("end", "\n...")

            for i in range(max(3, len(self.generator_polynomials) - 2), len(self.generator_polynomials)):
                self.poly_summary.insert("end",
                                         f"Полином {i + 1}: {self.generator_polynomials[i]} / {numeric_polys[i]}  ")

        self.poly_summary.configure(state="disabled")

    def get_channel_capacity(self, p, q, channel_type):
        """Вычисляет пропускную способность канала по типу и параметрам"""
        if channel_type == "ДСК":
            if p != 0 and p != 1:
                return 1 + p * np.log2(p) + (1 - p) * np.log2(1 - p)
            else:
                return 1
        elif channel_type == "ДСКС":
            if q != 1:
                if p != 0 and p != 1 - q:
                    return 1 - q + (1 - p - q) * np.log2((1 - p - q) / (1 - q)) + p * np.log2(p / (1 - q))
                else:
                    return 1 - q
            else:
                return 0
        elif channel_type == "Z-канал":
            if p != 0 and p != 1:
                return np.log2(1 + (1 - p) * (p ** (p / (1 - p))))
            else:
                return 1
        return 0