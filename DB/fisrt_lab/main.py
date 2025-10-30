"""
Приложение с GUI на Flet для работы с темпоральной базой данных
ВЕРСИЯ СО СХЕМОЙ temporal_lab
"""

import flet as ft
import psycopg2
from datetime import datetime
from typing import List, Dict

class TemporalDatabase:
    """Класс для работы с темпоральной БД"""

    def __init__(self, dbname: str = 'postgres', user: str = 'postgres',
                 password: str = 'superuser', host: str = 'localhost', port: str = '5432'):
        self.connection_params = {
            'dbname': dbname,
            'user': user,
            'password': password,
            'host': host,
            'port': port
        }
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            self.cursor = self.conn.cursor()
            # Устанавливаем схему по умолчанию
            self.cursor.execute("SET search_path TO temporal_lab, public;")
            return True, f"✓ Подключение успешно (схема: temporal_lab)"
        except Exception as e:
            return False, f"✗ Ошибка подключения: {e}"

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def get_current_state(self):
        query = "SELECT * FROM temporal_lab.v_current_state;"
        try:
            self.cursor.execute(query)
            columns = [desc[0] for desc in self.cursor.description]
            results = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            return results, "✓ Данные получены"
        except Exception as e:
            return [], f"✗ Ошибка: {e}"

    def get_state_at_time(self, timestamp: str):
        query = "SELECT * FROM temporal_lab.get_state_at_time(%s);"
        try:
            self.cursor.execute(query, (timestamp,))
            columns = [desc[0] for desc in self.cursor.description]
            results = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            return results, f"✓ Состояние на {timestamp}"
        except Exception as e:
            return [], f"✗ Ошибка: {e}"

    def get_history(self, table_name: str, record_id: int):
        query = f"SELECT * FROM temporal_lab.{table_name} WHERE id = %s ORDER BY time_create;"
        try:
            self.cursor.execute(query, (record_id,))
            columns = [desc[0] for desc in self.cursor.description]
            results = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            return results, f"✓ История {table_name}.{record_id}"
        except Exception as e:
            return [], f"✗ Ошибка: {e}"

    def get_table_data(self, table_name: str):
        query = f"""
            SELECT *, 
                CASE 
                    WHEN time_dead IS NULL THEN 'ACTIVE'
                    ELSE 'ARCHIVED'
                END as status
            FROM temporal_lab.{table_name}
            ORDER BY id, time_create DESC;
        """
        try:
            self.cursor.execute(query)
            columns = [desc[0] for desc in self.cursor.description]
            results = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            return results, f"✓ Данные из {table_name}"
        except Exception as e:
            return [], f"✗ Ошибка: {e}"

    def insert_student(self, student_id: int, name: str, surname: str, birth_date: str, group_id: int):
        query = "INSERT INTO temporal_lab.students (id, name, surname, birth_date, group_id) VALUES (%s, %s, %s, %s, %s);"
        try:
            self.cursor.execute(query, (student_id, name, surname, birth_date, group_id))
            self.conn.commit()
            return True, f"✓ Студент {name} {surname} добавлен/обновлен"
        except Exception as e:
            self.conn.rollback()
            return False, f"✗ Ошибка: {e}"

    def insert_group(self, group_id: int, group_name: str, faculty: str, course: int):
        query = "INSERT INTO groups (id, group_name, faculty, course) VALUES (%s, %s, %s, %s);"
        try:
            self.cursor.execute(query, (group_id, group_name, faculty, course))
            self.conn.commit()
            return True, f"✓ Группа {group_name} добавлена/обновлена"
        except Exception as e:
            self.conn.rollback()
            return False, f"✗ Ошибка: {e}"

    def insert_teacher(self, teacher_id: int, name: str, surname: str, department: str, position: str):
        query = "INSERT INTO temporal_lab.teachers (id, name, surname, department, job_position) VALUES (%s, %s, %s, %s, %s);"
        try:
            self.cursor.execute(query, (teacher_id, name, surname, department, position))
            self.conn.commit()
            return True, f"✓ Преподаватель {name} {surname} добавлен/обновлен"
        except Exception as e:
            self.conn.rollback()
            return False, f"✗ Ошибка: {e}"

    def insert_course(self, course_id: int, course_name: str, teacher_id: int, group_id: int, semester: int):
        query = "INSERT INTO temporal_lab.courses (id, course_name, teacher_id, group_id, semester) VALUES (%s, %s, %s, %s, %s);"
        try:
            self.cursor.execute(query, (course_id, course_name, teacher_id, group_id, semester))
            self.conn.commit()
            return True, f"✓ Курс {course_name} добавлен/обновлен"
        except Exception as e:
            self.conn.rollback()
            return False, f"✗ Ошибка: {e}"


class TemporalApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.db = None
        self.setup_page()
        self.create_ui()

    def setup_page(self):
        self.page.title = "Темпоральная База Данных"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.window_width = 1400
        self.page.window_height = 900
        self.page.scroll = "adaptive"

    def create_ui(self):
        header = ft.Container(
            content=ft.Column([
                ft.Text("🗄️ Темпоральная База Данных", size=32, weight=ft.FontWeight.BOLD),
                ft.Text("Система управления версионированными данными (схема: temporal_lab)", size=16),
            ]),
            padding=20,
            bgcolor="#E3F2FD",
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )

        self.db_host = ft.TextField(label="Хост", value="localhost", width=150)
        self.db_port = ft.TextField(label="Порт", value="5432", width=100)
        self.db_name = ft.TextField(label="База данных", value="temporal_lab", width=150)
        self.db_user = ft.TextField(label="Пользователь", value="postgres", width=150)
        self.db_password = ft.TextField(label="Пароль", password=True, can_reveal_password=True, width=200)

        self.connect_btn = ft.ElevatedButton(
            "Подключиться", icon=ft.Icons.POWER, on_click=self.connect_to_db,
            bgcolor="#4CAF50", color="white"
        )

        self.disconnect_btn = ft.ElevatedButton(
            "Отключиться", icon=ft.Icons.POWER_OFF, on_click=self.disconnect_from_db,
            disabled=True, bgcolor="#F44336", color="white"
        )

        self.connection_status = ft.Text("⚪ Не подключено")

        connection_form = ft.Container(
            content=ft.Column([
                ft.Text("Параметры подключения (схема: temporal_lab)", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([self.db_host, self.db_port, self.db_name, self.db_user, self.db_password], wrap=True),
                ft.Row([self.connect_btn, self.disconnect_btn, self.connection_status]),
            ]),
            padding=20,
            border=ft.border.all(2, "#BBDEFB"),
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )

        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text="📊 Текущее состояние", content=self.create_current_state_tab()),
                ft.Tab(text="🕒 История", content=self.create_temporal_tab()),
                ft.Tab(text="👥 Студенты", content=self.create_students_tab()),
                ft.Tab(text="📚 Группы", content=self.create_groups_tab()),
                ft.Tab(text="👨‍🏫 Преподаватели", content=self.create_teachers_tab()),
                ft.Tab(text="📖 Курсы", content=self.create_courses_tab()),
                ft.Tab(text="🔐 Права доступа", content=self.create_permissions_tab()),
            ],
            expand=1,
        )

        self.page.add(header, connection_form, self.tabs)

    def create_current_state_tab(self):
        self.current_state_container = ft.Column(scroll="auto")
        self.current_state_info = ft.Text("Нажмите 'Обновить' для загрузки данных")

        refresh_btn = ft.ElevatedButton("🔄 Обновить", on_click=self.load_current_state)

        return ft.Container(
            content=ft.Column([
                ft.Row([refresh_btn, self.current_state_info]),
                ft.Container(
                    content=self.current_state_container,
                    border=ft.border.all(1, "#E0E0E0"),
                    border_radius=10,
                    padding=10,
                    height=600,
                )
            ]),
            padding=20,
        )

    def create_temporal_tab(self):
        self.temporal_date = ft.TextField(
            label="Дата и время (YYYY-MM-DD HH:MM:SS)",
            value="2025-10-14 05:30:00",
            width=300
        )

        load_at_time_btn = ft.ElevatedButton("📅 Загрузить состояние на дату", on_click=self.load_state_at_time)

        self.history_table = ft.Dropdown(
            label="Таблица",
            options=[
                ft.dropdown.Option("students"),
                ft.dropdown.Option("groups"),
                ft.dropdown.Option("teachers"),
                ft.dropdown.Option("courses"),
            ],
            value="students",
            width=200
        )

        self.history_id = ft.TextField(label="ID записи", value="1", width=150)
        load_history_btn = ft.ElevatedButton("📜 Загрузить историю", on_click=self.load_history)

        self.temporal_result_container = ft.Column(scroll="auto")
        self.temporal_info = ft.Text("")

        return ft.Container(
            content=ft.Column([
                ft.Text("Состояние на определенную дату", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([self.temporal_date, load_at_time_btn]),
                ft.Divider(height=20),
                ft.Text("История изменений записи", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([self.history_table, self.history_id, load_history_btn]),
                self.temporal_info,
                ft.Container(
                    content=self.temporal_result_container,
                    border=ft.border.all(1, "#E0E0E0"),
                    border_radius=10,
                    padding=10,
                    height=500,
                )
            ]),
            padding=20,
        )

    def create_students_tab(self):
        self.student_id = ft.TextField(label="ID", width=100)
        self.student_name = ft.TextField(label="Имя", width=200)
        self.student_surname = ft.TextField(label="Фамилия", width=200)
        self.student_birth_date = ft.TextField(label="Дата рождения (YYYY-MM-DD)", width=200)
        self.student_group_id = ft.TextField(label="ID группы", width=150)

        add_student_btn = ft.ElevatedButton(
            "➕ Добавить/Обновить", on_click=self.add_student, bgcolor="#4CAF50", color="white"
        )
        load_students_btn = ft.ElevatedButton("🔄 Загрузить всех", on_click=self.load_students)

        self.students_container = ft.Column(scroll="auto")
        self.students_info = ft.Text("")

        return ft.Container(
            content=ft.Column([
                ft.Text("Управление студентами", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    self.student_id, self.student_name, self.student_surname,
                    self.student_birth_date, self.student_group_id
                ], wrap=True),
                ft.Row([add_student_btn, load_students_btn]),
                self.students_info,
                ft.Container(
                    content=self.students_container,
                    border=ft.border.all(1, "#E0E0E0"),
                    border_radius=10,
                    padding=10,
                    height=450,
                )
            ]),
            padding=20,
        )

    def create_groups_tab(self):
        self.group_id = ft.TextField(label="ID", width=100)
        self.group_name = ft.TextField(label="Название", width=200)
        self.group_faculty = ft.TextField(label="Факультет", width=300)
        self.group_course = ft.TextField(label="Курс", width=100)

        add_group_btn = ft.ElevatedButton("➕ Добавить/Обновить", on_click=self.add_group, bgcolor="#4CAF50", color="white")
        load_groups_btn = ft.ElevatedButton("🔄 Загрузить все", on_click=self.load_groups)

        self.groups_container = ft.Column(scroll="auto")
        self.groups_info = ft.Text("")

        return ft.Container(
            content=ft.Column([
                ft.Text("Управление группами", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([self.group_id, self.group_name, self.group_faculty, self.group_course]),
                ft.Row([add_group_btn, load_groups_btn]),
                self.groups_info,
                ft.Container(content=self.groups_container, border=ft.border.all(1, "#E0E0E0"), border_radius=10, padding=10, height=450)
            ]),
            padding=20,
        )

    def create_teachers_tab(self):
        self.teacher_id = ft.TextField(label="ID", width=100)
        self.teacher_name = ft.TextField(label="Имя", width=200)
        self.teacher_surname = ft.TextField(label="Фамилия", width=200)
        self.teacher_department = ft.TextField(label="Кафедра", width=250)
        self.teacher_position = ft.TextField(label="Должность", width=200)

        add_teacher_btn = ft.ElevatedButton("➕ Добавить/Обновить", on_click=self.add_teacher, bgcolor="#4CAF50", color="white")
        load_teachers_btn = ft.ElevatedButton("🔄 Загрузить всех", on_click=self.load_teachers)

        self.teachers_container = ft.Column(scroll="auto")
        self.teachers_info = ft.Text("")

        return ft.Container(
            content=ft.Column([
                ft.Text("Управление преподавателями", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([self.teacher_id, self.teacher_name, self.teacher_surname, self.teacher_department, self.teacher_position], wrap=True),
                ft.Row([add_teacher_btn, load_teachers_btn]),
                self.teachers_info,
                ft.Container(content=self.teachers_container, border=ft.border.all(1, "#E0E0E0"), border_radius=10, padding=10, height=450)
            ]),
            padding=20,
        )

    def create_courses_tab(self):
        self.course_id = ft.TextField(label="ID", width=100)
        self.course_name = ft.TextField(label="Название", width=300)
        self.course_teacher_id = ft.TextField(label="ID преподавателя", width=150)
        self.course_group_id = ft.TextField(label="ID группы", width=150)
        self.course_semester = ft.TextField(label="Семестр", width=100)

        add_course_btn = ft.ElevatedButton("➕ Добавить/Обновить", on_click=self.add_course, bgcolor="#4CAF50", color="white")
        load_courses_btn = ft.ElevatedButton("🔄 Загрузить все", on_click=self.load_courses)

        self.courses_container = ft.Column(scroll="auto")
        self.courses_info = ft.Text("")

        return ft.Container(
            content=ft.Column([
                ft.Text("Управление курсами", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([self.course_id, self.course_name, self.course_teacher_id, self.course_group_id, self.course_semester], wrap=True),
                ft.Row([add_course_btn, load_courses_btn]),
                self.courses_info,
                ft.Container(content=self.courses_container, border=ft.border.all(1, "#E0E0E0"), border_radius=10, padding=10, height=450)
            ]),
            padding=20,
        )

    def create_permissions_tab(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("🔐 Система разграничения прав доступа", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),
                ft.Container(
                    content=ft.Column([
                        ft.Text("👤 Администратор (postgres)", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("✓ Полный доступ ко всем таблицам в схеме temporal_lab", color="#2E7D32"),
                        ft.Text("✓ Чтение и изменение всех данных", color="#2E7D32"),
                    ]),
                    padding=20, bgcolor="#E8F5E9", border_radius=10, margin=ft.margin.only(bottom=10)
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("👤 Редактор (editor_user / editor_password)", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("✓ Чтение всех таблиц", color="#1976D2"),
                        ft.Text("✓ Изменение только таблицы students", color="#1976D2"),
                    ]),
                    padding=20, bgcolor="#E3F2FD", border_radius=10, margin=ft.margin.only(bottom=10)
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text("👤 Читатель (reader_user / reader_password)", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("✓ Только чтение всех таблиц", color="#F57C00"),
                        ft.Text("✗ Любые изменения запрещены", color="#C62828"),
                    ]),
                    padding=20, bgcolor="#FFF3E0", border_radius=10
                ),
            ], scroll="auto"),
            padding=20,
        )

    def connect_to_db(self, e):
        self.db = TemporalDatabase(
            self.db_name.value, self.db_user.value, self.db_password.value,
            self.db_host.value, self.db_port.value
        )
        success, message = self.db.connect()

        if success:
            self.connection_status.value = f"🟢 {message}"
            self.connect_btn.disabled = True
            self.disconnect_btn.disabled = False
            self.show_snackbar("Подключено к схеме temporal_lab!", "#4CAF50")
        else:
            self.connection_status.value = f"🔴 {message}"
            self.show_snackbar("Ошибка подключения!", "#F44336")
        self.page.update()

    def disconnect_from_db(self, e):
        if self.db:
            self.db.disconnect()
        self.connection_status.value = "⚪ Не подключено"
        self.connect_btn.disabled = False
        self.disconnect_btn.disabled = True
        self.show_snackbar("Отключено", "#2196F3")
        self.page.update()

    def load_current_state(self, e):
        if not self.check_connection():
            return
        results, message = self.db.get_current_state()
        self.current_state_info.value = message
        self.populate_container(self.current_state_container, results)
        self.page.update()

    def load_state_at_time(self, e):
        if not self.check_connection():
            return
        results, message = self.db.get_state_at_time(self.temporal_date.value)
        self.temporal_info.value = message
        self.populate_container(self.temporal_result_container, results)
        self.page.update()

    def load_history(self, e):
        if not self.check_connection():
            return
        try:
            record_id = int(self.history_id.value)
        except:
            self.show_snackbar("Введите корректный ID!", "#F44336")
            return
        results, message = self.db.get_history(self.history_table.value, record_id)
        self.temporal_info.value = message
        self.populate_container(self.temporal_result_container, results)
        self.page.update()

    def add_student(self, e):
        if not self.check_connection():
            return
        try:
            success, message = self.db.insert_student(
                int(self.student_id.value), self.student_name.value,
                self.student_surname.value, self.student_birth_date.value,
                int(self.student_group_id.value)
            )
            self.students_info.value = message
            if success:
                self.show_snackbar(message, "#4CAF50")
                self.clear_student_fields()
        except ValueError:
            self.show_snackbar("ID должны быть числами!", "#F44336")
        self.page.update()

    def load_students(self, e):
        if not self.check_connection():
            return
        results, message = self.db.get_table_data('students')
        self.students_info.value = message
        self.populate_container(self.students_container, results)
        self.page.update()

    def add_group(self, e):
        if not self.check_connection():
            return
        try:
            success, message = self.db.insert_group(
                int(self.group_id.value), self.group_name.value,
                self.group_faculty.value, int(self.group_course.value)
            )
            self.groups_info.value = message
            if success:
                self.show_snackbar(message, "#4CAF50")
                self.clear_group_fields()
        except ValueError:
            self.show_snackbar("ID и курс должны быть числами!", "#F44336")
        self.page.update()

    def load_groups(self, e):
        if not self.check_connection():
            return
        results, message = self.db.get_table_data('groups')
        self.groups_info.value = message
        self.populate_container(self.groups_container, results)
        self.page.update()

    def add_teacher(self, e):
        if not self.check_connection():
            return
        try:
            success, message = self.db.insert_teacher(
                int(self.teacher_id.value), self.teacher_name.value,
                self.teacher_surname.value, self.teacher_department.value,
                self.teacher_position.value
            )
            self.teachers_info.value = message
            if success:
                self.show_snackbar(message, "#4CAF50")
                self.clear_teacher_fields()
        except ValueError:
            self.show_snackbar("ID должен быть числом!", "#F44336")
        self.page.update()

    def load_teachers(self, e):
        if not self.check_connection():
            return
        results, message = self.db.get_table_data('teachers')
        self.teachers_info.value = message
        self.populate_container(self.teachers_container, results)
        self.page.update()

    def add_course(self, e):
        if not self.check_connection():
            return
        try:
            success, message = self.db.insert_course(
                int(self.course_id.value), self.course_name.value,
                int(self.course_teacher_id.value), int(self.course_group_id.value),
                int(self.course_semester.value)
            )
            self.courses_info.value = message
            if success:
                self.show_snackbar(message, "#4CAF50")
                self.clear_course_fields()
        except ValueError:
            self.show_snackbar("ID и семестр должны быть числами!", "#F44336")
        self.page.update()

    def load_courses(self, e):
        if not self.check_connection():
            return
        results, message = self.db.get_table_data('courses')
        self.courses_info.value = message
        self.populate_container(self.courses_container, results)
        self.page.update()

    def populate_container(self, container: ft.Column, data: List[Dict]):
        container.controls.clear()

        if not data:
            container.controls.append(ft.Text("Нет данных для отображения", color="#757575"))
            return

        columns = list(data[0].keys())
        table = ft.DataTable(
            columns=[ft.DataColumn(ft.Text(col, weight=ft.FontWeight.BOLD, size=11)) for col in columns],
            rows=[],
            border=ft.border.all(1, "#BDBDBD"),
            border_radius=10,
            heading_row_color="#E3F2FD",
        )

        for row_data in data:
            cells = []
            for col in columns:
                value = row_data[col]
                if value is None:
                    display_value, color = "NULL", "#9E9E9E"
                elif col == 'status':
                    display_value = str(value)
                    color = "#2E7D32" if value == 'ACTIVE' else "#C62828"
                elif isinstance(value, datetime):
                    display_value = value.strftime('%Y-%m-%d %H:%M:%S')
                    color = "#000000"
                else:
                    display_value, color = str(value), "#000000"
                cells.append(ft.DataCell(ft.Text(display_value, color=color, size=11)))
            table.rows.append(ft.DataRow(cells=cells))

        container.controls.append(table)

    def check_connection(self):
        if not self.db:
            self.show_snackbar("Сначала подключитесь к БД!", "#F44336")
            return False
        return True

    def show_snackbar(self, message: str, bgcolor: str):
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message, color="white"), bgcolor=bgcolor)
        self.page.snack_bar.open = True
        self.page.update()

    def clear_student_fields(self):
        self.student_id.value = ""
        self.student_name.value = ""
        self.student_surname.value = ""
        self.student_birth_date.value = ""
        self.student_group_id.value = ""

    def clear_group_fields(self):
        self.group_id.value = ""
        self.group_name.value = ""
        self.group_faculty.value = ""
        self.group_course.value = ""

    def clear_teacher_fields(self):
        self.teacher_id.value = ""
        self.teacher_name.value = ""
        self.teacher_surname.value = ""
        self.teacher_department.value = ""
        self.teacher_position.value = ""

    def clear_course_fields(self):
        self.course_id.value = ""
        self.course_name.value = ""
        self.course_teacher_id.value = ""
        self.course_group_id.value = ""
        self.course_semester.value = ""


def main(page: ft.Page):
    TemporalApp(page)

if __name__ == "__main__":
    ft.app(target=main)