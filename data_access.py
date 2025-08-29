import pyodbc
from config import Config


class DataAccess:
    def __init__(self):
        self.connection_string = Config.get_database_connection_string()
        
        
    def get_empleado_by_credentials(self, username, password):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Cargo FROM Empleado WHERE Correo = ? AND Identificacion = ?", (username, password))
                user = cursor.fetchone()
                return user
        except pyodbc.Error as e:
            raise RuntimeError(f"Error de base de datos: {e}")
        except Exception as e:
            raise RuntimeError(f"Error inesperado: {e}")

    def authenticate_user(self, username, password):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT Cargo FROM Empleado WHERE Correo = ? AND Identificacion = ?", (username, password))
                return cursor.fetchone()
        except pyodbc.Error as e:
            raise RuntimeError(f"Error de base de datos: {e}")
        except Exception as e:
            raise RuntimeError(f"Error inesperado: {e}")

    def save_distribuidora(self, identificacion, nombre, telefono,direccion):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    EXEC InsertarDistribuidora 
                        @Identificacion_Distribuidora = ?, 
                        @Nombre = ?, 
                        @Telefono = ?, 
                        @Direccion = ?
                ''', (identificacion, nombre, telefono, direccion))
                conn.commit()
            return f"Distribuidora '{nombre}' guardada correctamente."
        except Exception as e:
            raise RuntimeError(f"Error al guardar distribuidora: {e}")

    def get_distribuidora(self, identificacion):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC ConsultarDistribuidora @Identificacion_Distribuidora = ?", (identificacion,))
                row = cursor.fetchone()
                if row:
                    distribuidora = {
                        "identificacion": row[0],
                        "nombre": row[1],
                        "telefono": row[2],
                        "direccion": row[3]
                    }
                    return distribuidora
                else:
                    return None
        except Exception as e:
            raise RuntimeError(f"Error al obtener la distribuidora: {e}")
        
    def get_all_distribuidoras(self):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC ConsultarTodasLasDistribuidoras")
                rows = cursor.fetchall()
                distribuidoras = [
                    {
                        "identificacion": row[0],
                        "nombre": row[1],
                        "telefono": row[2],
                        "direccion": row[3]
                    }
                    for row in rows
                ]
            return distribuidoras
        except Exception as e:
            raise RuntimeError(f"Error al obtener todas las distribuidoras: {e}")

    def update_distribuidora(self, distribuidora):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    EXEC ActualizarDistribuidora @Identificacion_Distribuidora = ?, @Nombre = ?, 
                                                 @Telefono = ?, @Direccion = ?
                ''', (distribuidora.identificacion, distribuidora.nombre, distribuidora.telefono, distribuidora.direccion))
                conn.commit()
            return f"Distribuidora {distribuidora.nombre} actualizada correctamente"
        except Exception as e:
            raise RuntimeError(f"Error al actualizar Distribuidora: {e}")

    def delete_distribuidora(self, identificacion):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC EliminarDistribuidora @Identificacion_Distribuidora = ?", (identificacion,))
                conn.commit()
            return f"Distribuidora con ID {identificacion} eliminada correctamente"
        except Exception as e:
            raise RuntimeError(f"Error al eliminar Distribuidora: {e}")
        
