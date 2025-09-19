import os
from flask import Flask, jsonify
from azure.communication.identity import CommunicationIdentityClient
from dotenv import load_dotenv

# โหลด .env (ใช้ตอนรัน local)
load_dotenv()

app = Flask(__name__)

# โหลดค่า ACS Connection String (จาก Environment ของ Render หรือ local .env)
ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")

if not ACS_CONNECTION_STRING:
    raise ValueError("❌ ACS_CONNECTION_STRING is not set in environment variables")

# สร้าง Identity Client
identity_client = CommunicationIdentityClient.from_connection_string(ACS_CONNECTION_STRING)

@app.route("/")
def home():
    return "ACS Flask Server is running ✅"

@app.route("/get_token")
def get_token():
    # สร้าง ACS User Identity ใหม่
    user = identity_client.create_user()

    # ออก Token สำหรับ VoIP + Chat
    token_response = identity_client.get_token(
        user,
        scopes=["voip", "chat"]  # กำหนดสิทธิ์
    )

    return jsonify({
        "userId": user.properties["id"],
        "token": token_response.token,
        "expiresOn": str(token_response.expires_on)
    })

if __name__ == "__main__":
    # สำหรับ local dev (บน Render ไม่ต้องใส่ debug)
    app.run(host="0.0.0.0", port=5000, debug=True)
