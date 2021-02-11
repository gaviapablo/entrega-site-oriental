from flask import Blueprint
from .controllers import (ProdutoDetails,PaginaProduto)

produto_api = Blueprint('produto_api',__name__)

produto_api.add_url_rule(
    '/produtos',
    view_func = ProdutoDetails.as_view('index'),methods=['POST','GET']
)

produto_api.add_url_rule(
    '/produtos/<int:id>',
    view_func = PaginaProduto.as_view('detalhes_produtos'),methods=['GET','PATCH','DELETE']
)