import os
import json
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='../templates')

PHONE_NUMBER_ID = "1073473392514608"
WHATSAPP_TOKEN  = os.environ.get("WHATSAPP_TOKEN", "")
VERIFY_TOKEN    = os.environ.get("VERIFY_TOKEN", "carniceria_arias_2025")

INFO = {
    "horarios":  "Lunes a Viernes: 8:00 a 13:00 y 17:00 a 20:00 hs\nSabados: 8:00 a 13:00 hs\nDomingos: cerrado",
    "direccion": "La Plata, Buenos Aires (escribinos y te damos la direccion exacta)",
    "delivery":  "Si hacemos delivery en la zona. Consultanos disponibilidad y costo.",
    "productos": "Carnes de novillo, Pollo, Cerdo, Pescado, Mariscos. Todos frescos del dia!",
}

MENU = (
    "Hola! Soy el asistente de Carniceria Arias\n\n"
    "En que te puedo ayudar?\n\n"
    "1 - Ver productos\n"
    "2 - Consultar precios / hacer un pedido\n"
    "3 - Horarios de atencion\n"
    "4 - Direccion\n"
    "5 - Delivery\n\n"
    "Escribi el numero o tu consulta directamente"
)

def send_message(to, text):
    if not REQUESTS_AVAILABLE or not WHATSAPP_TOKEN:
        return
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    try:
        requests.post(url, headers=headers, json=payload, timeout=10)
    except Exception:
        pass

def get_response(msg):
    msg = msg.strip().lower()
    saludos = ["hola", "buenas", "buenos dias", "buenas tardes", "buenas noches", "hi", "inicio", "menu"]
    if any(s in msg for s in saludos):
        return MENU
    if msg == "1" or any(w in msg for w in ["producto", "tienen", "venden", "pescado", "pollo", "cerdo", "mariscos"]):
        return INFO["productos"]
    if msg == "2" or any(w in msg for w in ["precio", "cuanto", "pedido", "pedir", "quiero", "kilo", "kg"]):
        return "Para precios actualizados y hacer tu pedido, escribinos que necesitas y te respondemos enseguida!"
    if msg == "3" or any(w in msg for w in ["horario", "hora", "abren", "cierran", "abierto"]):
        return "Horarios:\n" + INFO["horarios"]
    if msg == "4" or any(w in msg for w in ["direccion", "donde", "ubicacion", "local"]):
        return INFO["direccion"]
    if msg == "5" or any(w in msg for w in ["delivery", "envio", "mandan", "reparten"]):
        return INFO["delivery"]
    return "Gracias por escribirnos! Escribi 'menu' para ver las opciones, o hacenos tu consulta directamente y te respondemos."

@app.route("/")
def home():
    whatsapp = os.environ.get("WHATSAPP_NUMBER", "5491100000000")
    return render_template("index.html", phone_number=whatsapp)

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    try:
        data    = request.get_json(force=True)
        entry   = data["entry"][0]
        changes = entry["changes"][0]["value"]
        msg_obj = changes["messages"][0]
        sender  = msg_obj["from"]
        text    = msg_obj["text"]["body"]
        reply   = get_response(text)
        send_message(sender, reply)
    except Exception:
        pass
    return jsonify({"status": "ok"}), 200

