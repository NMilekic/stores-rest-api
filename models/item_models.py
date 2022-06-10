from db import db
from models.store_models import StoreModel


class ItemModel(db.Model):
    from models.store_models import Item_Store
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float(precision=2))
    unit_of_m = db.Column(db.String(10))
    # quantity = db.Column(db.Float(precision=2))

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('CategoryModel')
    stock = db.relationship('Item_Store', backref='item', primaryjoin=id == Item_Store.item_id)

    def __init__(self, name, price, unit_of_m, category_id):
        self.name = name
        self.price = price
        self.unit_of_m = unit_of_m
        # self.quantity = quantity
        self.category_id = category_id

    def json(self, quantity=None):
        if quantity:
            return {
                'name': self.name,
                'category': self.category.name,
                'price': self.price,
                'quantity': quantity,
                'unit_of_m': self.unit_of_m
            }
        return {
            'name': self.name,
            'category': self.category.name,
            'price': self.price,
            'unit_of_m': self.unit_of_m
        }

    def json_item_stores(self):
        store_arr = []
        for delivery in self.stock:
            store = StoreModel.find_by_id(id=delivery.store_id)
            store_arr.append({'store_name': store.name,
                              'quantity': delivery.quantity,
                              'unit_of_m': self.unit_of_m
                              })
        return {'item': self.name,
                'category': self.category.name,
                'stores': store_arr}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