###############################################################################33

    def get_productop(self, codigo_producto):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC ConsultarProducto @Codigo_Producto = ?", (codigo_producto,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        "nombre": row[1], 
                        "precio": row[2]  
                    }
                else:
                    return None
        except Exception as err:
            raise RuntimeError(f"Error al obtener el producto: {err}")

        
    def get_producto_cliente(self, codigo_producto):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC sp_ConsultarProducto @Codigo_Producto = ?", (codigo_producto,))
                row = cursor.fetchone()
                
                if row:
                    return {
                        "nombre": row[1],   
                        "precio": row[2]   
                    }
                else:
                    return None
        except Exception as err:
            raise RuntimeError(f"Error al obtener el producto: {err}")
        
        
    def save_producto(self, codigo_producto, nombre, precio, tipo, marca, distribuidora_id):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    EXEC InsertarProducto @Codigo_Producto = ?, @Nombre = ?, @Precio = ?, 
                                        @Tipo = ?, @Marca = ?, @Distribuidora_ID = ?
                ''', (codigo_producto, nombre, precio, tipo, marca, distribuidora_id))
                conn.commit() 
            return "Producto guardado exitosamente"  
        except Exception as e:
            raise RuntimeError(f"Error al guardar Producto: {e}")

    def consultar_producto_por_nombre(self, nombre):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC sp_ConsultarProductoPorNombre @Nombre = ?", nombre)
                rows = cursor.fetchall()
                productos = [
                    {
                        "codigo_producto": row[0],
                        "nombre": row[1],
                        "precio": row[2],
                        "tipo": row[3],
                        "marca": row[4]
                    }
                    for row in rows
                ]
                return productos
        except Exception as e:
            raise RuntimeError(f"Error al consultar producto por nombre: {str(e)}")
    
    
    def get_ver_consultas_productos(self):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC sp_VerConsultasProductos")
                rows = cursor.fetchall()
                
                productos = [{
                    "Codigo_Producto": row[0],
                    "Nombre": row[1],
                    "Cantidad_Consultas": row[2]
                } for row in rows]
                
            return productos

        except pyodbc.Error as err:
            raise RuntimeError(f"Error al obtener los productos con sus consultas: {err}")
        
    def get_all_productos(self):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC ConsultarTodosLosProductos")
                rows = cursor.fetchall()
                productos = [{
                    "Codigo_Producto": row[0],
                    "Nombre": row[1],
                    "Precio": row[2],
                    "Tipo": row[3],
                    "Marca": row[4],
                    "Distribuidora_ID": row[5]
                } for row in rows]
            return productos
        except Exception as err:
            raise RuntimeError(f"Error al obtener los productos: {err}")

    def get_producto(self, codigo_producto):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC ConsultarProductos @Codigo_Producto = ?", (codigo_producto,))
                row = cursor.fetchone()
                if row:
                    producto = {
                        "Codigo_Producto": row[0],
                        "Nombre": row[1],
                        "Precio": row[2],
                        "Tipo": row[3],
                        "Marca": row[4],
                        "Distribuidora_ID": row[5]
                    }
                    return producto
                else:
                    return None
        except Exception as err:
            raise RuntimeError(f"Error al obtener el producto: {err}")

    def update_producto(self, codigo_producto, nombre, precio, tipo, marca, distribuidora_id):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    EXEC ActualizarProducto @Codigo_Producto = ?, @Nombre = ?, @Precio = ?, @Tipo = ?, 
                                            @Marca = ?, @Distribuidora_ID = ?
                ''', (codigo_producto, nombre, precio, tipo, marca, distribuidora_id))
                conn.commit()
        except Exception as err:
            raise RuntimeError(f"Error al actualizar producto: {err}")

    def delete_producto(self, codigo_producto):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC EliminarProducto @Codigo_Producto = ?", (codigo_producto,))
                conn.commit()
        except Exception as err:
            raise RuntimeError(f"Error al eliminar producto: {err}")
#####################################################################################3


    def insert_empleado(self, identificacion, nombre, correo, cargo, salario, seccion_tipo, seccion_nombre):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    EXEC InsertarEmpleado @Identificacion = ?, @Nombre = ?, @Correo = ?, @Cargo = ?, 
                                          @Salario = ?, @Seccion_Tipo = ?, @Seccion_Nombre = ?
                ''', (identificacion, nombre, correo, cargo, salario, seccion_tipo, seccion_nombre))
                conn.commit()
                return f"Empleado {nombre} registrado correctamente"
        except pyodbc.Error as e:
            raise RuntimeError(f"Error de base de datos: {e}")
        except Exception as e:
            raise RuntimeError(f"Error inesperado: {e}")

    def get_all_empleados(self):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC ObtenerTodosEmpleados")
                rows = cursor.fetchall()

                empleados = [{
                    "identificacion": row[0],
                    "nombre": row[1],
                    "correo": row[2],
                    "cargo": row[3],
                    "salario": row[4],
                    "seccion_tipo": row[5],
                    "seccion_nombre": row[6]
                } for row in rows]
            return empleados
        except Exception as err:
            raise RuntimeError(f"Error al obtener los empleados: {err}")

    def get_empleado_por_identificacion(self, identificacion):
        try:

            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC ObtenerEmpleadoPorIdentificacion @Identificacion = ?", (identificacion,))
                row = cursor.fetchone()
                if row:
                    empleado = {
                        "identificacion": row[0],
                        "nombre": row[1],
                        "correo": row[2],
                        "cargo": row[3],
                        "salario": row[4],
                        "seccion_tipo": row[5],
                        "seccion_nombre": row[6]
                    }
                    return empleado
                else:
                    return None
        except Exception as err:
            raise RuntimeError(f"Error al obtener el empleado: {err}")
        
    def obtener_correo_por_carnet(self, identificacion):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT correo FROM Empleado WHERE identificacion = ?''', (identificacion,))
                result = cursor.fetchone()
                if result:
                    return result[0] 
                return None 
        except Exception as err:
            raise RuntimeError(f"Error al obtener el correo: {err}")
    
    def update_empleado(self, identificacion, nombre, correo, cargo, salario, seccion_tipo, seccion_nombre):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    EXEC ActualizarEmpleado @Identificacion = ?, @Nombre = ?, @Correo = ?,
                                            @Cargo = ?, @Salario = ?, 
                                            @Seccion_Tipo = ?, @Seccion_Nombre = ?
                ''', (identificacion, nombre, correo, cargo, salario, seccion_tipo, seccion_nombre))
                conn.commit()
        except Exception as err:
            raise RuntimeError(f"Error al actualizar empleado: {err}")

    def delete_empleado(self, identificacion):
        try:
            with pyodbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC EliminarEmpleado @Identificacion = ?", (identificacion,))
                conn.commit()
        except Exception as err:
            raise RuntimeError(f"Error al eliminar empleado: {err}")

            