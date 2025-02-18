from modelo.extensao import db
from modelo.usuario import Usuario
from modelo.sala import Sala
from datetime import datetime

class Reserva(db.Model):
    __tablename__ = "reservas"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)  # Ajuste aqui
    sala_id = db.Column(db.Integer, db.ForeignKey("salas.id"), nullable=False)
    data = db.Column(db.Date, nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    ativa = db.Column(db.Boolean, default=True) 

    usuario = db.relationship("Usuario", backref="reservas")
    sala = db.relationship("Sala", backref="reservas")

    def __init__(self, usuario_id, sala_id, data, horario_inicio, horario_fim, ativa=True):
        self.usuario_id = usuario_id
        self.sala_id = sala_id
        self.data = data
        self.horario_inicio = horario_inicio
        self.horario_fim = horario_fim
        self.ativa = ativa
