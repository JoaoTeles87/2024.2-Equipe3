from backend.modelo.extensao import db

# Modelo da Tabela de Usuários
class Usuario(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    professor = db.Column(db.String(1), nullable=False)  # "S" ou "N"
    senha = db.Column(db.String(200), nullable=False)