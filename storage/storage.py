import json as _json
import os as _os
from loguru import logger

        
class Storage:
    _opened = False
    _modified = False
    _data = None

    def _load_data(self):
        ''' update _data from disk'''
        logger.debug('load data') 

    def _save_data(self):
        ''' push _data to disk '''
        #logger.debug('save data')
    
    def __enter__(self):
        logger.debug('__enter__') 
        self._load_data()
        self._opened = True

    def __exit__(self, type, value, traceback):
        self._save_data()
        logger.debug(f'__exit__')
        self._opened = False
        self._modified = False

    def modifier(func):
        def wrapper(self, *args, **kwargs):
            self._modified = True
            logger.debug('data modified')
            return func(self, *args, **kwargs)
        return wrapper

class FileStorage(Storage):
    def __init__(self, filepath):
        super(FileStorage, self).__init__()
        self._filepath = _os.path.abspath(filepath)
        if not _os.path.exists(self._filepath):
            self._init_file_storage(self._filepath)
        logger.debug(f'Storage {self._filepath} initialized.')
    
    def _init_file_storage(self, filepath):
        with open(filepath, 'w') as f:
            f.write('')

    def get_path(self):
        return self._filepath

class JSONStorage(FileStorage):
    def __init__(self, filepath, factory=None):
        super(JSONStorage, self).__init__(filepath)
        self._load_data()
        self._data = self.get_all(factory)
    
    def _init_file_storage(self, filepath):
        super(JSONStorage, self)._init_file_storage(filepath)
        with open(filepath, 'w') as f:
            _json.dump([], f)

    def _load_data(self):
        #super(JSONStorage, self)._load_data()
        logger.debug(f'read {self._filepath}')
        with open(self._filepath, 'r') as file:
            self._data = _json.load(file)

    @Storage.modifier
    def append(self, element: dict):
        assert self._opened, 'Called without context'
        self._data.append(element)
    
    def get_all(self, factory=None):
        if factory is None:
            return self._data
        else:
            return [factory(**record) for record in self._data]

    def _save_data(self): 
        super(JSONStorage, self)._save_data()
        if self._modified:
            logger.debug(f'write {self._filepath}')
            with open(self._filepath, 'w') as file:
                _json.dump(self._data, file)
        else:
            logger.debug(f'_data not modified')

