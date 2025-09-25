import os
import uuid
import traceback
from flask import Flask, jsonify, request
from azure.communication.identity import CommunicationIdentityClient

app = Flask(__name__)

# ✅ ใช้ environment variable จาก Render โดยตรง
ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")

if not ACS_CONNECTION_STRING:
    raise ValueError("❌ Environment variable 'ACS_CONNECTION_STRING' is not set on Render.")

identity_client = CommunicationIdentityClient.from_connection_string(ACS_CONNECTION_STRING)

@app.route("/get_token", methods=["POST"])
def get_token():
    try:
        data = request.json
        store_name = data.get("storeName")

        if not store_name:
            return jsonify({"error": "storeName is required"}), 400

        user = identity_client.create_user()
        token_response = identity_client.get_token(user, scopes=["voip", "chat"])

        group_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(store_name)))
        user_id = getattr(user, "identifier", None) or getattr(user, "properties", {}).get("id")

        return jsonify({
            "userId": user_id,
            "token": token_response.token,
            "expiresOn": token_response.expires_on.isoformat(),
            "groupId": group_id
        })
    except Exception as e:
        print("❌ ERROR in /get_token:", e)
        traceback.print_exc()   # log ลง console
        return jsonify({"error": str(e)}), 500
