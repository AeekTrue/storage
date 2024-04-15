import json as _json
import os as _os
from loguru import logger
from collections import UserList

class NotOpenedStorageError(Exception):
    pass

class AlreadyOpenedStorageError(Exception):
    pass

class FileStorage:
    '''
    store = Storage('/path/to/storage.txt')
    '''

    data = None 

    def __init__(self, filepath):
        self._filepath = _os.path.abspath(filepath)
        if not _os.path.exists(self._filepath):
            self._init_storage_file(self._filepath)
            logger.debug(f'Storage {self._filepath} initialized.')
        self.load()

    def _init_storage_file(self, filepath):
        '''initialize empty storage file'''
        raise NotImplementedError

    def load(self):
        ''' load data from disk'''
        raise NotImplementedError

    def save(self):
        ''' save data to disk '''
        raise NotImplementedError


class JSONStorage(FileStorage, UserList):
    def __init__(self, filepath):
        super(JSONStorage, self).__init__(filepath)
    
    def _init_storage_file(self, filepath):
        with open(filepath, 'w') as f:
            _json.dump([], f)

    def load(self):
        with open(self._filepath, 'r') as file:
            self.data = _json.load(file)

    def save(self): 
        with open(self._filepath, 'w') as file:
            _json.dump(self.data, file)

    def get_all(self, factory=None):
        if factory is None:
            return self.data
        else:
            return [factory(**record) for record in self.data]


