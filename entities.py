class Distribuidora:
    def __init__(self, identificacion, nombre, direccion, telefono):
        self.identificacion = identificacion
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono

    def validate(self):
        if not self.identificacion or not isinstance(self.identificacion, int):
            raise ValueError("La identificación debe ser un número entero válido.")
        if not self.nombre or not isinstance(self.nombre, str) or len(self.nombre.strip()) == 0:
            raise ValueError("El nombre de la distribuidora no puede estar vacío.")
        if not self.direccion or not isinstance(self.direccion, str) or len(self.direccion.strip()) == 0:
            raise ValueError("La dirección de la distribuidora no puede estar vacía.")
        if not self.telefono or not isinstance(self.telefono, str) or len(self.telefono.strip()) < 7:
            raise ValueError("El teléfono debe ser una cadena válida con al menos 7 dígitos.")

    def __repr__(self):
        return f"Distribuidora(identificacion={self.identificacion}, nombre={self.nombre}, direccion={self.direccion}, telefono={self.telefono})"

class Producto:
    def __init__(self, codigo_producto=None, nombre=None, precio=None, tipo=None, marca=None, distribuidora_id=None):
        self.codigo_producto = codigo_producto
        self.nombre = nombre
        self.precio = precio
        self.tipo = tipo
        self.marca = marca
        self.distribuidora_id = distribuidora_id

    def validate(self):
        if not self.codigo_producto or not isinstance(self.codigo_producto, int):
            raise ValueError("El código de producto debe ser un número entero válido.")
        if not self.precio or not isinstance(self.precio, (int, float)) or self.precio <= 0:
            raise ValueError("El precio debe ser un número positivo válido.")
        if not self.nombre or not isinstance(self.nombre, str) or len(self.nombre.strip()) == 0:
            raise ValueError("El nombre del producto no puede estar vacío.")
        if not self.tipo or not isinstance(self.tipo, str) or len(self.tipo.strip()) == 0:
            raise ValueError("El tipo de producto no puede estar vacío.")
        if not self.marca or not isinstance(self.marca, str) or len(self.marca.strip()) == 0:
            raise ValueError("La marca del producto no puede estar vacía.")
        if not self.distribuidora_id or not isinstance(self.distribuidora_id, int):
            raise ValueError("La identificación de la distribuidora debe ser un número entero válido.")

    def __repr__(self):
        return f"Producto(codigo_producto={self.codigo_producto}, precio={self.precio}, tipo={self.tipo}, marca={self.marca}, distribuidora_id={self.distribuidora_id})"


class Empleado:
    def __init__(self, identificacion, nombre, correo, cargo, salario, seccion_tipo, seccion_nombre):
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo 
        self.cargo = cargo
        self.salario = salario
        self.seccion_tipo = seccion_tipo
        self.seccion_nombre = seccion_nombre
        
    # Método para validar los datos del empleado
    def validate(self):
        if not self.identificacion or not isinstance(self.identificacion, int):
            raise ValueError("La identificación debe ser un número entero válido.")
        if not self.nombre or not isinstance(self.nombre, str) or len(self.nombre.strip()) == 0:
            raise ValueError("El nombre debe ser una cadena de texto válida y no puede estar vacío.")
        if not self.correo or not isinstance(self.correo, str) or len(self.correo.strip()) == 0:
            raise ValueError("El correo debe ser una cadena de texto válida y no puede estar vacío.")
        if not self.cargo or not isinstance(self.cargo, str) or len(self.cargo.strip()) == 0:
            raise ValueError("El cargo debe ser una cadena de texto válida y no puede estar vacío.")
        if self.salario is None or (not isinstance(self.salario, (int, float)) and not str(self.salario).replace('.', '').isdigit()) or float(self.salario) <= 0:
            raise ValueError("El salario debe ser un número positivo válido.")
        if not self.seccion_tipo or not isinstance(self.seccion_tipo, str) or len(self.seccion_tipo.strip()) == 0:
            raise ValueError("El tipo de sección debe ser una cadena de texto válida y no puede estar vacío.")
        if not self.seccion_nombre or not isinstance(self.seccion_nombre, str) or len(self.seccion_nombre.strip()) == 0:
            raise ValueError("El nombre de la sección debe ser una cadena de texto válida y no puede estar vacío.")


class Email:
    def __init__(self, subject, sender, recipients, body, attachments=None):
        self.subject = subject
        self.sender = sender
        self.recipients = recipients
        self.body = body
        self.attachments = attachments or []  
        

class AportePatronal:
    def __init__(self):

        #Aporte Patronal
        self.sem = 9.25
        self.ivm = 5.42
        self.bpop = 0.25
        self.asig = 5.00
        self.fcl = 1.50
        self.opc = 2.00
        self.bpop2 = 0.25
        self.ins = 1.00
        self.ima = 0.50
        self.ina = 1.50
       
class Deducciones:
    def __init__(self):
        
        #CCSS
        self.semm = 5.50
        self.ivmm = 4.17

        #Otras Instituciones (Banco Popular)
        self.bpopp = 1.00

       