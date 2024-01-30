from flask import Flask, request

from db import get_products, create_product, update_product, delete_product
from exceptions import ValidationError
from serializers import serialize_product
from deserializers import deserialize_product

app = Flask(__name__)


@app.route('/hello_world')
def hello_world():
    # Return hello world
    return "Hello, World!"


@app.route('/products', methods=['GET', 'POST'])
def products_api():
    if request.method == "GET":
        name_filter = request.args.get('name')

        products = get_products(name_filter)

        # Convert products to list of dicts
        products_dicts = [
            serialize_product(product)
            for product in products
        ]

        # Return products
        return products_dicts
    if request.method == "POST":
        # Create a product
        product = deserialize_product(request.get_json())

        # Return success
        return serialize_product(product), 201


@app.route('/products/<int:product_id>', methods=['PUT', 'PATCH', 'DELETE'])
def product_api(product_id):
    if request.method == "PUT":
        # Update a product
        product = deserialize_product(request.get_json(), product_id)
        # Return success
        return serialize_product(product)
    if request.method == "PATCH":
        # Update a product
        product = deserialize_product(request.get_json(), product_id, partial=True)
        # Return success
        return serialize_product(product)
    if request.method == "DELETE":
        delete_product(product_id)

        return "", 204


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return {
        'error': str(e)
    }, 422


if __name__ == '__main__':
    app.run(debug=True, port=5001)
