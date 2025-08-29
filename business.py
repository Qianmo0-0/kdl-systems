import smtplib
from email.mime.multipart import MIMEMultipart  
from email.mime.text import MIMEText  
from email.mime.base import MIMEBase  
from email import encoders
from config import Config  
from data_access import DataAccess
from entities import  Email, Empleado,AportePatronal,Deducciones, Producto, Distribuidora
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import io
from decimal import Decimal

class EmailService:  
    def send_email(self, email_data: Email):  
        if not email_data.sender or not email_data.recipients:
            raise ValueError("El remitente y los destinatarios deben ser proporcionados")
        if not email_data.subject or not email_data.body:
            raise ValueError("El asunto y el cuerpo del correo deben ser proporcionados")
        msg = MIMEMultipart()  
        msg['From'] = email_data.sender
        msg['To'] = ", ".join(email_data.recipients)
        msg['Subject'] = email_data.subject
        msg.attach(MIMEText(email_data.body, 'plain'))  
        if email_data.attachments:
            for attachment in email_data.attachments:
                if hasattr(attachment, 'filename') and attachment.filename:
                    attachment_part = MIMEBase('application', 'octet-stream')
                    attachment_part.set_payload(attachment.read())
                    encoders.encode_base64(attachment_part)
                    attachment_part.add_header('Content-Disposition', f'attachment; filename={attachment.filename}')
                    msg.attach(attachment_part)
        try:
            with smtplib.SMTP_SSL(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
                server.set_debuglevel(1) 
                server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)  
                server.send_message(msg)  
        except smtplib.SMTPException as e:
            raise RuntimeError(f"Error al enviar el correo: {e}")
        
        
class BusinessLogic:
    def __init__(self):
        self.data_access = DataAccess()
        self.deducciones = Deducciones()
        self.aporte_patronal = AportePatronal()

    
    def authenticate_user(self, username, password):
        user = self.data_access.get_empleado_by_credentials(username, password)
        if user:
            return {"username": username, "role": user[0]}
        return None

    def process_producto(self, producto: Producto):
        producto.validate()
        codigo_producto = self.data_access.save_producto(
            producto.codigo_producto, producto.nombre, producto.precio, producto.tipo,
            producto.marca, producto.distribuidora_id
        )
        producto.codigo_producto = codigo_producto
        
        return f"Producto {producto.tipo} guardado con Código de Producto {producto.codigo_producto}"
    
    
    def get_productop(self, codigo_producto):
        producto_data = self.data_access.get_productop(codigo_producto)
        if producto_data:
            return producto_data
        else:
            return None
        
    def get_producto_cliente(self, codigo_producto):
        producto_data = self.data_access.get_producto_cliente(codigo_producto)
        if producto_data:
            return producto_data
        else:
            return None
        
    def get_consultas_productos(self):
        """
        Obtiene los productos y sus cantidades de consultas, transformando los datos de la capa de acceso a un formato uniforme.
        """
        productos = self.data_access.get_ver_consultas_productos()
        return [
            {
                "codigo_producto": producto["Codigo_Producto"],
                "nombre": producto["Nombre"],
                "cantidad_consultas": producto["Cantidad_Consultas"]
            }
            for producto in productos
        ]
    
    def consultar_producto_por_nombre(self, nombre):
        if not nombre or len(nombre.strip()) == 0:
            raise ValueError("El nombre del producto no puede estar vacío.")
        return self.data_access.consultar_producto_por_nombre(nombre)
        
    def get_all_productos(self):
        productos = self.data_access.get_all_productos()
        return [
            {
                "codigo_producto": producto["Codigo_Producto"],  
                "nombre":producto["Nombre"],
                "precio": producto["Precio"],
                "tipo": producto["Tipo"],
                "marca": producto["Marca"],
                "distribuidora_id": producto["Distribuidora_ID"]
            }
            for producto in productos
    ]

    def get_producto(self, codigo_producto):
        producto_data = self.data_access.get_producto(codigo_producto)
        if producto_data:
            producto = Producto(
                codigo_producto=producto_data['Codigo_Producto'],
                nombre = producto_data['Nombre'],
                precio=producto_data['Precio'],
                tipo=producto_data['Tipo'],
                marca=producto_data['Marca'],
                distribuidora_id=producto_data['Distribuidora_ID']
            )
            return producto
        return None
    
    def update_producto(self, producto: Producto):
        producto.validate()
        self.data_access.update_producto(
            producto.codigo_producto, producto.nombre, producto.precio, producto.tipo,
            producto.marca, producto.distribuidora_id
        )
        return f"Producto {producto.tipo} actualizado correctamente"
    
    def delete_producto(self, producto: Producto):
        self.data_access.delete_producto(producto.codigo_producto)
        return f"Producto {producto.tipo} eliminado correctamente"

