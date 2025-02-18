import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações do JWT
    JWT_TOKEN_LOCATION = ["cookies"]  # Habilitar JWT em cookies
    JWT_SECRET_KEY = 'jwtchavesecreta'  
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"  # Nome do cookie JWT
    JWT_COOKIE_SECURE = False  # Se for produção, definir True para HTTPS
    JWT_COOKIE_HTTPONLY = True  # Impede acesso via JavaScript
    JWT_COOKIE_CSRF_PROTECT = False  # Pode ativar proteção CSRF se necessário
    JWT_COOKIE_SAMESITE = "None"

