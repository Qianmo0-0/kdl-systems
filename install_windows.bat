@echo off
echo ========================================
echo    INSTALADOR KDL SYSTEMS - WINDOWS
echo ========================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado o no esta en el PATH
    echo Por favor instala Python 3.8 o superior desde https://python.org
    pause
    exit /b 1
)

echo Python encontrado: 
python --version
echo.

echo Verificando pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip no esta disponible
    echo Por favor reinstala Python con pip habilitado
    pause
    exit /b 1
)

echo pip encontrado:
pip --version
echo.

echo Creando entorno virtual...
if exist venv (
    echo El entorno virtual ya existe, eliminando...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ERROR: No se pudo crear el entorno virtual
    pause
    exit /b 1
)

echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo ========================================
echo    INSTALACION COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Para ejecutar la aplicacion:
echo 1. Activa el entorno virtual: venv\Scripts\activate.bat
echo 2. Ejecuta: python run.py
echo.
echo Para ejecutar las pruebas:
echo python test_basic.py
echo.
pause
