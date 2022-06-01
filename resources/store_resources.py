from flask_restful import Resource, reqparse

from models.store_models import StoreModel
from models.item_models import ItemModel

class Store(Resource):
    # PARSER SETTINGS
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='You must enter Store name.')
    parser.add_argument('address',
                        type=str,
                        required=True,
                        help='You must enter Store address.')
    parser.add_argument('phone',
                        type=str,
                        required=True,
                        help='You must enter Store number.')

    # CRUD
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Item not found'}, 404

    def put(self, name):
        data = Store.parser.parse_args()

        store = StoreModel.find_by_name(name)

        if store is None:
            store = StoreModel(name, **data)
        else:
            store.address = data['address']
            store.phone = data['phone']

        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred updating the item.'}, 500

        return store.json()

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            try:
                store.delete_from_db()
            except:
                return {'message': 'An error occurred deleting the item.'}, 500
            return {'message': 'Item deleted'}

        return {'message': 'Item not exist'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}

    def post(self):
        data = Store.parser.parse_args()
        if StoreModel.find_by_name(data['name']):
            return {'message': f"An store with name '{data['name']}' already exist."}, 400

        store = StoreModel(**data)

        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500

        return store.json(), 201


class Assortment(Resource):
    # PARSER SETTINGS
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='You must enter Store name.')
    parser.add_argument('item',
                        type=str,
                        required=True,
                        help='You must enter item that add in store.')
    def post(self):
        data = Assortment.parser.parse_args()
        store = StoreModel.find_by_name(data['name'])
        if not store:
            return {'message': f"An store with name '{data['name']}' doesn't exist."}, 400
        elif data['item'] in [item.name for item in store.items]:
            return {'message': f"The item '{data['item']}' is already in '{data['name']}'."}, 400

        item = ItemModel.find_by_name(data['item'])
        if item:
            try:
                store.insert_item_in_store(item)
            except:
                return {'message': 'An error occurred inserting the item.'}, 500
            return item.json(), 201

        return {'message': f"Item with name '{data['item']}' doesn't exist."}

    def delete(self):
        data = Assortment.parser.parse_args()
        store = StoreModel.find_by_name(data['name'])
        if not store:
            return {'message': f"An store with name '{data['name']}' doesn't exist."}, 400
        elif data['item'] in [item.name for item in store.items]:
            item = ItemModel.find_by_name(data['item'])
            try:
                store.delete_item_from_store(item)
            except:
                return {'message': 'An error occurred inserting the item.'}, 500

            return {'message': f"Item with name '{data['item']}' removed from store '{data['name']}'."}

        return {'message': f"Item with name '{data['item']}' isn't in store '{data['name']}'."}