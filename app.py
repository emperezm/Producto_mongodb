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


