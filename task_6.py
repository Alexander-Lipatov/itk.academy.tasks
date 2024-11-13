import random
import math
from typing import List
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, cpu_count, Process, set_start_method, Queue
import time
from queue import Empty


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f'{func.__name__} took {end - start}s')
        return result
    return wrapper


def genrate_data(n: int, start: int = 0, end: int = 1000) -> list[int]:
    """Генерируем списолк n чисел от start до end """
    return [random.randint(start, end) for _ in range(n)]


def process_number(number: int) -> int:
    """Обрабатываем число и возвращаем его факториал """
    return math.factorial(number)


# ****************************************************************

@timeit
def simple_variante(data: list[int]):
    for number in data:
        process_number(number)

# ****************************************************************


@timeit
def variant_a(data: list[int]):
    with ThreadPoolExecutor(max_workers=10) as executor:
        for number in data:
            executor.submit(process_number, number)

# ****************************************************************


@timeit
def variant_b(data: list[int]):
    with Pool(processes=cpu_count()) as p:
        p.map(process_number, data)


# ****************************************************************

def worker(input_queue, output_queue):
    while True:
        try:
            numbers = input_queue.get()
        except Empty:
            continue

        if numbers is None:
            break

        results = [process_number(number) for number in numbers]
        output_queue.put(results)


@timeit
def variant_c(data: list[int]):
    processes: list[Process] = []
    input_queue = Queue()
    output_queue = Queue()

    i = 0
    size_queue = int(len(data)/cpu_count())

    # Создаем процессы и запускаем их
    for _ in range(cpu_count()):
        p = Process(target=worker, args=(input_queue, output_queue))
        processes.append(p)
        p.start()

    # Заполнение input_queue данными
    while len(data) > i:
        numbers = data[i:size_queue+i]
        input_queue.put(numbers)
        i += size_queue

    # Отправляем сигнал завершения для каждого процесса
    for _ in processes:
        input_queue.put(None)

    # Сбор результатов из output_queue
    results = []
    while any(p.is_alive() for p in processes) or not output_queue.empty():
        try:
            results.extend(output_queue.get(timeout=0))
        except Empty:
            continue

    # Ожидание завершения всех процессов
    for p in processes:
        p.join()



if __name__ == '__main__':
    data = genrate_data(1000000)

    simple_variante(data)
    variant_a(data)
    variant_b(data)
    variant_c(data)
