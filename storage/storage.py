import json as _json
import os as _os
from loguru import logger
from collections import UserList

class NotOpenedStorageError(Exception):
    pass

class AlreadyOpenedStorageError(Exception):
    pass

class Storage:
    '''
    store = Storage('/path/to/storage.txt')
    store.open() # load data to RAM
    data = store.get_data()
    # modificate storage
    store.commit() # write data to RAM
    store.close()
    '''
    _opened = False
    _modified = False
    data = None
    _auto_commit = False
    
    def open(self):
        if self._opened:
            raise AlreadyOpenedStorageError()
        else:
            self._opened = True
            self._load_data()

    def get_data(self):
        if self._opened:
            return self.data
        else:
            raise NotOpenedStorageError()

    def _load_data(self):
        ''' load data from disk'''
        pass

    def _save_data(self):
        ''' save data to disk '''
        pass
    
    def commit(self):
        ''' save changes to disk '''
        if self._modified:
            self._save_data()
            logger.debug('Changes saved.')
        else:
            logger.debug('No changes to commit.')
        self._modified = False

    def close(self):
        if self._opened:
            self._opened = False
            self._modified=False
            self.data = None
        else:
            raise NotOpenedStorageError()

    def modifier(func):
        def wrapper(self, *args, **kwargs):
            if not self._opened:
                raise NotOpenedStorageError()
            r = func(self, *args, **kwargs)
            self._modified = True
            logger.debug('Data modified')
            if self._auto_commit:
                self.commit()
            return r
        return wrapper


class FileStorage(Storage):
    def __init__(self, filepath):
        super(FileStorage, self).__init__()
        self._filepath = _os.path.abspath(filepath)
        if not _os.path.exists(self._filepath):
            self._init_file_storage(self._filepath)
        logger.debug(f'Storage {self._filepath} initialized.')
    
    def _init_file_storage(self, filepath):
        pass

    def get_path(self):
        return self._filepath


class JSONStorage(FileStorage, UserList):
    def __init__(self, filepath):
        super(JSONStorage, self).__init__(filepath)
    
    def _init_file_storage(self, filepath):
        with open(filepath, 'w') as f:
            _json.dump([], f)

    def _load_data(self):
        with open(self._filepath, 'r') as file:
            self.data = _json.load(file)

    @Storage.modifier
    def append(self, element: dict):
        self.data.append(element)
    
    def get_all(self, factory=None):
        if factory is None:
            return self.data
        else:
            return [factory(**record) for record in self.data]

    def _save_data(self): 
        with open(self._filepath, 'w') as file:
            _json.dump(self.data, file)

