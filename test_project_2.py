import sys

from PyQt6.QtSql import QSqlQuery, QSqlDatabase
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QHBoxLayout, QListWidget, QLineEdit, QTextEdit,
                             QListWidgetItem, QLabel, QMessageBox)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(400, 500)
        self.setWindowTitle('Список задач')
        self.setWindowIcon(QIcon('task_list.png'))

        self.task_label = QLabel('Список задач:')
        self.task_list = QListWidget()
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.task_label)
        self.vbox.addWidget(self.task_list)

        self.all_task = QPushButton('Все задачи', self)
        self.active_task = QPushButton('Активные задачи', self)
        self.completed_task = QPushButton('Выполненные задачи', self)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.all_task)
        self.hbox.addWidget(self.active_task)
        self.hbox.addWidget(self.completed_task)
        self.vbox.addLayout(self.hbox)

        self.task_name = QLabel('Название задачи:')
        self.task_line = QLineEdit()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.task_name)
        self.hbox.addWidget(self.task_line)
        self.vbox.addLayout(self.hbox)

        self.task_description = QLabel('Описание задачи:')
        self.task_text = QTextEdit()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.task_description)
        self.hbox.addWidget(self.task_text)
        self.vbox.addLayout(self.hbox)

        self.category_name = QLabel('Категория:')
        self.category_line = QLineEdit()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.category_name)
        self.hbox.addWidget(self.category_line)
        self.vbox.addLayout(self.hbox)

        self.category_label = QLabel('Список категорий:')
        self.category_list = QListWidget()
        self.vbox.addWidget(self.category_label)
        self.vbox.addWidget(self.category_list)

        self.add_task_button = QPushButton('Добавить задачу', self)
        self.edit_task = QPushButton('Изменить задачу', self)
        self.delete_task = QPushButton('Удалить задачу', self)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.add_task_button)
        self.hbox.addWidget(self.edit_task)
        self.hbox.addWidget(self.delete_task)
        self.vbox.addLayout(self.hbox)

        self.add_category_button = QPushButton('Добавить категорию', self)
        self.edit_category = QPushButton('Изменить категорию', self)
        self.delete_category = QPushButton('Удалить категорию', self)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.add_category_button)
        self.hbox.addWidget(self.edit_category)
        self.hbox.addWidget(self.delete_category)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)

        self.create_tables()
        self.load_tasks()
        self.load_categories()

        self.add_category_button.clicked.connect(self.add_category)
        self.add_task_button.clicked.connect(self.add_task)

        self.task_list.itemClicked.connect(self.task_detail)
        self.category_list.itemClicked.connect(self.category_detail)

    def create_tables(self):
        query = QSqlQuery()

        query.exec(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL
            );
            """
        )

        query.exec(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) NOT NULL,
                description VARCHAR(255) NOT NULL,
                active BOOL NOT NULL DEFAULT TRUE,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            );
            """
        )

    def load_categories(self):
        query = QSqlQuery()
        query.exec(
            """
            SELECT * FROM categories;
            """
        )

        self.categories = []
        count = query.record().count()

        while query.next():
            temp = []

            for i in range(count):
                temp.append(query.value(i))

            self.categories.append(temp)

        self.category_list.clear()

        for category in self.categories:
            self.category_list.addItem(QListWidgetItem(category[1]))

    def load_tasks(self):
        print('add')
        query = QSqlQuery()
        query.exec(
            """
            SELECT * FROM tasks;
            """
        )

        self.tasks = []
        count = query.record().count()

        while query.next():
            temp = []

            for i in range(count):
                temp.append(query.value(i))

            self.tasks.append(temp)

        self.task_list.clear()
        print(self.tasks)

        for task in self.tasks:
            self.task_list.addItem(QListWidgetItem(task[1]))

    def add_category(self):
        name = self.category_line.text()

        query = QSqlQuery()
        query.exec(
            f"""
            INSERT INTO categories (name) VALUES ('{name}');
            """
        )

        self.load_categories()

    def add_task(self):
        name = self.task_line.text()
        description = self.task_text.text()
        row = self.category_list.currentRow()
        category_id = self.categories[row][0]

        query = QSqlQuery()
        query.exec(
            f"""
            INSERT INTO tasks (name, description, category_id) VALUES ('{name}', '{description}', '{category_id}');
            """
        )

        self.load_tasks()

    def task_detail(self):
        row = self.task_list.currentRow()

        self.task_line.setText(self.tasks[row][1])
        self.task_text.setText(self.tasks[row][2])
        #self.category_line.setText(self.tasks[row][2])

    def category_detail(self):
        row = self.category_list.currentRow()

        self.category_line.setText(self.categories[row][1])


if __name__ == '__main__':
    conn = QSqlDatabase.addDatabase('QSQLITE')
    conn.setDatabaseName('task_list')

    conn.open()

    app = QApplication(sys.argv)
    window = MainWindow()

    print(conn.tables())

    window.show()
    app.exec()
