import os
import sys

class Config:
    def __init__(self):
        pass

    def importsDB(self):
        database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        sys.path.insert(0, database_path)
        from database.SoftwareDB import StorageRegisterClassDB
        VarDB = StorageRegisterClassDB.LoadStorageDB(listbox=None)
        return VarDB

    def importsAT(self):
        database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        sys.path.insert(0, database_path)
        from database.SoftwareDB import DBLog
        VarAT = DBLog.LowCountMain()
        return VarAT


class Functions(Config):
    def __init__(self):
        super().__init__()

    def LoadInfosRegistred(self):
        VarDB = self.importsDB()
        if VarDB is None:
            return 0
        else:
            return len(VarDB)

    def LoadAlertRegistred(self):
        VarAT = self.importsAT()
        if VarAT is None:
            return 0
        else:
            return VarAT