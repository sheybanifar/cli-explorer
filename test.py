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

import time
from pathlib import Path

def file_size(path: Path) -> int:
    return path.stat().st_size

p = Path('i:/')

def sub_files(path: Path):
    path_walk = path.walk()
    for item in path_walk:
        for filename in item[-1]:
            path_obj = item[0] / filename
            return file_size(path_obj)

start = time.time()
total = sum(f for f in sub_files(p))
end = time.time()
print(f'elapsed time: {end - start}s   {total}')

# ======================= 

import time
from pathlib import Path
import os

def file_size(path: Path) -> int:
    return path.stat().st_size

p = Path('i:/')

def sub_files(path: Path):
    sizes_iterator = []
    path_walk = path.walk()
    for item in path_walk:
        for filename in item[-1]:
            path_obj = item[0] / filename
            sizes_iterator.append(path_obj)
    yield iter(sizes_iterator)

ranges = [

]

chunk = 
