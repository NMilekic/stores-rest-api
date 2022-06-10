from db import db


#store_item = db.Table('store_item',
#                      db.Column('store_id', db.Integer, db.ForeignKey('stores.id'), primary_key=True),
#                      db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True)
#                      )

class Item_Store(db.Model):
    __tablename__ = 'item_store'
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), primary_key=True)
    quantity = db.Column(db.Float(precision=2))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    address = db.Column(db.String(30))
    phone = db.Column(db.String(20))

    stock = db.relationship('Item_Store', backref='store', primaryjoin=id == Item_Store.store_id)
#    items = db.relationship('ItemModel', secondary=store_item, backref='stores')

    def __repr__(self):
        return f'<Store: {self.name}>'

    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def json(self):
        from models.item_models import ItemModel
        item_arr = []
        for delivery in self.stock:
            item = ItemModel.find_by_id(id=delivery.item_id)
            item_arr.append(item.json(delivery.quantity))
        return {
            'store_id': self.id,
            'store_name': self.name,
            'store_phone': self.phone,
            'store_assortment': item_arr
            # 'store_assortment': [item.json() for item in self.stack]
        }

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

    def insert_item_in_store(self, item, quantity):
        # self.items.append(item)
        # db.session.commit()
        delivery = Item_Store(store_id=self.id, item_id=item.id, quantity=quantity)
        self.stock.append(delivery)
        item.stock.append(delivery)
        db.session.commit()

    def delete_item_from_store(self, item):
        # self.items.remove(item)
        # db.session.commit()
        delivery = Item_Store.query.filter_by(store_id=self.id).filter_by(item_id=item.id).first()
        db.session.delete(delivery)
        db.session.commit()

