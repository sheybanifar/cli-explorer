from pathlib import Path
import shutil
import sys

class Explorer:
    try:
        cwd = sys.argv[1]
    except IndexError:
        cwd = ''    # current working directory

    # def _id_associate(self):
    #     pass

    @classmethod
    def navigator(cls):
        path = Path(cls.cwd).resolve()
        # print(*path.iterdir(), sep='\n')
        iterpath = path.iterdir()

    @classmethod
    def run(cls):
        cls.navigator()

explorer = Explorer()
explorer.run()