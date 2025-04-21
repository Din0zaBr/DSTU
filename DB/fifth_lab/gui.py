# -*- coding: utf-8 -*-
import psycopg2
from tkinter import *
from tkinter import messagebox, ttk

# Подключение к базе данных
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="my_DB",
            user="postgres",
            password="superuser",
            host="localhost"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось подключиться к базе данных: {e}")
        return None

# Проверка аутентификации
def authenticate(username, password):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            if result:
                return result[0]  # Возвращаем роль пользователя
            else:
                return None
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при аутентификации: {e}")
        finally:
            conn.close()
    return None

# Получение списка таблиц (кроме users)
def get_tables():
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name != 'users'
            """)
            tables = cursor.fetchall()
            return [table[0] for table in tables]
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении списка таблиц: {e}")
        finally:
            conn.close()
    return []

# Получение данных из таблицы
def get_table_data(table_name):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return columns, rows
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении данных из таблицы: {e}")
        finally:
            conn.close()
    return [], []

# Интерфейс для обычного пользователя
def user_interface():
    def show_table_data(table_name):
        columns, rows = get_table_data(table_name)
        if columns and rows:
            # Очистка Treeview
            for item in tree.get_children():
                tree.delete(item)
            # Настройка колонок
            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            # Добавление данных
            for row in rows:
                tree.insert("", "end", values=row)

    root = Tk()
    root.title("Интерфейс пользователя")
    root.geometry("800x600")

    # Список таблиц
    tables = get_tables()
    table_buttons_frame = Frame(root)
    table_buttons_frame.pack(fill=X, padx=10, pady=10)

    for table in tables:
        Button(table_buttons_frame, text=table, command=lambda t=table: show_table_data(t)).pack(side=LEFT, padx=5)

    # Treeview для отображения данных
    tree = ttk.Treeview(root, show="headings")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    root.mainloop()

# Интерфейс для администратора
def admin_interface():
    def show_table_data(table_name):
        columns, rows = get_table_data(table_name)
        if columns and rows:
            # Очистка Treeview
            for item in tree.get_children():
                tree.delete(item)
            # Настройка колонок
            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            # Добавление данных
            for row in rows:
                tree.insert("", "end", values=row)

    def execute_sql():
        sql = sql_entry.get("1.0", "end-1c")
        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                conn.commit()
                messagebox.showinfo("Успех", "SQL-запрос выполнен успешно")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при выполнении SQL-запроса: {e}")
            finally:
                conn.close()

    def refresh_tables():
        # Обновление списка таблиц
        for widget in table_buttons_frame.winfo_children():
            widget.destroy()
        tables = get_tables()
        for table in tables:
            Button(table_buttons_frame, text=table, command=lambda t=table: show_table_data(t)).pack(side=LEFT, padx=5)

    root = Tk()
    root.title("Интерфейс администратора")
    root.geometry("800x600")

    # Фрейм для кнопок таблиц
    table_buttons_frame = Frame(root)
    table_buttons_frame.pack(fill=X, padx=10, pady=10)

    # Обновление списка таблиц
    refresh_tables()

    # Treeview для отображения данных
    tree = ttk.Treeview(root, show="headings")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Поле для ввода SQL-запросов
    sql_entry = Text(root, height=5, width=50)
    sql_entry.pack(padx=10, pady=10)

    # Кнопка для выполнения SQL-запросов
    Button(root, text="Выполнить SQL", command=execute_sql).pack(side=LEFT, padx=5)

    # Кнопка для обновления таблиц
    Button(root, text="Обновить таблицы", command=refresh_tables).pack(side=LEFT, padx=5)

    root.mainloop()

# Главное окно аутентификации
def main():
    def login():
        username = entry_username.get()
        password = entry_password.get()
        role = authenticate(username, password)
        if role == "user":
            user_interface()
        elif role == "admin":
            admin_interface()
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    root = Tk()
    root.title("Аутентификация")
    root.geometry("300x200")

    Label(root, text="Имя пользователя").grid(row=0, column=0, padx=10, pady=10)
    entry_username = Entry(root)
    entry_username.grid(row=0, column=1, padx=10, pady=10)

    Label(root, text="Пароль").grid(row=1, column=0, padx=10, pady=10)
    entry_password = Entry(root, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

    Button(root, text="Войти", command=login).grid(row=2, column=1, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
