# -*- coding: utf-8 -*-
from pymongo import MongoClient
import json
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from bson import ObjectId
from datetime import datetime


class DocumentDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Document Database Client")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")

        self.db_params = {
            'host': 'localhost',
            'port': 27017,
            'database': 'DocumentDB'
        }

        self.client = None
        self.db = None
        self.connect_to_db()

        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()

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
            self.client = MongoClient(self.db_params['host'], self.db_params['port'])
            self.db = self.client[self.db_params['database']]
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
            documents = self.db.documents.find().sort("_id")

            # Очищаем текущие данные
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Добавляем новые данные
            for doc in documents:
                self.tree.insert('', tk.END,
                                 values=(str(doc['_id']), doc['doc_type'], doc['created_at'], doc['updated_at']))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load documents: {e}")

    def show_document_details(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0])
        doc_id = ObjectId(item['values'][0])

        try:
            document = self.db.documents.find_one({"_id": doc_id})
            self.detail_text.delete(1.0, tk.END)
            self.detail_text.insert(tk.END, json.dumps(document, indent=2, default=str))
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
            document = {
                "doc_type": doc_type,
                "data": data,
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            result = self.db.documents.insert_one(document)
            messagebox.showinfo("Success", f"Document created with ID: {result.inserted_id}")
            self.load_documents()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create document: {e}")

    def search_documents(self):
        # Упрощенный поиск только по типу документа
        doc_type = simpledialog.askstring("Search Documents", "Enter document type to search:")
        if not doc_type:
            return

        try:
            documents = self.db.documents.find({"doc_type": doc_type}).sort("_id")

            # Очищаем текущие данные
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Добавляем найденные документы
            for doc in documents:
                self.tree.insert('', tk.END,
                                 values=(str(doc['_id']), doc['doc_type'], doc['created_at'], doc['updated_at']))

            messagebox.showinfo("Info", f"Found {documents.count()} documents of type '{doc_type}'")
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

    def update_document(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a document to update")
            return

        item = self.tree.item(selected_item[0])
        doc_id = ObjectId(item['values'][0])

        try:
            document = self.db.documents.find_one({"_id": doc_id})

            # Запрашиваем новые данные
            new_type = simpledialog.askstring("Document Type", "Enter new document type:",
                                              initialvalue=document['doc_type'])
            if not new_type:
                return

            new_data = simpledialog.askstring("Document Data", "Enter new JSON data:",
                                              initialvalue=json.dumps(document['data'], indent=2))
            if not new_data:
                return

            try:
                parsed_data = json.loads(new_data)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Invalid JSON format")
                return

            # Обновляем документ
            self.db.documents.update_one(
                {"_id": doc_id},
                {"$set": {
                    "doc_type": new_type,
                    "data": parsed_data,
                    "updated_at": datetime.now()
                }}
            )
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
        doc_id = ObjectId(item['values'][0])

        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete document #{doc_id}?"):
            return

        try:
            self.db.documents.delete_one({"_id": doc_id})
            messagebox.showinfo("Success", "Document deleted successfully")
            self.load_documents()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete document: {e}")

    def export_to_json(self):
        try:
            documents = self.db.documents.find().sort("_id")

            # Формируем JSON
            docs_list = []
            for doc in documents:
                doc['_id'] = str(doc['_id'])
                docs_list.append(doc)

            # Сохраняем JSON в файл
            file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
            if file_path:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(docs_list, f, indent=4, default=str)
                messagebox.showinfo("Success", f"Documents exported to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export documents: {e}")

    def __del__(self):
        if self.client:
            self.client.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = DocumentDBApp(root)
    root.mainloop()
