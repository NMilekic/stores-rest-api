import os

from flask import Flask
from flask_restful import Api

from db import db
from resources.item_resources import Item, ItemList, ItemStoreList
from resources.category_resources import Category, CategoryList
from resources.store_resources import Store, StoreList, Assortment


# FLASK APP
app = Flask(__name__)

# CONNECTION TO DATABASE
uri = os.getenv("DATABASE_URL")  # or other relevant config var
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
else:
    uri = 'sqlite:///data.db'

app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# API OBJECT
api = Api(app)

# CREATE TABLES
@app.before_first_request
def create_tables():
    db.create_all()

# API ROUTE
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Category, '/category/<string:name>')
api.add_resource(CategoryList, '/categories')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Assortment, '/stores/item')
api.add_resource(ItemStoreList, '/item/stores/<string:name>')

# APP RUN
if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
