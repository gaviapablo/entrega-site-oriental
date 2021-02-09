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
        dados = request.json #pega apenas o corpo da requisição, ou seja, o json

        nome = dados.get('nome')
        preço = dados.get('preço')
        estoque = dados.get('estoque')

        if nome is None:
            return {"error": "Nome obrigatorio"},400

        if not isinstance(nome,str) or not isinstance(preço,float) or not isinstance(estoque,int):
            return {"error": "Algum tipo invalido"},400

        produto = Produto(nome=nome,preço=preço,estoque=estoque)

        db.session.add(produto)
        db.session.commit()

        return produto.json(),200

@produto_api.route('/produtos/<int:id>',methods=['PUT','GET','PATCH','DELETE'])
def detalhes_produtos(id):
    produto = Produto.query.get_or_404(id) #verifica se existe

    if request.method == 'GET':
        return produto.json(),200
    if request.method == 'PATCH':
        dados = request.json

        nome = dados.get('nome',produto.nome)    #caso nada seja inputado para atualizar as informações de nome, o nome permanece o mesmo, ou seja, aluno.nome
        preço = dados.get('preço',produto.preço)
        estoque = dados.get('cpf',produto.estoque)
        #falta verificar tamanho e tipo dos dados que nem na primeira função
        produto.nome = nome
        produto.preço = preço
        produto.estoque = estoque

        db.session.commit()

        


