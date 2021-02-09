from ..extensions import db


class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(50),unique=True,nullable=False)
    preço = db.Column(db.Float)
    estoque = db.Column(db.Integer,unique=True)


    def json(self):
        return {
            "nome" : self.nome, 
            "preço" : self.preço,
            "estoque" : self.estoque,
        }

    