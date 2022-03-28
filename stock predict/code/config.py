DIALECT = 'mysql'
DRIVER = 'mysqlconnector'
USERNAME = 'root'
PASSWORD = 'Ipbd@mysql123'
HOST = '39.107.231.30'
PORT = '3306'
DATABASE = 'stock_trend'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                          PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False

DEBUG = True
