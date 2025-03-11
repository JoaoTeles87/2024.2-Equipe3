from backend.modelo.extensao import db
from datetime import datetime

# Definindo a tabela de Reservas
class Reserva(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)  
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