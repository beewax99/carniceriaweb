from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bot', methods=['POST'])
def whatsapp_bot():
    # Lógica básica del bot
    return jsonify({"status": "ok", "message": "Bot de Carnicería activo"}), 200

if __name__ == '__main__':
    app.run(debug=True)
