from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    
    # Inicializar configuración
    Config.init_app(app)
    
    # Registrar blueprints y rutas
    with app.app_context():
        from . import routes
    
    # Crear directorio de uploads si no existe
    import os
    if not os.path.exists(Config.UPLOAD_FOLDER):
        os.makedirs(Config.UPLOAD_FOLDER)

    return app