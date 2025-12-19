import multiprocessing
import time
import math


def calculate_factorial(n):
    """
    Вычисляет факториал числа (CPU-intensive операция)
    """
    print(f"Начало вычисления факториала {n}!")
    result = math.factorial(n)
    print(f"Завершено вычисление факториала {n}!")
    return result


def calculate_prime(n):
    """
    Проверяет, является ли число простым
    """
    print(f"Начало проверки числа {n} на простоту")

    if n < 2:
        result = False
    else:
        result = all(n % i != 0 for i in range(2, int(math.sqrt(n)) + 1))

    print(f"Число {n} простое: {result}")
    return result


def worker(func, arg, queue):
    """Функция-воркер для выполнения в процессе"""
    result = func(arg)
    queue.put(result)


def task3_multiprocess_calculations():
    """
    Задача: Реализуйте многопроцессные вычисления.
    """
    calculations = [
        (calculate_factorial, 10000),
        (calculate_factorial, 8000),
        (calculate_prime, 10000019),
        (calculate_prime, 10000033)
    ]

    # Многопроцессное выполнение
    print("=== МНОГОПРОЦЕССНОЕ ВЫПОЛНЕНИЕ ===")
    start_time = time.time()

    processes = []
    queue = multiprocessing.Queue()
    results = []

    # Создаем и запускаем процессы
    for func, arg in calculations:
        process = multiprocessing.Process(
            target=worker,
            args=(func, arg, queue)
        )
        processes.append(process)
        process.start()

    # Дожидаемся завершения всех процессов
    for process in processes:
        process.join()

    # Получаем результаты из очереди
    while not queue.empty():
        results.append(queue.get())

    end_time = time.time()
    multiprocess_time = end_time - start_time

    # Синхронное выполнение для сравнения
    print("\n=== СИНХРОННОЕ ВЫПОЛНЕНИЕ ===")
    start_time = time.time()

    sync_results = []
    for func, arg in calculations:
        sync_results.append(func(arg))

    end_time = time.time()
    sync_time = end_time - start_time

    print(f"\nСравнение времени:")
    print(f"Многопроцессное: {multiprocess_time:.2f} сек")
    print(f"Синхронное: {sync_time:.2f} сек")

    if multiprocess_time > 0:
        acceleration = sync_time / multiprocess_time
        print(f"Ускорение: {acceleration:.2f}x")


# Запуск задачи
if __name__ == "__main__":
    task3_multiprocess_calculations()
