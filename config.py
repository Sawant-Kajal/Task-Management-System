import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    DATABASE_CONNECTION = (
       'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-INFGORM1;'
        'DATABASE=TaskDB;'
        'UID=sa;'
        'PWD=Kajal@123;'
    )
