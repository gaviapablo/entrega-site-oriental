from flask import request, Blueprint, jsonify
from app.produtos.model import Produto
from app.extensions import db

produto_api = Blueprint('produto_api',__name__)

@produto_api.route('/produtos',methods=['POST','GET'])
def index():
    if request.method == 'GET':
        produtos = Produto.query.all() #pega todos os alunos de uma vez
        return jsonify([produto.json() for produto in produtos]),200

    if request.method == 'POST':
        
        dados = request.json #pega apenas o corpo da requisição, ou seja, o json, para poder fazer um POST desses dados

        nome = dados.get('nome') #pega o nome que esta no formato json
        preço = dados.get('preço')
        estoque = dados.get('estoque')
        

        if nome is None or preço is None or estoque is None:
            return {"error": "Nome, preço e estoque obrigatórios!"},400

        if Produto.query.filter_by(nome=nome).first():
            return {"error": "Já existe um produto cadastrado com este nome!"},400

        if len(nome)>50:
            return {"error": "String de nome excede o tamanho de 50 caracteres!"},400

        if not isinstance(nome,str) or not isinstance(preço,float) or not isinstance(estoque,int):
            return {"error": "Algum tipo inserido é inválido!"},400

        produto = Produto(nome=nome,preço=preço,estoque=estoque)

        db.session.add(produto)
        db.session.commit()

        return produto.json(),200

@produto_api.route('/produtos/<int:id>',methods=['GET','PATCH','DELETE'])  #put tem q alterar tudo, patch pode alterar o que quiser
def detalhes_produtos(id):
    produto = Produto.query.get_or_404(id) #verifica se existe, caso contrario retorna erro 404

    if request.method == 'GET':
        return produto.json(),200
    if request.method == 'PATCH':
        dados = request.json

        nome = dados.get('nome',produto.nome)    #caso nada seja inputado para atualizar as informações de nome, o nome permanece o mesmo, ou seja, aluno.nome
        preço = dados.get('preço',produto.preço)
        estoque = dados.get('estoque',produto.estoque)

        #falta verificar tamanho e tipo dos dados que nem na primeira função

        if Produto.query.filter_by(nome=nome).first():
            return {"error": "Já existe um produto cadastrado com este nome!"},400
        
        if len(nome)>50:
            return {"error": "String de nome excede o tamanho de 50 caracteres!"},400

        if not isinstance(nome,str) or not isinstance(preço,float) or not isinstance(estoque,int):
            return {"error": "Algum tipo inserido é inválido!"},400
        
        produto.nome = nome
        produto.preço = preço
        produto.estoque = estoque
       

        db.session.add(produto)
        db.session.commit()

        return produto.json(),200 #retorna um json desse produto

    if request.method == 'DELETE':
        db.session.delete(produto)
        db.session.commit()
        return jsonify([pro.json() for pro in Produto.query.all()]),200 #retorna um json contendo todos os produtos ainda existentes

        


