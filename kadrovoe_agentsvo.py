import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget,   
                             QTableWidgetItem, QPushButton,   
                             QMessageBox, QDialog, QFormLayout,   
                             QComboBox, QLineEdit, QDateEdit, QMainWindow, QApplication, QTabWidget)  
from PyQt5.QtGui import QIntValidator, QRegularExpressionValidator  
from PyQt5.QtCore import QRegularExpression, QDate, Qt
import psycopg2
    

class MainApp(QMainWindow):  
    def __init__(self):  
        super().__init__()  
        self.setWindowTitle("HR App")  
        self.setGeometry(100, 100, 800, 600)  

        self.central_widget = QWidget(self)  
        self.setCentralWidget(self.central_widget)  

        self.layout = QVBoxLayout(self.central_widget)  

        # Create tabs  
        self.tabs = QTabWidget(self)  
        self.layout.addWidget(self.tabs)  

        # Create tab instances  
        self.candidates_tab = CandidateTab(self)  
        self.employers_tab = EmployerTab(self)  
        self.vacancies_tab = VacancyTab(self)  

        # Add tabs to the interface  
        self.tabs.addTab(self.candidates_tab, "Кандидаты")  
        self.tabs.addTab(self.employers_tab, "Работодатели")  
        self.tabs.addTab(self.vacancies_tab, "Вакансии")  

        self.setMinimumSize(800, 600)  

class CandidateTab(QWidget):  
    def __init__(self, parent):  
        super().__init__(parent)  
        self.layout = QVBoxLayout(self)  

        self.table = QTableWidget(self)  
        self.table.setColumnCount(10)  # Увеличиваем на 1 для ID  
        self.table.setHorizontalHeaderLabels([  
            "ID", "ФИО", "Дата рождения", "Телефон", "Email", "Резюме",  
            "Опыт работы", "Образование", "Навыки", "Статус"  
        ])  

        self.layout.addWidget(self.table)  
        self.load_data()  

        # Скрываем столбец ID  
        self.table.hideColumn(0)  # Скрываем первый столбец (ID)  

        # Кнопки для управления  
        self.add_button = QPushButton("Добавить")  
        self.add_button.clicked.connect(self.add_candidate)  
        self.layout.addWidget(self.add_button)  

        self.edit_button = QPushButton("Изменить")  
        self.edit_button.clicked.connect(self.edit_candidate)  
        self.layout.addWidget(self.edit_button)  

        self.delete_button = QPushButton("Удалить")  
        self.delete_button.clicked.connect(self.delete_candidate)  
        self.layout.addWidget(self.delete_button)  

    def load_data(self):  
        connection = psycopg2.connect(  
            dbname='postgres',  
            user='postgres',  
            password='1234',  
            host='localhost',  
            port='5432'  
        )  
        cursor = connection.cursor()  
        cursor.execute("SELECT id, фио, дата_рождения, телефон, email, резюме, опыт_работы, образование, навыки, статус FROM Кандидаты ORDER BY id ASC")  
        rows = cursor.fetchall()  

        self.table.setRowCount(len(rows))  
        for i, row in enumerate(rows):  
            for j in range(len(row)):  
                self.table.setItem(i, j, QTableWidgetItem(str(row[j])))  

        cursor.close()  
        connection.close()  

    def add_candidate(self):  
        dialog = CandidateDialog(self, "Добавить кандидата")  
        if dialog.exec_() == QDialog.Accepted:  
            self.load_data()  

    def edit_candidate(self):  
        selected_row = self.table.currentRow()  
        if selected_row < 0:  
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите кандидата для изменения.")  
            return  
        
        candidate_id = self.table.item(selected_row, 0).text()  
        current_data = [self.table.item(selected_row, i).text() for i in range(1, 10)]  
        dialog = CandidateDialog(self, "Изменить кандидата", current_data, candidate_id)  
        if dialog.exec_() == QDialog.Accepted:  
            self.load_data()   

    def delete_candidate(self):  
        selected_row = self.table.currentRow()  
        if selected_row < 0:  
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите кандидата для удаления.")  
            return  

        confirmed = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить этого кандидата?", QMessageBox.Yes | QMessageBox.No)  
        if confirmed == QMessageBox.Yes:  
            candidate_id = self.table.item(selected_row, 0).text()  
            self.delete_from_db("Кандидаты", candidate_id)  
            self.load_data()  

    def delete_from_db(self, table_name, candidate_id):
        connection = psycopg2.connect(  
            dbname='postgres',  
            user='postgres',  
            password='1234',  
            host='localhost',  
            port='5432'  
        )  
        cursor = connection.cursor()  
        cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (candidate_id,))  
        connection.commit()  
        cursor.close()  
        connection.close()  

