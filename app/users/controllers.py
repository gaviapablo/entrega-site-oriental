from flask import request, jsonify, render_template
from app.users.model import User
from app.extensions import db,mail
from flask_mail import Message
import bcrypt
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


class UserDetails(MethodView):
    def get(self):
        users = User.query.all() #pega todos os users de uma vez
        return jsonify([user.json() for user in users]),200
    
    def post(self):
        dados = request.json #pega apenas o corpo da requisição, ou seja, o json, para poder fazer um POST desses dados

        nome = dados.get('nome')
        email = dados.get('email') #pega o nome que esta no formato json
        password = dados.get('password')
        estado = dados.get('estado')
        cidade = dados.get('cidade')
        cep = dados.get('cep')
        endereço = dados.get('endereço')
        bloco_apartamento = dados.get('bloco_apartamento')
        

        if not email or not password or not nome or not estado or not cidade or not cep or not endereço or not bloco_apartamento:
            return {"error": "Email, nome, senha e dados de endereço obrigatórios!"},400

        if User.query.filter_by(email=email).first():
            return {"error": "Já existe um usuário cadastrado com este email!"},400

        if len(email)>40:
            return {"error": "String de email excede o tamanho de 40 caracteres!"},400
        
        if len(nome)>50:
            return {"error": "String de nome excede o tamanho de 50 caracteres!"},400
        
        if len(estado)>20:
            return {"error": "String de estado excede o tamanho de 20 caracteres!"},400

        if len(password)>200:
            return {"error": "String de senha excede o tamanho de 50 caracteres!"},400

        if not isinstance(email,str) or not isinstance(password,str) or not isinstance(nome,str) or not isinstance(estado,str) or not isinstance(cidade,str) or not isinstance(cep,int) or not isinstance(endereço,str) or not isinstance(bloco_apartamento,str):
            return {"error": "Algum tipo inserido é inválido!"},400
        
        password_hash = bcrypt.hashpw(password.encode(),bcrypt.gensalt())

        user = User(nome=nome,email=email,password_hash=password_hash,estado=estado,cidade=cidade,cep=cep,endereço=endereço,bloco_apartamento=bloco_apartamento)

        db.session.add(user)
        db.session.commit()

        msg = Message(
            sender='gaviapablo@hotmail.com',
            recipients=[email],
            subject='Obrigado pelo Cadastro - Naomi', 
            html = render_template('email1.html',nome=nome) #por configuração esse render_template já busca pelo folder templates
        )

        mail.send(msg)

        return user.json(),200


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

        if email is None or password is None:
            return  {"error": "Email e senha são necessários!"},400

        user = User.query.filter_by(email=email).first()

        if user is None:
            return {"error": "Usuário ou senha são necessários!"},400
        
        if not bcrypt.checkpw(password.encode(),user.password_hash):
            return {"error": "Senha incorreta!"}

        token = create_access_token(identity=user.id,expires_delta=False)

        return {"token":token},200

 

