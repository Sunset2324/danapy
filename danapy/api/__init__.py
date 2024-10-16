from flask import Flask, jsonify
from .client import DanaClient

app = Flask(__name__)

@app.route('/cek_mutasi', methods=['GET'])
def cek_mutasi():
    client = DanaClient()
    data = client.cek_mutasi()
    return jsonify(data)

@app.route('/transfer', methods=['POST'])
def transfer():
    client = DanaClient()
    data = client.transfer()
    return jsonify(data)

@app.route('/simpan_bukti_transfer', methods=['POST'])
def simpan_bukti_transfer():
    client = DanaClient()
    data = client.simpan_bukti_transfer()
    return jsonify(data)