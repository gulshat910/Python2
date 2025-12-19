import sqlite3
from datetime import datetime

DB_PATH = 'university.db'

#  Создание базы и таблиц 
def init_db():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    group_name TEXT NOT NULL,
                    admission_year INTEGER NOT NULL,
                    average_grade REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_name TEXT UNIQUE NOT NULL,
                    instructor TEXT NOT NULL,
                    credits INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS student_courses (
                    student_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    PRIMARY KEY (student_id, course_id),
                    FOREIGN KEY (student_id) REFERENCES students(id),
                    FOREIGN KEY (course_id) REFERENCES courses(id)
                )
            """)
            print("База данных и таблицы созданы")
    except sqlite3.Error as e:
        print(f"Ошибка инициализации БД: {e}")

#  CRUD студенты 
def add_student(first_name, last_name, group_name, admission_year, average_grade=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students (first_name, last_name, group_name, admission_year, average_grade)
                VALUES (?, ?, ?, ?, ?)
            """, (first_name, last_name, group_name, admission_year, average_grade))
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Ошибка добавления студента: {e}")
        return None

def get_all_students():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        return [dict(row) for row in cursor.fetchall()]

def get_students_by_group(group_name):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE group_name = ?", (group_name,))
        return [dict(row) for row in cursor.fetchall()]

def update_student_grade(student_id, new_grade):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE students SET average_grade = ? WHERE id = ?", (new_grade, student_id))
    except sqlite3.Error as e:
        print(f"Ошибка обновления оценки: {e}")

def delete_student(student_id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    except sqlite3.Error as e:
        print(f"Ошибка удаления студента: {e}")

#  CRUD курсы 
def add_course(course_name, instructor, credits):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO courses (course_name, instructor, credits) VALUES (?, ?, ?)",
                           (course_name, instructor, credits))
            return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Ошибка добавления курса: {e}")
        return None

def enroll_student_in_course(student_id, course_id):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)",
                           (student_id, course_id))
    except sqlite3.IntegrityError:
        pass  # студент уже зачислен
    except sqlite3.Error as e:
        print(f"Ошибка зачисления на курс: {e}")

def get_student_courses(student_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, c.course_name, c.instructor
            FROM courses c
            JOIN student_courses sc ON c.id = sc.course_id
            WHERE sc.student_id = ?
        """, (student_id,))
        return [dict(row) for row in cursor.fetchall()]

def transfer_student(student_id, new_group):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("BEGIN")
            cursor.execute("UPDATE students SET group_name = ? WHERE id = ?", (new_group, student_id))
            cursor.execute("DELETE FROM student_courses WHERE student_id = ?", (student_id,))
            conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Ошибка перевода студента: {e}")

#  Консольный интерфейс 
def main_menu():
    init_db()
    while True:
        print("\n=== Университетский учет ===")
        print("1. Добавить студента")
        print("2. Просмотреть всех студентов")
        print("3. Найти студентов по группе")
        print("4. Обновить оценку студента")
        print("5. Удалить студента")
        print("6. Добавить курс")
        print("7. Зачислить студента на курс")
        print("8. Показать курсы студента")
        print("9. Перевести студента в другую группу")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            first_name = input("Имя: ")
            last_name = input("Фамилия: ")
            group_name = input("Группа: ")
            admission_year = int(input("Год поступления: "))
            add_student(first_name, last_name, group_name, admission_year)
        elif choice == '2':
            for s in get_all_students():
                print(s)
        elif choice == '3':
            group = input("Группа: ")
            for s in get_students_by_group(group):
                print(s)
        elif choice == '4':
            student_id = int(input("ID студента: "))
            grade = float(input("Новый средний балл: "))
            update_student_grade(student_id, grade)
        elif choice == '5':
            student_id = int(input("ID студента: "))
            delete_student(student_id)
        elif choice == '6':
            name = input("Название курса: ")
            instructor = input("Преподаватель: ")
            credits = int(input("Количество кредитов: "))
            add_course(name, instructor, credits)
        elif choice == '7':
            student_id = int(input("ID студента: "))
            course_id = int(input("ID курса: "))
            enroll_student_in_course(student_id, course_id)
        elif choice == '8':
            student_id = int(input("ID студента: "))
            for c in get_student_courses(student_id):
                print(c)
        elif choice == '9':
            student_id = int(input("ID студента: "))
            new_group = input("Новая группа: ")
            transfer_student(student_id, new_group)
        elif choice == '0':
            break
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main_menu()
