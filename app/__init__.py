from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os

# Veritabanı bağlantısı
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Config ayarlarını yükle
    app.config.from_object("app.config.Config")

    # Veritabanı bağlantısını başlat
    db.init_app(app)
    migrate.init_app(app, db)

    # JWT'yi başlat
    jwt = JWTManager(app)

    # Blueprint'leri import et ve yükle (Importları FONKSİYON içinde yapmalıyız!)
    from app.models import User  # Veritabanı modellerini burada import et
    from routes.auth import auth_bp
    from routes.meals import meals_bp
    from routes.analyze import analyze_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(meals_bp, url_prefix="/meals")
    app.register_blueprint(analyze_bp, url_prefix="/analyze")

    return app
