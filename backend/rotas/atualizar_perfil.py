from flask import Blueprint, jsonify, request
import re

# Simulação de dados do usuário autenticado
usuario = {
    "email": "teste@email.com",
    "nome": "Usuário Teste",
    "cpf": "123.456.789-00",
    "senha": "1234",
    "professor": True,
    "siape": "987654"
}

# Função para validar um CPF verdadeiro
def validar_cpf(cpf):
    cpf = re.sub(r"\D", "", cpf)  # Remove pontos e traços

    if len(cpf) != 11 or cpf in [str(i) * 11 for i in range(10)]:
        return False  # CPFs com todos os números iguais são inválidos

    # Cálculo do primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11
    digito1 = 0 if digito1 == 10 else digito1

    # Cálculo do segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11
    digito2 = 0 if digito2 == 10 else digito2

    return cpf[-2:] == f"{digito1}{digito2}"

# Função para validar o nome
def validar_nome(nome):
    return bool(re.match(r"^[A-Za-zÀ-ÿ\s]+$", nome)) and len(nome) > 1

# Criando o Blueprint para a atualização do perfil
atualizar_perfil_bp = Blueprint("atualizar_perfil", __name__)

@atualizar_perfil_bp.route("/api/perfil", methods=["PUT"])
def atualizar_perfil():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Nenhum dado enviado."}), 400

    # Obtém os campos enviados na requisição
    nome = data.get("nome")
    cpf = data.get("cpf")
    email = data.get("email")
    nova_senha = data.get("nova_senha")

    # Valida o CPF
    if not cpf:
        return jsonify({"error": "O campo 'cpf' é obrigatório."}), 400
    if not validar_cpf(cpf):
        return jsonify({"error": "O CPF fornecido é inválido."}), 400

    # Valida o nome
    if not nome or not validar_nome(nome):
        return jsonify({"error": "O nome é inválido. Deve conter apenas letras e espaços, e ter pelo menos 2 caracteres."}), 400

    # Valida o email
    if not email:
        return jsonify({"error": "O campo 'email' é obrigatório."}), 400

    # Atualiza os dados do usuário estático
    usuario["nome"] = nome
    usuario["cpf"] = cpf
    usuario["email"] = email
    usuario["senha"] = nova_senha or usuario["senha"]

    if usuario["professor"]:
        siape = data.get("siape")
        if siape:
            usuario["siape"] = siape

    return jsonify({"message": "Perfil atualizado com sucesso!", "usuario": usuario}), 200
