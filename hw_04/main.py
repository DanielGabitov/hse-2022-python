import multiprocessing
import threading
import os
import math

from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed


def fib(n: int):
    if n <= 0:
        raise RuntimeError()
    nums = [-1] * n
    nums[0] = 0
    nums[1] = 1
    if n <= 2:
        return nums[n - 1]
    for i in range(2, n - 1):
        nums[i] = nums[i - 1] + nums[i - 2]
    return nums[n - 1]


def integrate(f, a, b, *, n_jobs=1, n_iter=10000):
    acc = 0
    step = (b - a) / n_iter
    for i in range(n_iter):
        acc += f(a + i * step) * step
    return acc


def integrate_updated(f, a, b, *, pool, n_jobs=4, n_iter=100_000_00):
    acc = 0
    step = (b - a) / n_iter
    futures = []
    with pool(max_workers=n_jobs) as executor:
        for i in range(n_jobs):
            futures.append(executor.submit(integrate_subroutine, f, a + i * (b - a) / n_jobs, step, n_iter // n_jobs, pool == ThreadPoolExecutor))
    logs = []
    for future in as_completed(futures):
        value, log = future.result()
        acc += value
        logs.append(log)
    return acc, "\n".join(logs)


def integrate_subroutine(f, a, step, step_n, is_thread_pool):
    now = datetime.now()
    log = ''
    log += f'{now.hour}:{now.minute}:{now.second}:{now.microsecond} '
    if is_thread_pool:
        log += f'Thread {threading.get_ident()} started working on function {f.__name__} integration'
    else:
        log += f'Process {os.getpid()} started working on function {f.__name__} integration'
    log += '\n'
    acc = 0
    for i in range(step_n):
        acc += f(a + i * step) * step
    log += f'{now.hour}:{now.minute}:{now.second}:{now.microsecond} '
    if is_thread_pool:
        log += f'Thread {threading.get_ident()} ended working on function {f.__name__} integration'
    else:
        log += f'Process {os.getpid()} ended working on function {f.__name__} integration'
    return acc, log


if __name__ == '__main__':
    file = open("artifacts/easy.txt", "w")
    iter_amount = 10
    n = 100000

    start_time = datetime.now()
    for _ in range(iter_amount):
        fib(n)
    result = datetime.now() - start_time
    file.write(f"No threading/multiprocessing:\n{str(result)}\n")

    start_time = datetime.now()
    threads = []
    for _ in range(iter_amount):
        thread = threading.Thread(target=fib, args=(n,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    result = datetime.now() - start_time
    file.write(f"Threading:\n{str(result)}\n")

    start_time = datetime.now()
    processes = []
    for _ in range(iter_amount):
        process = multiprocessing.Process(target=fib, args=(n,))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    result = datetime.now() - start_time
    file.write(f"Multiprocessing:\n{str(result)}")
    file.close()

    ## LOGGING
    with open('artifacts/medium_logs.txt', 'w') as file:
        _, t_log = integrate_updated(math.cos, 0, math.pi / 2, pool=ThreadPoolExecutor)
        _, p_log = integrate_updated(math.cos, 0, math.pi / 2, pool=ProcessPoolExecutor)
        file.write(t_log + '\n' + p_log)

    ## TIME CMP

    with open('artifacts/medium_cmp.txt', 'w') as file:
        cpu_amount = 4
        for jobs in range(1, cpu_amount * 2 + 1):
            thread_pool_start_time = datetime.now()
            integrate_updated(math.cos, 0, math.pi / 2, n_jobs=jobs, pool=ThreadPoolExecutor)
            thread_pool_result_time = datetime.now() - thread_pool_start_time

            process_pool_start_time = datetime.now()
            integrate_updated(math.cos, 0, math.pi / 2, n_jobs=jobs, pool=ProcessPoolExecutor)
            process_pool_result_time = datetime.now() - process_pool_start_time
            file.write(f'Workers: {jobs}, ThreadPool: {thread_pool_result_time}, ProcessPool: {process_pool_result_time}\n')
