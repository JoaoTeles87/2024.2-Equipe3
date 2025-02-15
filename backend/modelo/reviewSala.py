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
    id = db.Column(db.Integer, primary_key=True)  
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  
    sala_id = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)  
    data_reserva = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  
    data_inicio = db.Column(db.DateTime, nullable=False)  
    data_fim = db.Column(db.DateTime, nullable=False)  
    status = db.Column(db.String(50), nullable=False, default='pendente')  
    created_at = db.Column(db.DateTime, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 

    # Relacionamentos
    usuario = db.relationship('Usuario', backref=db.backref('reservas', lazy=True))
    sala = db.relationship('Sala', backref=db.backref('reservas', lazy=True))

    def __repr__(self):
        return f'<Reserva {self.id} - Sala {self.sala_id} - Usuario {self.usuario_id}>'

# Definindo a tabela de Avaliações de Salas (ReviewSala)
class ReviewSala(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    reserva_id = db.Column(db.Integer, db.ForeignKey('reserva.id'), nullable=False) 
    sala_id = db.Column(db.Integer, db.ForeignKey('sala.id'), nullable=False)  
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)  
    nota = db.Column(db.Integer, nullable=False) 
    comentario = db.Column(db.String(500))  
    data_avaliacao = db.Column(db.DateTime, default=db.func.now())  

    # Relacionamento
    reserva = db.relationship('Reserva', backref=db.backref('reviews', lazy=True))
    sala = db.relationship('Sala', backref=db.backref('reviews', lazy=True))
    usuario = db.relationship('Usuario', backref=db.backref('reviews', lazy=True))

    def __repr__(self):
        return f'<ReviewSala {self.id} - Nota {self.nota} - Usuario {self.usuario_id}>'
