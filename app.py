'''
from flask import Flask, render_template,request,Response,jsonify,redirect,url_for
import database as dbase
from product import Product

db =dbase.dbConnection()

app = Flask(__name__)

#Rutas de la aplicación
@app.route('/')
def home():
    products=db['products']
    productsReceived=products.find()
    return render_template('index.html',products=productsReceived)

#Method Post
@app.route('/products', methods=['POST'])
def add_products(): #cambio
    products=db['products'] 
    name = request.form.get('name')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    description = request.form.get('description')

    if name and price and quantity:
        product = Product(name, price, quantity,description)
        products.insert_one(product.toDBCollection())
        Response=jsonify({
            'name': name,
            'price': price,
            'quantity': quantity,
            'description': description})

        return redirect(url_for('home'))
    else: 
        return notFound()
    
#Method delete
@app.route('/delete/<string:product_name>')
def delete_product(product_name):
    products=db['products']
    products.delete_one({'name': product_name})
    return redirect(url_for('home'))
    
#Method Put
@app.route('/edit/<string:product_name>', methods=['POST'])
def edit_product(product_name):
    products=db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    description = request.form['description']

    if name and price and quantity:
        products.update_one({'name': product_name}, {'$set': {'name': name, 'price': price, 'quantity': quantity, 'description': description}})
        Response=jsonify({'message': 'producto'+ product_name + 'actualizado correctamente'})
        return redirect(url_for('home'))
    else:
        return notFound()
    
@app.errorhandler(404)
def notFound(error=None):
    message = {
        'message': 'No encontrado' + request.url,
        'status': '404 Not Found'
    }
    Response = jsonify(message)
    Response.status_code = 404
    return Response
    
if __name__ == '__main__':
    app.run(debug=True, port=4200)
'''
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import database as dbase  # Importa el módulo de conexión
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

db = dbase.dbConnection()  # Conectar a la base de datos
cursor = db.cursor()  
app = Flask(__name__)
app.secret_key = "ProyectoSENA25Abril"

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
            cursor = db.cursor()
            cursor.execute("SELECT id, username, password FROM Usuarios WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if user and check_password_hash(user[2], password):
                session['usuario_id'] = user[0]
                session['usuario_nombre'] = user[1]
                flash('Has iniciado sesión correctamente', 'success')
                return redirect(url_for('home'))
            else:
                flash('Usuario o contraseña incorrectos', 'danger')
                
        except Exception as e:
            flash(f'Error al intentar iniciar sesión: {e}', 'danger')
        finally:
            cursor.close()
            
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
            cursor = db.cursor()
            
            # Verificar si el usuario ya existe
            cursor.execute("SELECT id FROM Usuarios WHERE username = ?", (username,))
            if cursor.fetchone():
                flash('Este nombre de usuario ya está registrado', 'danger')
                return render_template('register.html')
                
            # Crear usuario nuevo
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO Usuarios (username, password) VALUES (?, ?)", 
                         (username, hashed_password))
            db.commit()
            flash('Cuenta creada correctamente, ahora puedes iniciar sesión', 'success')
            return redirect(url_for('login'))
                
        except Exception as e:
            flash(f'Error al registrar usuario: {e}', 'danger')
        finally:
            cursor.close()
            
    return render_template('register.html')

# Cerrar sesión
@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('login'))


# Página principal
@app.route('/')
def home():
    cursor.execute("SELECT nombre_producto, precio, cantidad, descripcion FROM Inventario")  # Nombres de columnas corregidos
    productsReceived = cursor.fetchall()
    return render_template('index.html', products=productsReceived)

# Agregar producto (POST)
@app.route('/products', methods=['POST'])
@login_required
def add_products():
    nombre_producto = request.form.get('nombre_producto')  # Debe coincidir con el HTML
    precio = request.form.get('precio')
    cantidad = request.form.get('cantidad')
    descripcion = request.form.get('descripcion')

    if nombre_producto and precio and cantidad:
        cursor.execute("INSERT INTO Inventario (nombre_producto, precio, cantidad, descripcion) VALUES (?, ?, ?, ?)",
                       (nombre_producto, precio, cantidad, descripcion))  # Nombres de columnas corregidos
        db.commit()  # Guardar cambios en la BD
        return redirect(url_for('home'))
    else:
        return notFound()

# Eliminar producto (DELETE)
@app.route('/delete/<string:product_name>')
@login_required
def delete_product(product_name):
    cursor.execute("DELETE FROM Inventario WHERE nombre_producto = ?", (product_name,))  # Nombre de columna corregido
    db.commit()
    return redirect(url_for('home'))

# Editar producto (PUT)
@app.route('/edit/<string:product_name>', methods=['POST'])
@login_required
def edit_product(product_name):
    nombre_producto = request.form.get('name')  
    precio = request.form.get('price')  
    cantidad = request.form.get('quantity')  
    descripcion = request.form.get('description')  

    if nombre_producto and precio and cantidad:
        cursor.execute("UPDATE Inventario SET nombre_producto = ?, precio = ?, cantidad = ?, descripcion = ? WHERE nombre_producto = ?", 
                       (nombre_producto, precio, cantidad, descripcion, product_name))  # Nombres de columnas corregidos
        db.commit()
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