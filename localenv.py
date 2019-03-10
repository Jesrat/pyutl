import os
import sys


class NoEnvironmentFile(Exception):
    pass


class LocalEnv:
    def __init__(self):
        self.file = None
        self.data = {}

    def load(self, file=None):
        """
        If no file is defined, the .env file will be searched
        in invoker module's directory
        """
        if file is not None:
            self.file = file
        else:
            self.file = self._invoker()

        if not os.path.isfile(self.file):
            raise NoEnvironmentFile(f'for file {self.file}')

        with open(self.file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                key = key.replace('export', '')
                key = key.strip()
                value = value.strip().strip('\'"')
                self.data[key] = value

    def get(self, key, cast=None):
        if cast is None:
            return self.data[key]

        return cast(self.data[key])

    @staticmethod
    def _invoker():
        # tip from:
        # https://github.com/henriquebastos/python-decouple/blob/master/decouple.py
        # MAGIC! Get the caller's module path.
        frame = sys._getframe()
        path = os.path.dirname(frame.f_back.f_back.f_code.co_filename)
        file = os.path.join(path, '.env')
        return file


localenv = LocalEnv()
