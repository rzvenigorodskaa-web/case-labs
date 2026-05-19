import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QComboBox, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QSpinBox
)

class AnalyticsApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Аналитика успеваемости — ДПО")
        self.setGeometry(100, 100, 750, 500)

        # Данные
        self.students = ["Иванов Иван", "Петрова Мария", "Сидоров Алексей"]
        self.modules = ["Python для начинающих", "Базы данных SQL", "Веб-разработка"]
        self.scores = {student: {module: None for module in self.modules} for student in self.students}

        # UI
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # Выбор студента
        student_layout = QHBoxLayout()
        student_layout.addWidget(QLabel("Студент:"))
        self.student_combo = QComboBox()
        self.student_combo.addItems(self.students)
        student_layout.addWidget(self.student_combo)
        main_layout.addLayout(student_layout)

        # Выбор модуля и ввод оценки
        module_layout = QHBoxLayout()
        module_layout.addWidget(QLabel("Модуль:"))
        self.module_combo = QComboBox()
        self.module_combo.addItems(self.modules)
        module_layout.addWidget(self.module_combo)

        module_layout.addWidget(QLabel("Оценка (0–100):"))
        self.score_spin = QSpinBox()
        self.score_spin.setRange(0, 100)
        module_layout.addWidget(self.score_spin)

        self.add_btn = QPushButton("Сохранить оценку")
        self.add_btn.clicked.connect(self.save_score)
        module_layout.addWidget(self.add_btn)
        main_layout.addLayout(module_layout)

        # Таблица успеваемости
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.modules) + 1)
        self.table.setHorizontalHeaderLabels(["Студент"] + self.modules)
        main_layout.addWidget(self.table)

        # Кнопка расчёта среднего балла
        self.calc_btn = QPushButton("Показать средний балл по группе")
        self.calc_btn.clicked.connect(self.show_average)
        main_layout.addWidget(self.calc_btn)

        self.update_table()

    def save_score(self):
        student = self.student_combo.currentText()
        module = self.module_combo.currentText()
        score = self.score_spin.value()
        self.scores[student][module] = score
        self.update_table()
        QMessageBox.information(self, "Успех", f"Оценка для {student} по модулю «{module}» сохранена.")

    def update_table(self):
        self.table.setRowCount(len(self.students))
        for row, student in enumerate(self.students):
            self.table.setItem(row, 0, QTableWidgetItem(student))
            for col, module in enumerate(self.modules):
                score = self.scores[student][module]
                self.table.setItem(row, col + 1, QTableWidgetItem(str(score) if score is not None else "—"))

    def show_average(self):
        avg_scores = {}
        for module in self.modules:
            scores = [self.scores[student][module] for student in self.students if self.scores[student][module] is not None]
            avg_scores[module] = round(sum(scores) / len(scores), 1) if scores else 0

        msg = "\n".join([f"{module}: средний балл {avg}" for module, avg in avg_scores.items()])
        QMessageBox.information(self, "Средний балл по группе", msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnalyticsApp()
    window.show()
    sys.exit(app.exec_())













