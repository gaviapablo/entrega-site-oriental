from flask import Blueprint
from .controllers import ComprasDetails

compra_api = Blueprint('compra_api',__name__)

compra_api.add_url_rule(
    '/compras',
    view_func = ComprasDetails.as_view('index'),methods=['POST']
)
