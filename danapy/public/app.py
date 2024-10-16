from flask import Flask, Blueprint, render_template, jsonify, request
from api.client import DanaClient
from main import DANA
import sys
sys.path.insert(0, '../')

main_blueprint = Blueprint('main', __name__)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/login', methods=['POST'])
def login():
    phone_number = request.json['phone_number']
    password = request.json['password']
    # Implementasi login menggunakan library DANA API
    dana = DANA()
    response = dana.login(phone_number, password)
    return jsonify(response)

@main_blueprint.route('/register', methods=['POST'])
def register():
    phone_number = request.json['phone_number']
    email = request.json['email']
    password = request.json['password']
    # Implementasi register menggunakan library DANA API
    dana = DANA()
    response = dana.register(phone_number, email, password)
    return jsonify(response)
@app.route('/cek_mutasi', methods=['GET'])
def cek_mutasi():
    """Cek mutasi transfer"""
    client = DanaClient()
    data = client.cek_mutasi()
    return jsonify(data)

@app.route('/transfer', methods=['POST'])
def transfer():
    """Lakukan transfer"""
    client = DanaClient()
    data = request.get_json()
    result = client.transfer(data)
    return jsonify(result)

@app.route('/simpan_bukti_transfer', methods=['POST'])
def simpan_bukti_transfer():
    """Simpan bukti transfer"""
    client = DanaClient()
    data = request.get_json()
    result = client.simpan_bukti_transfer(data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)