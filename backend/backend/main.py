from flask import Flask
from flask_cors import CORS
from blueprints import registrarBlueprints
from modelo.extensao import db
from config import Config
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object(Config)
CORS(app, supports_credentials=True)  # Permite cookies via CORS
jwt = JWTManager(app)
db.init_app(app)
registrarBlueprints(app)    



with app.app_context():
    db.create_all()
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)

