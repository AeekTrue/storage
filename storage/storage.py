import json as _json
import os as _os

class Storage:
    _opened = False
    def load_data(self):
        print('load data') 

    def save_data(self):
        print('save data')
    
    def __enter__(self):
        print('enter') 
        self.load_data()
        self._opened = True
    
    def __exit__(self, type, value, traceback):
        self.save_data()
        print('exit')
        self._opened = False

class FileStorage(Storage):
    def __init__(self, filepath):
        super(FileStorage, self).__init__()
        self._filepath = filepath
        if not _os.path.exists(self._filepath):
            self._init_file_storage(self._filepath)

    
    def _init_file_storage(self, filepath):
        with open(filepath, 'w') as f:
            f.write('')

class JSONStorage(FileStorage):
    def __init__(self, filepath):
        super(JSONStorage, self).__init__(filepath)
        self._data = []
    
    def _init_file_storage(self, filepath):
        super(JSONStorage, self)._init_file_storage(filepath)
        with open(filepath, 'w') as f:
            _json.dump([], f)

    def load_data(self):
        super(JSONStorage, self).load_data()
        with open(self._filepath, 'r') as file:
            self._data = _json.load(file)

    def append(self, element: dict):
        assert self._opened, 'Called without context'
        self._data.append(element)
    
    def get_all(self):
        assert self._opened, 'Called without context'
        return self._data

    def save_data(self): 
        super(JSONStorage, self).save_data()
        with open(self._filepath, 'w') as file:
            _json.dump(self._data, file)

