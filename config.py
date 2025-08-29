import os

class Config:
    # Configuración de la aplicación
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kdl_systems_secret_key_2024'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Configuración de la base de datos
    DB_SERVER = os.environ.get('DB_SERVER') or '浅陌\\SQLEXPRESS'
    DB_NAME = os.environ.get('DB_NAME') or 'KdlSystems'
    DB_USER = os.environ.get('DB_USER') or 'sa'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or '123456'
    DB_DRIVER = os.environ.get('DB_DRIVER') or 'ODBC Driver 17 for SQL Server'
    
    # Configuración de email
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 465)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'True').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'jdklinnovations@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'ccyaaliongjelzec'
    
    # Configuración de la aplicación
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    @classmethod
    def get_database_connection_string(cls):
        """Genera la cadena de conexión a la base de datos"""
        return f'DRIVER={{{cls.DB_DRIVER}}};SERVER={cls.DB_SERVER};DATABASE={cls.DB_NAME};UID={cls.DB_USER};PWD={cls.DB_PASSWORD}'
    
    @classmethod
    def init_app(cls, app):
        """Inicializa la configuración en la aplicación Flask"""
        app.config['SECRET_KEY'] = cls.SECRET_KEY
        app.config['DEBUG'] = cls.DEBUG
        app.config['UPLOAD_FOLDER'] = cls.UPLOAD_FOLDER
        app.config['MAX_CONTENT_LENGTH'] = cls.MAX_CONTENT_LENGTH