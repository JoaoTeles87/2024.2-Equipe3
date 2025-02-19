from flask import Flask, jsonify
from flask_cors import CORS
from backend.blueprints import registrarBlueprints
from backend.modelo.extensao import db
from backend.config import Config

app = Flask(__name__)
app.config["TESTING"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)  # Permite conexão com o frontend

db.init_app(app)

registrarBlueprints(app)

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Avaliação não encontrada para o ID fornecido."}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

with app.app_context():
    db.create_all()
    db.drop_all()
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)