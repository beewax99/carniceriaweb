import os
import json
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='../templates')

# ── Configuración ──────────────────────────────────────────────
PHONE_NUMBER_ID = "1073473392514608"
WHATSAPP_TOKEN  = os.environ.get("WHATSAPP_TOKEN", "")
VERIFY_TOKEN    = os.environ.get("VERIFY_TOKEN", "carniceria_arias_2025")

# ── Info de la carnicería ───────────────────────────────────────
INFO = {
    "horarios":   "Lunes a Viernes: 8:00 a 13:00 y 17:00 a 20:00 hs\nSábados: 8:00 a 13:00 hs\nDomingos: cerrado 🚫",
    "direccion":  "📍 [Reemplazá con tu dirección], La Plata, Buenos Aires",
    "delivery":   "🛵 Sí hacemos delivery dentro de la zona. Consultá disponibilidad y costo según tu ubicación.",
    "productos":  "🥩 Carnes de novillo\n🍗 Pollo\n🐷 Cerdo\n🐟 Pescado\n🦐 Mariscos\n\nTodos frescos del día. ¡Consultá precios y cortes disponibles!",
}

MENU = """👋 ¡Hola! Soy el asistente de *Carnicería Arias* 🥩

¿En qué te puedo ayudar?

1️⃣ Ver productos
2️⃣ Consultar precios / hacer un pedido
3️⃣ Horarios de atención
4️⃣ Dirección
5️⃣ Delivery

Escribí el número o tu consulta directamente 💬"""

# ── Función para enviar mensajes ────────────────────────────────
def send_message(to, text):
    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type":  "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }
    requests.post(url, headers=headers, json=payload)

# ── Lógica de respuesta ─────────────────────────────────────────
def get_response(msg):
    msg = msg.strip().lower()

    if msg in ["hola", "buenas", "buenos dias", "buenas tardes", "buenas noches", "hi", "inicio", "menu", "menú"]:
        return MENU

    if msg == "1" or any(w in msg for w in ["producto", "tienen", "venden", "carnes", "pescado", "pollo", "cerdo", "mariscos"]):
        return INFO["productos"]

    if msg == "2" or any(w in msg for w in ["precio", "cuanto", "cuánto", "pedido", "pedir", "quiero", "kilo", "kg"]):
        return (
            "💰 Para precios actualizados y hacer tu pedido, escribinos directamente aquí.\n\n"
            "Decinos qué corte o producto necesitás y te respondemos al toque 🔪🥩"
        )

    if msg == "3" or any(w in msg for w in ["horario", "hora", "cuando abren", "abierto", "abren", "cierran"]):
        return f"🕐 *Horarios de atención:*\n\n{INFO['horarios']}"

    if msg == "4" or any(w in msg for w in ["direccion", "dirección", "donde", "dónde", "ubicacion", "ubicación", "local"]):
        return f"*Nuestra ubicación:*\n\n{INFO['direccion']}"

    if msg == "5" or any(w in msg for w in ["delivery", "envio", "envío", "mandan", "reparten", "llevan"]):
        return INFO["delivery"]

    # Respuesta por defecto
    return (
        "¡Gracias por escribirnos! 🥩\n\n"
        "No entendí tu consulta. Escribí *menú* para ver las opciones disponibles, "
        "o hacenos tu pregunta directamente y te respondemos enseguida 💬"
    )

# ── Rutas Flask ─────────────────────────────────────────────────

@app.route("/")
def home():
    whatsapp = os.environ.get("WHATSAPP_NUMBER", "5491100000000")
    return render_template("index.html", phone_number=whatsapp)

# Verificación del webhook (Meta lo llama una vez al configurar)
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

# Recepción de mensajes entrantes
@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    try:
        entry   = data["entry"][0]
        changes = entry["changes"][0]["value"]
        msg_obj = changes["messages"][0]
        sender  = msg_obj["from"]
        text    = msg_obj["text"]["body"]
        reply   = get_response(text)
        send_message(sender, reply)
    except (KeyError, IndexError):
        pass  # Ignorar notificaciones que no son mensajes de texto
    return jsonify({"status": "ok"}), 200

