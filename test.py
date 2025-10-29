from pathlib import Path

path_iter = Path('c:\\Windows').resolve().iterdir()

def get_length():   
    '''Get length of the directory iterator'''
    length = 0
    for i in path_iter:
        length += 1
    return length

def get_mode(path):
    '''look for path mode whether is a directory or a file'''
    if path.is_dir():
        return 'D'
    else:
        return 'F'
    
def get_last_modified_time(path):
    '''getting last modified time'''
    import time
    lastModifiedTimeInSec = time.gmtime(path.stat().st_mtime)
    lastModifiedTime = time.strftime(r'%m/%d/%Y %H:%M', lastModifiedTimeInSec)
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
    
def yield_row():
    _id = 1
    path_data = [('Id', 'Mode', 'Date Modified', 'Size', 'Name'),
                 ('--', '-'*4, '-'*13, '-'*4, '-'*4)]
    for path in path_iter:
        mode = get_mode(path)
        last_modified_time = get_last_modified_time(path)
        size = get_size(path)
        name = get_pathname(path)
        path_data.append((
            str(_id),
            mode,
            last_modified_time,
            size,
            name
        ))
        _id += 1
    yield path_data

rows = yield_row()

def get_max_col():
    # id = 0
    # name_lengths = []
    for row in rows:
        if len(row) < 10:
            id_length = str(2)
        else:
            id_length = len(str(len(row)))
        # for col in row:
            # name_lengths.append(len(col[-1]))
            # max_name_len = max(name_lengths)
        max_name_len = max(len(col[-1]) for col in row) + 1
        for col in row:
            # print(col[4])
            print(col[0].ljust(id_length), col[1].center(9), col[2].rjust(18), col[3].rjust(8), col[4].ljust(max_name_len))
        
get_max_col()
# id_col_len, name_col_len = get_max_col()
# print(id_col_len, name_col_len)

# data = [
#     [1, 2, 3, 4, 5],
#     [22, 33, 44, 5545, 567],
#     [546, 6548, 453354, 54354, 44],
#     [645454, 44, 58823, 45, 3888465]
# ]

