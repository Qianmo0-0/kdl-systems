# Usar imagen base de Python 3.11
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    unixodbc \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requisitos
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Crear directorio de uploads
RUN mkdir -p uploads

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV FLASK_APP=wsgi.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Comando para ejecutar la aplicación
CMD ["python", "wsgi.py"]
