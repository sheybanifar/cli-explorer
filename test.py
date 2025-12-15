import time
import concurrent.futures as cc

l = range(100_000_000)

def task(iterable):
    result = 0
    for i in iterable:
        result += i
    return result

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

start = time.time()
with cc.ProcessPoolExecutor() as exc:
    future = exc.submit(task, l)
    result = future.result()
end = time.time()

print(result, f'ProcessPool time: {end - start}')