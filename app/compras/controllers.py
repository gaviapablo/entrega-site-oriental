from flask import request
from app.compras.model import Compra
from app.extensions import db
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity


class ComprasDetails(MethodView):
    #Apenas o usuario administrador deveria ser capaz de ver esta seção com todas as compras de todos os usuarios

    '''
    def get(self):
        compras = Compra.query.all() #pega todas as compras de todos os users
        return jsonify([compra.json() for compra in compras]),200
    '''
    decorators = [jwt_required] #para saber se o usuario está logado para conseguir alterar seus dados, um token é necessario
                                #e então este decorator verifica se existe alguem logado
    def post(self):

        dados = request.json #pega apenas o corpo da requisição, ou seja, o json, para poder fazer um POST desses dados

        produtos = dados.get('produtos')
        preço = dados.get('preço') #pega o nome que esta no formato json
        user_id = get_jwt_identity() #a compra recebe o id do usuario logado
        
        if not produtos or not preço or not user_id: #caso nao tenha usuario logado, a compra não ocorrerá
            return {"error": "Produtos, preço e usuário obrigatórios!"},400

        if not isinstance(preço,float):
            return {"error": "Algum tipo inserido é inválido!"},400

        compra = Compra(produtos=produtos,preço=preço,user_id=user_id)

        db.session.add(compra)
        db.session.commit()

        return compra.json(),200



    


