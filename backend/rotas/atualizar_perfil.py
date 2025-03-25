from flask import Blueprint, jsonify, request
from flask_cors import CORS
import re

atualizar_perfil_bp = Blueprint("atualizar_perfil", __name__)

CORS(atualizar_perfil_bp, resources={
    r"/api/perfil": {
        "origins": "*",
        "methods": ["PUT", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Mock user data
usuario = {
    "email": "teste@email.com",
    "nome": "Usuário Teste",
    "cpf": "123.456.789-00",
    "senha": "1234",
    "professor": True,
    "siape": "987654"
}

def validar_cpf(cpf):
    cpf = re.sub(r"\D", "", cpf)  # Remove non-digit characters
    
    # Check if all digits are the same or invalid length
    if len(cpf) != 11 or all(d == cpf[0] for d in cpf):
        return False

    # Calculate first verification digit
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11
    digito1 = 0 if digito1 == 10 else digito1

    # Calculate second verification digit
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11
    digito2 = 0 if digito2 == 10 else digito2

    return cpf[-2:] == f"{digito1}{digito2}"

def validar_nome(nome):
    """Validate name contains only letters and spaces"""
    return bool(re.match(r"^[A-Za-zÀ-ÿ\s]{2,}$", nome))

@atualizar_perfil_bp.route("/api/perfil", methods=["PUT", "OPTIONS"])
def atualizar_perfil():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    data = request.get_json()
    if not data:
        return jsonify({"error": "Nenhum dado enviado."}), 400

    # Lista de campos permitidos para atualização
    campos_permitidos = ['nome', 'email', 'cpf', 'nova_senha', 'siape']
    campos_atualizados = {}

    # Verifica e valida cada campo que foi enviado
    if 'nome' in data:
        if not validar_nome(data['nome']):
            return jsonify({
                "error": "Nome inválido. Deve conter apenas letras e espaços, com mínimo 2 caracteres."
            }), 400
        campos_atualizados['nome'] = data['nome']

    if 'cpf' in data:
        if not validar_cpf(data['cpf']):
            return jsonify({"error": "CPF inválido."}), 400
        campos_atualizados['cpf'] = data['cpf']

    if 'email' in data:
        if not data['email'] or "@" not in data['email']:
            return jsonify({"error": "Email inválido."}), 400
        campos_atualizados['email'] = data['email']

    if 'nova_senha' in data:
        campos_atualizados['senha'] = data['nova_senha']

    if 'siape' in data and usuario['professor']:
        campos_atualizados['siape'] = data['siape']

    if not campos_atualizados:
        return jsonify({"error": "Nenhum campo válido para atualização foi enviado."}), 400

    usuario.update(campos_atualizados)

    return jsonify({
        "message": "Perfil atualizado com sucesso!",
        "campos_atualizados": list(campos_atualizados.keys()),
        "usuario": {
            "nome": usuario["nome"],
            "email": usuario["email"],
            "cpf": usuario["cpf"],
            "professor": usuario["professor"],
            "siape": usuario.get("siape")
        }
    }), 200