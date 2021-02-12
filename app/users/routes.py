from flask import Blueprint
from .controllers import (UserDetails,PaginaUser,UserLogin)

user_api = Blueprint('user_api',__name__)

user_api.add_url_rule(
    '/user',
    view_func = UserDetails.as_view('user_details'),
    methods=['POST','GET']
)

user_api.add_url_rule(
    '/users/<int:id>',
    view_func = PaginaUser.as_view('pagina_users'),
    methods=['GET','PATCH','DELETE']
)

user_api.add_url_rule(
    '/login',
    view_func = UserLogin.as_view('login'),
    methods=['POST']
)
