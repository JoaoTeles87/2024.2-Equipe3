from backend.modelo.extensao import db
from backend.modelo.sala import Sala
from backend.modelo.reserva import Reserva

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
