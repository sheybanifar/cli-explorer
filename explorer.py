from pathlib import Path
import shutil
import sys

class Explorer:
    try:
        cwd = sys.argv[1]
    except IndexError:
        cwd = ''    # current working directory

    def _id_assign(self):
        pass

    @classmethod
    def navigator(cls):
        pass

    @classmethod
    def run(cls):
        p = Path(cls.cwd).resolve()  
        print(p)

explorer = Explorer()
explorer.run()