class CandidateDialog(QDialog):  
    def __init__(self, parent, title, candidate_data=None, candidate_id=None):  
        super().__init__(parent)  
        self.setWindowTitle(title)  
        self.layout = QFormLayout(self)  

        self.name_input = QLineEdit(self)  
        self.birthday_input = QDateEdit(self)  
        self.phone_input = QLineEdit(self)  
        self.phone_input.setInputMask("+7(999)999-99-99;_")  # Маска для телефона  
        self.email_input = QLineEdit(self)  
        
        # Устанавливаем валидатор для email  
        email_regex = QRegularExpression(r"^[\w\.-]+@[\w\.-]+\.(ru|com)$")  
        self.email_validator = QRegularExpressionValidator(email_regex, self.email_input)  
        self.email_input.setValidator(self.email_validator)  

        self.resume_input = QLineEdit(self)  
        
        # Устанавливаем валидатор для опыта работы (только цифры)  
        self.experience_input = QLineEdit(self)  
        self.experience_input.setValidator(QIntValidator(0, 100, self))  # Допускаем ввод только положительных чисел  

        self.education_input = QComboBox(self)  
        self.education_input.addItems(["Высшее", "СПО"])  # Выпадающий список для образования  
        self.skills_input = QLineEdit(self)  
        self.status_input = QComboBox(self)  
        self.status_input.addItems(["Активный", "Архивированный", "Ушел"])  # Выпадающий список для статуса  
        self.candidate_id = candidate_id  

        # Заполняем поля только если переданы данные кандидата  
        if candidate_data:  
            self.name_input.setText(candidate_data[0])  
            self.birthday_input.setDate(QDate.fromString(candidate_data[1], "yyyy-MM-dd"))   
            self.phone_input.setText(candidate_data[2])  
            self.email_input.setText(candidate_data[3])  
            self.resume_input.setText(candidate_data[4])  
            self.experience_input.setText(candidate_data[5])  
            self.education_input.setCurrentText(candidate_data[6])  # Устанавливаем выбранное образование  
            self.skills_input.setText(candidate_data[7])  
            self.status_input.setCurrentText(candidate_data[8])  # Устанавливаем выбранный статус  

        self.layout.addRow("ФИО:", self.name_input)  
        self.layout.addRow("Дата рождения:", self.birthday_input)  
        self.layout.addRow("Телефон:", self.phone_input)  
        self.layout.addRow("Email:", self.email_input)  
        self.layout.addRow("Резюме:", self.resume_input)  
        self.layout.addRow("Опыт работы:", self.experience_input)  
        self.layout.addRow("Образование:", self.education_input)  
        self.layout.addRow("Навыки:", self.skills_input)  
        self.layout.addRow("Статус:", self.status_input)  

        self.save_button = QPushButton("Сохранить", self)  
        self.save_button.clicked.connect(self.save)  
        self.layout.addWidget(self.save_button)  

        self.setLayout(self.layout)  

    def save(self):  
        # Сбор данных из полей  
        name = self.name_input.text()  
        birthday = self.birthday_input.date().toString("yyyy-MM-dd")  
        phone = self.phone_input.text()  
        email = self.email_input.text()  
        resume = self.resume_input.text()  
        experience = self.experience_input.text()   
        education = self.education_input.currentText()  
        skills = self.skills_input.text()  
        status = self.status_input.currentText()  

        # Проверка на заполнение всех обязательных полей  
        if not all([name, birthday, phone, email, resume, experience, education, skills, status]):  
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все обязательные поля.")  
            return  

        # Проверка на валидность email  
        if self.email_input.hasAcceptableInput() == False:  
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректный Email по шаблону: xxxxxx@xxxx.ru/com.")  
            return  

        # Определяем, добавляем или редактируем  
        is_editing = self.windowTitle() == "Изменить кандидата"  

        # Подключение к базе данных  
        connection = psycopg2.connect(  
            dbname='postgres',  
            user='postgres',  
            password='1234',  
            host='localhost',  
            port='5432'  
        )  
        cursor = connection.cursor()  

        if is_editing:  
            # Обновление существующей записи, используя id  
            cursor.execute("""  
                UPDATE Кандидаты   
                SET фио = %s, дата_рождения = %s, телефон = %s, email = %s, резюме = %s,  
                    опыт_работы = %s, образование = %s, навыки = %s, статус = %s   
                WHERE id = %s  
            """, (name, birthday, phone, email, resume, experience, education, skills, status, self.candidate_id))  
        else:  
            # Вставка новой записи  
            cursor.execute("""  
                INSERT INTO Кандидаты (фио, дата_рождения, телефон, email, резюме,   
                    опыт_работы, образование, навыки, статус)   
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)  
            """, (name, birthday, phone, email, resume, experience, education, skills, status))  

        connection.commit()  
        cursor.close()  
        connection.close()  
        self.accept()  # Закрываем диалог с успешным завершением  

