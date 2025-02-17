from flask import Flask, Blueprint, jsonify, request

app = Flask(__name__)

exclusao_perfil_bp = Blueprint("exclusao_perfil", __name__)

# 🔹 Simulação de um usuário (dados estáticos)
usuario = {
    "email": "teste@email.com",
    "nome": "Usuário Teste",
    "senha": "1234",
    "reservas_ativas": False  # Simulando que o usuário tem reservas ativas
}

# 🔹 Função para verificar a senha (simulação)
def verificar_senha(senha_input):
    return senha_input == usuario["senha"]

# 🔹 Rota para excluir o perfil com verificação de reservas ativas e tratamento de erro
@exclusao_perfil_bp.route("/api/perfil", methods=["DELETE"])
def excluir_perfil():
    data = request.get_json()
    senha = data.get("senha")

    if not senha:
        return jsonify({"error": "O campo 'senha' é obrigatório."}), 400

    # Simulando a verificação do usuário
    if usuario["email"] != "teste@email.com":
        return jsonify({"error": "Usuário não encontrado."}), 404
    
    # Simulando a verificação de reservas ativas
    if usuario["reservas_ativas"]:
        return jsonify({"error": "Não é possível excluir o perfil com reservas ativas. Cancele todas as reservas primeiro."}), 400
    
    # Simulando a verificação da senha
    if not verificar_senha(senha):
        return jsonify({"error": "Senha incorreta."}), 400

    try:
        # Simulando a exclusão do perfil (apaga os dados do usuário)
        usuario.clear()
        return jsonify({"message": "Conta excluída com sucesso!"}), 200
    except Exception as e:
        return jsonify({"error": "Houve um problema ao excluir sua conta. Tente novamente mais tarde."}), 500

# 🔹 Registrar o Blueprint no app
app.register_blueprint(exclusao_perfil_bp)

if __name__ == "__main__":
    app.run(debug=True)
