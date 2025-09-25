import os
import uuid
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from azure.communication.identity import CommunicationIdentityClient
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)  # อนุญาตให้ทุก domain เข้าถึง
ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")
if not ACS_CONNECTION_STRING:
    raise ValueError("❌ Environment variable 'ACS_CONNECTION_STRING' is not set.")

identity_client = CommunicationIdentityClient.from_connection_string(ACS_CONNECTION_STRING)


@app.route("/get_token", methods=["POST"])
def get_token():
    try:
        data = request.json
        store_name = data.get("storeName")

        if not store_name:
            return jsonify({"error": "storeName is required"}), 400

        # สร้าง user ใหม่
        user = identity_client.create_user()

        # ขอ token สำหรับ user
        token_response = identity_client.get_token(user, scopes=["voip", "chat"])

        # สร้าง group_id จาก storeName
        group_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(store_name)))

        # ดึง user_id จาก user object
        user_id = getattr(user, "identifier", None) or user.properties.get("id")

        print(f"[DEBUG] user_id: {user_id}")
        print(f"[DEBUG] token: {token_response.token}")
        print(f"[DEBUG] expires_on: {token_response.expires_on}")

        return jsonify({
            "userId": user_id,
            "token": token_response.token,
            "expiresOn": token_response.expires_on,  # แก้ตรงนี้ ไม่ใช้ .isoformat()
            "groupId": group_id
        })
    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
