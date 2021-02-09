from flask import request, Blueprint, jsonify
from app.users.model import User
from app.extensions import db

user_api = Blueprint('user_api',__name__)

@user_api.route('/users',methods=['POST','GET'])
def index():
    if request.method == 'GET':
        users = User.query.all() #pega todos os users de uma vez
        return jsonify([user.json() for user in users]),200

    if request.method == 'POST':
        
        dados = request.json #pega apenas o corpo da requisição, ou seja, o json, para poder fazer um POST desses dados

        email = dados.get('email') #pega o nome que esta no formato json
        senha = dados.get('senha')
        

        if email is None or senha is None:
            return {"error": "Email e senha obrigatórios!"},400

        if User.query.filter_by(email=email).first():
            return {"error": "Já existe um usuário cadastrado com este email!"},400

        if len(email)>40:
            return {"error": "String de email excede o tamanho de 40 caracteres!"},400

        if not isinstance(email,str) or not isinstance(senha,str):
            return {"error": "Algum tipo inserido é inválido!"},400

        user = User(email=email,senha=senha)

        db.session.add(user)
        db.session.commit()

        return user.json(),200

@user_api.route('/users/<int:id>',methods=['GET','PATCH','DELETE'])  #put tem q alterar tudo, patch pode alterar o que quiser
def detalhes_users(id):
    user = User.query.get_or_404(id) #verifica se existe, caso contrario retorna erro 404

    if request.method == 'GET':
        return user.json(),200
    if request.method == 'PATCH':
        dados = request.json

        email = dados.get('email',user.email)    #caso nada seja inputado para atualizar as informações de nome, o nome permanece o mesmo, ou seja, aluno.nome
        senha = dados.get('senha',user.senha)

        #falta verificar tamanho e tipo dos dados que nem na primeira função

        if User.query.filter_by(email=email).first():
            return {"error": "Já existe um usuário cadastrado com este email!"},400
        
        if len(email)>40:
            return {"error": "String de email excede o tamanho de 40 caracteres!"},400

        if not isinstance(email,str) or not isinstance(senha,str):
            return {"error": "Algum tipo inserido é inválido!"},400
        
        user.email = email
        user.senha = senha

        db.session.add(user)
        db.session.commit()

        return user.json(),200 #retorna um json desse produto

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify([user.json() for user in User.query.all()]),200 #retorna um json contendo todos os produtos ainda existentes
