from ..extensions import db



class Compra(db.Model):
    __tablename__ = 'compra'
    id = db.Column(db.Integer,primary_key=True)
    preço = db.Column(db.Float)
    
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'))
    produto = db.relationship("Produto")
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def json(self):
        return {
            "id" : self.id, 
            "produtos": self.produtos,
            "user": self.user_id
        }