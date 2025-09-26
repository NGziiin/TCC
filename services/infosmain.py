import os
import sys

class Config:
    def __init__(self):
        self.imports()

    def imports(self):
        database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        sys.path.insert(0, database_path)
        from database.StorageRegisterDB import StorageRegisterClassDB
        VarDB = StorageRegisterClassDB.LoadStorageDB(listbox=None)
        return VarDB


class Functions(Config):
    def __init__(self):
        super().__init__()
        self.LoadInfosRegistred()

    def LoadInfosRegistred(self):
        VarDB = self.imports()
        CounterRegister = 0
        if VarDB is None:
            CounterRegister = 0
            return CounterRegister
        else:
            for _ in VarDB:
                CounterRegister += 1
            return CounterRegister


if __name__ == '__main__':
    Functions()