import sqlite3 as sqlite3

class StorageRegisterDB:
    def __init__(self, db_name="storage_register.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS storage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                location TEXT NOT NULL
            )
        ''')
        self.connection.commit()

    def insert_item(self, item_name, quantity, location):
        self.cursor.execute('''
            INSERT INTO storage (item_name, quantity, location)
            VALUES (?, ?, ?)
        ''', (item_name, quantity, location))
        self.connection.commit()

    def close(self):
        self.connection.close()