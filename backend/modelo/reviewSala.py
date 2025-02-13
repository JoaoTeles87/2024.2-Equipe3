from modelo.extensao import db
from datetime import datetime

# Definindo a tabela de Salas
class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    capacidade = db.Column(db.Integer)

    def __repr__(self):
        return f'<Sala {self.id} - {self.nome}>'

# Definindo a tabela de Reservas
class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único da reserva
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # Relacionamento com a tabela Usuario
    sala_id = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)  # Relacionamento com a tabela Sala
    data_reserva = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Data e hora da reserva
    data_inicio = db.Column(db.DateTime, nullable=False)  # Data e hora de início da reserva
    data_fim = db.Column(db.DateTime, nullable=False)  # Data e hora de fim da reserva
    status = db.Column(db.String(50), nullable=False, default='pendente')  # Status da reserva
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Data de criação da reserva
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Data de atualização da reserva

    # Relacionamentos
    usuario = db.relationship('Usuario', backref=db.backref('reservas', lazy=True))
    sala = db.relationship('Sala', backref=db.backref('reservas', lazy=True))

    def __repr__(self):
        return f'<Reserva {self.id} - Sala {self.sala_id} - Usuario {self.usuario_id}>'

# Definindo a tabela de Avaliações de Salas (ReviewSala)
class ReviewSala(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único da avaliação
    reserva_id = db.Column(db.Integer, db.ForeignKey('reserva.id'), nullable=False)  # Relacionamento com a tabela Reserva
    sala_id = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)  # Relacionamento com a tabela Sala
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  # Relacionamento com a tabela Usuario
    nota = db.Column(db.Integer, nullable=False)  # Nota da avaliação (por exemplo, de 1 a 5)
    comentario = db.Column(db.String(500))  # Comentário da avaliação
    data_avaliacao = db.Column(db.DateTime, default=db.func.now())  # Data da criação da avaliação

    # Relacionamento
    reserva = db.relationship('Reserva', backref=db.backref('reviews', lazy=True))
    sala = db.relationship('Sala', backref=db.backref('reviews', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('reviews', lazy=True))

    def __repr__(self):
        return f'<ReviewSala {self.id} - Nota {self.nota} - Usuario {self.usuario_id}>'
