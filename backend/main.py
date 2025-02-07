from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Permite que o React acesse o backend

@app.route("/api")
def home():
    return jsonify({"message": "Backend Flask Fernanda!"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)