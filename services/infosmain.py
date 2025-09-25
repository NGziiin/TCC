import os
import sys

class Config:
    def __init__(self):
        self.imports()

    def imports(self):
        database_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        sys.path.insert(0, database_path)
        print("Path adicionado:", database_path)

        from database.StorageRegisterDB import StorageRegisterClassDB
        VarDB = StorageRegisterClassDB.LoadStorageDB(listbox=None)
        print("Banco carregado:", VarDB)


class Functions(Config):
    def __init__(self):
        super().__init__()
        self.LoadInfosRegistred()

    def LoadInfosRegistred(self):
        print('Oi novamente')


if __name__ == '__main__':
    Functions()