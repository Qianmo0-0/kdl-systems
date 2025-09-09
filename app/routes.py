from flask import Flask, request, session, render_template, redirect, url_for, send_file, make_response, current_app as app
from business import BusinessLogic , EmailService
from entities import Empleado, Email,Producto, Distribuidora
from datetime import datetime

email_service = EmailService()
business_logic = BusinessLogic()

@app.route('/cliente/consultar_producto', methods=['GET', 'POST'])
def consultar_producto_cliente():
    producto = None
    error = None
    all_productos = business_logic.get_all_productos()
    if request.method == 'POST':
        try:
            codigo_producto = int(request.form['codigo_producto'])

            producto_data = business_logic.get_producto_cliente(codigo_producto)
            if producto_data:
                producto = {
                    'nombre': producto_data['nombre'],
                    'precio': producto_data['precio']
                }
            else:
                error = "Producto no encontrado"
        except ValueError:
            error = "Código de producto no válido"
        except Exception as e:
            error = f"Error al consultar el producto: {str(e)}"
            
    return render_template('consultar_producto_cliente.html', producto=producto, error=error, productos=all_productos)

######################################################################################################

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = business_logic.authenticate_user(username, password)  
        
        if user:
            session['username'] = username
            session['role'] = user['role']
            if session['role'].lower() == 'administrador':
                return redirect(url_for('empleados'))
            elif session['role'].lower() == 'empleado':
                return redirect(url_for('consultar_producto_empleado'))
        else:
            return render_template('error.html', mensaje="El usuario no existe o las credenciales son incorrectas.")
    
    return render_template('login2.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login')) 
####################################################################################################################3


@app.route('/distribuidoras')
def distribuidoras():
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 

    all_distribuidoras = business_logic.get_all_distribuidoras()
    return render_template('distribuidoras.html', distribuidoras=all_distribuidoras)

@app.route('/distribuidora/<int:identificacion>')
def view_distribuidora(identificacion):
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    distribuidora = business_logic.get_distribuidora(identificacion)
    if distribuidora:
        return render_template('view_distribuidora.html', distribuidora=distribuidora)
    else:
        return "Distribuidora no encontrada", 404


@app.route('/add_distribuidora', methods=['GET', 'POST'])
def add_distribuidora():
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    if request.method == 'POST':
        try:
            identificacion = int(request.form['identificacion'])
        except ValueError:
            return "La identificación debe ser un número entero válido.", 400
        
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        distribuidora = Distribuidora(
            identificacion=identificacion,
            nombre=nombre,
            direccion=direccion,
            telefono=telefono
        )
        
        try:
            result = business_logic.process_distribuidora(distribuidora)
            return redirect(url_for('distribuidoras'))
        except ValueError as e:
            return str(e), 400
    return render_template('add_distribuidora.html')

@app.route('/edit_distribuidora/<int:identificacion>', methods=['GET', 'POST'])
def edit_distribuidora(identificacion):
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        distribuidora = Distribuidora(
            identificacion=identificacion,
            nombre=nombre,
            direccion=direccion,
            telefono=telefono
        )
        
        try:
            result = business_logic.update_distribuidora(distribuidora)
            return redirect(url_for('distribuidoras'))
        except ValueError as e:
            return str(e), 400
    else:
        distribuidora_data = business_logic.get_distribuidora(identificacion)
        if distribuidora_data:
            return render_template('edit_distribuidora.html', distribuidora=distribuidora_data)
        else:
            return "Distribuidora no encontrada", 404

@app.route('/delete_distribuidora/<int:identificacion>', methods=['GET', 'POST'])
def delete_distribuidora(identificacion):
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    if request.method == 'POST':
        result = business_logic.delete_distribuidora(identificacion)
        return redirect(url_for('distribuidoras'))
    else:
        distribuidora_data = business_logic.get_distribuidora(identificacion)
        if distribuidora_data:
            return render_template('delete_distribuidora.html', distribuidora=distribuidora_data)
        else:
            return "Distribuidora no encontrada", 404
        
@app.route('/productos')
def productos():
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    all_productos = business_logic.get_all_productos()
    return render_template('productos.html', productos=all_productos)


