import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import resend
from datetime import datetime

load_dotenv()

app = Flask(__name__)


# CORS(app, resources={"*": {"origins": "*"}})


# test connection
@app.route("/test-connection", methods=["GET"])
def test_connection():
    print("Received request to test connection")
    return jsonify({
        "status": "ok", 
        "message": "Conexión exitosa con la API de OrderEat 🚀"
        }), 200
  
    

@app.route("/send-intern-email", methods=["POST"])
def ordereat_send_intern_email():
    data = request.json

    file_path = os.path.join(os.path.dirname(__file__), "./templates", "intern-email.html")

    with open(file_path, "r", encoding="utf-8") as file:
        
        email_template = file.read()
        
        template_vars = {
            "{{from_name}}": data.get("fromName", ""),
            "{{from_email}}": data.get("fromEmail", ""),
            "{{from_phone}}": data.get("fromPhone", ""),
            "{{from_school}}": data.get("fromSchool", ""),
            "{{from_position}}": data.get("fromPosition", ""),
            "{{from_message}}": data.get("fromMessage", "(No se proporcionó mensaje)"),
            "{{timestamp}}": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        for var, value in template_vars.items():
            email_template = email_template.replace(var, value)
    
    try:
        resend.api_key = os.getenv("RESEND_API_KEY")
        if not resend.api_key:
            raise ValueError("API key not found in environment variables.")
        
        params_for_email = {
            "from": "🌶️chiliSites <contacto@chilisites.com>",
            "to": [],                           # a que mail ordereat quieren que les llegue?
            "subject": f"Nuevo mensaje de {data.get('fromName', '** SIN NOMBRE **')}",
            "html": email_template,
        }
        
        params: resend.Emails.SendParams = params_for_email
        
        email = resend.Emails.send(params)
        
        if email:
            print("✅ Correo interno enviado correctamente")
            
        return jsonify({
            "message": "Correo enviado ✅",
            "status": "ok"
            }), 200
    except Exception as e:
        print("❌ Error al enviar el correo:", str(e))
        return jsonify({"error": "❌ No se pudo enviar el correo interno"}), 500

@app.route("/send-thanks-email", methods=["POST"])
def ordereat_send_email():
    data = request.json

    file_path = os.path.join(os.path.dirname(__file__), "orderEat/templates", "thanks-email.html")
    
    with open(file_path, "r", encoding="utf-8") as file:
        
        email_template = file.read()
        
        template_vars = {
            "{{from_name}}": data.get("name", "")
        }
        
        for var, value in template_vars.items():
            email_template = email_template.replace(var, value)

    try:
        resend.api_key = os.getenv("RESEND_API_KEY_ORDEREAT")
        params: resend.Emails.SendParams = {
            "from": "Acme <onboarding@resend.dev>", # mail de order 
            "to": [data['email']],
            "subject": "Hemos recibido tu mensaje!",
            "html": email_template,
        }
        
        print("✅ Correo de agradecimiento enviado correctamente:")
        
        return jsonify({"message": "Correo de agradecimiento enviado correctamente ✅"}), 200
    
    except Exception as e:
        print("❌ Error al enviar el correo de agradecimiento:", str(e))
        return jsonify({"error": "No se pudo enviar el correo de agradecimiento ❌"}), 500



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
    