# Employer Tab Class  
class EmployerTab(QWidget):  
    def __init__(self, parent):  
        super().__init__(parent)  
        self.layout = QVBoxLayout(self)  

        self.table = QTableWidget(self)  
        self.table.setColumnCount(4)   
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Контактные данные", "Описание"])  
        self.table.setColumnHidden(0, True)  # Скрываем столбец ID  

        self.layout.addWidget(self.table)  
        self.load_data()  

        # Add buttons for CRUD operations  
        self.add_button = QPushButton("Добавить")  
        self.add_button.clicked.connect(self.add_employer)  
        self.layout.addWidget(self.add_button)  

        self.edit_button = QPushButton("Изменить")  
        self.edit_button.clicked.connect(self.edit_employer)  
        self.layout.addWidget(self.edit_button)  

        self.delete_button = QPushButton("Удалить")  
        self.delete_button.clicked.connect(self.delete_employer)  
        self.layout.addWidget(self.delete_button)  

    def load_data(self):  
        connection = psycopg2.connect(  
            dbname='postgres',  
            user='postgres',  
            password='1234',  
            host='localhost',  
            port='5432'  
        )  
        cursor = connection.cursor()  
        cursor.execute("SELECT id, название, контактные_данные, описание FROM Работодатели ORDER BY id ASC")  # Сортировка по id  
        rows = cursor.fetchall()  

        self.table.setRowCount(len(rows))  
        for i, row in enumerate(rows):  
            for j in range(len(row)):  
                self.table.setItem(i, j, QTableWidgetItem(str(row[j])))  

        cursor.close()  
        connection.close()  

        # Установите сортировку по первой колонке (id)  
        self.table.sortItems(0, Qt.AscendingOrder)  

    def add_employer(self):  
        dialog = EmployerDialog(self, "Добавить работодателя")  
        if dialog.exec_() == QDialog.Accepted:  
            self.load_data()  

    def edit_employer(self):  
        selected_row = self.table.currentRow()  
        if selected_row < 0:  
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите работодателя для изменения.")  
            return  
        current_data = [self.table.item(selected_row, i).text() for i in range(4)]  # Получаем данные включая ID  
        dialog = EmployerDialog(self, "Изменить работодателя", current_data)  
        if dialog.exec_() == QDialog.Accepted:  
            self.load_data()  

    def delete_employer(self):  
        selected_row = self.table.currentRow()  
        if selected_row < 0:  
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите работодателя для удаления.")  
            return  

        confirmed = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить этого работодателя?", QMessageBox.Yes | QMessageBox.No)  
        if confirmed == QMessageBox.Yes:  
            employer_id = self.table.item(selected_row, 0).text()  # Получаем ID для удаления  
            self.delete_from_db(employer_id)  
            self.load_data()  

    def delete_from_db(self, employer_id):  
        connection = psycopg2.connect(  
            dbname='postgres',  
            user='postgres',  
            password='1234',  
            host='localhost',  
            port='5432'  
        )  
        cursor = connection.cursor()  
        cursor.execute("DELETE FROM Работодатели WHERE id = %s", (employer_id,))  
        connection.commit()  
        cursor.close()  
        connection.close()  

