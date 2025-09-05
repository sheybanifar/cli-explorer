from pathlib import Path

path_iter = Path('I:\\Videos\\Tutorial').resolve().iterdir()

def get_length():   
    '''Get length of the directory iterator'''
    length = 0
    for i in path_iter:
        length += 1
    return length

def get_mode(path):
    '''look for path mode, which is either a directory or a file'''
    if path.is_dir():
        return 'D'
    else:
        return 'F'
    
def get_last_modified_time(path):
    '''getting the last modified time'''
    import time
    lastModifiedTimeInSec = time.gmtime(path.stat().st_mtime)
    lastModifiedTime = time.strftime(r'%m/%d/%Y %H:%M:%S', lastModifiedTimeInSec)
    return lastModifiedTime

def get_size(path):
    KB = 1000
    MB = KB ** 2
    GB = MB ** 2
    if not path.is_dir():
        size_in_bytes = path.stat().st_size
        # print(size_in_bytes)
        if size_in_bytes < KB:
            size = f'{size_in_bytes}B'
        elif KB <= size_in_bytes <  MB:
            size_kb = round(size_in_bytes / KB)
            size = f'{size_kb} KB'
        elif MB <= size_in_bytes <= GB:
            size_mb = round(size_in_bytes / MB)
            size = f'{size_mb} MB'
        elif GB <= size_in_bytes:
            size_gb = round(size_in_bytes / GB, 1)
            size = f'{size_gb} GB'
        return size
    else:
        return ''
    
def get_pathname(path):
    if path.is_dir():
        pathname = path.name + '/'
        return pathname
    else:
        return path.name
    
Id = 1
path_data = {}
def yield_row():
    global Id
    for path in path_iter:
        mode = get_mode(path)
        last_modified_time = get_last_modified_time(path)
        size = get_size(path)
        name = get_pathname(path)
        # print(Id)
        path_data[Id] = (
            mode,
            last_modified_time,
            size,
            name,
        )
        Id += 1
    yield path_data

output = yield_row()

for o in output:
    print(*o.items(), sep='\n')

# print(*path_data.items(), sep='\n')

# output = next(yield_path())
# print(output)
# print(row for row in yield_path())
    
# length = get_length()
# print(length)

# data = [
#     [1, 2, 3, 4, 5],
#     [22, 33, 44, 5545, 567],
#     [546, 6548, 453354, 54354, 44],
#     [645454, 44, 58823, 45, 3888465]
# ]

