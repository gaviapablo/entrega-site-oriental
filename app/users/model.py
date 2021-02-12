from sqlalchemy.orm import backref
from ..extensions import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(40),unique=True,nullable=False)
    password_hash = db.Column(db.String(200),nullable=False)
    estado = db.Column(db.String(20),nullable=False)
    cidade = db.Column(db.Text,nullable=False)
    cep = db.Column(db.Integer)
    endereço = db.Column(db.Text,nullable=False)
    bloco_apartamento = db.Column(db.Text,nullable=False)

    compras = db.relationship('Compra',backref='user')


    def json(self):
        return {
            "nome" : self.nome,
            "email" : self.email,
            "estado": self.estado,
            "cidade": self.cidade,
            "cep": self.cep,
            "endereço": self.endereço,
            "bloco_apartamento": self.bloco_apartamento,
            "compras": self.compras
        }