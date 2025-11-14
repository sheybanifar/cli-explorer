from pathlib import Path
import shutil
import sys
import threading

class CustomThread(threading.Thread):
    def __init__(self, target, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.target = target
        self.result = None

    def run(self):
        self.result = self.target(self._args[0])
        # print(self.target)
        # print(self.result)


class Explorer:
    try:
        cwd = sys.argv[1]
    except IndexError:
        cwd = ''    # current working directory

    # def get_length():   
    #     '''Get length of the directory iterator'''
    #     length = 0
    #     for i in path_iter:
    #         length += 1
    #     return length
    @staticmethod
    def get_mode(path):
        '''look for path mode whether is a directory or a file'''
        if path.is_dir():
            return 'D'
        else:
            return 'F'
    
    @staticmethod
    def get_last_modified_time(path):
        '''getting last modified time'''
        import time
        lastModifiedTimeInSec = time.gmtime(path.stat().st_mtime)
        lastModifiedTime = time.strftime(r'%m/%d/%Y %H:%M', lastModifiedTimeInSec)
        return lastModifiedTime
    
    @staticmethod
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
    
    @staticmethod
    def get_pathname(path):
        if path.is_dir():
            pathname = path.name + '/'
            return pathname
        else:
            return path.name

    @classmethod
    def yield_row(cls, iterpath):
        _id = 1
        path_data = [('Id', 'Mode', 'Date Modified', 'Size', 'Name'),
                    ('--', '-'*4, '-'*13, '-'*4, '-'*4)]
        for path in iterpath:
            mode = cls.get_mode(path)
            last_modified_time = cls.get_last_modified_time(path)
            size = cls.get_size(path)
            name = cls.get_pathname(path)
            path_data.append((
                str(_id),
                mode,
                last_modified_time,
                size,
                name
            ))
            _id += 1
        yield path_data

    @classmethod
    def print_path(cls, rows):
        for row in rows:
            if len(row) < 10:
                id_length = 2
            else:
                id_length = len(str(len(row)))
            max_len_name = max(len(col[-1]) for col in row) + 1
            for col in row:
                print(col[0].ljust(id_length), col[1].center(9), col[2].rjust(18), col[3].rjust(8), col[4].ljust(max_len_name))

    @classmethod
    def navigator(cls):
        try:
            path = Path(cls.cwd).resolve()
            iterpath = path.iterdir()
            # rows = cls.yield_row(iterpath)
            # cls.print_path(rows)
            # t1 = threading.Thread(target=cls.yield_row, args=(iterpath,))
            # t1.start()
            # t1.join()
            t1 = CustomThread(target=cls.yield_row, args=(iterpath,))
            t1.start()
            t1.join()
            cls.print_path(t1.result)

        except FileNotFoundError:
            print('such file or directory does not exist!')
        # print(*path.iterdir(), sep='\n')

    @classmethod
    def run(cls):
        cls.navigator()

explorer = Explorer()
explorer.run()