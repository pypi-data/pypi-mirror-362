from functools import wraps
import time


def perf_counter_deco(func):
    """Декоратор для вимірювання часу виконання функції."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(
            f"Функція '{func.__name__}' виконалась за {end_time - start_time:.6f} секунд"
        )
        return result

    return wrapper
