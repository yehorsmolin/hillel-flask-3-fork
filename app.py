from flask import Flask, request

from db import get_products, create_product, update_product, delete_product, Product, get_product, get_categories, \
get_category, create_category, update_category, delete_category
from exceptions import ValidationError
from serializers import serialize_product, serialize_category
from deserializers import deserialize_product, deserialize_category

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


@app.route('/products/<int:product_id>', methods=['PUT', 'PATCH', 'DELETE', "GET"])
def product_api(product_id):
    if request.method == "GET":
        # Get a product
        product = get_product(product_id)

        # Return product
        return serialize_product(product)
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


@app.route('/categories', methods=['GET', 'POST'])
def categories_api():
    if request.method == "GET":
        name_filter = request.args.get('name')
        categories = get_categories(name_filter)

        if not categories:
            return "There are no categories available.", 404

        else:
            # Convert categories to list of dicts
            categories_dicts = [
                serialize_category(category)
                for category in categories
            ]

        # Return categories
        return categories_dicts

    elif request.method == "POST":
        # Create a category
        category = deserialize_category(request.get_json())

        # Return success
        return serialize_category(category), 201


@app.route('/categories/<int:category_id>', methods=['PUT', 'PATCH', 'DELETE', "GET"])
def category_api(category_id):
    if request.method == "GET":
        # Get a category by id
        category = get_category(category_id)

        if not category:
            return "There is no such category available.", 404

        else:
            # Return category by id
            return serialize_category(category), 200

    elif request.method == "PUT":
        # Update a category
        category = deserialize_category(request.get_json(), category_id)
        # Return success
        return serialize_category(category), 201

    elif request.method == "PATCH":
        # Update a category
        category = deserialize_category(request.get_json(), category_id, partial=True)
        # Return success
        return serialize_category(category), 200

    elif request.method == "DELETE":
        delete_category(category_id)

        return "The category was deleted.", 204

    else:
        return "Method not allowed.", 405


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return {
        'error': str(e)
    }, 422


@app.errorhandler(Product.DoesNotExist)
def handle_does_not_exist_error(e):
    return {
        'error': 'Product does not exist'
    }, 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)
