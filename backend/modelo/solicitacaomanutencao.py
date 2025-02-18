from backend.modelo.extensao import db
import datetime
    
class SolicitacaoManutencao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reserva_id = db.Column(db.Integer, nullable=False)
    descricao = db.Column(db.Text, nullable=False)  # Descrição da manutenção