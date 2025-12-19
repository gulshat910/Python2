import sqlite3
from datetime import datetime, timedelta


class LibraryManager:
    def __init__(self, db_path='library.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Инициализация базы данных и таблиц"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER,
                    genre TEXT,
                    is_available BOOLEAN DEFAULT 1
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS readers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    registration_date DATE DEFAULT CURRENT_DATE
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS borrowings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    reader_id INTEGER NOT NULL,
                    borrow_date DATE DEFAULT CURRENT_DATE,
                    return_date DATE,
                    FOREIGN KEY (book_id) REFERENCES books(id),
                    FOREIGN KEY (reader_id) REFERENCES readers(id)
                )
            """)

    def add_book(self, title, author, year=None, genre=None):
        """Добавить новую книгу в библиотеку"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO books (title, author, year, genre) VALUES (?, ?, ?, ?)",
                    (title, author, year, genre)
                )
                print(f"Книга '{title}' добавлена")
        except sqlite3.Error as e:
            print(f"Ошибка добавления книги: {e}")

    def add_reader(self, name, email=None, phone=None):
        """Зарегистрировать нового читателя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO readers (name, email, phone) VALUES (?, ?, ?)",
                    (name, email, phone)
                )
                print(f"Читатель '{name}' зарегистрирован")
        except sqlite3.IntegrityError:
            print(f"Ошибка: читатель с email '{email}' уже существует")
        except sqlite3.Error as e:
            print(f"Ошибка добавления читателя: {e}")

    def borrow_book(self, book_id, reader_id):
        """Выдать книгу читателю с проверкой доступности"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("SELECT is_available, title FROM books WHERE id = ?", (book_id,))
                book = cursor.fetchone()
                if not book:
                    raise ValueError("Книга не найдена")
                if not book['is_available']:
                    raise ValueError("Книга уже выдана")

                # Транзакция выдачи книги
                cursor.execute("UPDATE books SET is_available = 0 WHERE id = ?", (book_id,))
                cursor.execute("INSERT INTO borrowings (book_id, reader_id) VALUES (?, ?)", (book_id, reader_id))
                print(f"Книга '{book['title']}' успешно выдана читателю с ID {reader_id}")
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def return_book(self, borrowing_id):
        """Вернуть книгу в библиотеку"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("SELECT book_id FROM borrowings WHERE id = ? AND return_date IS NULL", (borrowing_id,))
                borrow = cursor.fetchone()
                if not borrow:
                    raise ValueError("Выдача не найдена или книга уже возвращена")

                # Транзакция возврата книги
                cursor.execute("UPDATE books SET is_available = 1 WHERE id = ?", (borrow['book_id'],))
                cursor.execute("UPDATE borrowings SET return_date = ? WHERE id = ?",
                               (datetime.now().date(), borrowing_id))
                print("Книга возвращена в библиотеку")
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def find_available_books(self, author=None, genre=None):
        """Найти доступные книги с фильтрацией"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                query = "SELECT * FROM books WHERE is_available = 1"
                params = []
                if author:
                    query += " AND author LIKE ?"
                    params.append(f"%{author}%")
                if genre:
                    query += " AND genre LIKE ?"
                    params.append(f"%{genre}%")
                cursor.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Ошибка поиска книг: {e}")
            return []

    def get_reader_borrowings(self, reader_id):
        """Получить список текущих выдач читателя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT b.id, b.title, br.borrow_date
                    FROM borrowings br
                    JOIN books b ON br.book_id = b.id
                    WHERE br.reader_id = ? AND br.return_date IS NULL
                """, (reader_id,))
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Ошибка получения выдач: {e}")
            return []

    def get_overdue_borrowings(self, days=30):
        """Найти просроченные выдачи больше N дней"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                limit_date = (datetime.now() - timedelta(days=days)).date()
                cursor.execute("""
                    SELECT br.id, b.title, r.name, br.borrow_date
                    FROM borrowings br
                    JOIN books b ON br.book_id = b.id
                    JOIN readers r ON br.reader_id = r.id
                    WHERE br.return_date IS NULL AND br.borrow_date < ?
                """, (limit_date,))
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Ошибка поиска просрочек: {e}")
            return []


# Пример использования
def main():
    library = LibraryManager()

    # Добавляем книги
    library.add_book("Преступление и наказание", "Федор Достоевский", 1866, "Роман")
    library.add_book("Мастер и Маргарита", "Михаил Булгаков", 1967, "Роман")
    library.add_book("1984", "Джордж Оруэлл", 1949, "Антиутопия")

    # Регистрируем читателей
    library.add_reader("Иван Иванов", "ivan@mail.com", "+79161234567")
    library.add_reader("Петр Петров", "petr@mail.com", "+79167654321")

    # Выдаем книги
    library.borrow_book(1, 1)
    library.borrow_book(2, 2)

    # Пытаемся выдать уже занятую книгу
    library.borrow_book(1, 2)

    # Ищем доступные книги
    available = library.find_available_books(author="Джордж Оруэлл")
    print("Доступные книги Оруэлла:", available)

    # Возвращаем книгу
    library.return_book(1)

    # Проверяем, что книга снова доступна
    available = library.find_available_books()
    print("Все доступные книги:", available)


if __name__ == "__main__":
    main()
