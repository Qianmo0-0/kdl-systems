#!/usr/bin/env python3
"""
Pruebas básicas del sistema KDL Systems
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Prueba que se puedan importar todos los módulos principales"""
    try:
        from entities import Empleado, Producto, Distribuidora, Email, AportePatronal, Deducciones
        print("✓ Entidades importadas correctamente")
        
        from data_access import DataAccess
        print("✓ Acceso a datos importado correctamente")
        
        from business import BusinessLogic, EmailService
        print("✓ Lógica de negocio importada correctamente")
        
        from config import Config
        print("✓ Configuración importada correctamente")
        
        return True
    except ImportError as e:
        print(f"✗ Error al importar: {e}")
        return False

def test_entities_validation():
    """Prueba la validación de entidades"""
    try:
        from entities import Empleado, Producto, Distribuidora
        
        # Prueba Empleado
        empleado = Empleado(123456789, "Juan Pérez", "juan@test.com", "Desarrollador", 500000, "TI", "Desarrollo")
        empleado.validate()
        print("✓ Validación de Empleado exitosa")
        
        # Prueba Producto
        producto = Producto(1001, "Laptop", 1500000, "Electrónico", "Dell", 1)
        producto.validate()
        print("✓ Validación de Producto exitosa")
        
        # Prueba Distribuidora
        distribuidora = Distribuidora(2001, "TechCorp", "San José", "2250-1234")
        distribuidora.validate()
        print("✓ Validación de Distribuidora exitosa")
        
        return True
    except Exception as e:
        print(f"✗ Error en validación de entidades: {e}")
        return False

def test_config():
    """Prueba la configuración del sistema"""
    try:
        from config import Config
        
        # Verificar que la configuración se puede generar
        conn_string = Config.get_database_connection_string()
        if conn_string and "DRIVER" in conn_string:
            print("✓ Configuración de base de datos generada correctamente")
        else:
            print("✗ Error en configuración de base de datos")
            return False
            
        return True
    except Exception as e:
        print(f"✗ Error en configuración: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("=== PRUEBAS BÁSICAS DEL SISTEMA KDL SYSTEMS ===\n")
    
    tests = [
        ("Importación de módulos", test_imports),
        ("Validación de entidades", test_entities_validation),
        ("Configuración del sistema", test_config),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Ejecutando: {test_name}")
        if test_func():
            passed += 1
        print()
    
    print(f"=== RESULTADOS: {passed}/{total} pruebas pasaron ===")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas básicas pasaron!")
        return 0
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores arriba.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
