from backend.modelo.extensao import db

# Definindo a tabela de Salas
class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    capacidade = db.Column(db.Integer)

    def __repr__(self):
        return f'<Sala {self.id} - {self.nome}>'
