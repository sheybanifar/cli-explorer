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
    operation_message = None

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
    def get_size(path: Path):
        '''Get size of file & folder in kb, mb or gb'''
        KB = 1000
        MB = KB ** 2
        GB = KB ** 3
        if path.is_file():
            size_in_bytes = path.stat().st_size
        elif path.is_dir():
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
    def store_pathnames(cls, rows):
        '''populates cls.dir_content'''
        for row in rows:
            cls.dir_content[row[0]] = row[-1] # latest index is pathname

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
    def build_row(cls, iterpath):
        id_ = 1
        rows = [('Id', 'Mode', 'Date Modified', 'Size', 'Name'),
                    ('--', '-'*4, '-'*13, '-'*4, '-'*4)]
        for path in iterpath:
            mode = cls.get_mode(path)
            last_modified_time = cls.get_last_modified_time(path)
            size = cls.get_size(path)
            name = cls.get_pathname(path)
            rows.append((
                str(id_),
                mode,
                last_modified_time,
                size,
                name
            ))
            id_ += 1
        return rows

    @classmethod
    def print_path(cls, rows):
        cls.dir_content.clear() # Clear it before new items addition
        if len(row) < 10:
            id_column_length = 2
        else:
            id_column_length = len(str(len(row)))
        max_len_name = max(len(col[-1]) for col for row in rows) + 1
        cls.store_pathnames(rows[2:])
        for row in rows:
            cls.dir_items_count = len(row) - 2  # number of dir content
            print()
            print(f'Directory: {cls.cwd}'.rjust(45))
            print()
            # for col in row:
                # print(col)
            print(row[0].ljust(id_column_length), row[1].center(9), row[2].rjust(18), row[3].rjust(8), row[4].ljust(max_len_name))
            print()
            print(f'Directory: {cls.cwd}'.rjust(45))
            print()

    @classmethod
    def navigator(cls):
        '''This method is responsible for updating Explorer's cwd attribute
        dynamically after every navigation and calling Explorer's print_path
        to display content of that directory.'''
        while True:
            try:
                iterpath = cls.cwd.iterdir()    # Generator of the path
                cls.print_path(cls.build_row(iterpath))
            except FileNotFoundError:
                print('such file or directory does not exist!')
                # cls.navigator()
            except PermissionError:
                print('Access is denied!')
                cls.cwd = cls.cwd.resolve().parent

            try:
                if cls.operation_message:
                    print(cls.operation_message)
                    cls.operation_message = None
                entry = input('Prompt -> ')
            except KeyboardInterrupt:
                print('\nExiting the program...')
                exit()

            if entry == '' or entry == '.':
                # Refresh the "cwd"
                continue
            elif entry == '..':
                # Backward navigation
                directory = cls.cwd.resolve().parent
                if directory.is_dir():
                    cls.cwd = directory.resolve()
                    continue
            elif entry in ('/n', '/N', '/new', '/NEW'):
                chance = 3
                while chance > 0:
                    try:
                        new_name = input('Enter new name: ')
                        Operator.validate_name(new_name)
                        Operator.make_dir(Explorer.cwd, new_name)
                    except OperationError as op:
                        cls.operation_message = op.args[0]
                        print(op)
                        chance -= 1
                        continue
                    except FileExistsError as exists_err:
                        cls.operation_message = 'Name already exists!'
                        print(cls.operation_message)
                        chance -= 1
                        continue
                    except KeyboardInterrupt:
                        break
                    except Exception as e:
                        cls.operation_message = 'Unexpected error occurred!'
                        print(type(e), e)
                        chance -= 1
                        continue
                    else:
                        os.system('cls')
                        cls.operation_message = '===== Folder was created! ====='
                        continue
                continue
            elif entry.isnumeric():
                if int(entry) <= 0:
                    print('Invalid input!')
                    continue
                elif entry.lstrip('0') in cls.dir_content.keys():
                    entry = entry.lstrip('0')
                    directory = cls.cwd / cls.dir_content[entry]
                    if directory.is_dir():
                        cls.cwd = directory.resolve()
                        continue
            else:
                if entry in cls.dir_content.values():
                    cls.cwd = cls.cwd / entry
                    continue
                else:
                    # if an absolute path with drive letter had been passed; navigate it
                    directory = Path(entry)
                    if directory.exists() and directory.is_absolute():
                        cls.cwd = directory
                        continue
    @classmethod
    def run(cls):
        cls.navigator()

class OperationError(Exception):
    pass

class Operator:
    message = None

    @staticmethod
    def validate_name(name: str):
        if not name:
            raise OperationError('Name can\'t be empty!')
        if name != name.strip():
            raise OperationError('Invalid name!')
        if 224 < len(name):
            raise OperationError('it\'s too long! max 224 character.')

        forbidden = ('|', '<', '>', '\"', '?', '*', ':', '/', '\\')
        for char in forbidden:
            if char in name:
                raise OperationError('Name can\'t contains | < > " \\ ? / : *')
        return True
    
    @classmethod
    def make_dir(cls, base_path: Path, name: str):
        cls.validate_name(name)
        new_folder = base_path / name
        new_folder.mkdir()
        return new_folder
        # while True:
        #     try:
        #         pathname = input('New folder name: ')
        #         if cls.validate_name(pathname):
        #             new_folder = Explorer.cwd / pathname
        #             new_folder.mkdir()
        #             Operator.message = '=====Folder was created!====='
        #             break
        #     except KeyboardInterrupt:
        #         break
        #     except FileNotFoundError:
        #         print('Operation failed!')
        #         continue
        #     except FileExistsError:
        #         print('This name already exists!')
        #         continue
    # @classmethod
    # def rename(cls):
    #     while True:
    #         try:
    #             identifier = input('Enter path\'s Id to rename: ')
    #             if identifier in Explorer.dir_content.keys():
    #                 # pathname = Explorer.dir_content[identifier]
    #                 # path_obj = Explorer.cwd / pathname
    #                 # new_path = path_obj.rename(path_obj)


explorer = Explorer()
explorer.run()