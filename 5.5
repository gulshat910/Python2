import time
import threading
import multiprocessing
import asyncio


def io_task(name, duration):
    """I/O-bound задача"""
    time.sleep(duration)
    print(f"{name} completed")
    return f"{name} completed"


async def async_io_task(name, duration):
    """Асинхронная I/O-bound задача"""
    await asyncio.sleep(duration)
    print(f"{name} completed")
    return f"{name} completed"


# Функция для многопроцессного выполнения (должна быть определена на верхнем уровне)
def process_worker(name, duration):
    """Рабочая функция для процесса"""
    time.sleep(duration)
    print(f"{name} completed")
    return f"{name} completed"


def task5_performance_comparison():
    """
    Задача: Сравните производительность разных подходов.

    Набор I/O-bound задач (имитация):
    1. "Task1" - 2 секунды
    2. "Task2" - 3 секунды
    3. "Task3" - 1 секунда
    4. "Task4" - 2 секунды
    5. "Task5" - 1 секунда
    """
    tasks = [("Task1", 2), ("Task2", 3), ("Task3", 1), ("Task4", 2), ("Task5", 1)]

    # 1. Синхронное выполнение
    print("=== СИНХРОННОЕ ВЫПОЛНЕНИЕ ===")
    start_time = time.time()

    for name, duration in tasks:
        io_task(name, duration)

    sync_time = time.time() - start_time

    # 2. Многопоточное выполнение
    print("\n=== МНОГОПОТОЧНОЕ ВЫПОЛНЕНИЕ ===")
    start_time = time.time()

    threads = []
    for name, duration in tasks:
        thread = threading.Thread(target=io_task, args=(name, duration))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    thread_time = time.time() - start_time

    # 3. Многопроцессное выполнение (используем process_worker чтобы избежать рекурсии)
    print("\n=== МНОГОПРОЦЕССНОЕ ВЫПОЛНЕНИЕ ===")
    start_time = time.time()

    processes = []
    for name, duration in tasks:
        process = multiprocessing.Process(target=process_worker, args=(name, duration))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    process_time = time.time() - start_time

    # 4. Асинхронное выполнение
    print("\n=== АСИНХРОННОЕ ВЫПОЛНЕНИЕ ===")

    async def run_async():
        async_tasks = []
        for name, duration in tasks:
            async_tasks.append(async_io_task(name, duration))

        await asyncio.gather(*async_tasks)

    start_time = time.time()
    asyncio.run(run_async())
    async_time = time.time() - start_time

    # Анализ результатов
    print("\n=== АНАЛИЗ РЕЗУЛЬТАТОВ ===")
    print(f"Синхронное время: {sync_time:.2f} сек")
    print(f"Многопоточное время: {thread_time:.2f} сек")
    print(f"Многопроцессное время: {process_time:.2f} сек")
    print(f"Асинхронное время: {async_time:.2f} сек")

    # Выводы
    print("\n=== ВЫВОДЫ ===")
    print("Для I/O-bound задач (имитированных time.sleep):")
    print("1. Синхронный подход самый медленный (сумма всех задержек)")
    print("2. Многопоточный и асинхронный подходы самые быстрые")
    print("3. Многопроцессный подход быстрый, но имеет больше накладных расходов")
    print("4. Асинхронность наиболее эффективна для большого количества I/O операций")


# Запуск задачи
if __name__ == "__main__":
    task5_performance_comparison()
