import os
import sys

class Config:
    def __init__(self):
        pass

    def imports(self):
        database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        sys.path.insert(0, database_path)
        from database.StorageRegisterDB import StorageRegisterClassDB
        VarDB = StorageRegisterClassDB.LoadStorageDB(listbox=None)
        return VarDB


class Functions(Config):
    def __init__(self):
        super().__init__()

    def LoadInfosRegistred(self):
        VarDB = self.imports()
        if VarDB is None:
            return 0
        else:
            return len(VarDB)