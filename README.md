# Sistema de Gestión KDL Systems

Sistema web desarrollado en Flask para la gestión de empleados, productos y distribuidoras de la empresa KDL Systems.

## Características

- **Gestión de Empleados**: Registro, edición, eliminación y consulta de empleados
- **Gestión de Productos**: CRUD completo de productos con información de distribuidoras
- **Gestión de Distribuidoras**: Administración de proveedores
- **Sistema de Autenticación**: Login con roles de administrador y empleado
- **Generación de PDFs**: Nóminas y reportes de aportes patronales
- **Envío de Emails**: Notificaciones automáticas al registrar empleados
- **Interfaz Web Responsiva**: Diseño moderno con Bootstrap

## Requisitos del Sistema

- Python 3.8 o superior
- SQL Server con ODBC Driver 17
- Base de datos "KdlSystems"

## Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd proyecto2
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar base de datos**
   - Asegúrate de tener SQL Server ejecutándose
   - Modifica la cadena de conexión en `data_access.py` si es necesario
   - Ejecuta los scripts SQL para crear las tablas y procedimientos almacenados

6. **Configurar email**
   - Modifica `config.py` con tus credenciales de Gmail
   - Habilita la autenticación de 2 factores y genera una contraseña de aplicación

## Uso

1. **Ejecutar la aplicación**
   ```bash
   python run.py
   ```

2. **Acceder al sistema**
   - Abrir navegador en `http://localhost:5000`
   - Usar credenciales de administrador o empleado

## Estructura del Proyecto

```
proyecto2/
├── app/
│   ├── __init__.py          # Configuración de Flask
│   ├── routes.py            # Rutas de la aplicación
│   ├── static/              # Archivos estáticos (CSS, JS, imágenes)
│   └── templates/           # Plantillas HTML
├── business.py              # Lógica de negocio
├── data_access.py           # Acceso a datos
├── entities.py              # Entidades del sistema
├── config.py                # Configuración
├── run.py                   # Punto de entrada
└── requirements.txt         # Dependencias
```

## Funcionalidades Principales

### Empleados
- Registro con validación de datos
- Gestión de información personal y laboral
- Cálculo automático de nóminas
- Generación de PDFs de aportes patronales

### Productos
- Catálogo completo de productos
- Búsqueda por código o nombre
- Asociación con distribuidoras
- Control de inventario

### Distribuidoras
- Gestión de proveedores
- Información de contacto
- Relación con productos

### Sistema de Usuarios
- Roles diferenciados (Administrador/Empleado)
- Autenticación segura
- Control de acceso por funcionalidad

## Tecnologías Utilizadas

- **Backend**: Flask, Python
- **Base de Datos**: SQL Server
- **Frontend**: HTML, CSS, Bootstrap
- **Generación de PDFs**: ReportLab
- **Envío de Emails**: SMTP con SSL

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

- Desarrollado para: KDL Systems
- Curso: Base de Datos 2 - ULATINA
- Período: C3-2024
