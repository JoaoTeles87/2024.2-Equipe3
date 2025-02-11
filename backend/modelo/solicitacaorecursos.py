from modelo.extensao import db
import datetime

class SolicitacaoRecursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reserva_id = db.Column(db.Integer, nullable=False)  # Associa à reserva
    recursos = db.Column(db.Text, nullable=True)  # Itens solicitados
    itens_nao_listados = db.Column(db.Text, nullable=True)
    observacoes = db.Column(db.Text, nullable=True)