########################################################################
    def process_distribuidora(self, distribuidora: Distribuidora):
        distribuidora.validate()

        try:
            identificacion = self.data_access.save_distribuidora(
                distribuidora.identificacion, distribuidora.nombre, 
                distribuidora.telefono, distribuidora.direccion,
            )

            return f"Empleado {distribuidora.nombre} fue registrado correctamente con el identifcacion {identificacion}"     
        except Exception as e:
            raise RuntimeError(f"Error al procesar el empleado: {e}")
        
    def get_distribuidora(self, identificacion):
        distribuidora_data = self.data_access.get_distribuidora(identificacion) 
        if distribuidora_data:
            distribuidora = Distribuidora(
                identificacion=distribuidora_data['identificacion'],
                nombre=distribuidora_data['nombre'],
                telefono=distribuidora_data['telefono'],
                direccion=distribuidora_data['direccion']
            )
            return distribuidora
        return None

    def get_all_distribuidoras(self):
        distribuidoras_data = self.data_access.get_all_distribuidoras()
        distribuidoras = [
            Distribuidora(
                identificacion=data['identificacion'],
                nombre=data['nombre'],
                direccion=data['direccion'],
                telefono=data['telefono']
            ) for data in distribuidoras_data
        ]
        return distribuidoras
    
    def update_distribuidora(self, distribuidora: Distribuidora):
        distribuidora.validate()
        return self.data_access.update_distribuidora(distribuidora)

    def delete_distribuidora(self, identificacion):
        return self.data_access.delete_distribuidora(identificacion)
