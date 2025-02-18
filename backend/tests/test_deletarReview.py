import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
import pytest
import json
from datetime import datetime
from backend.modelo.__init__ import create_app 
from backend.modelo.extensao import db
from backend.modelo.reviewSala import ReviewSala

@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        from modelo.reviewSala import ReviewSala  
        db.create_all()  
    yield app
    with app.app_context():
        db.drop_all() 

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def criar_review(app):
    with app.app_context():
        data_avaliacao = datetime.strptime("Sat, 15 Feb 2025 16:31:37 GMT", "%a, %d %b %Y %H:%M:%S GMT")
        review = ReviewSala(
            reserva_id=1,
            sala_id=2,
            usuario_id=3,
            nota=4,
            comentario="Sala boa, mas com algumas falhas.",
            data_avaliacao=data_avaliacao
        )
        db.session.add(review)
        db.session.commit()
        db.session.refresh(review)
        return review

def test_deletar_review_existente(client, criar_review, app):
    response = client.delete(f"/api/reviews/{criar_review.id}")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['mensagem'] == "Avaliação deletada com sucesso!"

    with app.app_context():
        review_deletado = db.session.get(ReviewSala, criar_review.id)
        assert review_deletado is None

def test_deletar_review_nao_existente(client):
    response = client.delete("/api/reviews/9999")
    assert response.status_code == 404

    data = json.loads(response.data)
    assert data['error'] == "Avaliação não encontrada para o ID fornecido."