class EmployerDialog(QDialog):  
    def __init__(self, parent, title, employer_data=None):  
        super().__init__(parent)  
        self.setWindowTitle(title)  
        self.layout = QFormLayout(self)  

        self.id_input = QLineEdit(self)  # Поле для id, которое будет скрыто  
        self.id_input.setVisible(False)  # Скрываем поле id  

        self.name_input = QLineEdit(self)  
        self.contact_input = QLineEdit(self)  
        self.description_input = QLineEdit(self)  

        # Устанавливаем валидатор для email  
        email_regex = QRegularExpression(r"^[\w\.-]+@[\w\.-]+\.(ru|com)$")  
        self.email_validator = QRegularExpressionValidator(email_regex, self.contact_input)  
        self.contact_input.setValidator(self.email_validator)  

        if employer_data:  
            self.id_input.setText(employer_data[0])  # Устанавливаем id  
            self.name_input.setText(employer_data[1])  
            self.contact_input.setText(employer_data[2])  
            self.description_input.setText(employer_data[3])  
        
        self.layout.addRow("ID:", self.id_input)  # Добавляем id (но скрываем)  
        self.layout.addRow("Название:", self.name_input)  
        self.layout.addRow("Контактные данные:", self.contact_input)  
        self.layout.addRow("Описание:", self.description_input)  

        self.save_button = QPushButton("Сохранить", self)  
        self.save_button.clicked.connect(self.save)  
        self.layout.addWidget(self.save_button)  

        self.setLayout(self.layout)  

    def save(self):  
        employer_id = self.id_input.text()  # Получаем id из скрытого поля  
        name = self.name_input.text()  
        contact = self.contact_input.text()  
        description = self.description_input.text()  

        # Проверка на заполнение всех обязательных полей  
        if not name or not contact or not description:  
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все обязательные поля.")  
            return  
        
        # Проверка на валидность email  
        if not self.contact_input.hasAcceptableInput():  
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, введите корректный Email в формате xxxxxx@xxxxx.ru/com.")  
            return  

        is_editing = self.windowTitle() == "Изменить работодателя"  

        connection = psycopg2.connect(  
            dbname='postgres',  
            user='postgres',  
            password='1234',  
            host='localhost',  
            port='5432'  
        )  
        cursor = connection.cursor()  

        if is_editing:  
            cursor.execute("""  
                UPDATE Работодатели   
                SET название = %s, контактные_данные = %s, описание = %s   
                WHERE id = %s  
            """, (name, contact, description, employer_id))  
        else:  
            cursor.execute("""  
                INSERT INTO Работодатели (название, контактные_данные, описание)   
                VALUES (%s, %s, %s)  
            """, (name, contact, description))  

        connection.commit()  
        cursor.close()  
        connection.close()  
        self.accept() 

