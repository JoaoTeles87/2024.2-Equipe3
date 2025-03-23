from flask import Flask, jsonify
from flask_cors import CORS
from backend.blueprints import registrarBlueprints
from backend.modelo.extensao import db
from backend.config import Config
from sqlalchemy import inspect


app = Flask(__name__)
app.config["TESTING"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app, origins=["http://localhost:3000"])

db.init_app(app)
with app.app_context():
    db.create_all()
   
    
registrarBlueprints(app)

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Avaliação não encontrada para o ID fornecido."}), 404

    
if __name__ == "__main__":
    app.run(debug=True, port=5000)