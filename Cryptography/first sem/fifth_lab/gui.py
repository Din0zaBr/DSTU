"""
Модуль графического интерфейса для шифра Гронсфельда.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
from typing import Optional

from gronsfeld_cipher import encrypt_text, decrypt_text


class GronsfeldApp:
    """Графический интерфейс для шифра Гронсфельда."""
    
    def __init__(self, root: tk.Tk) -> None:
        """Инициализирует приложение."""
        self.root: tk.Tk = root
        self.root.title("Шифр Гронсфельда")
        self.root.geometry("750x750")
        self.root.resizable(True, True)
        
        ttk.Style().theme_use('clam')
        
        self.text_input: Optional[scrolledtext.ScrolledText] = None
        self.key_input: Optional[tk.Entry] = None
        self.result_output: Optional[scrolledtext.ScrolledText] = None
        self.result_content: str = ""
        
        self.create_widgets()
    
    def create_widgets(self) -> None:
        """Создает все виджеты интерфейса."""
        # Заголовок
        header = tk.Frame(self.root, bg='#2c3e50', height=60)
        header.pack(fill='x')
        header.pack_propagate(False)
        tk.Label(header, text="Шифр Гронсфельда", font=('Arial', 18, 'bold'),
                bg='#2c3e50', fg='white').pack(pady=12)
        
        main_frame = tk.Frame(self.root, bg='#ecf0f1', padx=20, pady=15)
        main_frame.pack(fill='both', expand=True)
        
        # Поле для ввода текста
        self._create_label(main_frame, "Введите текст:", 0)
        self.text_input = self._create_text_area(main_frame, 1)
        
        # Кнопки загрузки для текста
        text_btn_frame = tk.Frame(main_frame, bg='#ecf0f1')
        text_btn_frame.pack(fill='x', pady=(0, 15))
        self._create_button(text_btn_frame, "Загрузить текст из файла", 
                          '#95a5a6', self.load_text_from_file).pack(side='left', padx=5)
        
        # Поле для ввода ключа
        key_frame = tk.Frame(main_frame, bg='#ecf0f1')
        key_frame.pack(fill='x', pady=(0, 15))
        tk.Label(key_frame, text="Числовой ключ:", font=('Arial', 11, 'bold'),
                bg='#ecf0f1').pack(side='left')
        self.key_input = tk.Entry(key_frame, font=('Arial', 11), width=25, borderwidth=2, relief='solid')
        self.key_input.pack(side='left', padx=(10, 5))
        self._create_button(key_frame, "Загрузить ключ", '#95a5a6', 
                          self.load_key_from_file).pack(side='left', padx=5)
        
        # Кнопки операций
        btn_frame = tk.Frame(main_frame, bg='#ecf0f1')
        btn_frame.pack(pady=(0, 10))
        self._create_button(btn_frame, "Зашифровать", '#27ae60', self.encrypt).pack(side='left', padx=5)
        self._create_button(btn_frame, "Расшифровать", '#3498db', self.decrypt).pack(side='left', padx=5)
        self._create_button(btn_frame, "Очистить", '#e74c3c', self.clear_fields).pack(side='left', padx=5)
        
        # Разделитель
        separator = tk.Frame(main_frame, bg='#bdc3c7', height=2)
        separator.pack(fill='x', pady=10)
        
        # Секция работы с файлами
        file_label = tk.Label(main_frame, text="Работа с файлами:", 
                             font=('Arial', 11, 'bold'), bg='#ecf0f1')
        file_label.pack(anchor='w', pady=(0, 5))
        
        file_btn_frame = tk.Frame(main_frame, bg='#ecf0f1')
        file_btn_frame.pack(fill='x', pady=(0, 15))
        self._create_button(file_btn_frame, "Зашифровать из файлов", '#16a085', 
                          self.encrypt_from_files).pack(side='left', padx=5)
        self._create_button(file_btn_frame, "Расшифровать из файлов", '#2980b9', 
                          self.decrypt_from_files).pack(side='left', padx=5)
        
        # Поле для вывода результата
        self._create_label(main_frame, "Результат:", 0)
        self.result_output = self._create_text_area(main_frame, 1, bg='#f8f9fa')
        self._setup_result_protection()
        
        # Кнопка сохранения результата
        save_btn_frame = tk.Frame(main_frame, bg='#ecf0f1')
        save_btn_frame.pack(fill='x', pady=(5, 0))
        self._create_button(save_btn_frame, "Сохранить результат в файл", 
                          '#9b59b6', self.save_result_to_file).pack(side='left', padx=5)
    
    def _create_label(self, parent: tk.Frame, text: str, pady_bottom: int) -> None:
        """Создает метку."""
        tk.Label(parent, text=text, font=('Arial', 11, 'bold'),
                bg='#ecf0f1').pack(anchor='w', pady=(0, pady_bottom))
    
    def _create_text_area(self, parent: tk.Frame, pady_bottom: int, **kwargs) -> scrolledtext.ScrolledText:
        """Создает текстовую область."""
        text_area = scrolledtext.ScrolledText(
            parent, height=8, font=('Arial', 11), wrap='word',
            borderwidth=2, relief='solid', **kwargs
        )
        text_area.pack(fill='both', expand=True, pady=(0, pady_bottom))
        return text_area
    
    def _create_button(self, parent: tk.Frame, text: str, bg: str, command) -> tk.Button:
        """Создает кнопку."""
        return tk.Button(
            parent, text=text, font=('Arial', 11, 'bold'), bg=bg, fg='white',
            activebackground=bg, activeforeground='white', borderwidth=0,
            padx=15, pady=8, cursor='hand2', command=command
        )
    
    def _setup_result_protection(self) -> None:
        """Настраивает защиту поля результата от редактирования."""
        if self.result_output is None:
            return
        self.result_output.bind('<Key>', self._prevent_editing)
        self.result_output.bind('<Button-3>', self._on_right_click)
    
    def _get_text(self) -> Optional[str]:
        """Получает текст из поля ввода."""
        return self.text_input.get('1.0', 'end-1c').strip() if self.text_input else None
    
    def _get_key(self) -> Optional[str]:
        """Получает ключ из поля ввода."""
        return self.key_input.get().strip() if self.key_input else None
    
    def _set_result(self, text: str) -> None:
        """Устанавливает результат в поле вывода."""
        if self.result_output is None:
            return
        self.result_output.delete('1.0', 'end')
        self.result_output.insert('1.0', text)
        self.result_content = text
    
    def _process_operation(self, operation: str) -> None:
        """Обрабатывает операцию шифрования или расшифрования."""
        if not all([self.text_input, self.key_input, self.result_output]):
            return
        
        text = self._get_text()
        key = self._get_key()
        
        if not text:
            messagebox.showwarning("Предупреждение", f"Введите текст для {operation}!")
            return
        if not key:
            messagebox.showwarning("Предупреждение", "Введите ключ!")
            return
        
        try:
            result = encrypt_text(text, key) if operation == "шифрования" else decrypt_text(text, key)
            self._set_result(result)
        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))
    
    def encrypt(self) -> None:
        """Обработчик кнопки шифрования."""
        self._process_operation("шифрования")
    
    def decrypt(self) -> None:
        """Обработчик кнопки расшифрования."""
        self._process_operation("расшифрования")
    
    def clear_fields(self) -> None:
        """Очищает все поля."""
        if self.text_input:
            self.text_input.delete('1.0', 'end')
        if self.key_input:
            self.key_input.delete(0, 'end')
        if self.result_output:
            self.result_output.delete('1.0', 'end')
        self.result_content = ""
    
    def load_text_from_file(self) -> None:
        """Загружает текст из файла."""
        filename = filedialog.askopenfilename(
            title="Выберите файл с текстом",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not filename:
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            if self.text_input:
                self.text_input.delete('1.0', 'end')
                self.text_input.insert('1.0', content)
            messagebox.showinfo("Успех", "Текст загружен из файла!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")
    
    def load_key_from_file(self) -> None:
        """Загружает ключ из файла."""
        filename = filedialog.askopenfilename(
            title="Выберите файл с ключом",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not filename:
            return
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                key = f.read().strip()
            if self.key_input:
                self.key_input.delete(0, 'end')
                self.key_input.insert(0, key)
            messagebox.showinfo("Успех", "Ключ загружен из файла!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")
    
    def save_result_to_file(self) -> None:
        """Сохраняет результат в файл."""
        if not self.result_content:
            messagebox.showwarning("Предупреждение", "Нет результата для сохранения!")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Сохранить результат",
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not filename:
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.result_content)
            messagebox.showinfo("Успех", "Результат сохранен в файл!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{e}")
    
    def encrypt_from_files(self) -> None:
        """Шифрует текст из файла с ключом из другого файла и сохраняет результат."""
        # Запрашиваем файл с текстом
        text_filename = filedialog.askopenfilename(
            title="Выберите файл с текстом для шифрования",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not text_filename:
            return
        
        # Запрашиваем файл с ключом
        key_filename = filedialog.askopenfilename(
            title="Выберите файл с ключом",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not key_filename:
            return
        
        try:
            # Читаем текст
            with open(text_filename, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Читаем ключ
            with open(key_filename, 'r', encoding='utf-8') as f:
                key = f.read().strip()
            
            # Шифруем
            encrypted = encrypt_text(text, key)
            
            # Сохраняем результат
            result_filename = filedialog.asksaveasfilename(
                title="Сохранить зашифрованный текст",
                defaultextension=".txt",
                filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
            )
            if result_filename:
                with open(result_filename, 'w', encoding='utf-8') as f:
                    f.write(encrypted)
                
                # Обновляем интерфейс
                if self.text_input:
                    self.text_input.delete('1.0', 'end')
                    self.text_input.insert('1.0', text)
                if self.key_input:
                    self.key_input.delete(0, 'end')
                    self.key_input.insert(0, key)
                self._set_result(encrypted)
                
                messagebox.showinfo("Успех", 
                    f"Текст зашифрован и сохранен в файл:\n{result_filename}")
        except ValueError as e:
            messagebox.showerror("Ошибка шифрования", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обработать файлы:\n{e}")
    
    def decrypt_from_files(self) -> None:
        """Расшифровывает текст из файла с ключом из другого файла и сохраняет результат."""
        # Запрашиваем файл с зашифрованным текстом
        encrypted_filename = filedialog.askopenfilename(
            title="Выберите файл с зашифрованным текстом",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not encrypted_filename:
            return
        
        # Запрашиваем файл с ключом
        key_filename = filedialog.askopenfilename(
            title="Выберите файл с ключом",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        if not key_filename:
            return
        
        try:
            # Читаем зашифрованный текст
            with open(encrypted_filename, 'r', encoding='utf-8') as f:
                encrypted_text = f.read()
            
            # Читаем ключ
            with open(key_filename, 'r', encoding='utf-8') as f:
                key = f.read().strip()
            
            # Расшифровываем
            decrypted = decrypt_text(encrypted_text, key)
            
            # Сохраняем результат
            result_filename = filedialog.asksaveasfilename(
                title="Сохранить расшифрованный текст",
                defaultextension=".txt",
                filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
            )
            if result_filename:
                with open(result_filename, 'w', encoding='utf-8') as f:
                    f.write(decrypted)
                
                # Обновляем интерфейс
                if self.text_input:
                    self.text_input.delete('1.0', 'end')
                    self.text_input.insert('1.0', encrypted_text)
                if self.key_input:
                    self.key_input.delete(0, 'end')
                    self.key_input.insert(0, key)
                self._set_result(decrypted)
                
                messagebox.showinfo("Успех", 
                    f"Текст расшифрован и сохранен в файл:\n{result_filename}")
        except ValueError as e:
            messagebox.showerror("Ошибка расшифрования", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обработать файлы:\n{e}")
    
    def _prevent_editing(self, event: tk.Event) -> Optional[str]:
        """Блокирует редактирование поля результата, но разрешает копирование."""
        if event.state & 0x4:  # Ctrl
            if event.keysym.lower() in ['c', 'a']:
                return None
            if event.keysym.lower() in ['x', 'v']:
                return "break"
        elif event.state & 0x1:  # Shift
            if event.keysym in ['Left', 'Right', 'Up', 'Down', 'Home', 'End']:
                return None
        
        if event.keysym in ['Left', 'Right', 'Up', 'Down', 'Home', 'End', 
                           'Page_Up', 'Page_Down', 'Prior', 'Next', 'Tab']:
            return None
        
        if event.keysym.startswith('F') and event.keysym[1:].isdigit():
            return None
        
        if len(event.keysym) == 1 or event.keysym in ['Return', 'space', 'BackSpace', 'Delete']:
            return "break"
        return None
    
    def _on_right_click(self, event: tk.Event) -> None:
        """Обработчик правого клика - создает контекстное меню."""
        if self.result_output is None:
            return
        
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Копировать", command=self._copy_selected)
        menu.add_command(label="Выделить все", command=self._select_all)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def _copy_selected(self) -> None:
        """Копирует выделенный текст в буфер обмена."""
        if self.result_output is None:
            return
        
        try:
            text = self.result_output.selection_get()
            if text:
                self.root.clipboard_clear()
                self.root.clipboard_append(text)
        except tk.TclError:
            all_text = self.result_output.get('1.0', 'end-1c')
            if all_text:
                self.root.clipboard_clear()
                self.root.clipboard_append(all_text)
    
    def _select_all(self) -> None:
        """Выделяет весь текст в поле результата."""
        if self.result_output is None:
            return
        self.result_output.tag_add('sel', '1.0', 'end')
        self.result_output.mark_set('insert', '1.0')
        self.result_output.see('insert')
