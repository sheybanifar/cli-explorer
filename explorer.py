from pathlib import Path
import shutil
import os
import sys
import threading

class Explorer:
    try:
        cwd = Path(sys.argv[1]).resolve()
    except IndexError:
        cwd = Path().resolve()    # current working directory

    dir_items_count = None   # Number of listed items
    dir_content = {}   # holding id & name as "Id: Name" pairs

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
    def get_size(file: Path = None, folder: Path = None):
        '''Get size of file & folder in kb, mb or gb'''
        KB = 1000
        MB = KB ** 2
        GB = KB ** 3
        if file and file.is_file():
            size_in_bytes = file.stat().st_size
        elif folder and folder.is_dir():
            size_in_bytes = folder.stat().st_size
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
    def store_pathnames(cls, path_data):
        '''populates cls.dir_content'''
        for column in path_data[2:]:
            cls.dir_content[column[0]] = column[-1] # latest index is pathname

    @staticmethod
    def all_files(path: Path):
        '''
        walks the path and yields the all files
        in directory and sub-directories
        '''
        for self_path, _, filenames in path.walk():
            for file in filenames:
                yield Path(self_path) / file

    @classmethod
    def yield_row(cls, iterpath):
        id_ = 1
        path_data = [('Id', 'Mode', 'Date Modified', 'Size', 'Name'),
                    ('--', '-'*4, '-'*13, '-'*4, '-'*4)]
        for path in iterpath:
            mode = cls.get_mode(path)
            last_modified_time = cls.get_last_modified_time(path)
            size = cls.get_size(path)
            name = cls.get_pathname(path)
            path_data.append((
                str(id_),
                mode,
                last_modified_time,
                size,
                name
            ))
            id_ += 1
        yield path_data

    @classmethod
    def print_path(cls, path_data):
        for tuple in path_data:
            if len(tuple) < 10:
                id_column_length = 2
            else:
                id_column_length = len(str(len(tuple)))
            cls.dir_items_count = len(tuple) - 2  # number of dir content
            cls.store_pathnames(tuple)
            max_len_name = max(len(col[-1]) for col in tuple) + 1
            print()
            print(f'Directory: {cls.cwd}'.rjust(45))
            print()
            for col in tuple:
                print(col[0].ljust(id_column_length), col[1].center(9), col[2].rjust(18), col[3].rjust(8), col[4].ljust(max_len_name))
            print()
            print(f'Directory: {cls.cwd}'.rjust(45))
            print()

    @classmethod
    def navigator(cls):
        try:
            iterpath = cls.cwd.iterdir()    # Generator of the path
            cls.print_path(cls.yield_row(iterpath))
        except FileNotFoundError:
            print('such file or directory does not exist!')
            # cls.navigator()
        except PermissionError:
            print('Access is denied!')
            cls.cwd = cls.cwd.resolve().parent

        while True:
            try:
                message = Operator.message
                if message:
                    print(message)
                    Operator.message = None
                # print(message)
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
            elif entry in ('/n', '/N', '/new', '/NEW'):
                Operator.make_dir()
                os.system('cls')
                cls.navigator()
            elif entry.isnumeric():
                if int(entry) <= 0:
                    print('Invalid input!')
                    continue
                elif entry.lstrip('0') in cls.dir_content.keys():
                    entry = entry.lstrip('0')
                    directory = cls.cwd / cls.dir_content[entry]
                    if directory.is_dir():
                        cls.cwd = directory.resolve()
                        cls.navigator()
            else:
                if entry in cls.dir_content.values():
                    cls.cwd = cls.cwd / entry
                    cls.navigator()
                else:
                    # if an absolute dir with drive letter had been given; navigate it
                    directory = Path(entry)
                    if directory.exists() and directory.is_absolute():
                        cls.cwd = directory
                        cls.navigator()
    @classmethod
    def run(cls):
        cls.navigator()

class Operator:
    message = None

    @classmethod
    def validate_name(cls, name: str):
        if name == '':
            print('can\'t be empty!')
            return False
        stripped_name = name.strip()
        if name != stripped_name:
            print('Impossible name!')
            return False
        elif 224 < len(stripped_name):
            print('it\'s too long! max 224 character.')
            return False
        for char in ('|', '<', '>', '\"', '?', '*', ':', '/', '\\'):
            if char in stripped_name:
                print('name can\'t contains (| < > " \\ ? / : *)')
                return False
        else:
            return True
    @classmethod
    def make_dir(cls):
        while True:
            try:
                pathname = input('New folder name: ')
                if cls.validate_name(pathname):
                    new_folder = Explorer.cwd / pathname
                    new_folder.mkdir()
                    Operator.message = '=====Folder was created!====='
                    break
            except KeyboardInterrupt:
                break
            except FileNotFoundError:
                print('Operation failed!')
                continue
            except FileExistsError:
                print('This name already exists!')
                continue
    @classmethod
    def rename(cls):
        while True:
            try:
                identifier = input('Enter path\'s Id to rename: ')
                if identifier in Explorer.dir_content.keys():
                    # pathname = Explorer.dir_content[identifier]
                    # path_obj = Explorer.cwd / pathname
                    # new_path = path_obj.rename(path_obj)


explorer = Explorer()
explorer.run()