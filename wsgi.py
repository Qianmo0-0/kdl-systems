#!/usr/bin/env python3
"""
Archivo WSGI para despliegue en producción
"""

import os
import sys

# Agregar el directorio del proyecto al path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Configurar variables de entorno para producción
os.environ.setdefault('FLASK_ENV', 'production')
os.environ.setdefault('FLASK_DEBUG', 'False')

from app import create_app

# Crear la aplicación Flask
application = create_app()

if __name__ == "__main__":
    # Para desarrollo local
    application.run(host='0.0.0.0', port=5000)
