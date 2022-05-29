from flask_restful import Resource, reqparse

from models.category_models import CategoryModel


class Category(Resource):
    # PARSER SETTINGS
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='You must enter name of category.')

    # CRUD
    def get(self, name):
        category = CategoryModel.find_by_name(name)
        if category:
            return category.json()
        return {'message': 'Item not found'}, 404


    def delete(self, name):
        category = CategoryModel.find_by_name(name)

        if category:
            try:
                category.delete_from_db()
            except:
                return {'message': 'An error occurred deleting the item.'}, 500
            return {'message': 'Item deleted'}

        return {'message': 'Item not exist'}


class CategoryList(Resource):
    def get(self):
        return {'categores': [category.json() for category in CategoryModel.query.all()]}

    def post(self):
        data = Category.parser.parse_args()

        if CategoryModel.find_by_name(data['name']):
            return {'message': f"An category with name '{data['name']}' already exist."}, 400

        category = CategoryModel(data['name'])

        try:
            category.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500

        return category.json(), 201

