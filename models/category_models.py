from db import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    items = db.relationship('ItemModel')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {
            'category_id': self.id,
            'name': self.name,
            'items': [item.name for item in self.items]
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

