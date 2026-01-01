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

# import time
# from pathlib import Path
# from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed

# def file_size(path: Path) -> int:
#     return path.stat().st_size

# def total_size_parallel(root: Path, workers: int = 4) -> int:
#     files = list(root.rglob('*'))
#     total = 0

#     with ThreadPoolExecutor(max_workers=workers) as exc:
#         futures = [exc.submit(file_size, f) for f in files if f.is_file()]

#         for future in as_completed(futures):
#             total += future.result()

#     return total

# if __name__ == "__main__":
#     p = Path("i:/")
#     start = time.time()
#     size = total_size_parallel(p, workers=4)
#     end = time.time()
#     print(f"Total size: {size} bytes")
#     print(f"Time: {end - start}")

# ================= 4th edition ================

import concurrent.futures as cc
import time
from pathlib import Path

from pathlib import Path

def batch_size(files: list[Path]) -> int:
    total = 0
    for f in files:
        try:
            total += f.stat().st_size
        except (PermissionError, FileNotFoundError):
            pass
    return total

def all_files(root: Path):
    for dirpath, _, filenames in Path.walk(root):
        for name in filenames:
            yield Path(dirpath) / name

def chunked(iterable, size):
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

if __name__ == "__main__":
    root = Path("c:/")
    BATCH_SIZE = 1000

    start = time.time()

    files = all_files(root)
    batches = chunked(files, BATCH_SIZE)

    total = 0
    with cc.ProcessPoolExecutor() as executor:
        futures = [executor.submit(batch_size, batch) for batch in batches]

        for future in cc.as_completed(futures):
            total += future.result()

    end = time.time()
    print(f"elapsed time: {end - start:.2f}s   total={total}")

# ================= 5th edition ================

# import concurrent.futures as cc
# import time
# from pathlib import Path
# import os

# def batch_size(files: list[Path]) -> int:
#     total = 0
#     for f in files:
#         try:
#             total += f.stat().st_size
#         except (PermissionError, FileNotFoundError):
#             pass
#     return total

# def all_files(root: Path):
#     for dirpath, _, filenames in os.walk(root):
#         for name in filenames:
#             yield Path(dirpath) / name

# def chunked(iterable, size):
#     chunk = []
#     for item in iterable:
#         chunk.append(item)
#         if len(chunk) == size:
#             yield chunk
#             chunk = []
#     if chunk:
#         yield chunk

# if __name__ == "__main__":
#     root = Path("i:/")
#     BATCH_SIZE = 1000

#     start = time.time()

#     files = all_files(root)
#     batches = chunked(files, BATCH_SIZE)

#     total = 0
#     with cc.ThreadPoolExecutor(max_workers=2) as executor:
#         futures = [executor.submit(batch_size, batch) for batch in batches]

#         for future in cc.as_completed(futures):
#             total += future.result()

#     end = time.time()
#     print(f"elapsed time: {end - start:.2f}s   total={total}")
