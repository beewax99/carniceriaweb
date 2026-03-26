import os
from flask import Flask, render_template

app = Flask(__name__, template_folder='../templates')

@app.route('/')
def home():
    # Obtiene el número de la variable WHATSAPP_NUMBER de Vercel
    # Si no la encuentra, usa el número que pongas acá por defecto
    whatsapp = os.environ.get('WHATSAPP_NUMBER', '5491100000000') 
    
    # IMPORTANTE: Enviamos 'whatsapp' al HTML bajo el nombre 'phone_number'
    return render_template('index.html', phone_number=whatsapp)
