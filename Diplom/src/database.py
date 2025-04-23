# src/database.py
import pymysql as mdb

class DB_Settings:
    """Класс для подключения к бд"""
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'database': 'SmartDB'
    }

    @staticmethod
    def get_connection():
        try:
            return mdb.connect(**DB_Settings.DB_CONFIG)
        except mdb.err as e:
            raise ConnectionError(f"Ошибка подключения {e}")