@app.route('/producto/<int:codigo_producto>', methods=['GET'])
def view_producto(codigo_producto):
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    producto = business_logic.get_producto(codigo_producto)
    if producto:
        return render_template('view_producto.html', producto=producto)
    else:
        return "Producto no encontrado", 404

@app.route('/add_producto', methods=['GET', 'POST'])
def add_producto():
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    if request.method == 'POST':
        codigo_producto = int(request.form['codigo_producto'])
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        tipo = request.form['tipo']
        marca = request.form['marca']
        distribuidora_id = int(request.form['distribuidora_id'])
        
        producto = Producto(
            codigo_producto=codigo_producto,
            nombre=nombre,
            precio=precio,
            tipo=tipo,
            marca=marca,
            distribuidora_id=distribuidora_id
        )
        
        result = business_logic.process_producto(producto)
        return redirect(url_for('productos'))
    return render_template('add_producto.html')


@app.route('/consultar_producto', methods=['GET', 'POST'])
def consultar_producto():

    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login'))

    producto = None
    productos = None
    error = None

    try:

        productos_data = business_logic.get_consultas_productos()
        if productos_data:
            productos = [
                {
                    'codigo_producto': p['codigo_producto'],
                    'nombre': p['nombre'],
                    'cantidad_consultas': p['cantidad_consultas']
                } for p in productos_data
            ]
    except Exception as e:
        error = f"Error al cargar el listado de productos: {str(e)}"

    if request.method == 'POST':
        try:
            codigo_producto = int(request.form['codigo_producto'])
            producto_data = business_logic.get_productop(codigo_producto)

            if producto_data:
                producto = {
                    'nombre': producto_data['nombre'],
                    'precio': producto_data['precio']
                }
            else:
                error = "Producto no encontrado"
        except ValueError:
            error = "Código de producto no válido"
        except Exception as e:
            error = f"Error al consultar el producto: {str(e)}"

    return render_template('consultar_producto.html', producto=producto, productos=productos, error=error)

@app.route('/buscar_producto_por_nombre', methods=['GET', 'POST'])
def buscar_producto_por_nombre():
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login'))

    productos = []
    error = None

    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            productos = business_logic.consultar_producto_por_nombre(nombre)
        except ValueError as ve:
            error = str(ve)
        except Exception as e:
            error = f"Error al buscar productos: {str(e)}"

    return render_template('buscar_producto_por_nombre.html', productos=productos, error=error)

@app.route('/edit_producto/<int:codigo_producto>', methods=['GET', 'POST'])
def edit_producto(codigo_producto):
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        tipo = request.form['tipo']
        marca = request.form['marca']
        distribuidora_id = int(request.form['distribuidora_id'])
        
        producto = Producto(
            codigo_producto=codigo_producto,
            nombre=nombre,
            precio=precio,
            tipo=tipo,
            marca=marca,
            distribuidora_id=distribuidora_id
        )
        
        result = business_logic.update_producto(producto)
        return redirect(url_for('productos'))
    else:
        producto_data = business_logic.get_producto(codigo_producto)
        return render_template('edit_producto.html', producto=producto_data)

@app.route('/delete_producto/<int:codigo_producto>', methods=['GET', 'POST'])
def delete_producto(codigo_producto):
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    if request.method == 'POST':
        producto = Producto(codigo_producto=codigo_producto)
        result = business_logic.delete_producto(producto)
        return redirect(url_for('productos'))
    else:
        producto_data = business_logic.get_producto(codigo_producto)
        return render_template('delete_producto.html', producto=producto_data)


@app.route('/email')
def email():
    return render_template('email.html')


@app.route('/send-email', methods=['POST'])
def send_email():
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    subject = request.form['subject']
    sender = request.form['sender']
    recipients = request.form['recipients'].split(',')
    body = request.form['body']
    attachments = request.files.getlist('attachments')

    if not sender or not recipients:
        return "Sender and recipients must be provided", 400

    email_data = Email(subject, sender, recipients, body, attachments)
    email_service.send_email(email_data)

    return redirect(url_for('email'))

@app.route('/home')
def home():
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    return render_template('index.html')

