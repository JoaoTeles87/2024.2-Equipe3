import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import json
import pytest
from datetime import datetime

from backend.modelo.extensao import db
from backend.modelo.reviewSala import ReviewSala

@pytest.fixture(scope="module")
def criar_review(app):
    with app.app_context():
        review = ReviewSala(
            reserva_id=1,
            sala_id=2,
            usuario_id=3,
            nota=5,  
            comentario="Sala excelente, as mudanças foram feitas e ficou ótima.",
        )
        db.session.add(review)
        db.session.commit()
        db.session.refresh(review)
        return review

def test_obter_review_existente(client, criar_review):
    response = client.get(f"/api/reviews/{criar_review.id}")
    
    assert response.status_code == 200
    
    data = json.loads(response.data)
    
    assert data['id'] == criar_review.id
    assert data['reserva_id'] == 1
    assert data['sala_id'] == 2
    assert data['usuario_id'] == 3
    assert data['nota'] == 5
    assert data['comentario'] == "Sala excelente, as mudanças foram feitas e ficou ótima."

def test_obter_review_inexistente(client):
    response = client.get("/api/reviews/9999")
    
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['error'] == "Avaliação não encontrada para o ID fornecido."