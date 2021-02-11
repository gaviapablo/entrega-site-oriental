from flask import request, jsonify
from flask.views import MethodView
from app.produtos.model import Produto
from app.extensions import db

#produto_api = Blueprint('produto_api',__name__)

class ProdutoDetails(MethodView):
    def get(self):
        produtos = Produto.query.all() #pega todos os produtos de uma vez
        return jsonify([produto.json() for produto in produtos]),200

    def post(self):
        dados = request.json #pega apenas o corpo da requisição, ou seja, o json, para poder fazer um POST desses dados

        nome = dados.get('nome') #pega o nome que esta no formato json
        preço = dados.get('preço')
        estoque = dados.get('estoque')
        descrição = dados.get('descrição')
        

        if nome is None or preço is None or estoque is None or descrição is None:
            return {"error": "Nome, preço, estoque e descrição obrigatórios!"},400

        if Produto.query.filter_by(nome=nome).first():
            return {"error": "Já existe um produto cadastrado com este nome!"},400

        if len(nome)>50:
            return {"error": "String de nome excede o tamanho de 50 caracteres!"},400

        if not isinstance(nome,str) or not isinstance(preço,float) or not isinstance(estoque,int) or not isinstance(descrição,str):
            return {"error": "Algum tipo inserido é inválido!"},400

        produto = Produto(nome=nome,preço=preço,estoque=estoque,descrição=descrição)

        db.session.add(produto)
        db.session.commit()

        return produto.json(),200

class PaginaProduto(MethodView):
    def get(self,id):
        produto = Produto.query.get_or_404(id) #verifica se existe, caso contrario retorna erro 404
        return produto.json(),200


    def patch(self,id):
        produto = Produto.query.get_or_404(id) #verifica se existe, caso contrario retorna erro 404
        dados = request.json

        nome = dados.get('nome',produto.nome)    #caso nada seja inputado para atualizar as informações de nome, o nome permanece o mesmo, ou seja, aluno.nome
        preço = dados.get('preço',produto.preço)
        estoque = dados.get('estoque',produto.estoque)
        descrição = dados.get('descrição',produto.descrição)

        #falta verificar tamanho e tipo dos dados que nem na primeira função

        if Produto.query.filter_by(nome=nome).first():
            return {"error": "Já existe um produto cadastrado com este nome!"},400
        
        if len(nome)>50:
            return {"error": "String de nome excede o tamanho de 50 caracteres!"},400

        if not isinstance(nome,str) or not isinstance(preço,float) or not isinstance(estoque,int) or not isinstance(descrição,str):
            return {"error": "Algum tipo inserido é inválido!"},400

        
        produto.nome = nome
        produto.preço = preço
        produto.estoque = estoque
        produto.descrição = descrição       

        db.session.add(produto)
        db.session.commit()

        return produto.json(),200 #retorna um json desse produto
    
    def delete(self,id):
        produto = Produto.query.get_or_404(id) #verifica se existe, caso contrario retorna erro 404
        db.session.delete(produto)
        db.session.commit()
        return jsonify([pro.json() for pro in Produto.query.all()]),200 #retorna um json contendo todos os produtos ainda existentes




