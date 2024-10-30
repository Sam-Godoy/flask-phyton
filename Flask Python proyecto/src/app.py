from flask import Flask, render_template, request, redirect, url_for, abort
from dotenv import load_dotenv
import os
from flask_pymongo import PyMongo
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

# Configuración de MongoDB
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

# Función de conexión a la base de datos
def dbConnection():
    try:
        client = MongoClient(app.config['MONGO_URI'])
        db = client["dbb_products_app"]
    except Exception as e:
        print('Error de conexión con la base de datos:', e)
    return db

db = dbConnection()

# Ruta principal
@app.route('/')
def home():
    products = db['products']
    products_received = products.find()

    # Calcular la calificación promedio para cada producto
    products_with_ratings = []
    for product in products_received:
        reviews = product.get("reviews", [])
        if reviews:
            avg_rating = sum([review["rating"] for review in reviews]) / len(reviews)
            product["avg_rating"] = round(avg_rating, 2)  # Calificación promedio redondeada a 2 decimales
        else:
            product["avg_rating"] = None  # Sin calificación si no hay reseñas
        products_with_ratings.append(product)

    return render_template('index.html', products=products_with_ratings)

# Ruta para agregar un producto
@app.route('/products', methods=['POST'])
def addProduct():
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
        product = {
            'name': name,
            'price': price,
            'quantity': quantity,
            'reviews': []  # Lista de reseñas vacía al crear un nuevo producto
        }
        products.insert_one(product)
        return redirect(url_for('home'))
    else:
        return abort(404)

# Ruta para eliminar un producto
@app.route('/delete/<string:product_name>')
def delete(product_name):
    products = db['products']
    products.delete_one({'name': product_name})
    return redirect(url_for('home'))

# Ruta para editar un producto
@app.route('/edit/<string:product_name>', methods=['POST'])
def edit(product_name):
    products = db['products']
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']

    if name and price and quantity:
        products.update_one({'name': product_name}, {'$set': {'name': name, 'price': price, 'quantity': quantity}})
        return redirect(url_for('home'))
    else:
        return abort(404)

# Ruta para agregar una reseña
@app.route('/rate/<string:product_name>', methods=['POST'])
def rate(product_name):
    products = db['products']
    rating = int(request.form['rating'])
    comment = request.form['comment']

    if 1 <= rating <= 5 and comment:
        review = {
            "rating": rating,
            "comment": comment
        }
        products.update_one({'name': product_name}, {'$push': {'reviews': review}})
        return redirect(url_for('home'))
    else:
        return abort(400)

if __name__ == '__main__':
    app.run(debug=True)
