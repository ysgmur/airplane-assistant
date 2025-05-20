import firebase_admin
from firebase_admin import credentials, firestore
from flask_jwt_extended import decode_token
from app.chat_agent.intent_parser import parse_intent
from app.gateway.router import call_airline_api
from app import create_app

# Flask app context'i başlat
app = create_app()

# Firebase bağlantısı
cred = credentials.Certificate("app/firestore/firebase_key.json")
firebase_admin.initialize_app(cred)
db_firestore = firestore.client()

def listen_chat():
    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name != 'ADDED':
                continue

            doc = change.document
            data = doc.to_dict()

            if data.get("processed", False):
                print("⏭ Already processed, skipping.")
                continue

            user_message = data.get("message")
            token = data.get("token", "")
            raw_token = token.replace("Bearer ", "")

            # ✅ Flask app context içinde çalış
            with app.app_context():
                username = "ChatUser"

                # 🔓 Token çöz ve kullanıcıyı al
                try:
                    decoded = decode_token(raw_token)
                    username = decoded.get("sub") or decoded.get("username", "ChatUser")
                    print(f"✅ Decoded username: {username}")
                except Exception as e:
                    print("❌ JWT decode failed:", e)
                    doc.reference.update({
                        "response": {"msg": "Invalid or missing token"},
                        "processed": True
                    })
                    return

                if not isinstance(user_message, str) or not user_message.strip():
                    return

                print("💬 Yeni mesaj:", user_message)
                parsed = parse_intent(user_message)
                print("🧠 OpenAI raw output:", parsed)

                # 🔁 Ana API işlevi
                api_response = call_airline_api(parsed, passenger_name=username)

                # 🔁 Firestore'a yaz
                doc.reference.update({
                    "response": api_response,
                    "processed": True
                })

    # Firebase chat koleksiyonu dinleniyor
    db_firestore.collection("chat").on_snapshot(on_snapshot)
