from flask_restful import Resource, reqparse

from models.item_models import ItemModel

class Item(Resource):
    # PARSER SETTINGS
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='You must enter price.')
    parser.add_argument('unit_of_m',
                        type=str,
                        required=False,
                        help='You must enter unit of measure.')
    # parser.add_argument('quantity',
    #                     type=float,
    #                     required=True,
    #                     help='You must enter quantity.')
    parser.add_argument('category_id',
                        type=int,
                        required=False,
                        help='You must enter category.')

    # CRUD
    def post(self, name):
        data = Item.parser.parse_args()

        if ItemModel.find_by_name(name):
            return {'message': f"An item with name '{name}' already exist."}, 400

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500

        return item.json(), 201

    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def put(self, name):
        data = Item.parser.parse_args()
        print(data)

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred updating the item.'}, 500

        return item.json(), 200

    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            try:
                item.delete_from_db()
            except:
                return {'message': 'An error occurred deleting the item.'}, 500
            return {'message': 'Item deleted'}, 200

        return {'message': 'Item not exist'}, 400


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}


class ItemStoreList(Resource):
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json_item_stores()
        return {'message': 'Item not found'}, 404



