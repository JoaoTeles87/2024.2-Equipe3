from modelo.extensao import db

class Reserva(db.Model):
    __tablename__ = "reservas"
    __table_args__ = {'extend_existing': True}  # Adicionando extend_existing

    id = db.Column(db.Integer, primary_key=True)
    sala_id = db.Column(db.Integer, db.ForeignKey('salas.id'), nullable=False)  # Chave estrangeira referenciando 'salas.id'
    usuario_id = db.Column(db.Integer, nullable=False)
    data_reserva = db.Column(db.DateTime, nullable=False)

    sala = db.relationship('Sala', backref='reservas', lazy=True)  # Relacionamento com a tabela 'salas'

    def __init__(self, sala_id, usuario_id, data_reserva):
        self.sala_id = sala_id
        self.usuario_id = usuario_id
        self.data_reserva = data_reserva
