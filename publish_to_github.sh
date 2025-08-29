#!/bin/bash

echo "========================================"
echo "    PUBLICANDO PROYECTO EN GITHUB"
echo "========================================"
echo

# Verificar Git
if ! command -v git &> /dev/null; then
    echo "ERROR: Git no está instalado"
    echo "Por favor instala Git desde https://git-scm.com"
    exit 1
fi

echo "Git encontrado:"
git --version
echo

# Verificar estado del repositorio
if [ ! -d ".git" ]; then
    echo "Inicializando repositorio Git..."
    git init
    echo
fi

echo "Agregando archivos al staging..."
git add .

echo "Verificando cambios..."
git status

echo
echo "========================================"
echo "    CONFIGURACION DEL REPOSITORIO"
echo "========================================"
echo

read -p "Ingresa tu nombre de usuario de GitHub: " GITHUB_USERNAME
read -p "Ingresa el nombre del repositorio (o presiona Enter para usar 'kdl-systems'): " REPO_NAME

if [ -z "$REPO_NAME" ]; then
    REPO_NAME="kdl-systems"
fi

echo
echo "Configurando repositorio remoto..."
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

echo
echo "========================================"
echo "    CREANDO PRIMER COMMIT"
echo "========================================"
echo

echo "Creando commit inicial..."
git commit -m "feat: lanzamiento inicial del sistema KDL Systems

- Sistema completo de gestión empresarial
- Autenticación y autorización por roles
- Generación de PDFs para nóminas
- Sistema de emails automático
- Interfaz web responsiva
- Configuración Docker y CI/CD
- Documentación completa del proyecto"

echo
echo "========================================"
echo "    ENVIANDO A GITHUB"
echo "========================================"
echo

echo "Enviando a GitHub..."
git branch -M main
git push -u origin main

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: No se pudo enviar a GitHub"
    echo
    echo "Posibles causas:"
    echo "1. El repositorio no existe en GitHub"
    echo "2. No tienes permisos para escribir"
    echo "3. Problemas de autenticación"
    echo
    echo "Pasos para resolver:"
    echo "1. Ve a https://github.com/new"
    echo "2. Crea un repositorio llamado: $REPO_NAME"
    echo "3. NO inicialices con README, .gitignore o licencia"
    echo "4. Ejecuta este script nuevamente"
    echo
    exit 1
fi

echo
echo "========================================"
echo "    ¡PUBLICACION EXITOSA!"
echo "========================================"
echo
echo "Tu proyecto ha sido publicado en:"
echo "https://github.com/$GITHUB_USERNAME/$REPO_NAME"
echo
echo "Próximos pasos recomendados:"
echo "1. Ve a tu repositorio en GitHub"
echo "2. Configura la descripción del proyecto"
echo "3. Agrega temas (topics) relevantes"
echo "4. Configura GitHub Pages si deseas"
echo "5. Invita colaboradores si es necesario"
echo
echo "¡Felicidades! Tu proyecto está ahora en GitHub."
echo
