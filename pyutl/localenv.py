import os
import sys
import json


class NoEnvironmentFile(Exception):
    pass


class KeyNotFound(Exception):
    pass


DEFAULT = object()


class LocalEnv:
    _BOOLEANS = {'1': True, 'yes': True, 'true': True, 'on': True,
                 '0': False, 'no': False, 'false': False, 'off': False, '': False}

    def __init__(self):
        self.files = []
        self.data = {}
        self.first_load = False

    def load(self, file=None):
        """
        If no file is defined, the .env file will be searched
        in invoker module's directory
        """
        if file:
            self.files.append({'file': file, 'exists': '', 'loaded': False})
        else:
            self.files.append({'file': self._invoker(), 'exists': '', 'loaded': False})
            self.files.append({
                'file': os.path.join(os.getcwd(), '.env'),
                'exists': '',
                'loaded': False
            })

        # search all files given and load them
        for file_dict in self.files:
            file_dict['exists'] = os.path.isfile(file_dict['file'])
            if file_dict['exists'] and not file_dict['loaded']:
                with open(file_dict['file']) as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#') or '=' not in line:
                            continue
                        key, value = line.split('=', 1)
                        key = key.replace('export', '')
                        key = key.strip()
                        value = value.strip().strip('\'"')
                        self.data[key] = value
                    file_dict['loaded'] = True

    def _cast(self, cast, data):
        if cast is bool and str(data).lower() not in self._BOOLEANS:
            raise ValueError(f'value can not be parsed as boolean')
        elif cast is bool:
            return self._BOOLEANS[str(data).lower()]
        else:
            return cast(data)

    def get(self, key, default=DEFAULT, cast=None):
        if not self.first_load:
            self.load()
            self.first_load = True

        try:
            ret_val = self.data[key]
            # support for 1password CLI <op run -->
            if ret_val.startswith('op://') and os.environ.get(key):
                ret_val = os.environ.get(key) if cast is None else self._cast(cast, os.environ.get(key))
            else:
                ret_val = ret_val if cast is None else self._cast(cast, self.data[key])
        except KeyError:
            from_os = os.environ.get(key)
            if from_os:
                ret_val = from_os if cast is None else self._cast(cast, from_os)
            elif default != DEFAULT:
                ret_val = default if cast is None else self._cast(cast, default)
            else:
                raise KeyNotFound(f'value not found in files: \n{json.dumps(self.files, indent=4)}')
        return ret_val

    @staticmethod
    def _invoker():
        # tip from:
        # https://github.com/henriquebastos/python-decouple/blob/master/decouple.py
        # MAGIC! Get the caller's module path.
        # noinspection PyProtectedMember
        frame = sys._getframe()
        path = os.path.dirname(frame.f_back.f_back.f_back.f_code.co_filename)
        file = os.path.join(path, '.env')
        return file


localenv = LocalEnv()
