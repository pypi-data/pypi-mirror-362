import os
import time
import functools
import logging
import tracemalloc
import psutil
from typing import Optional, Callable
from pathlib import Path


class PerformanceMonitor:
    @staticmethod
    def timer(logger: Optional[logging.Logger] = None):
        """
        Decorator to measure function execution time with optional logging
        
        :param logger: Optional logger to use instead of print
        :type logger: logging.Logger, optional
        """
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()

                execution_time = end_time - start_time
                hours = int(execution_time // 3600)
                minutes = int((execution_time % 3600) // 60)
                seconds = int(execution_time % 60)
                milliseconds = int((execution_time % 1) * 1000)

                formatted_time = f"{hours}h {minutes}m {seconds}s {milliseconds:03d}ms"

                log_message = f"{func.__name__} levou {formatted_time}"

                if logger:
                    logger.info(log_message)
                else:
                    print(log_message)

                return result
            return wrapper
        return decorator

    @staticmethod
    def memory_tracker(logger: Optional[logging.Logger] = None):
        """
        Decorator to track memory usage with optional logging
        
        :param logger: Optional logger to use instead of print
        :type logger: logging.Logger, optional
        """
        def decorator(func: Callable):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                tracemalloc.start()

                result = func(*args, **kwargs)

                current, peak = tracemalloc.get_traced_memory()
                memory_message = (
                    f"\nFunção: {func.__name__}.\n"
                    f"Uso de memória:\n"
                    f"- Memoria corrente pós processamento {current / 1024 / 1024:.4f} MB\n"
                    f"- Pico {peak / 1024 / 1024:.4f} MB"
                )
                if logger:
                    logger.info(memory_message)
                else:
                    print(memory_message)

                tracemalloc.stop()
                return result
            return wrapper
        return decorator


class ManageExecution:
    @staticmethod
    def check_and_manage_execution(etapa: str = 'inicio', pid_file: str = 'execution.pid') -> bool:
        """
        Gerencia a execução única do script através de arquivo PID
        
        Args:
            etapa: 'inicio' para verificar/criar PID ou 'fim' para remover
            pid_file: nome do arquivo para armazenar o PID
        Returns:
            bool: True se pode executar, False se já está em execução
        """
        pid_path = Path(pid_file)

        if etapa == 'inicio':
            if pid_path.exists():
                try:
                    with open(pid_path, 'r') as f:
                        old_pid = int(f.read().strip())

                    if psutil.pid_exists(old_pid):
                        print(f"Processo já está em execução (PID: {old_pid})")
                        return False
                    else:
                        pid_path.unlink()
                except (ValueError, IOError) as e:
                    print(f"Erro ao ler arquivo PID: {e}")
                    pid_path.unlink(missing_ok=True)

            try:
                with open(pid_path, 'w') as f:
                    f.write(str(os.getpid()))
                return True
            except IOError as e:
                print(f"Erro ao criar arquivo PID: {e}")
                return False

        elif etapa == 'fim':
            # Remove arquivo PID
            pid_path.unlink(missing_ok=True)
            return True

        return False

    @staticmethod
    def run_with_pid_control(func):
        def wrapper(*args, **kwargs):
            if ManageExecution.check_and_manage_execution(etapa='inicio'):
                try:
                    result = func(*args, **kwargs)
                    ManageExecution.check_and_manage_execution(etapa='fim')
                    return result
                except Exception as e:
                    ManageExecution.check_and_manage_execution(etapa='fim')
                    raise e
            return None
        return wrapper


if __name__ == '__main__':
    performance = PerformanceMonitor()

    @performance.memory_tracker()
    @performance.timer()
    def slow_function():
        time.sleep(2)
        return "Done"

    result = slow_function()

    @performance.memory_tracker()
    @performance.timer()
    def memory_intensive_function():
        data = [i for i in range(1000000)]

        temp = [i**2 for i in data]

        processed_data = [x for x in temp if x % 2 == 0]

        return data, processed_data

    result = memory_intensive_function()
