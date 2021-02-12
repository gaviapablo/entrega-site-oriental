from ..extensions import db
from ..users.model import User 


class Compra(db.Model):
    __tablename__ = 'compra'
    id = db.Column(db.Integer,primary_key=True)
    preço = db.Column(db.Float)
    
    produtos = db.relationship('Produto')
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def json(self):
        return {
            "id" : self.id, 
            "produtos": self.produtos,
            "user": self.user_id
        }