from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from src.database import DB_Settings

class MainWindow(QMainWindow):
    def __init__(self, user_data=None):  # Изменяем параметр на user_data
        super().__init__()
        # Устанавливаем значения по умолчанию
        self.user_data = user_data or {
            'id': 0,
            'username': 'Гость',
            'full_name': 'Иванов И.И.',
            'role': 'student'
        }
        self.setup_ui()




    def setup_ui(self):
        # Используем реальные данные пользователя
        self.setWindowTitle(f"SmartУчеба - {self.user_data['full_name']} ({self.user_data['role'].capitalize()})")
        self.setFixedSize(1200, 800)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QHBoxLayout(central_widget)

        # Боковое меню с реальными данными пользователя
        self.setup_sidebar()

        # Рабочая область
        self.workspace = QStackedWidget()
        self.layout.addWidget(self.workspace, stretch=5)

        # Настройка интерфейсов для разных ролей
        if self.user_data['role'] == "admin":
            self.setup_admin_workspace()
        elif self.user_data['role'] == "teacher":
            self.setup_teacher_workspace()
        else:
            self.setup_student_workspace()

        # Применение стилей
        self.setup_styles()

    def setup_sidebar(self):
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        sidebar_layout = QVBoxLayout(sidebar)

        # Используем реальные данные пользователя
        user_info = QLabel(f"{self.user_data['full_name']}\n{self.user_data['role'].capitalize()}")
        user_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(user_info)

        buttons = [
            ("Расписание", self.show_schedule),
            ("Нагрузка", self.show_workload),
            ("Отчеты", self.show_reports),
            ("Настройки", self.show_settings)
        ]

        for text, handler in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            sidebar_layout.addWidget(btn)

        # Кнопка выхода
        sidebar_layout.addStretch()
        logout_btn = QPushButton("Выход")
        logout_btn.clicked.connect(self.close)
        sidebar_layout.addWidget(logout_btn)

        self.layout.addWidget(sidebar, stretch=1)

    def setup_admin_workspace(self):
        tabs = QTabWidget()

        # Вкладка дашборда
        dashboard_tab = QWidget()
        grid = QGridLayout(dashboard_tab)

        # Heatmap аудиторий
        grid.addWidget(QLabel("Загрузка аудиторий"), 0, 0)
        self.room_heatmap = QLabel("График будет здесь")
        grid.addWidget(self.room_heatmap, 1, 0)

        # Список конфликтов
        grid.addWidget(QLabel("Текущие конфликты"), 0, 1)
        self.conflict_list = QListWidget()
        self.conflict_list.addItems(["Конфликт 1", "Конфликт 2"])
        grid.addWidget(self.conflict_list, 1, 1)

        # Кнопки управления
        btn_generate = QPushButton("Сгенерировать расписание")
        btn_generate.clicked.connect(self.generate_schedule)
        grid.addWidget(btn_generate, 2, 0, 1, 2)

        tabs.addTab(dashboard_tab, "Дашборд")
        self.workspace.addWidget(tabs)

    def setup_teacher_workspace(self):
        container = QWidget()
        layout = QVBoxLayout(container)

        # Календарь
        self.calendar = QCalendarWidget()
        layout.addWidget(self.calendar)

        # Таблица занятий
        self.lessons_table = QTableWidget()
        self.lessons_table.setColumnCount(4)
        self.lessons_table.setHorizontalHeaderLabels(["Дата", "Дисциплина", "Аудитория", "Тип"])
        self.lessons_table.setRowCount(3)
        for i in range(3):
            self.lessons_table.setItem(i, 0, QTableWidgetItem(f"01.0{i + 1}.2023"))
            self.lessons_table.setItem(i, 1, QTableWidgetItem(["Маркетинг", "Финансы", "Менеджмент"][i]))
            self.lessons_table.setItem(i, 2, QTableWidgetItem(f"Ауд. {i + 100}"))
            self.lessons_table.setItem(i, 3, QTableWidgetItem(["Лекция", "Семинар", "Практика"][i]))
        layout.addWidget(self.lessons_table)

        # Кнопка запроса
        btn_request = QPushButton("Запрос изменения")
        btn_request.clicked.connect(self.show_request_dialog)
        layout.addWidget(btn_request)

        self.workspace.addWidget(container)

    def setup_student_workspace(self):
        splitter = QSplitter(Qt.Orientation.Vertical)  # Исправлено здесь

        # Панель фильтров
        filter_panel = QWidget()
        filter_layout = QHBoxLayout(filter_panel)
        filter_layout.addWidget(QLabel("Группа:"))
        self.group_combo = QComboBox()
        self.group_combo.addItems(["Бизнес-101", "Бизнес-102", "Маркетинг-201"])
        filter_layout.addWidget(self.group_combo)
        splitter.addWidget(filter_panel)

        # Таблица расписания
        self.schedule_table = QTableWidget(6, 5)  # 6 пар, 5 дней
        self.schedule_table.setHorizontalHeaderLabels(["Пн", "Вт", "Ср", "Чт", "Пт"])
        self.schedule_table.setVerticalHeaderLabels([f"{i + 1}. 9:00-10:30" for i in range(6)])
        splitter.addWidget(self.schedule_table)

        self.workspace.addWidget(splitter)

    def setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
                font-family: Arial;
            }
            QPushButton {
                padding: 8px;
                background: #3f51b5;
                color: white;
                border: none;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #5c6bc0;
            }
            QTableWidget {
                gridline-color: #e0e0e0;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #e3f2fd;
                padding: 5px;
                border: none;
            }
            QFrame {
                background: white;
                border-right: 1px solid #ddd;
            }
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
            }
        """)

    def show_schedule(self):
        QMessageBox.information(self, "Навигация", "Переход в раздел расписания")

    def show_workload(self):
        """Отображение нагрузки пользователя"""
        try:
            with DB_Settings.get_connection() as conn:
                with conn.cursor() as cursor:
                    if self.user_data['role'] == 'teacher':
                        # Для преподавателя
                        cursor.execute("""
                            SELECT s.SubjectName, w.Hours, g.GroupName, w.LessonType 
                            FROM TeacherWorkload w
                            JOIN Subject s ON w.SubjectId = s.SubjectId
                            JOIN StudentGroup g ON w.GroupId = g.GroupId
                            WHERE w.TeacherId = %s AND w.AcademicYear = '2023-2024'
                            """, (self.user_data['id'],))

                        workload_data = cursor.fetchall()

                        dialog = QDialog(self)
                        dialog.setWindowTitle(f"Нагрузка преподавателя {self.user_data['full_name']}")
                        dialog.resize(800, 400)

                        layout = QVBoxLayout(dialog)

                        # Таблица с нагрузкой
                        table = QTableWidget()
                        table.setColumnCount(4)
                        table.setHorizontalHeaderLabels(["Дисциплина", "Часы", "Группа", "Тип занятия"])
                        table.setRowCount(len(workload_data))

                        total_hours = 0
                        for row, (subject, hours, group, lesson_type) in enumerate(workload_data):
                            table.setItem(row, 0, QTableWidgetItem(subject))
                            table.setItem(row, 1, QTableWidgetItem(str(hours)))
                            table.setItem(row, 2, QTableWidgetItem(group))
                            table.setItem(row, 3, QTableWidgetItem(lesson_type))
                            total_hours += hours

                        layout.addWidget(table)

                        # Суммарная нагрузка
                        lbl_total = QLabel(f"Общая нагрузка: {total_hours} часов")
                        layout.addWidget(lbl_total)

                        # Кнопка закрытия
                        btn_close = QPushButton("Закрыть")
                        btn_close.clicked.connect(dialog.close)
                        layout.addWidget(btn_close)

                        dialog.exec()

                    elif self.user_data['role'] == 'admin':
                        # Для администратора - сводная нагрузка
                        cursor.execute("""
                            SELECT u.Username, COUNT(w.WorkloadId) as SubjectsCount, 
                                   SUM(w.Hours) as TotalHours
                            FROM TeacherWorkload w
                            JOIN user u ON w.TeacherId = u.userId
                            WHERE w.AcademicYear = '2023-2024'
                            GROUP BY u.Username
                            """)

                        workload_data = cursor.fetchall()

                        dialog = QDialog(self)
                        dialog.setWindowTitle("Нагрузка преподавателей (2023-2024)")
                        dialog.resize(600, 400)

                        layout = QVBoxLayout(dialog)

                        table = QTableWidget()
                        table.setColumnCount(3)
                        table.setHorizontalHeaderLabels(["Преподаватель", "Кол-во дисциплин", "Всего часов"])
                        table.setRowCount(len(workload_data))

                        for row, (teacher, subjects, hours) in enumerate(workload_data):
                            table.setItem(row, 0, QTableWidgetItem(teacher))
                            table.setItem(row, 1, QTableWidgetItem(str(subjects)))
                            table.setItem(row, 2, QTableWidgetItem(str(hours)))

                        layout.addWidget(table)

                        # Кнопка закрытия
                        btn_close = QPushButton("Закрыть")
                        btn_close.clicked.connect(dialog.close)
                        layout.addWidget(btn_close)

                        dialog.exec()

                    else:
                        QMessageBox.information(self, "Нагрузка",
                                                "Функция доступна только преподавателям и администраторам")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные о нагрузке: {str(e)}")

    def show_reports(self):
        """Отображение отчетов в зависимости от роли пользователя"""
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle(f"Отчеты - {self.user_data['full_name']}")
            dialog.resize(1000, 700)

            layout = QVBoxLayout(dialog)
            tab_widget = QTabWidget()

            # 1. Общие отчеты (для всех пользователей)
            self.add_general_reports_tab(tab_widget)

            # 2. Отчеты для преподавателей
            if self.user_data['role'] == 'teacher':
                self.add_teacher_reports_tab(tab_widget)

            # 3. Отчеты для администраторов
            if self.user_data['role'] == 'admin':
                self.add_admin_reports_tab(tab_widget)

            layout.addWidget(tab_widget)
            dialog.exec()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сформировать отчеты: {str(e)}")

    def add_general_reports_tab(self, tab_widget):
        """Общие отчеты доступные всем пользователям"""
        # 1. Отчет по группам
        group_widget = QWidget()
        group_layout = QVBoxLayout(group_widget)

        with DB_Settings.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT g.GroupName, g.Specialization, COUNT(u.UserId) as StudentCount
                    FROM StudentGroup g
                    LEFT JOIN user u ON g.GroupId = u.GroupId AND u.UserPositionId = 2
                    GROUP BY g.GroupId
                    ORDER BY g.GroupName
                """)
                group_data = cursor.fetchall()

                group_table = QTableWidget()
                group_table.setColumnCount(3)
                group_table.setHorizontalHeaderLabels(["Группа", "Специализация", "Студентов"])
                group_table.setRowCount(len(group_data))

                for row, (group, spec, count) in enumerate(group_data):
                    group_table.setItem(row, 0, QTableWidgetItem(group))
                    group_table.setItem(row, 1, QTableWidgetItem(spec if spec else "-"))
                    group_table.setItem(row, 2, QTableWidgetItem(str(count)))

                group_layout.addWidget(group_table)

        tab_widget.addTab(group_widget, "Группы")

        # 2. Отчет по аудиториям
        classroom_widget = QWidget()
        classroom_layout = QVBoxLayout(classroom_widget)

        with DB_Settings.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT c.RoomNumber, c.Capacity, c.RoomType, 
                           COUNT(s.ScheduleId) as LessonsCount
                    FROM Classroom c
                    LEFT JOIN Schedule s ON c.ClassroomId = s.ClassroomId
                    GROUP BY c.ClassroomId
                """)
                classroom_data = cursor.fetchall()

                classroom_table = QTableWidget()
                classroom_table.setColumnCount(4)
                classroom_table.setHorizontalHeaderLabels(["Аудитория", "Вместимость", "Тип", "Занятий"])
                classroom_table.setRowCount(len(classroom_data))

                for row, (room, capacity, room_type, lessons) in enumerate(classroom_data):
                    classroom_table.setItem(row, 0, QTableWidgetItem(room))
                    classroom_table.setItem(row, 1, QTableWidgetItem(str(capacity)))
                    classroom_table.setItem(row, 2, QTableWidgetItem(room_type))
                    classroom_table.setItem(row, 3, QTableWidgetItem(str(lessons)))

                classroom_layout.addWidget(classroom_table)

        tab_widget.addTab(classroom_widget, "Аудитории")

    def add_teacher_reports_tab(self, tab_widget):
        """Отчеты для преподавателей"""
        # 1. Отчет по нагрузке преподавателя
        workload_widget = QWidget()
        workload_layout = QVBoxLayout(workload_widget)

        with DB_Settings.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT s.SubjectName, g.GroupName, w.Hours, w.LessonType, w.Semester, w.AcademicYear
                    FROM TeacherWorkload w
                    JOIN Subject s ON w.SubjectId = s.SubjectId
                    JOIN StudentGroup g ON w.GroupId = g.GroupId
                    WHERE w.TeacherId = %s
                    ORDER BY w.AcademicYear, w.Semester
                """, (self.user_data['id'],))

                workload_data = cursor.fetchall()

                workload_table = QTableWidget()
                workload_table.setColumnCount(6)
                workload_table.setHorizontalHeaderLabels(["Предмет", "Группа", "Часы", "Тип", "Семестр", "Учебный год"])
                workload_table.setRowCount(len(workload_data))

                total_hours = 0
                for row, (subject, group, hours, lesson_type, semester, year) in enumerate(workload_data):
                    workload_table.setItem(row, 0, QTableWidgetItem(subject))
                    workload_table.setItem(row, 1, QTableWidgetItem(group))
                    workload_table.setItem(row, 2, QTableWidgetItem(str(hours)))
                    workload_table.setItem(row, 3, QTableWidgetItem(lesson_type))
                    workload_table.setItem(row, 4, QTableWidgetItem(str(semester)))
                    workload_table.setItem(row, 5, QTableWidgetItem(year))
                    total_hours += hours

                workload_layout.addWidget(workload_table)

                # Итоговая нагрузка
                lbl_total = QLabel(f"Общая нагрузка: {total_hours} часов")
                lbl_total.setStyleSheet("font-weight: bold; font-size: 12pt;")
                workload_layout.addWidget(lbl_total)

        tab_widget.addTab(workload_widget, "Моя нагрузка")

        # 2. Отчет по успеваемости
        grades_widget = QWidget()
        grades_layout = QVBoxLayout(grades_widget)

        with DB_Settings.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT g.GroupName, s.SubjectName, 
                           AVG(gr.Grade) as AvgGrade, 
                           COUNT(DISTINCT gr.StudentId) as StudentsCount
                    FROM Grades gr
                    JOIN StudentGroup g ON gr.GroupId = g.GroupId
                    JOIN Subject s ON gr.SubjectId = s.SubjectId
                    WHERE gr.TeacherId = %s
                    GROUP BY gr.GroupId, gr.SubjectId
                """, (self.user_data['id'],))

                grades_data = cursor.fetchall()

                if grades_data:
                    grades_table = QTableWidget()
                    grades_table.setColumnCount(4)
                    grades_table.setHorizontalHeaderLabels(["Группа", "Предмет", "Ср. балл", "Студентов"])
                    grades_table.setRowCount(len(grades_data))

                    for row, (group, subject, avg_grade, count) in enumerate(grades_data):
                        grades_table.setItem(row, 0, QTableWidgetItem(group))
                        grades_table.setItem(row, 1, QTableWidgetItem(subject))
                        grades_table.setItem(row, 2, QTableWidgetItem(f"{avg_grade:.2f}"))
                        grades_table.setItem(row, 3, QTableWidgetItem(str(count)))

                    grades_layout.addWidget(grades_table)
                else:
                    grades_layout.addWidget(QLabel("Нет данных об успеваемости"))

        tab_widget.addTab(grades_widget, "Успеваемость")

    def add_admin_reports_tab(self, tab_widget):
        """Отчеты для администраторов"""
        # 1. Сводный отчет по нагрузке преподавателей
        teacher_workload_widget = QWidget()
        teacher_workload_layout = QVBoxLayout(teacher_workload_widget)

        with DB_Settings.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT u.UserName, u.UserFullName, 
                           COUNT(DISTINCT w.SubjectId) as SubjectsCount,
                           SUM(w.Hours) as TotalHours,
                           COUNT(DISTINCT w.GroupId) as GroupsCount
                    FROM TeacherWorkload w
                    JOIN user u ON w.TeacherId = u.UserId
                    GROUP BY w.TeacherId
                    ORDER BY TotalHours DESC
                """)

                teacher_data = cursor.fetchall()

                teacher_table = QTableWidget()
                teacher_table.setColumnCount(5)
                teacher_table.setHorizontalHeaderLabels(["Логин", "ФИО", "Дисциплин", "Часов", "Групп"])
                teacher_table.setRowCount(len(teacher_data))

                for row, (login, name, subjects, hours, groups) in enumerate(teacher_data):
                    teacher_table.setItem(row, 0, QTableWidgetItem(login))
                    teacher_table.setItem(row, 1, QTableWidgetItem(name))
                    teacher_table.setItem(row, 2, QTableWidgetItem(str(subjects)))
                    teacher_table.setItem(row, 3, QTableWidgetItem(str(hours)))
                    teacher_table.setItem(row, 4, QTableWidgetItem(str(groups)))

                teacher_workload_layout.addWidget(teacher_table)

                # Кнопка экспорта
                btn_export = QPushButton("Экспорт в Excel")
                btn_export.clicked.connect(lambda: self.export_to_excel(
                    teacher_data,
                    ["Логин", "ФИО", "Кол-во дисциплин", "Всего часов", "Кол-во групп"],
                    "teacher_workload"
                ))
                teacher_workload_layout.addWidget(btn_export)

        tab_widget.addTab(teacher_workload_widget, "Нагрузка преподавателей")

        # 2. Отчет по успеваемости групп
        group_grades_widget = QWidget()
        group_grades_layout = QVBoxLayout(group_grades_widget)

        with DB_Settings.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT g.GroupName, s.SubjectName, 
                           AVG(gr.Grade) as AvgGrade, 
                           COUNT(DISTINCT gr.StudentId) as StudentsCount
                    FROM Grades gr
                    JOIN StudentGroup g ON gr.GroupId = g.GroupId
                    JOIN Subject s ON gr.SubjectId = s.SubjectId
                    GROUP BY gr.GroupId, gr.SubjectId
                    ORDER BY g.GroupName, s.SubjectName
                """)

                group_grades_data = cursor.fetchall()

                if group_grades_data:
                    group_grades_table = QTableWidget()
                    group_grades_table.setColumnCount(4)
                    group_grades_table.setHorizontalHeaderLabels(["Группа", "Предмет", "Ср. балл", "Студентов"])
                    group_grades_table.setRowCount(len(group_grades_data))

                    for row, (group, subject, avg_grade, count) in enumerate(group_grades_data):
                        group_grades_table.setItem(row, 0, QTableWidgetItem(group))
                        group_grades_table.setItem(row, 1, QTableWidgetItem(subject))
                        group_grades_table.setItem(row, 2, QTableWidgetItem(f"{avg_grade:.2f}"))
                        group_grades_table.setItem(row, 3, QTableWidgetItem(str(count)))

                    group_grades_layout.addWidget(group_grades_table)
                else:
                    group_grades_layout.addWidget(QLabel("Нет данных об успеваемости"))

        tab_widget.addTab(group_grades_widget, "Успеваемость групп")

    def export_to_excel(self, data, headers, report_name):
        """Экспорт данных в Excel"""
        try:
            from openpyxl import Workbook
            from datetime import datetime
            import os

            wb = Workbook()
            ws = wb.active
            ws.title = "Отчет"

            # Заголовки
            ws.append(headers)

            # Данные
            for row in data:
                ws.append(row)

            # Автоматическая ширина столбцов
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2) * 1.2
                ws.column_dimensions[column].width = adjusted_width

            # Сохраняем файл
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = f"{report_name}_{timestamp}.xlsx"
            wb.save(file_path)

            QMessageBox.information(self, "Экспорт",
                                    f"Отчет успешно сохранен:\n{os.path.abspath(file_path)}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось экспортировать данные: {str(e)}")

    def show_settings(self):
        QMessageBox.information(self, "Навигация", "Переход в настройки")

    def generate_schedule(self):
        QMessageBox.information(self, "Генерация", "Запущен процесс генерации расписания")

    def show_request_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Запрос изменения")
        form = QFormLayout(dialog)

        date_edit = QDateEdit()
        reason_edit = QTextEdit()

        form.addRow("Дата изменения:", date_edit)
        form.addRow("Причина:", reason_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok |
                                   QDialogButtonBox.StandardButton.Cancel)  # Исправлено здесь
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        form.addRow(buttons)

        if dialog.exec() == QDialog.DialogCode.Accepted:  # Исправлено здесь
            QMessageBox.information(self, "Успешно", "Запрос отправлен")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow(user_role="teacher")
    window.show()
    sys.exit(app.exec())