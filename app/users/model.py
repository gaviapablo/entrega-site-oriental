from ..extensions import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(40),unique=True,nullable=False)
    senha = db.Column(db.String(50),nullable=False)


    def json(self):
        return {
            "nome" : self.nome,
            "email" : self.email, 
            "senha" : self.senha
        }