####################################################################################################

    def process_empleado(self, empleado: Empleado):
        empleado.validate()
        try:
            identificacion = self.data_access.insert_empleado(
                empleado.identificacion, empleado.nombre, empleado.correo, empleado.cargo,
                empleado.salario, empleado.seccion_tipo, empleado.seccion_nombre
            )
            
            email_data = Email(
            subject="Registro de Empleado",
            sender=Config.MAIL_USERNAME,
            recipients=[empleado.correo],
            body=f"El Empleado {empleado.nombre} fue registrado correctamente con el nombre usuario {empleado.correo} y contrasena {empleado.identificacion}.",
            attachments=None
        )
            email_service = EmailService()
            email_service.send_email(email_data)
        
            return f"Empleado {empleado.nombre} fue registrado correctamente con el nombre usuario {empleado.correo} y contrasena de {empleado.identificacion}"
        except Exception as e:
            raise RuntimeError(f"Error al procesar el empleado: {e}")
        
    def register_empleado(self, identificacion, nombre, cargo, salario, seccion_tipo, seccion_nombre):
        empleado = Empleado(identificacion, nombre, cargo, salario, seccion_tipo, seccion_nombre)
        self.data_access.insert_empleado(
            empleado.identificacion, 
            empleado.nombre, 
            empleado.cargo, 
            empleado.salario, 
            empleado.seccion_tipo, 
            empleado.seccion_nombre
        )    
        
    def update_empleado(self, empleado: Empleado):

        empleado.validate()
        self.data_access.update_empleado(
            empleado.identificacion, empleado.nombre, empleado.correo, empleado.cargo,
            empleado.salario, empleado.seccion_tipo, empleado.seccion_nombre
        )
        return f"Empleado {empleado.nombre} actualizado correctamente"

    def delete_empleado(self, empleado: Empleado):
        self.data_access.delete_empleado(empleado.identificacion)
        return f"Empleado {empleado.nombre} eliminado correctamente"

    def get_all_empleado(self):
        empleados_data = self.data_access.get_all_empleados()
        empleados = [
            Empleado(
                identificacion=data['identificacion'],
                nombre=data['nombre'],
                correo=data['correo'],
                cargo=data['cargo'],
                salario=data['salario'],
                seccion_tipo=data['seccion_tipo'],
                seccion_nombre=data['seccion_nombre']
            ) for data in empleados_data
        ]
        return empleados

    def get_empleado(self, identificacion):
        empleado_data = self.data_access.get_empleado_por_identificacion(identificacion)
        if empleado_data:
            empleado = Empleado(
                identificacion=empleado_data['identificacion'],
                nombre=empleado_data['nombre'],
                correo=empleado_data['correo'],
                cargo=empleado_data['cargo'],
                salario=empleado_data['salario'],
                seccion_tipo=empleado_data['seccion_tipo'],
                seccion_nombre=empleado_data['seccion_nombre']
            )
            return empleado
        return None
    
    def obtener_correo_empleado(self, identificacion):
        if not identificacion:
            raise ValueError("El carnet del empleado no puede estar vacío")

        correo = self.data_access.obtener_correo_por_carnet(identificacion)
        
        if not correo:
            raise ValueError(f"No se encontró un correo para el carnet {identificacion}")
        return correo


    def calcular_aporte_patrono(self, salario):

        aporte_patronal_sem = Decimal(salario) * Decimal(self.aporte_patronal.sem) / Decimal(100)
        aporte_patronal_ivm = Decimal(salario) * Decimal(self.aporte_patronal.ivm) / Decimal(100)
        aporte_patronal_bpop = Decimal(salario) * Decimal(self.aporte_patronal.bpop) / Decimal(100)
        aporte_patronal_fcl = Decimal(salario) * Decimal(self.aporte_patronal.fcl) / Decimal(100)
        aporte_patronal_opc = Decimal(salario) * Decimal(self.aporte_patronal.opc) / Decimal(100)
        aporte_patronal_ins = Decimal(salario) * Decimal(self.aporte_patronal.ins) / Decimal(100)
        aporte_patronal_bpop2 = Decimal(salario) * Decimal(self.aporte_patronal.bpop2) / Decimal(100)
        aporte_patronal_ima = Decimal(salario) * Decimal(self.aporte_patronal.ima) / Decimal(100)
        aporte_patronal_ina = Decimal(salario) * Decimal(self.aporte_patronal.ina) / Decimal(100)
        aporte_patronal_asig = Decimal(salario) * Decimal(self.aporte_patronal.asig) / Decimal(100)
        return aporte_patronal_sem, aporte_patronal_ivm, aporte_patronal_bpop,aporte_patronal_fcl, aporte_patronal_opc, aporte_patronal_ins, aporte_patronal_bpop2,aporte_patronal_ima, aporte_patronal_ina, aporte_patronal_asig
        
    def calcular_salario_neto(self, salario):
        aporte_patronal_sem, aporte_patronal_ivm, aporte_patronal_bpop, aporte_patronal_fcl, aporte_patronal_opc, aporte_patronal_ins, aporte_patronal_bpop2,aporte_patronal_ima, aporte_patronal_ina,aporte_patronal_asig = self.calcular_aporte_patrono(salario)
        total_deducciones = aporte_patronal_sem + aporte_patronal_ivm + aporte_patronal_bpop + aporte_patronal_fcl + aporte_patronal_opc +aporte_patronal_ins + aporte_patronal_bpop2 + aporte_patronal_ima + aporte_patronal_ina + aporte_patronal_asig
        return Decimal(salario) - total_deducciones 
    
    

    def generate_payroll_pdf(self, empleado:Empleado ):

        buffer = io.BytesIO()
        page_size = landscape(letter) 
        p = canvas.Canvas(buffer, pagesize=page_size)
        width, height = page_size
        empleado.validate()


        salario = Decimal(empleado.salario)
        aporte_patronal_sem, aporte_patronal_ivm, aporte_patronal_bpop, aporte_patronal_fcl,aporte_patronal_opc, aporte_patronal_ins, aporte_patronal_bpop2,aporte_patronal_ima, aporte_patronal_ina, aporte_patronal_asig = self.calcular_aporte_patrono(salario)
        salario_neto = self.calcular_salario_neto(salario)
        


        
        # Dibujar título 
        p.setFont("Helvetica-Bold", 24)
        p.setFillColor(colors.black)
        p.drawString(50, height - 70, "Aporte Patronal")

        # Dibujar información del empleado
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 100, f"Identificación: {empleado.identificacion}")
        p.drawString(50, height - 120, f"Empleado: {empleado.nombre} ")
        p.drawString(50, height - 140, f"Cargo: {empleado.cargo}")
        p.drawString(50, height - 160, f"Salario Bruto: ¢{float(empleado.salario):.2f} CRC")
        p.drawString(50, height - 185, f"Aportes Patronales")

        # Datos de deducciones
        data = [
            ['Descripción', 'Porcentaje', 'Monto'],
            ['Salario Bruto', '', f'¢{float(empleado.salario):.2f} CRC'],
            ['Deducción SEM', f'{self.aporte_patronal.sem:.2f}%', f'¢{float(aporte_patronal_sem):.2f} CRC'],
            ['Deducción IVM', f'{self.aporte_patronal.ivm:.2f}%', f'¢{float(aporte_patronal_ivm):.2f} CRC'],
            ['Deducción BPOP', f'{self.aporte_patronal.bpop:.2f}%', f'¢{float(aporte_patronal_bpop):.2f} CRC'],
            ['Asignaciones Familiares', f'{self.aporte_patronal.asig:.2f}%', f'¢{float(aporte_patronal_asig):.2f} CRC'],
            ['Deducción IMA', f'{self.aporte_patronal.ima:.2f}%', f'¢{float(aporte_patronal_ima):.2f} CRC'],
            ['Deducción INA', f'{self.aporte_patronal.ina:.2f}%', f'¢{float(aporte_patronal_ina):.2f} CRC'],
            ['Deducción BPOP', f'{self.aporte_patronal.bpop:.2f}%', f'¢{float(aporte_patronal_bpop2):.2f} CRC'],
            ['Deducción FCL', f'{self.aporte_patronal.fcl:.2f}%', f'¢{float(aporte_patronal_fcl):.2f} CRC'],
            ['Deducción OPC', f'{self.aporte_patronal.opc:.2f}%', f'¢{float(aporte_patronal_opc):.2f} CRC'],
            ['Deducción INS', f'{self.aporte_patronal.ins:.2f}%', f'¢{float(aporte_patronal_ins):.2f} CRC'],
            ['Total de Pago', '', f'¢{float(salario_neto):.2f} CRC']
        ]
        # Crear tabla
        table = Table(data, colWidths=[3 * inch, 1 * inch, 2 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),      # Fondo de la cabecera
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),           # Texto blanco en la cabecera
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),                  # Alineación centrada
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),        # Texto en negrita en cabecera
            ('FONTSIZE', (0, 0), (-1, 0), 14),                      # Tamaño de la fuente de cabecera
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),                  # Espaciado inferior en cabecera
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),     # Fondo blanco suave para el resto de la tabla
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),            # Bordes de la tabla
            ('FONTSIZE', (0, 0), (-1, -1), 10),                     # Tamaño de fuente para el cuerpo  
        ]))

        # Posicionar la tabla
        table_width, table_height = table.wrap(0, 0)
        x_table = 50
        y_table = height - 440  # Ajustar según la posición deseada
        table.drawOn(p, x_table, y_table)

        # Finalizar PDF
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer
    
    def calcular_deduccion (self,salario):
        deduccion_semm = Decimal(salario) * Decimal(self.deducciones.semm) / Decimal(100)
        deduccion_ivmm = Decimal(salario) * Decimal(self.deducciones.ivmm) / Decimal(100)
        deduccion_bpopp = Decimal(salario) * Decimal(self.deducciones.bpopp) / Decimal(100)
        return deduccion_semm, deduccion_ivmm, deduccion_bpopp

    def calcular_salario_neto_trabajador(self, salario):
        deduccion_semm, deduccion_ivmm, deduccion_bpopp = self.calcular_deduccion(salario)
        total_deducciones = deduccion_semm + deduccion_ivmm + deduccion_bpopp
        return Decimal(salario) - total_deducciones, deduccion_semm, deduccion_ivmm, deduccion_bpopp
    
    def generate_payroll_pdf_trabajador(self, empleado:Empleado ):
        # Crear un buffer para almacenar el PDF en memoria
        buffer = io.BytesIO()
        page_size = landscape(letter)  # Tamaño de la página en formato apaisado
        p = canvas.Canvas(buffer, pagesize=page_size)
        width, height = page_size
        # Validar el objeto empleado (debes asegurarte que el método validate() exista)
        empleado.validate()


        # Calcular deducciones y salario neto utilizando Decimal para precisión
        salario = Decimal(empleado.salario)
        salario_neto, deduccion_semm, deduccion_ivmm, deduccion_bpopp = self.calcular_salario_neto_trabajador(salario)


        
        # Dibujar título 
        p.setFont("Helvetica-Bold", 24)
        p.setFillColor(colors.black)
        p.drawString(50, height - 70, "Nomina de Pago")

        # Dibujar información del empleado
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 100, f"Identificación: {empleado.identificacion}")
        p.drawString(50, height - 120, f"Empleado: {empleado.nombre} ")
        p.drawString(50, height - 140, f"Cargo: {empleado.cargo}")
        p.drawString(50, height - 160, f"Salario Bruto: ¢{float(empleado.salario):.2f} CRC")
        p.drawString(50, height - 185, f"Deduccion Empleado")

        # Datos de deducciones
        data = [
            ['Descripción', 'Porcentaje', 'Monto'],
            ['Salario Bruto', '', f'¢{float(empleado.salario):.2f} CRC'],
            ['Deducción SEM', f'{self.deducciones.semm:.2f}%', f'¢{float(deduccion_semm):.2f} CRC'],
            ['Deducción IVM', f'{self.deducciones.ivmm:.2f}%', f'¢{float(deduccion_ivmm):.2f} CRC'],
            ['Deducción BPOP', f'{self.deducciones.bpopp:.2f}%', f'¢{float(deduccion_bpopp):.2f} CRC'],
            ['Salario Neto', '', f'¢{float(salario_neto):.2f} CRC']
        ]
        # Crear tabla
        table = Table(data, colWidths=[3 * inch, 1 * inch, 2 * inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),      # Fondo de la cabecera
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),           # Texto blanco en la cabecera
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),                  # Alineación centrada
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),        # Texto en negrita en cabecera
            ('FONTSIZE', (0, 0), (-1, 0), 14),                      # Tamaño de la fuente de cabecera
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),                  # Espaciado inferior en cabecera
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),     # Fondo blanco suave para el resto de la tabla
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),            # Bordes de la tabla
            ('FONTSIZE', (0, 0), (-1, -1), 10),                     # Tamaño de fuente para el cuerpo  
        ]))
        
        # Posicionar la tabla
        table_width, table_height = table.wrap(0, 0)
        x_table = 50
        y_table = height - 310  # Ajustar según la posición deseada
        table.drawOn(p, x_table, y_table)

        # Finalizar PDF
        p.showPage()
        p.save()
        buffer.seek(0)
        return buffer
