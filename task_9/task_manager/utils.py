import time
from datetime import datetime

from django.db import transaction

from .models import Task


def worker(worker_id):
    """
    Декоратор для рабочих функций.
    """
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                while True:
                    task = fetch_task(worker_id) 
                    if task:
                        func(task, *args, **kwargs)
                        complete_task(task)
                    else:
                        print(f"Worker {worker_id}: Нет доступных задач. Повторная попытка через 5 секунд...")
                        time.sleep(5)
            except KeyboardInterrupt:
                print(f"Worker {worker_id}: Interrupted.")
                
        return wrapper
    return decorator




def fetch_task(worker_id):
    """
    Получить задачу из очереди.
    """
    with transaction.atomic():
        task = Task.objects.select_for_update(skip_locked=True).filter(status='pending').first()
        if task:
            task.status = 'processing'
            task.worker_id = worker_id
            task.updated_at = datetime.now()
            task.save(update_fields=['status', 'worker_id', 'updated_at'])
            return task
    return None


def complete_task(task:Task):
    """
    Завершить выполнение задачи.
    """

    task.status = 'completed'
    task.updated_at = datetime.now()
    task.save(update_fields=['status', 'updated_at'])



@worker(worker_id=1)
def my_func(task: Task):
    print(f"Worker запущен...")
    print("Текущая задача: " + task.task_name)
    print("worker_id задачи: " + str(task.worker_id))
    time.sleep(1)

