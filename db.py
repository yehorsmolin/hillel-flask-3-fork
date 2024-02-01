from peewee import SqliteDatabase, Model, CharField, FloatField, ForeignKeyField, BooleanField, ManyToManyField
import logging


db = SqliteDatabase('db.sqlite')


logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)


class Category(Model):
    name = CharField()
    is_adult_only = BooleanField(default=False)

    # products = ...

    class Meta:
        database = db
        table_name = 'categories'


class Tag(Model):
    name = CharField()

    class Meta:
        database = db
        table_name = 'tags'


# Class is a Table in DB (model)
class Product(Model):
    # id INTEGER PRIMARY KEY
    # name TEXT
    # price REAL

    # Fields are columns in DB
    name = CharField()
    price = FloatField()
    category = ForeignKeyField(Category, backref='products')
    tags = ManyToManyField(Tag, backref='products')

    class Meta:
        database = db
        table_name = 'products'


def get_products(name_filter=None):
    # Get all products
    query = Product.select(
        Product, Category
    ).join(Category).order_by(-Product.name)

    if name_filter is not None:
        query = query.where(Product.name == name_filter)

    return query


def get_product(product_id):
    # Get product by id
    return Product.get_by_id(product_id)


def create_product(name, price, category_id):
    # Create product and return prudct id
    return Product.create(name=name, price=price, category_id=category_id)


def update_product(product_id, name, price, category_id):
    # Update product
    product = Product.get_by_id(product_id)

    if name is not None:
        product.name = name

    if price is not None:
        product.price = price

    if category_id is not None:
        product.category_id = category_id

    product.save()

    return product


def delete_product(product_id):
    # Delete product
    product = Product.get_by_id(product_id)

    product.delete_instance()


if __name__ == '__main__':
    cocacola = Product.get(Product.name == 'Coca-Cola')

    tag = Tag.create(name='Ціна тижня')
    another_tag = Tag.create(name='Новинка')

    cocacola.tags.add(tag)
    cocacola.tags.add(another_tag)
    cocacola.save()
