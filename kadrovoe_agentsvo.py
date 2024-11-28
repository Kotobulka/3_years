import sys  
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QStackedWidget, QWidget, QTableWidget, QTableWidgetItem, QLabel, QFormLayout, QLineEdit, QDateEdit, QComboBox, QDialog, QFileDialog  
from PyQt5.QtCore import QDate  

class MainWindow(QMainWindow):  
    def __init__(self):  
        super().__init__()  

        self.setWindowTitle('HR Application')  # Установка заголовка окна приложения  
        self.setGeometry(0, 0, 1920, 1080)  # Установка размеров и положения окна  

        # Создание кнопок  
        self.candidates_button = QPushButton('Кандидаты')  
        self.employers_button = QPushButton('Работодатели')  
        self.vacancies_button = QPushButton('Вакансии')  # Кнопка для вакансий  
        self.add_candidate_button = QPushButton('Добавить Кандидата')  
        self.add_employer_button = QPushButton('Добавить Работодателя')  
        self.add_vacancy_button = QPushButton('Добавить Вакансию')  # Кнопка для добавления вакансии  
        self.report_button = QPushButton('Отчет')  

        # Установка стиля для кнопок  
        button_style = "height: 50px; width: 200px; font-size: 16px;"  
        self.candidates_button.setStyleSheet(button_style)  
        self.employers_button.setStyleSheet(button_style)  
        self.vacancies_button.setStyleSheet(button_style)  # Применение стиля к кнопке вакансий  
        self.add_candidate_button.setStyleSheet(button_style)  
        self.add_employer_button.setStyleSheet(button_style)  
        self.add_vacancy_button.setStyleSheet(button_style)  # Применение стиля к кнопке для добавления вакансий  
        self.report_button.setStyleSheet(button_style)  

        # Создание горизонтального макета для кнопок  
        button_layout = QHBoxLayout()  
        button_layout.addWidget(self.candidates_button)  
        button_layout.addWidget(self.employers_button)  
        button_layout.addWidget(self.vacancies_button)  # Добавление кнопки для вакансий  
        button_layout.addWidget(self.add_employer_button)  # Кнопка добавления работодателя  
        button_layout.addWidget(self.add_candidate_button)  
        button_layout.addWidget(self.add_vacancy_button)  # Кнопка для добавления вакансии  
        button_layout.addWidget(self.report_button)  

        # Создание виджета с несколькими страницами для разных представлений  
        self.stacked_widget = QStackedWidget()  
        self.table_widget_candidates = QTableWidget()  # Таблица кандидатов  
        self.table_widget_employers = QTableWidget()  # Таблица работодателей  
        self.table_widget_vacancies = QTableWidget()  # Таблица вакансий  

        self.stacked_widget.addWidget(self.table_widget_candidates)  
        self.stacked_widget.addWidget(self.table_widget_employers)  
        self.stacked_widget.addWidget(self.table_widget_vacancies)  # Добавление таблицы вакансий  

        # Настройка основного макета  
        layout = QVBoxLayout()  
        layout.addLayout(button_layout)  # Добавление макета кнопок  
        layout.addWidget(self.stacked_widget)  # Добавление виджета с несколькими страницами  

        # Установка центрального виджета  
        central_widget = QWidget()  
        central_widget.setLayout(layout)  
        self.setCentralWidget(central_widget)  

        # Подключение кнопок к их функциям  
        self.candidates_button.clicked.connect(self.show_candidates)  
        self.employers_button.clicked.connect(self.show_employers)  
        self.vacancies_button.clicked.connect(self.show_vacancies)  # Подключение кнопки для отображения вакансий  
        self.add_candidate_button.clicked.connect(self.open_add_candidate_dialog)  
        self.add_employer_button.clicked.connect(self.open_add_employer_dialog)  # Подключение к функции добавления работодателя  
        self.add_vacancy_button.clicked.connect(self.open_add_vacancy_dialog)  # Подключение к функции добавления вакансии  

        # Инициализация таблиц  
        self.init_candidate_table()  
        self.init_employer_table()  
        self.init_vacancy_table()  

    def init_candidate_table(self):  
        self.table_widget_candidates.setColumnCount(10)  # Установка количества столбцов в таблице кандидатов  
        self.table_widget_candidates.setHorizontalHeaderLabels([  
            'ID', 'ФИО', 'Дата рождения', 'Номер телефона', 'Email',   
            'Резюме', 'Опыт работы', 'Образование', 'Навыки', 'Статус'  
        ])  # Установка заголовков столбцов  
        self.table_widget_candidates.setRowCount(0)  # Установка начального пустого состояния таблицы  

    def init_employer_table(self):  
        self.table_widget_employers.setColumnCount(5)  # Установка количества столбцов в таблице работодателей  
        self.table_widget_employers.setHorizontalHeaderLabels([  
            'ID', 'Название', 'Контактные данные', 'Описание', 'Дата создания'  
        ])  # Установка заголовков столбцов  
        self.table_widget_employers.setRowCount(0)  # Установка начального пустого состояния таблицы  

    def init_vacancy_table(self):  
        self.table_widget_vacancies.setColumnCount(9)  # Установка количества столбцов в таблице вакансий  
        self.table_widget_vacancies.setHorizontalHeaderLabels([  
            'ID', 'Название должности', 'Описание', 'Требования',   
            'Работодатель ID', 'Дата открытия', 'Дата закрытия', 'Статус',   
            'Дата создания', 'Минимальный опыт'  
        ])  # Установка заголовков столбцов  
        self.table_widget_vacancies.setRowCount(0)  # Установка начального пустого состояния таблицы  

    def show_candidates(self):  
        self.stacked_widget.setCurrentIndex(0)  # Показать таблицу кандидатов  

    def show_employers(self):  
        self.stacked_widget.setCurrentIndex(1)  # Показать таблицу работодателей  

    def show_vacancies(self):  
        self.stacked_widget.setCurrentIndex(2)  # Показать таблицу вакансий  

    def open_add_candidate_dialog(self):  
        dialog = AddCandidateDialog(self)  # Открытие диалога добавления кандидата  
        dialog.exec_()  

    def open_add_employer_dialog(self):  
        dialog = AddEmployerDialog(self)  # Открытие диалога добавления работодателя  
        dialog.exec_()  

    def open_add_vacancy_dialog(self):  
        dialog = AddVacancyDialog(self)  # Открытие диалога добавления вакансии  
        dialog.exec_()  

    def add_candidate(self, name, phone, dob, email, resume, experience, education, skills, status):  
        row_position = self.table_widget_candidates.rowCount()  # Получение текущего количества строк в таблице  
        self.table_widget_candidates.insertRow(row_position)  # Вставка новой строки в таблицу  
        self.table_widget_candidates.setItem(row_position, 0, QTableWidgetItem(str(row_position + 1)))  # Установка ID  
        self.table_widget_candidates.setItem(row_position, 1, QTableWidgetItem(name))  # Установка значения ФИО  
        self.table_widget_candidates.setItem(row_position, 2, QTableWidgetItem(dob))  # Установка даты рождения  
        self.table_widget_candidates.setItem(row_position, 3, QTableWidgetItem(phone))  # Установка номера телефона  
        self.table_widget_candidates.setItem(row_position, 4, QTableWidgetItem(email))  # Установка email  
        self.table_widget_candidates.setItem(row_position, 5, QTableWidgetItem(resume))  # Установка резюме  
        self.table_widget_candidates.setItem(row_position, 6, QTableWidgetItem(experience))  # Установка опыта работы  
        self.table_widget_candidates.setItem(row_position, 7, QTableWidgetItem(education))  # Установка образования  
        self.table_widget_candidates.setItem(row_position, 8, QTableWidgetItem(skills))  # Установка навыков  
        self.table_widget_candidates.setItem(row_position, 9, QTableWidgetItem(status))  # Установка статуса  

