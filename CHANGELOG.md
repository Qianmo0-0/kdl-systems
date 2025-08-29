# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Sistema de gestión completo para empleados, productos y distribuidoras
- Autenticación con roles de administrador y empleado
- Generación de PDFs para nóminas y aportes patronales
- Sistema de envío de emails automático
- Interfaz web responsiva con Bootstrap
- Validaciones robustas en todas las entidades
- Sistema de configuración centralizado
- Soporte para Docker y Docker Compose
- Configuración de Nginx para producción
- Scripts de instalación automatizados
- Sistema de pruebas básico
- Configuración de CI/CD con GitHub Actions
- Templates para issues y pull requests
- Código de conducta y guía de contribución

### Changed
- Mejorado el manejo de errores en todas las capas
- Refactorizada la arquitectura para mejor separación de responsabilidades
- Optimizadas las validaciones de entidades
- Mejorada la configuración de base de datos

### Fixed
- Corregido el orden de parámetros en la clase Empleado
- Mejorado el manejo de conexiones a base de datos
- Corregidos los mensajes de error para ser más descriptivos

## [1.0.0] - 2024-12-19

### Added
- Lanzamiento inicial del sistema KDL Systems
- Funcionalidades básicas de gestión empresarial
- Sistema de autenticación y autorización
- Generación de reportes en PDF
- Interfaz de usuario completa

---

## Notas de Versión

### Versionado Semántico

- **MAJOR**: Cambios incompatibles con versiones anteriores
- **MINOR**: Nuevas funcionalidades compatibles con versiones anteriores
- **PATCH**: Correcciones de bugs compatibles con versiones anteriores

### Tipos de Cambios

- **Added**: Nuevas funcionalidades
- **Changed**: Cambios en funcionalidades existentes
- **Deprecated**: Funcionalidades que serán removidas en futuras versiones
- **Removed**: Funcionalidades removidas
- **Fixed**: Correcciones de bugs
- **Security**: Mejoras de seguridad
