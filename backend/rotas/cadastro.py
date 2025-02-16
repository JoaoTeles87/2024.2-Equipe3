from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from backend.modelo.usuario import Usuario
from backend.modelo.extensao import db
import re
from sqlalchemy import exists  # Importação adicional para melhor verificação

cadastro_bp = Blueprint("cadastro", __name__)

def validarEmail(email):
    """Valida o formato do email."""
    padraoEmail = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(padraoEmail, email))

def validarCpf(cpf):
    """Valida se o CPF está no formato correto XXX.XXX.XXX-XX"""
    padraoCpf = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
    return bool(re.match(padraoCpf, cpf))

@cadastro_bp.route("/api/cadastro", methods=["POST"])
def cadastro():
    data = request.get_json()

    nome = data.get("nome", "").strip()
    cpf = data.get("cpf", "").strip()
    email = data.get("email", "").lower().strip()
    professor = data.get("professor", "").upper().strip()
    siape = data.get("siape", "").strip() if professor == "S" else None
    senha = data.get("senha", "").strip()
    confirmar_senha = data.get("confirmarSenha", "").strip()

    campos_obrigatorios = {
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "senha": senha,
        "Confirmar Senha": confirmar_senha
    }
    if professor == "S":
        campos_obrigatorios["siape"] = siape

    for campo, valor in campos_obrigatorios.items():
        if not valor:
            return jsonify({"error": f"{campo} é obrigatório."}), 400

    if not validarEmail(email):
        return jsonify({"error": "Formato de email inválido. Use um email válido, como exemplo@dominio.com."}), 400

    if not validarCpf(cpf):
        return jsonify({"error": "CPF inválido. Digite um CPF válido no formato XXX.XXX.XXX-XX."}), 400

    usuarioExistente = db.session.query(
        exists().where((Usuario.email == email) | (Usuario.cpf == cpf))
    ).scalar()

    if usuarioExistente:
        return jsonify({"error": "Erro: email/cpf já está registrado."}), 409

    if professor == "S":
        siapeExistente = db.session.query(
            exists().where(Usuario.siape == siape)
        ).scalar()

        if siapeExistente:
            return jsonify({"error": "Erro: siape já está registrado."}), 409

    if senha != confirmar_senha:
        return jsonify({"error": "As senhas não coincidem."}), 400

    senhaHash = generate_password_hash(senha)

    novo_usuario = Usuario(
        nome=nome, cpf=cpf, email=email, professor=professor, siape=siape, senha=senhaHash
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"message": "Cadastro criado com sucesso!"}), 201
