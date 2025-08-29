#!/bin/bash

echo "========================================"
echo "    INSTALADOR KDL SYSTEMS - LINUX/MAC"
echo "========================================"
echo

# Verificar Python
echo "Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 no está instalado"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi

echo "Python encontrado: $(python3 --version)"
echo

# Verificar pip
echo "Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 no está disponible"
    echo "Por favor instala pip3"
    exit 1
fi

echo "pip encontrado: $(pip3 --version)"
echo

# Crear entorno virtual
echo "Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "El entorno virtual ya existe, eliminando..."
    rm -rf venv
fi

python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudo crear el entorno virtual"
    exit 1
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi

echo
echo "========================================"
echo "    INSTALACION COMPLETADA EXITOSAMENTE"
echo "========================================"
echo
echo "Para ejecutar la aplicación:"
echo "1. Activa el entorno virtual: source venv/bin/activate"
echo "2. Ejecuta: python run.py"
echo
echo "Para ejecutar las pruebas:"
echo "python test_basic.py"
echo

# Hacer ejecutable el script
chmod +x run.py
chmod +x test_basic.py
chmod +x wsgi.py
