import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    DATABASE_CONNECTION = (
       'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=SERVER_NAME;'
        'DATABASE=YOUR_DATABASE;'
        'UID=USER_NAME;'
        'PWD=YOUR_PASSWORD;'
    )
