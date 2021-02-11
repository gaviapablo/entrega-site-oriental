from flask import Flask
from .config import Config
from .extensions import db, migrate, mail, jwt

from app.produtos.routes import produto_api
from app.users.routes import user_api

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app,db)
    mail.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(produto_api) #registra a rota
    app.register_blueprint(user_api)

    return app