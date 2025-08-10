# 数据库配置
DB_USER = 'root'
DB_PASSWORD = '286369'
DB_HOST = 'localhost'
DB_NAME = 'test'

SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