@app.route('/test-pdf')
def test_pdf():
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    return render_template('test_pdf.html')

@app.route('/create-test-employee')
def create_test_employee():
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login'))
    
    try:
        # Crear empleado de prueba
        empleado = Empleado(
            identificacion=1,
            nombre="Juan Pérez",
            correo="juan.perez@test.com",
            cargo="Desarrollador",
            salario=500000.0,
            seccion_tipo="TI",
            seccion_nombre="Desarrollo"
        )
        
        # Validar empleado
        empleado.validate()
        
        # Intentar insertar en la base de datos (puede fallar si ya existe)
        try:
            business_logic.data_access.insert_empleado(
                empleado.identificacion, empleado.nombre, empleado.correo, 
                empleado.cargo, empleado.salario, empleado.seccion_tipo, empleado.seccion_nombre
            )
            return "Empleado de prueba creado exitosamente"
        except Exception as e:
            return f"Empleado de prueba ya existe o error en BD: {str(e)}"
            
    except Exception as e:
        return f"Error al crear empleado de prueba: {str(e)}"



@app.route('/submit', methods=['POST'])
def submit():
    identificacion = int(request.form['identificacion'])
    nombre = request.form['nombre']
    correo = request.form['correo']
    cargo = request.form['cargo']
    salario = float(request.form['salario'])
    seccion_tipo = request.form['seccion_tipo']
    seccion_nombre = request.form['seccion_nombre']
    empleado = Empleado(
        identificacion=identificacion,
        nombre=nombre,
        correo=correo,
        cargo=cargo,
        salario=salario,
        seccion_tipo=seccion_tipo,
        seccion_nombre=seccion_nombre
    )

    result = business_logic.process_empleado(empleado)
    return render_template('result.html', result=result)

@app.route('/empleados')
def empleados():
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    all_empleado = business_logic.get_all_empleado()
    return render_template('empleados.html', empleados=all_empleado)

@app.route('/descargar')
def descargar():
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    all_empleado = business_logic.get_all_empleado()
    return render_template('descargar.html', empleados=all_empleado)

@app.route('/email/<int:identificacion>', methods=['GET'])
def mostrar_formulario_email(identificacion):
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    correo = business_logic.obtener_correo_empleado(identificacion)
    return render_template('email.html', correo=correo)
    
 
@app.route('/edit/<int:identificacion>', methods=['GET', 'POST'])
def edit_empleado(identificacion):
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    if request.method == 'POST':
        empleado = Empleado(
            identificacion=int(request.form['identificacion']),
            nombre=request.form['nombre'],
            correo=request.form['correo'],
            cargo=request.form['cargo'],
            salario=float(request.form['salario']),
            seccion_tipo=request.form['seccion_tipo'],
            seccion_nombre=request.form['seccion_nombre']
        )
        
        result = business_logic.update_empleado(empleado)
        return redirect(url_for('empleados'))
    else:
        empleado = business_logic.get_empleado(identificacion)
        return render_template('edit_empleado.html', empleado=empleado)

@app.route('/delete/<int:identificacion>', methods=['GET', 'POST'])
def delete_empleado(identificacion):
    if 'username' not in session or session.get('role', '').lower() != 'administrador':
        return redirect(url_for('login')) 
    if request.method == 'POST':
        empleado = Empleado(
            identificacion=identificacion,
            nombre=None,
            correo=None,
            cargo=None,
            salario=0,
            seccion_tipo=None,
            seccion_nombre=None
        )

        result = business_logic.delete_empleado(empleado)
        return redirect(url_for('empleados'))
    else:
        empleado = business_logic.get_empleado(identificacion)
        return render_template('delete_empleado.html', empleado=empleado)

