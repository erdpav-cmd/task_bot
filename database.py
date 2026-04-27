import sqlite3
import csv
from config import DATABASE_FILE

class Database:
    """Класс для работы с базой данных задач"""
    
    def __init__(self, db_path=DATABASE_FILE):
        # Подключаемся к БД. check_same_thread=False позволяет работать в асинхронном потоке
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Создаёт таблицу, если её ещё нет"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                user TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_task(self, text: str, user: str) -> int:
        """Добавляет новую задачу и возвращает её ID"""
        self.cursor.execute(
            'INSERT INTO tasks (text, user) VALUES (?, ?)', 
            (text, user)
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_tasks(self) -> list:
        """Возвращает все задачи, отсортированные по дате (новые сверху)"""
        self.cursor.execute('SELECT id, text, user, created_at FROM tasks ORDER BY id DESC')
        return self.cursor.fetchall()

    def export_to_csv(self, filepath: str = "tasks_export.csv") -> str:
        """Экспортирует задачи в CSV, совместимый с Excel"""
        tasks = self.get_all_tasks()
        # utf-8-sig гарантирует корректное отображение кириллицы в Excel
        with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Задача", "Пользователь", "Дата создания"])
            writer.writerows(tasks)
        return filepath