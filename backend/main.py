from flask import Flask
from flask_cors import CORS
from backend.blueprints import registrarBlueprints
from backend.modelo.extensao import db
from backend.config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # Permite conexão com o frontend
db.init_app(app)
registrarBlueprints(app)    

with app.app_context():
    db.drop_all()
    db.create_all()

print(app.url_map)  # Isso vai mostrar todas as rotas registradas
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)