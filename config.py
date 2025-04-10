import os

class Config:
    SECRET_KEY = 'clave_super_secreta'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/ecommerce_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
