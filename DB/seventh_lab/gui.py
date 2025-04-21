# -*- coding: utf-8 -*-
import psycopg2
import logging
from tkinter import *
from tkinter import messagebox, ttk

# Настройка логгирования
logging.basicConfig(level=logging.DEBUG)


# Подключение к базе данных
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="TemporalDB",
            user="postgres",
            password="superuser",
            host="localhost"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось подключиться к базе данных: {e}")
        print(e)
        return None


# Проверка аутентификации
def authenticate(username, password):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM users WHERE username = %s AND password = %s", ("user1", "user123"))
            result = cursor.fetchone()
            print(result)
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
                AND table_name != 'my_object'
            """)
            tables = cursor.fetchall()
            return [table[0] for table in tables]
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении списка таблиц: {e}")
        finally:
            conn.close()
    return []


# Получение данных из таблицы
def get_table_data(table_name, show_history=False):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            if show_history:
                cursor.execute(f"SELECT * FROM {table_name} ORDER BY time_create DESC")
            else:
                cursor.execute(f"SELECT * FROM {table_name} WHERE time_dead IS NULL AND operation_type <> 'D'")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return columns, rows
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении данных из таблицы: {e}")
        finally:
            conn.close()
    return [], []


# Получение истории изменений объекта
def get_object_history(table_name, obj_id):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM get_object_history(%s, %s)
            """, (table_name, obj_id))
            history = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            return columns, history
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при получении истории объекта: {e}")
        finally:
            conn.close()
    return [], []


# Восстановление версии объекта
def restore_version(table_name, obj_id, time_create):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT restore_object_version(%s, %s, %s)",
                           (table_name, obj_id, time_create))
            conn.commit()
            messagebox.showinfo("Успех", "Версия объекта успешно восстановлена")
            return True
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при восстановлении версии: {e}")
        finally:
            conn.close()
    return False


# Интерфейс для обычного пользователя
def user_interface():
    def show_table_data(table_name):
        columns, rows = get_table_data(table_name)
        if columns and rows:
            for item in tree.get_children():
                tree.delete(item)
            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            for row in rows:
                tree.insert("", "end", values=row)

    root = Tk()
    root.title("Интерфейс пользователя")

    tables = get_tables()
    for table in tables:
        Button(root, text=table, command=lambda t=table: show_table_data(t)).pack()

    tree = ttk.Treeview(root, show="headings")
    tree.pack(fill="both", expand=True)

    root.mainloop()


# Интерфейс для администратора
def admin_interface():
    def show_table_data(table_name, show_history=False):
        nonlocal current_table
        current_table = table_name
        table_var.set(table_name)
        columns, rows = get_table_data(table_name, show_history)
        if columns and rows:
            for item in tree.get_children():
                tree.delete(item)
            tree["columns"] = columns
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            for row in rows:
                tree.insert("", "end", values=row)

    def show_object_history():
        selected_item = tree.selection()
        if selected_item:
            item_data = tree.item(selected_item)
            table_name = table_var.get()
            obj_id = item_data['values'][0]

            history_window = Toplevel(root)
            history_window.title(f"История объекта {obj_id}")

            columns, history = get_object_history(table_name, obj_id)

            history_tree = ttk.Treeview(history_window, show="headings")
            history_tree["columns"] = columns
            for col in columns:
                history_tree.heading(col, text=col)
                history_tree.column(col, width=100)

            for row in history:
                history_tree.insert("", "end", values=row)

            history_tree.pack(fill="both", expand=True)

            def restore_selected_version():
                selected_history = history_tree.selection()
                if selected_history:
                    history_data = history_tree.item(selected_history)
                    time_create = history_data['values'][1]
                    if restore_version(table_name, obj_id, time_create):
                        show_table_data(table_name)
                        history_window.destroy()

            Button(history_window, text="Восстановить эту версию", command=restore_selected_version).pack()

    def execute_sql():
        sql = sql_entry.get("1.0", "end-1c").strip()
        if not sql:
            messagebox.showwarning("Предупреждение", "SQL-запрос не может быть пустым")
            return

        conn = connect_to_db()
        if conn:
            try:
                cursor = conn.cursor()
                query_type = sql.split()[0].upper()

                cursor.execute(sql)

                if query_type in ('UPDATE', 'DELETE', 'INSERT'):
                    rows_affected = cursor.rowcount
                    conn.commit()
                    messagebox.showinfo("Успех",
                                        f"SQL-запрос выполнен успешно. Затронуто строк: {rows_affected}")
                else:
                    messagebox.showinfo("Успех", "SQL-запрос выполнен успешно")

                # Обновляем текущую таблицу
                if current_table:
                    show_table_data(current_table)

            except Exception as e:
                if conn:
                    conn.rollback()
                messagebox.showerror("Ошибка", f"Ошибка при выполнении SQL-запроса: {e}")
                logging.error(f"SQL error: {e}")
            finally:
                if conn:
                    conn.close()

    def refresh_tables():
        for widget in table_buttons_frame.winfo_children():
            widget.destroy()
        tables = get_tables()
        for table in tables:
            Button(table_buttons_frame, text=table,
                   command=lambda t=table: show_table_data(t)).pack()

    root = Tk()
    root.title("Интерфейс администратора")

    # Переменные для хранения состояния
    table_var = StringVar()
    current_table = ""

    # Фрейм для кнопок таблиц
    table_buttons_frame = Frame(root)
    table_buttons_frame.pack()

    # Обновление списка таблиц
    refresh_tables()

    # Treeview для отображения данных
    tree = ttk.Treeview(root, show="headings")
    tree.pack(fill="both", expand=True)

    # Кнопки для работы с историей
    Button(root, text="Показать историю выбранного объекта", command=show_object_history).pack()
    Button(root, text="Показать всю историю таблицы",
           command=lambda: show_table_data(table_var.get(), True)).pack()
    Button(root, text="Показать текущие данные",
           command=lambda: show_table_data(table_var.get())).pack()

    # Поле для ввода SQL-запросов
    sql_entry = Text(root, height=5, width=50)
    sql_entry.pack()

    # Кнопка для выполнения SQL-запросов
    Button(root, text="Выполнить SQL", command=execute_sql).pack()

    # Кнопка для обновления таблиц
    Button(root, text="Обновить таблицы", command=refresh_tables).pack()

    root.mainloop()


# Главное окно аутентификации
def main():
    def login():
        username = entry_username.get()
        print(username)
        password = entry_password.get()
        print(password)
        role = authenticate(username, password)
        print(role)
        if role == "user":
            user_interface()
        elif role == "admin":
            admin_interface()
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    root = Tk()
    root.title("Аутентификация")

    Label(root, text="Имя пользователя").grid(row=0, column=0)
    entry_username = Entry(root)
    entry_username.grid(row=0, column=1)

    Label(root, text="Пароль").grid(row=1, column=0)
    entry_password = Entry(root, show="*")
    entry_password.grid(row=1, column=1)

    Button(root, text="Войти", command=login).grid(row=2, column=1)

    root.mainloop()

def test_connection():
    conn = connect_to_db()
    if conn:
        print("Подключение к базе данных успешно!")
        conn.close()
    else:
        print("Не удалось подключиться к базе данных.")

if __name__ == "__main__":
    test_connection()
    main()
