# Guía de Contribución

¡Gracias por tu interés en contribuir al proyecto KDL Systems! Este documento te guiará a través del proceso de contribución.

## Tabla de Contenidos

- [Cómo Contribuir](#cómo-contribuir)
- [Configuración del Entorno de Desarrollo](#configuración-del-entorno-de-desarrollo)
- [Proceso de Contribución](#proceso-de-contribución)
- [Estándares de Código](#estándares-de-código)
- [Reportando Bugs](#reportando-bugs)
- [Solicitando Funcionalidades](#solicitando-funcionalidades)
- [Preguntas Frecuentes](#preguntas-frecuentes)

## Cómo Contribuir

Hay muchas formas de contribuir al proyecto:

- 🐛 **Reportar bugs** - Ayúdanos a encontrar y corregir problemas
- 💡 **Solicitar funcionalidades** - Sugiere nuevas características
- 📝 **Mejorar documentación** - Ayuda a que otros entiendan mejor el proyecto
- 🔧 **Enviar pull requests** - Contribuye código directamente
- 🧪 **Escribir pruebas** - Ayuda a mantener la calidad del código
- 🌍 **Traducciones** - Ayuda a internacionalizar el proyecto

## Configuración del Entorno de Desarrollo

### Prerrequisitos

- Python 3.8 o superior
- Git
- SQL Server (para desarrollo local)

### Configuración Inicial

1. **Fork del repositorio**
   ```bash
   # Ve a GitHub y haz fork del repositorio
   # Luego clona tu fork
   git clone https://github.com/TU_USUARIO/proyecto2.git
   cd proyecto2
   ```

2. **Configurar el entorno virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos**
   - Modifica `config.py` con tus credenciales de base de datos
   - Asegúrate de que SQL Server esté ejecutándose

5. **Ejecutar pruebas**
   ```bash
   python test_basic.py
   ```

## Proceso de Contribución

### 1. Crear una Rama

```bash
git checkout -b feature/nombre-de-la-funcionalidad
# o
git checkout -b fix/nombre-del-bug
```

### 2. Hacer Cambios

- Escribe tu código siguiendo los estándares del proyecto
- Agrega pruebas para nuevas funcionalidades
- Actualiza la documentación según sea necesario

### 3. Commit y Push

```bash
git add .
git commit -m "feat: agregar nueva funcionalidad X"
git push origin feature/nombre-de-la-funcionalidad
```

### 4. Crear Pull Request

1. Ve a tu fork en GitHub
2. Haz clic en "New Pull Request"
3. Selecciona la rama con tus cambios
4. Completa el template de PR
5. Espera la revisión del código

## Estándares de Código

### Estilo de Código

- Sigue PEP 8 para Python
- Usa nombres descriptivos para variables y funciones
- Comenta código complejo
- Mantén funciones pequeñas y enfocadas

### Estructura de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: agregar nueva funcionalidad
fix: corregir bug en autenticación
docs: actualizar README
style: formatear código
refactor: refactorizar lógica de negocio
test: agregar pruebas para módulo X
chore: actualizar dependencias
```

### Pruebas

- Todas las nuevas funcionalidades deben tener pruebas
- Las pruebas deben pasar antes de enviar un PR
- Mantén la cobertura de código alta

## Reportando Bugs

### Antes de Reportar

1. Verifica que el bug no haya sido reportado ya
2. Asegúrate de que estés usando la versión más reciente
3. Intenta reproducir el bug en un entorno limpio

### Información Necesaria

- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs. actual
- Información del entorno (OS, Python, etc.)
- Capturas de pantalla si aplica

## Solicitando Funcionalidades

### Antes de Solicitar

1. Verifica que la funcionalidad no exista ya
2. Piensa en el caso de uso y beneficio
3. Considera la complejidad de implementación

### Información Necesaria

- Descripción clara de la funcionalidad
- Casos de uso específicos
- Beneficios para el proyecto
- Alternativas consideradas

## Preguntas Frecuentes

### ¿Puedo contribuir si soy principiante?

¡Absolutamente! Todos los niveles de experiencia son bienvenidos. Comienza con issues marcados como "good first issue" o "help wanted".

### ¿Qué pasa si mi PR es rechazado?

No te desanimes. Los mantenedores te darán feedback constructivo. Usa esa información para mejorar tu contribución.

### ¿Cómo puedo obtener ayuda?

- Abre un issue con la etiqueta "question"
- Únete a nuestras discusiones en GitHub
- Revisa la documentación existente

## Reconocimiento

Todas las contribuciones serán reconocidas en el archivo CHANGELOG.md y en la sección de contribuidores del README.

## Licencia

Al contribuir, aceptas que tu contribución será licenciada bajo la misma licencia del proyecto (MIT).

---

¡Gracias por contribuir a hacer KDL Systems mejor! 🚀
