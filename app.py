import os
from flask import Flask, jsonify
from azure.communication.identity import CommunicationIdentityClient
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# อ่าน Connection String จาก .env
ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")
identity_client = CommunicationIdentityClient.from_connection_string(ACS_CONNECTION_STRING)

@app.route("/get_token")
def get_token():
    # สร้าง User Identity ใหม่
    user = identity_client.create_user()

    # ออก Access Token สำหรับ user
    token_response = identity_client.issue_token(user, scopes=["voip", "chat"])

    return jsonify({
        "userId": user.id,
        "token": token_response.token,
        "expiresOn": token_response.expires_on.isoformat()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
