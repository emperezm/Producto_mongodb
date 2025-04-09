from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import database as dbase
from product import Product

# Conectar a la base de datos
db = dbase.dbConnection()
app = Flask(__name__)
app.secret_key = "ProyectoSENA25Abril"

# Decorador para requerir login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Por favor inicia sesión para acceder', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Por favor completa todos los campos', 'danger')
            return render_template('login.html')
        
        try:
            # Buscar usuario en MongoDB
            usuarios = db['usuarios']
            user = usuarios.find_one({"username": username})
            
            if user and check_password_hash(user["password"], password):
                session['usuario_id'] = str(user["_id"])
                session['usuario_nombre'] = user["username"]
                flash('Has iniciado sesión correctamente', 'success')
                return redirect(url_for('home'))
            else:
                flash('Usuario o contraseña incorrectos', 'danger')
                
        except Exception as e:
            flash(f'Error al intentar iniciar sesión: {e}', 'danger')
            
    return render_template('login.html')

# Registro de usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        if not username or not password or not password_confirm:
            flash('Por favor completa todos los campos', 'danger')
            return render_template('register.html')
            
        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('register.html')
        
        try:
            # Verificar si el usuario ya existe
            usuarios = db['usuarios']
            existing_user = usuarios.find_one({"username": username})
            if existing_user:
                flash('Este nombre de usuario ya está registrado', 'danger')
                return render_template('register.html')
                
            # Crear usuario nuevo
            hashed_password = generate_password_hash(password)
            new_user = {
                "username": username,
                "password": hashed_password
            }
            usuarios.insert_one(new_user)
            
            flash('Cuenta creada correctamente, ahora puedes iniciar sesión', 'success')
            return redirect(url_for('login'))
                
        except Exception as e:
            flash(f'Error al registrar usuario: {e}', 'danger')
            
    return render_template('register.html')

# Cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))

# Página principal
@app.route('/')
@login_required
def home():
    products = db['products']
    productsReceived = products.find()
    return render_template('index.html', products=productsReceived, user=session.get('usuario_nombre'))

# Agregar producto (POST)
@app.route('/products', methods=['POST'])
@login_required
def add_products():
    products = db['products']
    nombre_producto = request.form.get('nombre_producto')
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')
    descripcion = request.form.get('descripcion')

    if nombre_producto and precio and cantidad:
        try:
            product = {
                "nombre_producto": nombre_producto,
                "precio": float(precio),
                "cantidad": int(cantidad),
                "descripcion": descripcion
            }
            products.insert_one(product)
            flash('Producto agregado correctamente', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Error al agregar producto: {e}', 'danger')
            return redirect(url_for('home'))
    else:
        return notFound()

# Eliminar producto
@app.route('/delete/<string:product_name>')
@login_required
def delete_product(product_name):
    try:
        products = db['products']
        result = products.delete_one({"nombre_producto": product_name})
        if result.deleted_count > 0:
            flash('Producto eliminado correctamente', 'success')
        else:
            flash('No se encontró el producto a eliminar', 'warning')
        return redirect(url_for('home'))
    except Exception as e:
        flash(f'Error al eliminar producto: {e}', 'danger')
        return redirect(url_for('home'))

# Editar producto
@app.route('/edit/<string:product_name>', methods=['POST'])
@login_required
def edit_product(product_name):
    products = db['products']
    nombre_producto = request.form.get('nombre_producto')
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')
    descripcion = request.form.get('descripcion')

    if nombre_producto and precio and cantidad:
        try:
            products.update_one(
                {"nombre_producto": product_name},
                {"$set": {
                    "nombre_producto": nombre_producto,
                    "precio": float(precio),
                    "cantidad": int(cantidad),
                    "descripcion": descripcion
                }}
            )
            flash('Producto actualizado correctamente', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Error al actualizar producto: {e}', 'danger')
            return redirect(url_for('home'))
    else:
        return notFound()

# Página de error 404
@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado: ' + request.url,
        'status': '404 Not Found'
    }
    response = jsonify(message)
    response.status_code = 404
    return response

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(debug=True, port=4200)