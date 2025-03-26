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
from flask import Flask, render_template, request, jsonify, redirect, url_for
import database as dbase  # Importa el módulo de conexión

db = dbase.dbConnection()  # Conectar a la base de datos
cursor = db.cursor()  

app = Flask(__name__)

# Página principal
@app.route('/')
def home():
    cursor.execute("SELECT nombre_producto, precio, cantidad, descripcion FROM Inventario")  # Nombres de columnas corregidos
    productsReceived = cursor.fetchall()
    return render_template('index.html', products=productsReceived)

# Agregar producto (POST)
@app.route('/products', methods=['POST'])
def add_products():
    nombre_producto = request.form.get('name')  # Cambiado 'name' a 'nombre_producto'
    precio = request.form.get('price')  # Cambiado 'price' a 'precio'
    cantidad = request.form.get('quantity')  # Cambiado 'quantity' a 'cantidad'
    descripcion = request.form.get('description')  # Cambiado 'description' a 'descripcion'

    if nombre_producto and precio and cantidad:
        cursor.execute("INSERT INTO Inventario (nombre_producto, precio, cantidad, descripcion) VALUES (?, ?, ?, ?)", 
                       (nombre_producto, precio, cantidad, descripcion))  # Nombres de columnas corregidos
        db.commit()  # Guardar cambios en la BD
        return redirect(url_for('home'))
    else:
        return notFound()

# Eliminar producto (DELETE)
@app.route('/delete/<string:product_name>')
def delete_product(product_name):
    cursor.execute("DELETE FROM Inventario WHERE nombre_producto = ?", (product_name,))  # Nombre de columna corregido
    db.commit()
    return redirect(url_for('home'))

# Editar producto (PUT)
@app.route('/edit/<string:product_name>', methods=['POST'])
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