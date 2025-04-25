# -*- coding: utf-8 -*-
import psycopg2
from psycopg2.extras import Json
import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog


class DocumentDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Database Client")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")  # Темно-синий фон окна

        # Параметры подключения к БД
        self.db_params = {
            'dbname': 'DocumentDB',
            'user': 'postgres',
            'password': 'superuser',
            'host': 'localhost',
            'port': '5432'
        }

        self.conn = None
        self.connect_to_db()

        # Настройка стилей
        self.setup_styles()

        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()

        # Общий стиль фреймов
        style.configure("Main.TFrame", background="#34495e")  # Темно-серый фон
        style.configure("Action.TFrame", background="#34495e")
        style.configure("View.TFrame", background="#34495e")
        style.configure("Detail.TFrame", background="#34495e")

        # Стиль кнопок
        style.configure("Action.TButton", background="#1abc9c", foreground="black", font=("Arial", 10, "bold"))
        style.configure("Export.TButton", background="#e74c3c", foreground="black", font=("Arial", 10, "bold"))

        # Стиль текстового поля
        style.configure("Detail.TText", background="#ecf0f1", foreground="#2c3e50", font=("Arial", 10))

        # Стиль таблицы
        style.configure("Treeview", background="#ecf0f1", foreground="#2c3e50", rowheight=25, fieldbackground="#ecf0f1")
        style.map("Treeview", background=[("selected", "#1abc9c")])  # Цвет выделенной строки

    def connect_to_db(self):
        try:
            self.conn = psycopg2.connect(**self.db_params)
            messagebox.showinfo("Success", "Connected to database successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to database: {e}")

    def setup_ui(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10", style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Панель действий
        action_frame = ttk.LabelFrame(main_frame, text="Actions", padding="10", style="Action.TFrame")
        action_frame.pack(fill=tk.X, pady=5)

        ttk.Button(action_frame, text="Create Document", command=self.create_document, style="Action.TButton").pack(
            side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Search by Type", command=self.search_documents, style="Action.TButton").pack(
            side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Update Document", command=self.update_document, style="Action.TButton").pack(
            side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Delete Document", command=self.delete_document, style="Action.TButton").pack(
            side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Show All", command=self.load_documents, style="Action.TButton").pack(
            side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Export to JSON", command=self.export_to_json, style="Export.TButton").pack(
            side=tk.LEFT, padx=5)

        # Панель просмотра
        view_frame = ttk.LabelFrame(main_frame, text="Documents", padding="10", style="View.TFrame")
        view_frame.pack(fill=tk.BOTH, expand=True)

        # Таблица для отображения документов
        self.tree = ttk.Treeview(view_frame, columns=('ID', 'Type', 'Created', 'Updated'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Type', text='Type')
        self.tree.heading('Created', text='Created')
        self.tree.heading('Updated', text='Updated')
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Детали документа
        detail_frame = ttk.LabelFrame(main_frame, text="Document Details", padding="10", style="Detail.TFrame")
        detail_frame.pack(fill=tk.BOTH, pady=5)

        self.detail_text = tk.Text(detail_frame, height=10, bg="#ecf0f1", fg="#2c3e50", font=("Arial", 10))
        self.detail_text.pack(fill=tk.BOTH, expand=True)

        # Привязка события выбора документа
        self.tree.bind('<<TreeviewSelect>>', self.show_document_details)

        # Загружаем документы при старте
        self.load_documents()

    def load_documents(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, doc_type, created_at, updated_at FROM documents ORDER BY id")
                rows = cur.fetchall()

                # Очищаем текущие данные
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Добавляем новые данные
                for row in rows:
                    self.tree.insert('', tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load documents: {e}")

    def show_document_details(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0])
        doc_id = item['values'][0]

        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT data FROM documents WHERE id = %s", (doc_id,))
                data = cur.fetchone()[0]

                self.detail_text.delete(1.0, tk.END)
                self.detail_text.insert(tk.END, json.dumps(data, indent=2))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load document details: {e}")

    def create_document(self):
        try:
            # Запрашиваем тип документа
            doc_type = simpledialog.askstring("Document Type", "Enter document type:")
            if not doc_type:
                return

            # Запрашиваем JSON данные
            json_data = simpledialog.askstring("Document Data", "Enter JSON data:")
            if not json_data:
                return

            try:
                data = json.loads(json_data)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON format")
                return

            # Сохраняем документ в БД
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO documents (doc_type, data) VALUES (%s, %s) RETURNING id",
                    (doc_type, Json(data)))

                doc_id = cur.fetchone()[0]
                self.conn.commit()

                messagebox.showinfo("Success", f"Document created with ID: {doc_id}")
                self.load_documents()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create document: {e}")

    def search_documents(self):
        # Упрощенный поиск только по типу документа
        doc_type = simpledialog.askstring("Search Documents", "Enter document type to search:")
        if not doc_type:
            return

        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    "SELECT id, doc_type, created_at, updated_at FROM documents WHERE doc_type = %s ORDER BY id",
                    (doc_type,))
                rows = cur.fetchall()

                # Очищаем текущие данные
                for item in self.tree.get_children():
                    self.tree.delete(item)

                # Добавляем найденные документы
                for row in rows:
                    self.tree.insert('', tk.END, values=row)

                messagebox.showinfo("Info", f"Found {len(rows)} documents of type '{doc_type}'")
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

    def update_document(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a document to update")
            return

        item = self.tree.item(selected_item[0])
        doc_id = item['values'][0]

        try:
            with self.conn.cursor() as cur:
                # Получаем текущие данные документа
                cur.execute("SELECT doc_type, data FROM documents WHERE id = %s", (doc_id,))
                doc_type, data = cur.fetchone()

                # Запрашиваем новые данные
                new_type = simpledialog.askstring("Document Type", "Enter new document type:", initialvalue=doc_type)
                if not new_type:
                    return

                new_data = simpledialog.askstring("Document Data", "Enter new JSON data:",
                                                  initialvalue=json.dumps(data, indent=2))
                if not new_data:
                    return

                try:
                    parsed_data = json.loads(new_data)
                except json.JSONDecodeError:
                    messagebox.showerror("Error", "Invalid JSON format")
                    return

                # Обновляем документ
                cur.execute(
                    "UPDATE documents SET doc_type = %s, data = %s WHERE id = %s",
                    (new_type, Json(parsed_data), doc_id))
                self.conn.commit()

                messagebox.showinfo("Success", "Document updated successfully")
                self.load_documents()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update document: {e}")

    def delete_document(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a document to delete")
            return

        item = self.tree.item(selected_item[0])
        doc_id = item['values'][0]

        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete document #{doc_id}?"):
            return

        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM documents WHERE id = %s", (doc_id,))
                self.conn.commit()

                messagebox.showinfo("Success", "Document deleted successfully")
                self.load_documents()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete document: {e}")

    def export_to_json(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT id, doc_type, data, created_at, updated_at, tags 
                    FROM documents 
                    ORDER BY id
                """)
                rows = cur.fetchall()

                # Формируем JSON
                documents = []
                for row in rows:
                    doc_id, doc_type, data, created_at, updated_at, tags = row
                    documents.append({
                        "id": doc_id,
                        "type": doc_type,
                        "data": data,
                        "created_at": str(created_at),
                        "updated_at": str(updated_at),
                        "tags": tags
                    })

                # Сохраняем JSON в файл
                file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
                if file_path:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(documents, f, indent=4)
                    messagebox.showinfo("Success", f"Documents exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export documents: {e}")

    def __del__(self):
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentDBApp(root)
    root.mainloop()