from flask_restful import Resource, reqparse

from models.store_models import StoreModel, Item_Store
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

        return store.json(), 200

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            try:
                store.delete_from_db()
            except:
                return {'message': 'An error occurred deleting the item.'}, 500
            return {'message': 'Item deleted'}, 200

        return {'message': 'Item not exist'}, 400


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
    parser.add_argument('quantity',
                        type=int,
                        required=False)
    def post(self):
        data = Assortment.parser.parse_args()
        store = StoreModel.find_by_name(data['name'])
        item = ItemModel.find_by_name(data['item'])

        if not store:
            return {'message': f"An store with name '{data['name']}' doesn't exist."}, 400
        elif not item:
            return {'message': f"An item with name '{data['item']}' doesn't exist."}, 400
        elif item.id in [delivery.item_id for delivery in store.stock]:
            return {'message': f"The item '{data['item']}' is already in '{data['name']}'."}, 400

        try:
            store.insert_item_in_store(item, data['quantity'])
        except:
            return {'message': 'An error occurred inserting the item.'}, 500

        return item.json(data['quantity']), 201


    def delete(self):
        data = Assortment.parser.parse_args()
        store = StoreModel.find_by_name(data['name'])
        item = ItemModel.find_by_name(data['item'])

        if not store:
            return {'message': f"An store with name '{data['name']}' doesn't exist."}, 400
        elif not item:
            return {'message': f"An item with name '{data['item']}' doesn't exist."}, 400
        elif item.id in [delivery.item_id for delivery in store.stock]:
            try:
                store.delete_item_from_store(item)
            except:
                return {'message': 'An error occurred inserting the item.'}, 500
            return {'message': f"Item with name '{data['item']}' removed from store '{data['name']}'."}, 200

        return {'message': f"Item with name '{data['item']}' isn't in store '{data['name']}'."}, 400

    def patch(self):
        data = Assortment.parser.parse_args()
        store = StoreModel.find_by_name(data['name'])
        item = ItemModel.find_by_name(data['item'])
        if not store:
            return {'message': f"An store with name '{data['name']}' doesn't exist."}, 400
        elif not item:
            return {'message': f"An item with name '{data['item']}' doesn't exist."}, 400

        delivery = Item_Store.query.filter_by(item_id=item.id).filter_by(store_id=store.id).first()
        if not delivery:
            return {'message': f"An item with name '{data['item']}' doesn't in store '{data['name']}'."}, 400
        delivery.quantity = data['quantity']

        try:
            delivery.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500
        return item.json(data['quantity']), 200