@app.route('/download-pdf/<int:user_id>', methods=['GET', 'POST'])
def download_pdf(user_id):
    try:
        empleado = business_logic.get_empleado(user_id)
        if not empleado:
            return "Empleado no encontrado", 404
            
        pdf = business_logic.generate_payroll_pdf(empleado)
        now = datetime.now()
        timestamp = now.strftime('%Y%m%d_%H%M%S')
        
        filename = f'aporte_patronal_{empleado.identificacion}_{timestamp}.pdf'
        
        response = make_response(pdf.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    except Exception as e:
        return f"Error al generar PDF: {str(e)}", 500

@app.route('/download-pdf2/<int:user_id>', methods=['GET', 'POST'])
def download_pdf2(user_id):
    try:
        empleado = business_logic.get_empleado(user_id)
        if not empleado:
            return "Empleado no encontrado", 404
            
        pdf = business_logic.generate_payroll_pdf_trabajador(empleado)
        now = datetime.now()
        timestamp = now.strftime('%Y%m%d_%H%M%S')
        
        filename = f'nomina_trabajador_{empleado.identificacion}_{timestamp}.pdf'
        
        response = make_response(pdf.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        return response
    except Exception as e:
        return f"Error al generar PDF: {str(e)}", 500

@app.route('/view-pdf/<int:user_id>', methods=['GET', 'POST'])
def view_pdf(user_id):
    try:
        empleado = business_logic.get_empleado(user_id)
        if not empleado:
            return "Empleado no encontrado", 404
            
        pdf = business_logic.generate_payroll_pdf(empleado)
        
        response = make_response(pdf.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=aporte_patronal.pdf'
        return response
    except Exception as e:
        return f"Error al generar PDF: {str(e)}", 500

@app.route('/view-pdf2/<int:user_id>', methods=['GET', 'POST'])
def view_pdf2(user_id):
    try:
        empleado = business_logic.get_empleado(user_id)
        if not empleado:
            return "Empleado no encontrado", 404
            
        pdf = business_logic.generate_payroll_pdf_trabajador(empleado)
        
        response = make_response(pdf.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=nomina_trabajador.pdf'
        return response
    except Exception as e:
        return f"Error al generar PDF: {str(e)}", 500


###########################################################################################

@app.route('/empleado/productos')
def productos_empleado():
    if 'username' not in session or session.get('role', '').lower() != 'empleado':
        return redirect(url_for('login')) 
    all_productos = business_logic.get_all_productos()
    return render_template('productos_empleado.html', productos=all_productos)

@app.route('/empleado/producto/<int:codigo_producto>', methods=['GET'])
def view_producto_empleado(codigo_producto):
    if 'username' not in session or session.get('role', '').lower() != 'empleado':
        return redirect(url_for('login')) 
    producto = business_logic.get_producto(codigo_producto)
    if producto:
        return render_template('view_producto_empleado.html', producto=producto)
    else:
        return "Producto no encontrado", 404
    
@app.route('/empleado/add_producto', methods=['GET', 'POST'])
def add_producto_empleado():
    if 'username' not in session or session.get('role', '').lower() != 'empleado':
        return redirect(url_for('login')) 
    if request.method == 'POST':
        codigo_producto = int(request.form['codigo_producto'])
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        tipo = request.form['tipo']
        marca = request.form['marca']
        distribuidora_id = int(request.form['distribuidora_id'])
        
        producto = Producto(
            codigo_producto=codigo_producto,
            nombre=nombre,
            precio=precio,
            tipo=tipo,
            marca=marca,
            distribuidora_id=distribuidora_id
        )
        
        result = business_logic.process_producto(producto)
        return redirect(url_for('productos_empleado'))
    return render_template('add_producto_empleado.html')

@app.route('/empleado/consultar_producto', methods=['GET', 'POST'])
def consultar_producto_empleado():
    if 'username' not in session or session.get('role', '').lower() != 'empleado':
        return redirect(url_for('auth.login'))

    producto = None
    error = None
    all_productos = business_logic.get_all_productos()
    if request.method == 'POST':
        try:
            codigo_producto = int(request.form['codigo_producto'])
            producto_data = business_logic.get_productop(codigo_producto)
            if producto_data:
                producto = {
                    'nombre': producto_data['nombre'],
                    'precio': producto_data['precio']
                }
            else:
                error = "Producto no encontrado"
        except ValueError:
            error = "Código de producto no válido"
        except Exception as e:
            error = f"Error al consultar el producto: {str(e)}"

    return render_template('consultar_producto_empleado.html', producto=producto, error=error,productos=all_productos)


@app.route('/empleado/producto/<string:action>/<int:codigo_producto>', methods=['GET', 'POST'])
def producto_empleado(action, codigo_producto):
    if 'username' not in session or session.get('role', '').lower() != 'empleado':
        return redirect(url_for('login')) 

    producto = business_logic.get_producto(codigo_producto)

    if not producto:
        return "Producto no encontrado", 404

    if request.method == 'POST':
        if action == 'edit':
            nombre = request.form['nombre']
            precio = float(request.form['precio'])
            tipo = request.form['tipo']
            marca = request.form['marca']
            distribuidora_id = int(request.form['distribuidora_id'])

            producto_actualizado = Producto(
                codigo_producto=codigo_producto,
                nombre=nombre,
                precio=precio,
                tipo=tipo,
                marca=marca,
                distribuidora_id=distribuidora_id
            )
            result = business_logic.update_producto(producto_actualizado)
            return redirect(url_for('productos_empleado'))

        elif action == 'delete':

            producto_a_eliminar = Producto(codigo_producto=codigo_producto)
            result = business_logic.delete_producto(producto_a_eliminar)
            return redirect(url_for('productos_empleado'))

    if action == 'view':
        return render_template('producto_empleado_action.html', producto=producto)
    elif action == 'edit':
        return render_template('producto_empleado_action.html', action='edit', producto=producto)
    elif action == 'delete':
        return render_template('producto_empleado_action.html', action='delete', producto=producto)
    else:
        return "Acción no válida", 400

@app.route('/empleado/distribuidoras')
def distribuidoras_empleado():
    if 'username' not in session or session.get('role', '').lower() != 'empleado':
        return redirect(url_for('login'))
    all_distribuidoras = business_logic.get_all_distribuidoras()
    return render_template('distribuidoras_empleado.html', distribuidoras=all_distribuidoras)


@app.route('/empleado/add_distribuidora', methods=['GET', 'POST'])
def add_distribuidora_empleado():
    if 'username' not in session or session.get('role', '').lower() != 'empleado':
        return redirect(url_for('login')) 
    if request.method == 'POST':
        try:

            identificacion = int(request.form['identificacion'])
        except ValueError:
            return "La identificación debe ser un número entero válido.", 400
        
        nombre = request.form['nombre']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        distribuidora = Distribuidora(
            identificacion=identificacion,
            nombre=nombre,
            direccion=direccion,
            telefono=telefono
        )
        
        try:
            result = business_logic.process_distribuidora(distribuidora)
            return redirect(url_for('distribuidoras_empleado'))
        except ValueError as e:
            return str(e), 400
    return render_template('add_distribuidora_empleado.html')

@app.route('/empleado/distribuidora/<string:action>/<int:identificacion>', methods=['GET', 'POST'])
def distribuidora_empleado(action, identificacion):
    if 'username' not in session or session.get('role', '').lower() != 'empleado':
        return redirect(url_for('login'))

    distribuidora = business_logic.get_distribuidora(identificacion)

    if not distribuidora:
        return "Distribuidora no encontrada", 404

    if request.method == 'POST':
        if action == 'edit':
            nombre = request.form['nombre']
            direccion = request.form['direccion']
            telefono = request.form['telefono']

            distribuidora_actualizada = Distribuidora(
                identificacion=identificacion,
                nombre=nombre,
                direccion=direccion,
                telefono=telefono
            )
            try:
                result = business_logic.update_distribuidora(distribuidora_actualizada)
                return redirect(url_for('distribuidoras_empleado'))
            except ValueError as e:
                return str(e), 400

        elif action == 'delete':
            try:
                result = business_logic.delete_distribuidora(identificacion)
                return redirect(url_for('distribuidoras_empleado'))
            except ValueError as e:
                return str(e), 400
    if action == 'view':
        return render_template('distribuidora_empleado_action.html', action='view', distribuidora=distribuidora)
    elif action == 'edit':
        return render_template('distribuidora_empleado_action.html', action='edit', distribuidora=distribuidora)
    elif action == 'delete':
        return render_template('distribuidora_empleado_action.html', action='delete', distribuidora=distribuidora)
    else:
        return "Acción no válida", 400
