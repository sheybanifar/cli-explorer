from pathlib import Path
import shutil
import sys
import threading
import concurrent.futures as cc

class CustomThread(threading.Thread):
    '''This thread is provided to get
    Explorer's yield_row method as its target
    and ensure gathering all data from that'''

    def __init__(self, target, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.target = target
        self.result = None

    def run(self):
        self.result = self.target(self._args[0])

class Explorer:
    try:
        cwd = Path(sys.argv[1]).resolve()
    except IndexError:
        cwd = Path().resolve()    # current working directory

    dir_items = None   # Number of listed items
    dir_content = {}   # holding id & name as "Id: Name" pairs
    dir_size = 0

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
    def get_size(path=None, path_size=None):
        '''Get file size in kb, mb or gb'''
        KB = 1000
        MB = KB ** 2
        GB = KB ** 3
        if path and path.is_file():
            size_in_bytes = path.stat().st_size
        elif path_size:
            size_in_bytes = path_size
        
        else:
            return ''
        
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
        
    
    @staticmethod
    def get_pathname(path):
        '''returns name of a dir or file'''
        if path.is_dir():
            pathname = path.name + '/'
            return pathname
        else:
            return path.name

    @classmethod
    def get_dir_size(cls):
        dir_size = 0
        path_roots = cls.cwd.walk()
        for item in path_roots:
            for file in item[-1]:
                path_obj = item[0] / file
                dir_size += path_obj.stat().st_size
        cls.dir_size = cls.get_size(path_size=dir_size)

    @classmethod
    def store_pathnames(cls, path_data):
        '''populates cls.dir_content'''
        for column in path_data[2:]:
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
    def batch_size(cls, files: list[Path]):     # ProcessPool
        total = 0
        for file in files:
            try:
                total += file.stat().st_size
            except (PermissionError, FileNotFoundError):
                pass
        return total

    @staticmethod
    def all_files(path: Path):      # ProcessPool
        for self_path, _, filenames in path.walk():
            for file in filenames:
                yield Path(self_path) / file
    
    @staticmethod
    def chunks(all_files, size):    # ProcessPool
        chunk = []
        for i in all_files:
            chunk.append(i)
            if len(chunk) == size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

    @classmethod
    def print_path(cls, rows):
        for row in rows:
            if len(row) < 10:
                id_length = 2
            else:
                id_length = len(str(len(row)))
            cls.dir_items = len(row) - 2  # number of dir content
            cls.store_pathnames(row)
            max_len_name = max(len(col[-1]) for col in row) + 1
            print()
            print(f'Directory: {cls.cwd}'.rjust(45))
            print()
            for col in row:
                print(col[0].ljust(id_length), col[1].center(9), col[2].rjust(18), col[3].rjust(8), col[4].ljust(max_len_name))
            print()
            print(f'Directory: {cls.cwd}'.rjust(45))
            print(f'Total size: {cls.dir_size}'.rjust(45))
            print()

    @classmethod
    def navigator(cls):
        try:
            iterpath = cls.cwd.iterdir()    # Generator of the path
            thread_rows = CustomThread(target=cls.yield_row, args=(iterpath,))
            # thread_total_size = threading.Thread(target=cls.get_dir_size)
            
            thread_rows.start()
            # thread_total_size.start()

            # =================ProcessPool=================
            if __name__ == '__main__':
                with cc.ProcessPoolExecutor() as exc:
                    BATCH_SIZE = 1000
                    all_files = cls.all_files(cls.cwd)
                    batches = cls.chunks(all_files, BATCH_SIZE)
                    
                    futures = [exc.submit(cls.batch_size, batch) for batch in batches]

                    total = 0
                    for future in cc.as_completed(futures):
                        total += future.result()
                    cls.dir_size = cls.get_size(path_size=total)

            thread_rows.join()
            # thread_total_size.join()

            cls.print_path(thread_rows.result)

        except FileNotFoundError:
            print('such file or directory does not exist!')
            cls.navigator()
        except PermissionError:
            print('Access is denied!')
            cls.cwd = cls.cwd.resolve().parent

        while True:
            try:
                entry = input('Enter pathname or id: ')
            except KeyboardInterrupt:
                print('\nExiting the program...')
                exit()
            if entry == '':
                continue
            elif entry == '.':
                cls.navigator() # Refresh the "cwd"
            elif entry == '..': # Backward navigation
                directory = cls.cwd.resolve().parent
                if directory.is_dir():
                    cls.cwd = directory.resolve()
                    cls.navigator()
            elif entry.isnumeric():
                if int(entry) <= 0:
                    print('Invalid input!')
                    continue
                elif entry.lstrip('0') in cls.dir_content.keys():
                    directory = cls.cwd / cls.dir_content[entry]
                    if directory.is_dir():
                        cls.cwd = directory.resolve()
                        cls.navigator()
            else:
                if entry in cls.dir_content.values():
                    cls.cwd = cls.cwd / entry
                    cls.navigator()
                else:
                    # if an absolute dir (with drive letter are given); navigate it
                    directory = Path(entry)
                    if directory.drive:
                        cls.cwd = directory
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