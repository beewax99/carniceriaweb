import os
from flask import Flask, render_template

# Importante: template_folder debe apuntar a donde esté tu index.html
app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    # Buscamos la variable de Vercel. Si no existe, usamos uno de respaldo.
    # ASEGÚRATE que en Vercel la variable se llame: WHATSAPP_NUMBER
    whatsapp = os.environ.get('WHATSAPP_NUMBER', '5491100000000')
    
    # Pasamos el valor al HTML
    return render_template('index.html', phone_number=whatsapp)
