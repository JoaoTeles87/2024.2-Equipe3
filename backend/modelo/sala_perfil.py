from modelo.extensao import db

class Sala(db.Model):
    __tablename__ = "salas"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False)
    ativa = db.Column(db.Boolean, default=True)

    # Adicionando extend_existing=True para evitar conflitos de definição
    __table_args__ = {'extend_existing': True}

    def __init__(self, nome, capacidade, data_criacao, ativa=True):
        self.nome = nome
        self.capacidade = capacidade
        self.data_criacao = data_criacao
        self.ativa = ativa
