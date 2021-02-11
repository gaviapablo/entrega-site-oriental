from flask import request, jsonify
from app.compras.model import Compra
from app.extensions import db
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


class ComprasDetails(MethodView):
    def get(self):
        compras = Compra.query.all() #pega todos os users de uma vez
        return jsonify([compra.json() for compra in compras]),200
    
    def post(self):
        dados = request.json #pega apenas o corpo da requisição, ou seja, o json, para poder fazer um POST desses dados

        produtos = dados.get('produtos')
        preço = dados.get('preço') #pega o nome que esta no formato json
        user_id = dados.get('user_id')
        
        if not produtos or not preço or not user_id:
            return {"error": "Produtos, preço e usuário obrigatórios!"},400

        if not isinstance(produtos,list) or not isinstance(preço,int):
            return {"error": "Algum tipo inserido é inválido!"},400

        compra = Compra(produtos=produtos,preço=preço,user_id=user_id)

        db.session.add(compra)
        db.session.commit()

        return compra.json(),200


class PaginaUser(MethodView):

    decorators = [jwt_required] #para saber se o usuario está logado para conseguir alterar seus dados, um token é necessario
                                #e então este decorator faz esta função


    def get(self,id):

        if get_jwt_identity() != id:
            return {"error":"Usuário não permitido"},400

        user = User.query.get_or_404(id) #verifica se existe, caso contrario retorna erro 404
        return user.json(),200
    
    def patch(self,id):

        if get_jwt_identity() != id:
            return {"error":"Usuário não permitido"},400

        user = User.query.get_or_404(id) #verifica se existe, caso contrario retorna erro 404
        dados = request.json

        nome = dados.get('nome',user.nome)
        email = dados.get('email',user.email)    #caso nada seja inputado para atualizar as informações de nome, o nome permanece o mesmo, ou seja, aluno.nome
        password = dados.get('password',user.password)
        estado = dados.get('estado',user.estado)
        cidade = dados.get('estado',user.cidade)
        cep = dados.get('estado',user.cep)
        endereço = dados.get('estado',user.endereço)
        bloco_apartamento = dados.get('estado',user.bloco_apartamento)

        #falta verificar tamanho e tipo dos dados que nem na primeira função
        

        if User.query.filter_by(email=email).first():
            return {"error": "Já existe um usuário cadastrado com este email!"},400
        
        if len(email)>40:
            return {"error": "String de email excede o tamanho de 40 caracteres!"},400
        
        if len(nome)>50:
            return {"error": "String de nome excede o tamanho de 50 caracteres!"},400

        if len(password)>200:
            return {"error": "String de senha excede o tamanho de 50 caracteres!"},400

        if len(estado)>20:
            return {"error": "String de estado excede o tamanho de 20 caracteres!"},400

        if not isinstance(email,str) or not isinstance(password,str) or not isinstance(nome,str) or not isinstance(estado,str) or not isinstance(cidade,str) or not isinstance(cep,int) or not isinstance(endereço,str) or not isinstance(bloco_apartamento,str):
            return {"error": "Algum tipo inserido é inválido!"},400
        
        
        password_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        
        user.nome = nome
        user.email = email
        user.password_hash = password_hash
        user.estado = estado
        user.cidade = cidade
        user.cep = cep
        user.endereço = endereço
        user.bloco_apartamento = bloco_apartamento

        db.session.add(user)
        db.session.commit()

        return user.json(),200 #retorna um json desse produto
    
    def delete(self,id):

        if get_jwt_identity() != id:
            return {"error":"Usuário não permitido"},400

        user = User.query.get_or_404(id) #verifica se existe, caso contrario retorna erro 404
        db.session.delete(user)
        db.session.commit()
        return jsonify([user.json() for user in User.query.all()]),200 #retorna um json contendo todos os produtos ainda existentes


class UserLogin(MethodView):
    def post(self):
        dados = request.json #pega apenas o corpo da requisição, ou seja, o json, para poder fazer um POST desses dados

        email = dados.get('email') #pega o nome que esta no formato json
        password = dados.get('password')

        user = User.query.filter_by(email=email).first()

        if user is None or not bcrypt.checkpw(password.encode(),user.password_hash):
            return {"error": "Usuário ou senha incorretos!"},400

        token = create_access_token(identity=user.id)

        return {"token":token},200