# Здесь вы также должны создать классы AddEmployerDialog и AddVacancyDialog аналогично AddCandidateDialog  

class AddCandidateDialog(QDialog):  
    def __init__(self, parent=None):  
        super().__init__(parent)  
        self.setWindowTitle('Добавить Кандидата')  # Установка заголовка диалогового окна  

        # Создание макета формы  
        layout = QFormLayout()  

        self.name_input = QLineEdit()  # Поле ввода для ФИО  
        self.phone_input = QLineEdit()  # Поле ввода для номера телефона  
        self.email_input = QLineEdit()  # Поле ввода для email  
        self.dob_input = QDateEdit(QDate.currentDate())  # Поле ввода для даты рождения  
        self.dob_input.setDisplayFormat('dd.MM.yyyy')  # Установка формата отображения даты  

        self.resume_button = QPushButton('Добавить резюме')  # Кнопка для добавления резюме  
        self.resume_button.clicked.connect(self.add_resume)  # Подключение кнопки к функции добавления резюме  

        # Остальные поля для ввода  
        self.experience_input = QLineEdit()  
        self.education_input = QLineEdit()  
        self.skills_input = QLineEdit()  
        self.status_input = QComboBox()  
        self.status_input.addItems(['активный', 'неактивный', 'текущий'])  

        self.save_button = QPushButton('Сохранить')  # Кнопка для сохранения данных кандидата  
        self.save_button.clicked.connect(self.save_candidate)  # Подключение кнопки к функции сохранения кандидата  
        self.cancel_button = QPushButton('Отмена')  # Кнопка для отмены действия  
        self.cancel_button.clicked.connect(self.reject)  # Подключение кнопки к функции закрытия диалога  

        # Добавление виджетов в макет  
        layout.addRow(QLabel('Фамилия Имя Отчество'), self.name_input)  # Добавление поля ФИО  
        layout.addRow(QLabel('Номер телефона'), self.phone_input)  # Добавление поля для номера телефона  
        layout.addRow(QLabel('Email'), self.email_input)  # Добавление поля для Email  
        layout.addRow(QLabel('Дата рождения'), self.dob_input)  # Добавление поля для даты рождения  
        layout.addRow(QLabel('Опыт работы'), self.experience_input)  # Добавление поля для опыта работы  
        layout.addRow(QLabel('Образование'), self.education_input)  # Добавление поля для образования  
        layout.addRow(QLabel('Навыки'), self.skills_input)  # Добавление поля для навыков  
        layout.addRow(QLabel('Статус'), self.status_input)  # Добавление поля для статуса  
        layout.addRow(self.resume_button, self.save_button)  # Добавление кнопок для резюме и сохранения  
        layout.addRow(self.cancel_button)  # Добавление кнопки отмены  

        self.setLayout(layout)  # Установка макета в диалоговом окне  

        # Переменная для хранения пути к резюме  
        self.resume_path = ""  

    def add_resume(self):  
        # Открытие диалогового окна для выбора файла резюме  
        self.resume_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл резюме", "", "PDF Files (*.pdf);;Text Files (*.txt)")  

    def save_candidate(self):  
        # Сбор данных из полей ввода  
        name = self.name_input.text()  
        phone = self.phone_input.text()  
        email = self.email_input.text()  
        dob = self.dob_input.text()  
        experience = self.experience_input.text()  
        education = self.education_input.text()  
        skills = self.skills_input.text()  
        status = self.status_input.currentText()  

        # Добавление кандидата в таблицу  
        self.parent().add_candidate(name, phone, dob, email, self.resume_path, experience, education, skills, status)  
        self.accept()  # Закрытие диалогового окна после сохранения кандидата  

# Здесь вы также должны создать классы AddEmployerDialog и AddVacancyDialog аналогично AddCandidateDialog  

class AddEmployerDialog(QDialog):  
    # Реализуйте эту часть аналогично классу AddCandidateDialog  
    pass  

class AddVacancyDialog(QDialog):  
    # Реализуйте эту часть аналогично классу AddCandidateDialog  
    pass  

if __name__ == '__main__':  
    app = QApplication(sys.argv)  # Создание экземпляра приложения  
    main_win = MainWindow()  # Создание главного окна  
    main_win.show()  # Отображение главного окна  
    sys.exit(app.exec_())  # Запуск цикла обработки событий приложения  
