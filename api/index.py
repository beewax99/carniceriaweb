import os
from flask import Flask, render_template

# ... otra configuración de tu app ...

@app.route('/')
def home():
    # Buscamos la variable que configuraste en Vercel
    whatsapp_number = os.environ.get('WHATSAPP_NUMBER', '5491100000000')
    
    # Pasamos la variable al template HTML como 'phone_number'
    return render_template('index.html', phone_number=whatsapp_number)