# Vacancy Tab Class  
class VacancyTab(QWidget):  
    def __init__(self, parent):  
        super().__init__(parent)  
        self.layout = QVBoxLayout(self)  

        self.table = QTableWidget(self)  
        self.table.setColumnCount(8)  # Увеличиваем на 1 для ID  
        self.table.setHorizontalHeaderLabels([  
            "ID", "Название должности", "Описание", "Требования", "Работодатель ID", "Дата открытия", "Дата закрытия", "Статус"  
        ])  

        self.layout.addWidget(self.table)  
        self.load_data()  

        # Скрываем столбец ID  
        self.table.hideColumn(0)  # Скрываем первый столбец (ID)  

        # Кнопки для управления  
        self.add_button = QPushButton("Добавить")  
        self.add_button.clicked.connect(self.add_vacancy)  
        self.layout.addWidget(self.add_button)  

        self.edit_button = QPushButton("Изменить")  
        self.edit_button.clicked.connect(self.edit_vacancy)  
        self.layout.addWidget(self.edit_button)  

        self.delete_button = QPushButton("Удалить")  
        self.delete_button.clicked.connect(self.delete_vacancy)  
        self.layout.addWidget(self.delete_button)  

    def load_data(self):  
        connection = psycopg2.connect(  
            dbname='postgres',  
            user='postgres',  
            password='1234',  
            host='localhost',  
            port='5432'  
        )  
        cursor = connection.cursor()  
        cursor.execute("SELECT id, название_должности, описание, требования, работодатель_id, дата_открытия, дата_закрытия, статус FROM Вакансии ORDER BY id ASC")  
        rows = cursor.fetchall()  

        self.table.setRowCount(len(rows))  
        for i, row in enumerate(rows):  
            for j in range(len(row)):  
                self.table.setItem(i, j, QTableWidgetItem(str(row[j])))  

        cursor.close()  
        connection.close()  

    def add_vacancy(self):  
        dialog = VacancyDialog(self, "Добавить вакансию")  
        if dialog.exec_() == QDialog.Accepted:  
            self.load_data()  

    def edit_vacancy(self):  
        selected_row = self.table.currentRow()  
        if selected_row < 0:  
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите вакансию для изменения.")  
            return  
        
        vacancy_id = self.table.item(selected_row, 0).text()  # Получаем ID для редактирования  
        current_data = [self.table.item(selected_row, i).text() for i in range(1, 8)]  # Получаем данные без ID  
        dialog = VacancyDialog(self, "Изменить вакансию", current_data, vacancy_id)  
        if dialog.exec_() == QDialog.Accepted:  
            self.load_data()  

    def delete_vacancy(self):  
        selected_row = self.table.currentRow()  
        if selected_row < 0:  
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, выберите вакансию для удаления.")  
            return  

        confirmed = QMessageBox.question(self, "Подтверждение", "Вы уверены, что хотите удалить эту вакансию?", QMessageBox.Yes | QMessageBox.No)  
        if confirmed == QMessageBox.Yes:  
            vacancy_id = self.table.item(selected_row, 0).text()  # Получаем ID для удаления  
            self.delete_from_db("Вакансии", vacancy_id)  
            self.load_data()  

    def delete_from_db(self, table_name, vacancy_id):  
        connection = psycopg2.connect(  
            dbname='postgres',  
            user='postgres',  
            password='1234',  
            host='localhost',  
            port='5432'  
        )  
        cursor = connection.cursor()  
        cursor.execute(f"DELETE FROM {table_name} WHERE id = %s", (vacancy_id,))  
        connection.commit()  
        cursor.close()  
        connection.close()  

