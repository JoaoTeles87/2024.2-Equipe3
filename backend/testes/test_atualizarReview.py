import json
import pytest
import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from backend.modelo.extensao import db
from backend.modelo.reviewSala import ReviewSala
from flask.testing import FlaskClient
from datetime import datetime

@pytest.fixture(scope="module")
def criar_review(app):
    with app.app_context():
        review = ReviewSala(
            reserva_id=1,
            sala_id=2,
            usuario_id=3,
            nota=4,
            comentario="Sala boa, mas com algumas falhas.",
        )
        db.session.add(review)
        db.session.commit()
        db.session.refresh(review)

        return review


def test_atualizar_review_existente(client, criar_review, app):
    dados_atualizados = {
        "nota": 5,
        "comentario": "Modificações feitas, a sala está impecável agora!"
    }

    response = client.put(f"/api/reviews/{criar_review.id}", json=dados_atualizados)

    assert response.status_code == 200

    data = json.loads(response.data)
    assert data['mensagem'] == "Avaliação atualizada com sucesso!"

    with app.app_context():
        review_atualizado = db.session.get(ReviewSala, criar_review.id)
        assert review_atualizado.nota == 5
        assert review_atualizado.comentario == "Modificações feitas, a sala está impecável agora!"

def test_atualizar_review_nao_existente(client):
    dados_atualizados = {
        "nota": 5,
        "comentario": "Falhas corrigidas, a sala está impecável!"
    }

    response = client.put("/api/reviews/9999", json=dados_atualizados)

    assert response.status_code == 404

    data = json.loads(response.data)
    assert data['error'] == "Avaliação não encontrada para o ID fornecido."