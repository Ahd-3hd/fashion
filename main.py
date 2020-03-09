import os
from flask import Flask, jsonify, request, render_template
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
@app.route('/product/', methods=['POST', 'GET', 'DELETE', 'PUT'])
def create_product():
    # post a product
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        price = request.form['price']
        get_image = request.files['image']
        image = cloudinary.uploader.upload(get_image)['url']
        ########
        # POSTED DATA SCHEMA:
        # FORM-DATA KEY:VALUE
        #TITLE = STRING
        #DESC = STRING
        #PRICE = INT
        #IMAGE = FILE
        ########
        new_product = Product(title=title, desc=desc, price=price, image=image)
        db.session.add(new_product)
        db.session.commit()
        product_schema = ProductSchema()
        output = product_schema.dump(new_product)

        return jsonify(output)
    # query a single product
    if request.method == 'GET':
        id = request.args.get('id')
        product = Product.query.get(id)
        product_schema = ProductSchema()
        output = product_schema.dump(product)
        return jsonify(output)
    # query a single product then delete it from the db
    if request.method == 'DELETE':
        id = request.args.get('id')
        to_be_deleted = Product.query.get(id)
        db.session.delete(to_be_deleted)
        db.session.commit()
        return f'PRODUCT with the id = {id} has been deleted'

    # query a single product then update it with new data
    if request.method == 'PUT':
        id = request.args.get('id')
        updated = Product.query.get(id)
        updated.title = request.form['title']
        updated.desc = request.form['desc']
        updated.price = request.form['price']
        get_image = request.files['image']
        updated.image = cloudinary.uploader.upload(get_image)['url']
        db.session.merge(updated)
        db.session.flush()
        db.session.commit()

        return 'done'

        # {
        #     "desc": "from post man",
        #     "id": 2,
        #     "image": "http://res.cloudinary.com/ahd3hd/image/upload/v1583778474/nqdb3jkfnfiaohumz9yl.png",
        #     "price": 5,
        #     "title": "postman"
        # }

# get all products route
@app.route('/')
def index():
    all_products = Product.query.all()
    product_schema = ProductSchema(many=True)
    output = product_schema.dump(all_products)
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True)