class VacancyDialog(QDialog):  
    def __init__(self, parent, title, vacancy_data=None, vacancy_id=None):  
        super().__init__(parent)  
        self.setWindowTitle(title)  
        self.layout = QFormLayout(self)  

        self.title_input = QLineEdit(self)  
        self.description_input = QLineEdit(self)  
        self.requirements_input = QLineEdit(self)  
        self.employer_id_input = QComboBox(self)  # Используем QComboBox для выбора работодателя  
        self.open_date_input = QDateEdit(self)  
        self.close_date_input = QDateEdit(self)  
        self.status_input = QComboBox(self)  # Используем QComboBox для статуса  

        # Заполнение выпадающего списка для статуса  
        self.status_input.addItems(["Открыта", "Закрыта"])  

        # Заполнение выпадающего списка для работодателей  
        self.load_employers()  

        if vacancy_data:  
            self.title_input.setText(vacancy_data[0])  
            self.description_input.setText(vacancy_data[1])  
            self.requirements_input.setText(vacancy_data[2])  
            self.employer_id_input.setCurrentText(vacancy_data[3])  # Устанавливаем выбранного работодателя  
            self.open_date_input.setDate(QDate.fromString(vacancy_data[4], "yyyy-MM-dd"))  
            self.close_date_input.setDate(QDate.fromString(vacancy_data[5], "yyyy-MM-dd"))  
            self.status_input.setCurrentText(vacancy_data[6])  # Устанавливаем статус  
        
        self.layout.addRow("Название должности:", self.title_input)  
        self.layout.addRow("Описание:", self.description_input)  
        self.layout.addRow("Требования:", self.requirements_input)  
        self.layout.addRow("Работодатель:", self.employer_id_input)  # Изменено на QComboBox  
        self.layout.addRow("Дата открытия:", self.open_date_input)  
        self.layout.addRow("Дата закрытия:", self.close_date_input)  
        self.layout.addRow("Статус:", self.status_input)  # Изменено на QComboBox  

        self.save_button = QPushButton("Сохранить", self)  
        self.save_button.clicked.connect(self.save)  
        self.layout.addWidget(self.save_button)  

        self.setLayout(self.layout)  

    def load_employers(self):  
        connection = psycopg2.connect(  
            dbname='postgres',  
            user='postgres',  
            password='1234',  
            host='localhost',  
            port='5432'  
        )  
        cursor = connection.cursor()  
        cursor.execute("SELECT id, название FROM Работодатели")  # Получаем id и название работодателей  
        employers = cursor.fetchall()  

        for employer in employers:  
            self.employer_id_input.addItem(f"{employer[0]} - {employer[1]}")  # Добавляем в ComboBox  

        cursor.close()  
        connection.close()  

    def save(self):  
        title = self.title_input.text()  
        description = self.description_input.text()  
        requirements = self.requirements_input.text()  
        employer_id = self.employer_id_input.currentText().split(" - ")[0]  # Получаем только ID работодателя  
        open_date = self.open_date_input.date().toString("yyyy-MM-dd")  
        close_date = self.close_date_input.date().toString("yyyy-MM-dd")  
        status = self.status_input.currentText()  # Получаем выбранный статус  

        is_editing = self.windowTitle() == "Изменить вакансию"  
        
        connection = psycopg2.connect(  
            dbname='postgres',  
            user='postgres',  
            password='1234',  
            host='localhost',  
            port='5432'  
        )  
        cursor = connection.cursor()  

        if is_editing:  
            # Получаем ID вакансии по которому выполняется редактирование  
            cursor.execute("""  
                UPDATE Вакансии SET описание = %s, требования = %s, работодатель_id = %s, дата_открытия = %s, дата_закрытия = %s, статус = %s WHERE название_должности = %s """, (description, requirements, employer_id, open_date, close_date, status, title))  
        else:  
            cursor.execute("""INSERT INTO Вакансии (название_должности, описание, требования, работодатель_id, дата_открытия, дата_закрытия, статус) VALUES (%s, %s, %s, %s, %s, %s, %s)  """, (title, description, requirements, employer_id, open_date, close_date, status))  

        connection.commit()  
        cursor.close()  
        connection.close()  
        self.accept()

if __name__ == "__main__":  
    app = QApplication(sys.argv)  
    main_app = MainApp()  
    main_app.show()  
    sys.exit(app.exec_()) 