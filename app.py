import os
import uuid
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from azure.communication.identity import CommunicationIdentityClient

# โหลดค่า environment จากไฟล์ .env (เฉพาะตอนรัน local)
load_dotenv()

app = Flask(__name__)

# อ่านค่า ACS_CONNECTION_STRING จาก environment variable
ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")

if not ACS_CONNECTION_STRING:
    raise ValueError("❌ ACS_CONNECTION_STRING is not set. "
                     "Please configure it in Render Environment Variables.")

# สร้าง client สำหรับติดต่อกับ Azure Communication Services
identity_client = CommunicationIdentityClient.from_connection_string(ACS_CONNECTION_STRING)

@app.route("/get_token", methods=["POST"])
def get_token():
    try:
        data = request.json
        store_name = data.get("storeName")

        if not store_name:
            return jsonify({"error": "storeName is required"}), 400

        # สร้าง user identity ใหม่
        user = identity_client.create_user()

        # ขอ token สำหรับ user นี้
        token_response = identity_client.get_token(user, scopes=["voip", "chat"])

        # ใช้ store_name สร้าง groupId (จะได้ค่าเดิมทุกครั้งถ้า store_name เดิม)
        group_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(store_name)))

        # userId ต้องใช้ property "id"
        user_id = getattr(user, "identifier", None) or user.properties.get("id")

        return jsonify({
            "userId": user_id,
            "token": token_response.token,
            "expiresOn": token_response.expires_on.isoformat(),
            "groupId": group_id
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # host=0.0.0.0 → ให้ Flask เปิดให้เข้าจากภายนอกได้ (Render ใช้ได้)
    app.run(host="0.0.0.0", port=5000, debug=True)
