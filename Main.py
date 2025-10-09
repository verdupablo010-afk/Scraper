import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)  # permite llamadas desde frontend

EMAIL_RE = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', re.IGNORECASE)

@app.route('/')
def home():
    return "Servidor funcionando correctamente."

@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json(force=True)
    url = data.get("url")
    if not url:
        return jsonify({"error": "Falta la URL"}), 400

    try:
        response = requests.get(url, timeout=12, headers={"User-Agent":"Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        emails = list(set(re.findall(EMAIL_RE, soup.get_text())))
        return jsonify({"emails_encontrados": emails}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
