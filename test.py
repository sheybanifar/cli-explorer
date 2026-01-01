# import time
# import concurrent.futures as cc

# l = range(100_000_000)

# def task(iterable):
#     result = 0
#     for i in iterable:
#         result += i
#     return result

# start = time.time()
# result = task(l)
# end = time.time()

# print(result, f'Sequential time: {end - start}')

# start = time.time()
# with cc.ThreadPoolExecutor() as exc:
#     future = exc.submit(task, l)
#     result = future.result()
# end = time.time()
    

# print(result, f'ThreadPool time: {end - start}')

# def main():
#     start = time.time()
#     with cc.ProcessPoolExecutor() as exc:
#         future = exc.submit(task, l)
#         result = future.result()
#     end = time.time()

#     print(result, f'ProcessPool time: {end - start}')

# if __name__ == '__main__':
#     main()

# import time
# from pathlib import Path
# import concurrent.futures as cc

# def file_size(path: Path) -> int:
#     return path.stat().st_size

# p = Path('i:/')

# def sub_files(path: Path):
#     path_walk = path.walk()
#     for item in path_walk:
#         for filename in item[-1]:
#             path_obj = item[0] / filename
#             yield file_size(path_obj)

# start = time.time()

# with cc.ProcessPoolExecutor() as exc:
#     future = exc.submit(sub_files, p)
#     total = future.result()

# end = time.time()
# print(f'elapsed time: {end - start}s   {total}')
# total = sum(f for f in sub_files(p))
# ======================= 

# def sub_files(path: Path):
#     total_size = 0
#     for item in path.walk():
#         for filename in item[-1]:
#             path_obj = item[0] / filename
#             total_size += file_size(path_obj)
#     return total_size

# ======================= 

# import time
# from pathlib import Path
# import os

# def file_size(path: Path) -> int:
#     return path.stat().st_size

# p = Path('i:/')

# def sub_files(path: Path):
#     sizes_iterator = []
#     path_walk = path.walk()
#     for item in path_walk:
#         for filename in item[-1]:
#             path_obj = item[0] / filename
#             sizes_iterator.append(path_obj)
#     yield iter(sizes_iterator)

# ranges = [

# ]

# chunk = 

# =======================================
# SuperFastPython.com
# example of waiting for tasks to complete in the process pool
from time import sleep
from random import random
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import wait
 
# custom task that will sleep for a variable amount of time
def task(name):
    # sleep for less than a second
    sleep(random())
    print(f'Done: {name}')
 
# entry point
if __name__ == '__main__':
    # start the process pool
    with ProcessPoolExecutor(2) as executor:
        # submit tasks and collect futures
        futures = [executor.submit(task, i) for i in range(10)]
        # wait for all tasks to complete
        print('Waiting for tasks to complete...')
        executor.shutdown(wait=False, cancel_futures=True)
        print('All tasks are done!')
    print('this is from put of the context manager')