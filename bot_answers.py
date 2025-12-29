# =========FIRST EDITION=========

# import time
# import concurrent.futures as cc
# import os

# def task(start, end):
#     s = 0
#     for i in range(start, end):
#         s += i
#     return s

# if __name__ == '__main__':
#     N = 100_000_000
#     cpu_count = os.cpu_count()
#     chunk = N // cpu_count

#     ranges = [
#         (i * chunk, (i + 1) * chunk)
#         for i in range(cpu_count)
#     ]

#     start = time.time()
#     with cc.ProcessPoolExecutor() as exc:
#         results = exc.map(lambda x: task(*x), ranges)

#     total = sum(results)
#     end = time.time()

#     print(total, "time:", end - start)

# ===================== second edition =====================

# import time
# import os
# from concurrent.futures import ProcessPoolExecutor, as_completed

# def task(start, end):
#     s = 0
#     for i in range(start, end):
#         s += i
#     return s

# if __name__ == '__main__':
#     N = 100_000_000
#     cpu_count = os.cpu_count()
#     chunk = N // cpu_count

#     ranges = [
#         (i * chunk, (i + 1) * chunk)
#         for i in range(cpu_count)
#     ]

#     start = time.time()

#     total = 0
#     with ProcessPoolExecutor() as exc:
#         futures = [
#             exc.submit(task, start, end)
#             for start, end in ranges
#         ]

#         for future in as_completed(futures):
#             total += future.result()

#     end = time.time()

#     print(total, "time:", end - start)

# ================= 3rd edition ================

import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

def file_size(path: Path) -> int:
    return path.stat().st_size

def total_size_parallel(root: Path, workers: int = 4) -> int:
    files = list(root.rglob('*'))
    total = 0

    with ThreadPoolExecutor(max_workers=workers) as exc:
        futures = [exc.submit(file_size, f) for f in files if f.is_file()]

        for future in as_completed(futures):
            total += future.result()

    return total

if __name__ == "__main__":
    p = Path("i:/")
    start = time.time()
    size = total_size_parallel(p, workers=4)
    end = time.time()
    print(f"Total size: {size} bytes")
    print(f"Time: {end - start}")
