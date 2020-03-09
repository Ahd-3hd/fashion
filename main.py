import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv


# config cloudinary

cloudinary.config(
    cloud_name=os.environ.get('CLOUD_NAME'),
    api_key=os.environ.get('API_KEY'),
    api_secret=os.environ.get('API_SECRET')
)
# initilize the flask app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///product.db'

# init the db
db = SQLAlchemy(app)

# init marshmallow => to get json responses

ma = Marshmallow(app)

# The Products Model


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(255), default="default.jpg")


# Create Marshmallow Schema

class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product


# create single product
@app.route('/product', methods=['POST'])
def create_product():
    title = request.json['title']
    desc = request.json['desc']
    price = request.json['price']
    image = cloudinary.uploader.upload('hii.png')['url']

    new_product = Product(title=title, desc=desc, price=price, image=image)
    db.session.add(new_product)
    db.session.commit()
    return 'done'

# get all products route
@app.route('/')
def index():
    all_products = Product.query.all()
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(all_products)
    return jsonify({'products': output})


if __name__ == '__main__':
    app.run(debug=True)
