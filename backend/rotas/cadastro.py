from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from backend.modelo.usuario import Usuario
from backend.modelo.extensao import db
import re

def validarEmail(email):
    padrao_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(padrao_email, email):
        return False
    return True

def validarCpf(cpf):
    padrao_cpf = r'^\d{3}\.\d{3}\.\d{3}-\d{2}$'
    if not re.match(padrao_cpf, cpf):
        return False
    return True

cadastro_bp = Blueprint("cadastro", __name__)

@cadastro_bp.route("/api/cadastro", methods=["POST"])
def cadastro():
    data = request.get_json()
    
    nome = data.get("Nome", "").strip()
    cpf = data.get("CPF", "").strip()
    email = data.get("Email", "").lower().strip()
    professor = data.get("Professor", "").upper().strip()
    siape = data.get("SIAPE", "").strip() if professor == "S" else None
    senha = data.get("Senha", "").strip()
    confirmar_senha = data.get("Confirmar Senha", "").strip()
    
    
    # Verificação de campos obrigatórios
    campos_obrigatorios = {
        "Nome": nome,
        "Cpf": cpf,
        "Email": email,
        "Senha": senha,
        "Confirmar Senha": confirmar_senha
    }
    if professor == "S":
        campos_obrigatorios["SIAPE"] = siape
    
    for campo, valor in campos_obrigatorios.items():
        if not valor:
            return jsonify({"error": f"O campo '{campo}' é obrigatório."}), 400
    
    if not validarEmail(email):
        return jsonify({"erro": "Formato de email inválido. Use um email válido, como exemplo@dominio.com."}), 400
    
    if not validarCpf(cpf):
        return jsonify({"erro": "CPF inválido. Digite um CPF válido no formato XXX.XXX.XXX-XX."}), 400
    
    checagemCpf = Usuario.query.filter(Usuario.cpf == cpf).first()
    if checagemCpf:
        return jsonify({"error": "Erro: email/cpf já está registrado."}), 400
    
    checagemEmail = Usuario.query.filter(Usuario.email==email).first()
    if checagemEmail:
        return jsonify({"error": "Erro: email/cpf já está registrado."}), 400
    
    if professor == "S":
        checagenSiape = Usuario.query.filter(Usuario.siape == siape).first()
        if checagenSiape:
            return jsonify({"error": "Erro: siape já está registrado."}), 400

    if senha != confirmar_senha:
        return jsonify({"error": "As senhas não coincidem."}), 400

    senha_hash = generate_password_hash(senha)

    # Criar novo usuário
    novo_usuario = Usuario(
        nome=nome, cpf=cpf, email=email, professor=professor, siape=siape, senha=senha_hash
    )
    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"message": "Cadastro criado com sucesso!"}), 201
