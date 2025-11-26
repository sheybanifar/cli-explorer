from pathlib import Path
import shutil
import sys
import threading

class CustomThread(threading.Thread):
    '''This thread is provided to get yield_row method of
    Explorer class as its target and ensure gathering
    all data from that'''
    def __init__(self, target, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.target = target
        self.result = None

    def run(self):
        self.result = self.target(self._args[0])
        # print(self.target)

class Explorer:
    try:
        cwd = Path(sys.argv[1]).resolve()
    except IndexError:
        cwd = Path().resolve()    # current working directory

    dir_length = None
    dir_content = {}
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
                size = f'{size_in_bytes} B'
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
    def store_pathnames(cls, path_data):
        for column in path_data[2:]:
            # cls.dir_content.append(column[-1])
            cls.dir_content[column[0]] = column[-1] # latest index is pathname

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
            cls.dir_length = len(row) - 2  # number of dir content
            cls.store_pathnames(row)
            max_len_name = max(len(col[-1]) for col in row) + 1
            print()
            print(f'Directory: {cls.cwd}'.rjust(45))
            print()
            for col in row:
                print(col[0].ljust(id_length), col[1].center(9), col[2].rjust(18), col[3].rjust(8), col[4].ljust(max_len_name))
            print()
            print(f'Directory: {cls.cwd}'.rjust(45))
            print()

    @classmethod
    def navigator(cls):
        try:
            iterpath = cls.cwd.iterdir()    # Generator of the path
            thread = CustomThread(target=cls.yield_row, args=(iterpath,))
            thread.start()
            thread.join()
            cls.print_path(thread.result)

        except FileNotFoundError:
            print('such file or directory does not exist!')
            cls.navigator()
        except PermissionError:
            print('Access is denied!')
            cls.cwd = cls.cwd.resolve().parent
            # cls.navigator()

        while True:
            entry = input('Enter pathname or id: ')
            if entry == '':
                continue
            elif entry == '..':
                directory = cls.cwd.resolve().parent
                if directory.is_dir():
                    cls.cwd = directory.resolve()
                    cls.navigator()
            elif entry.isnumeric():
                if int(entry) <= 0:
                    print('Invalid input!')
                    continue
                elif int(entry) <= cls.dir_length:
                    directory = cls.cwd / cls.dir_content[entry]
                    if directory.is_dir():
                        cls.cwd = directory.resolve()
                        cls.navigator()

            # if path.isnumeric():
            #     for paths in thread.result:
            #         for item in paths:
            #             if path == item[0]:
            #                 if Path(item[-1]).is_dir():
            #                     cls.cwd = Path(item[-1]).resolve()
    @classmethod
    def run(cls):
        cls.navigator()

explorer = Explorer()
explorer.run()