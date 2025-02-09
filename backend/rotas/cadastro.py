from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from modelo.usuario import Usuario
from modelo.extensao import db

cadastro_bp = Blueprint("cadastro", __name__)

@cadastro_bp.route("/api/cadastro", methods=["POST"])
def cadastro():
    data = request.get_json()
    nome = data.get("nome")
    cpf = data.get("cpf")
    email = data.get("email")
    professor = data.get("professor")
    senha = data.get("senha")
    confirmarSenha = data.get("confirmarSenha")

    if not nome or not cpf or not email or not senha:
        return jsonify({"error": "Todos os campos são obrigatórios."}), 400

    if Usuario.query.filter_by(nome=nome).first():
        return jsonify({"error": "Nome já cadastrado."}), 409
    
    if Usuario.query.filter_by(cpf=cpf).first():
        return jsonify({"error": "CPF já cadastrado."}), 409

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"error": "Email já cadastrado."}), 409
    
    if senha != confirmarSenha: 
        return jsonify({"error": "Senhas não conferem."}), 400
    

    senha_hash = generate_password_hash(senha)

    novoUsuario = Usuario(
        nome=nome, cpf=cpf, email=email, professor=professor, senha=senha_hash
    )
    db.session.add(novoUsuario)
    db.session.commit()

    return jsonify({"message": "Cadastro criado com sucesso!"}), 201