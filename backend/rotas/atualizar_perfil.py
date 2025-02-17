from flask import Flask, Blueprint, jsonify, request

app = Flask(__name__)

atualizar_perfil_bp = Blueprint("atualizar_perfil", __name__)

# 🔹 Simulação de usuário (dados estáticos)
usuario = {
    "email": "teste@email.com",
    "nome": "Usuário Teste",
    "cpf": "123.456.789-00",
    "senha": "1234",
    "professor": True,
    "siape": "987654"
}

# 🔹 Função para validar o CPF (exemplo básico)
import re
def validar_cpf(cpf):
    return bool(re.match(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf))

# 🔹 Rota para atualizar o perfil com tratamento de erro
@atualizar_perfil_bp.route("/api/perfil", methods=["PUT"])
def atualizar_perfil():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Nenhum dado enviado."}), 400

    # Verifica se os campos obrigatórios foram enviados
    nome = data.get("nome")
    cpf = data.get("cpf")
    email = data.get("email")
    nova_senha = data.get("nova_senha")

    if not nome:
        return jsonify({"error": "O campo 'nome' é obrigatório."}), 400
    if not cpf:
        return jsonify({"error": "O campo 'cpf' é obrigatório."}), 400
    if not email:
        return jsonify({"error": "O campo 'email' é obrigatório."}), 400

    # Valida o formato do CPF
    if not validar_cpf(cpf):
        return jsonify({"error": "O CPF fornecido é inválido. Use o formato XXX.XXX.XXX-XX."}), 400

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

# 🔹 Registrar o Blueprint no app
app.register_blueprint(atualizar_perfil_bp)

if __name__ == "__main__":
    app.run(debug=True)
