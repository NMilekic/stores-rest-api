from db import db

store_item = db.Table('store_item',
                      db.Column('store_id', db.Integer, db.ForeignKey('stores.id'), primary_key=True),
                      db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True)
                      )

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    address = db.Column(db.String(30))
    phone = db.Column(db.String(20))

    items = db.relationship('ItemModel', secondary=store_item, backref='stores')

    def __repr__(self):
        return f'<Store: {self.name}>'

    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def json(self):
        return {
            'store_id': self.id,
            'store_name': self.name,
            'store_phone': self.phone,
            'store_assortment': [item.json() for item in self.items]
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def insert_item_in_store(self, item):
        self.items.append(item)
        db.session.commit()

    def delete_item_from_store(self, item):
        self.items.remove(item)
        db.session.commit()