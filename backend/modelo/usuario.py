from backend.modelo.extensao import db

# Modelo da Tabela de Usuários
class Usuario(db.Model):
    __tablename__ = "Usuario" 
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    professor = db.Column(db.String(1), nullable=False)  # "S" ou "N"
    siape = db.Column(db.String(6), unique=True)
    senha = db.Column(db.String(200), nullable=False)