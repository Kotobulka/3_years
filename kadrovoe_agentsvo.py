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
        self.vacancies_button = QPushButton('Найденные Вакансии')  
        self.add_candidate_button = QPushButton('Добавить Кандидата')  
        self.add_employer_button = QPushButton('Добавить Работодателя')  
        self.report_button = QPushButton('Отчет')  

        # Создание горизонтального макета для кнопок  
        button_layout = QHBoxLayout()  
        button_layout.addWidget(self.candidates_button)  
        button_layout.addWidget(self.employers_button)  
        button_layout.addWidget(self.vacancies_button)  
        button_layout.addWidget(self.add_candidate_button)  
        button_layout.addWidget(self.add_employer_button)  
        button_layout.addWidget(self.report_button)  

        # Создание виджета с несколькими страницами для разных представлений  
        self.stacked_widget = QStackedWidget()  
        self.table_widget = QTableWidget()  
        self.stacked_widget.addWidget(self.table_widget)  # Таблица кандидатов  
        self.stacked_widget.addWidget(QTableWidget())  # Таблица работодателей  
        self.stacked_widget.addWidget(QTableWidget())  # Таблица вакансий  

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
        self.vacancies_button.clicked.connect(self.show_vacancies)  
        self.add_candidate_button.clicked.connect(self.open_add_candidate_dialog)  

        # Инициализация таблицы кандидатов  
        self.init_candidate_table()  

    def init_candidate_table(self):  
        self.table_widget.setColumnCount(2)  # Установка количества столбцов в таблице  
        self.table_widget.setHorizontalHeaderLabels(['ФИО', 'Номер телефона'])  # Установка заголовков столбцов  
        self.table_widget.setRowCount(0)  # Установка начального пустого состояния таблицы  

    def show_candidates(self):  
        self.stacked_widget.setCurrentIndex(0)  # Показать таблицу кандидатов  

    def show_employers(self):  
        self.stacked_widget.setCurrentIndex(1)  # Показать таблицу работодателей  

    def show_vacancies(self):  
        self.stacked_widget.setCurrentIndex(2)  # Показать таблицу вакансий  

    def open_add_candidate_dialog(self):  
        dialog = AddCandidateDialog(self)  # Открытие диалога добавления кандидата  
        dialog.exec_()  

    def add_candidate(self, name, phone, dob, gender, position, comment, status, city, area, citizenship, resume_path):  
        row_position = self.table_widget.rowCount()  # Получение текущего количества строк в таблице  
        self.table_widget.insertRow(row_position)  # Вставка новой строки в таблицу  
        self.table_widget.setItem(row_position, 0, QTableWidgetItem(name))  # Установка значения ФИО в первую ячейку  
        self.table_widget.setItem(row_position, 1, QTableWidgetItem(phone))  # Установка номера телефона во вторую ячейку  


class AddCandidateDialog(QDialog):  
    def __init__(self, parent=None):  
        super().__init__(parent)  
        self.setWindowTitle('Добавить Кандидата')  # Установка заголовка диалогового окна  

        # Создание макета формы  
        layout = QFormLayout()  
        
        self.name_input = QLineEdit()  # Поле ввода для ФИО  
        self.phone_input = QLineEdit()  # Поле ввода для номера телефона  
        self.dob_input = QDateEdit(QDate.currentDate())  # Поле ввода для даты рождения  
        self.dob_input.setDisplayFormat('dd.MM.yyyy')  # Установка формата отображения даты  
        
        self.gender_input = QComboBox()  # Выпадающий список для выбора пола  
        self.gender_input.addItems(['муж', 'жен'])  # Добавление вариантов в выпадающий список  
        
        self.position_input = QLineEdit()  # Поле ввода для желаемой должности  
        self.comment_input = QLineEdit()  # Поле ввода для комментария  
        
        self.status_input = QComboBox()  # Выпадающий список для статуса кандидата  
        self.status_input.addItems(['найдена работа', 'ожидание', 'не прошел'])  # Добавление вариантов в выпадающий список  
        
        self.city_input = QLineEdit()  # Поле ввода для города проживания  
        self.area_input = QLineEdit()  # Поле ввода для района проживания  
        self.citizenship_input = QLineEdit()  # Поле ввода для гражданства  

        self.resume_button = QPushButton('Добавить резюме')  # Кнопка для добавления резюме  
        self.resume_button.clicked.connect(self.add_resume)  # Подключение кнопки к функции добавления резюме  

        self.save_button = QPushButton('Сохранить')  # Кнопка для сохранения данных кандидата  
        self.save_button.clicked.connect(self.save_candidate)  # Подключение кнопки к функции сохранения кандидата  
        self.cancel_button = QPushButton('Отмена')  # Кнопка для отмены действия  
        self.cancel_button.clicked.connect(self.reject)  # Подключение кнопки к функции закрытия диалога  

        # Добавление виджетов в макет  
        layout.addRow(QLabel('Фамилия Имя Отчество'), self.name_input)  # Добавление поля ФИО  
        layout.addRow(QLabel('Номер телефона'), self.phone_input)  # Добавление поля для номера телефона  
        layout.addRow(QLabel('Дата рождения'), self.dob_input)  # Добавление поля для даты рождения  
        layout.addRow(QLabel('Пол'), self.gender_input)  # Добавление поля для выбора пола  
        layout.addRow(QLabel('Желаемая должность'), self.position_input)  # Добавление поля для желаемой должности  
        layout.addRow(QLabel('Комментарий'), self.comment_input)  # Добавление поля для комментария  
        layout.addRow(QLabel('Статус'), self.status_input)  # Добавление поля для статуса  
        layout.addRow(QLabel('Город проживания'), self.city_input)  # Добавление поля для города проживания  
        layout.addRow(QLabel('Район проживания'), self.area_input)  # Добавление поля для района проживания  
        layout.addRow(QLabel('Гражданство'), self.citizenship_input)  # Добавление поля для гражданства  
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
        dob = self.dob_input.text()  
        gender = self.gender_input.currentText()  
        position = self.position_input.text()  
        comment = self.comment_input.text()  
        status = self.status_input.currentText()  
        city = self.city_input.text()  
        area = self.area_input.text()  
        citizenship = self.citizenship_input.text()  

        # Добавление кандидата в таблицу  
        self.parent().add_candidate(name, phone, dob, gender, position, comment, status, city, area, citizenship, self.resume_path)  
        self.accept()  # Закрытие диалогового окна после сохранения кандидата  


if __name__ == '__main__':  
    app = QApplication(sys.argv)  # Создание экземпляра приложения  
    main_win = MainWindow()  # Создание главного окна  
    main_win.show()  # Отображение главного окна  
    sys.exit(app.exec_())  # Запуск цикла обработки событий приложения  