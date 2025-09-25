import os
import uuid
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from azure.communication.identity import CommunicationIdentityClient

load_dotenv()

app = Flask(__name__)

ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")
identity_client = CommunicationIdentityClient.from_connection_string(ACS_CONNECTION_STRING)

@app.route("/get_token", methods=["POST"])
def get_token():
    data = request.json
    store_name = data.get("storeName")

    if not store_name:
        return jsonify({"error": "storeName is required"}), 400

    user = identity_client.create_user()
    token_response = identity_client.get_token(user, scopes=["voip", "chat"])

    group_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(store_name)))

    user_id = getattr(user, "identifier", None) or user.properties.get("id")

    return jsonify({
        "userId": user_id,
        "token": token_response.token,
        "expiresOn": token_response.expires_on.isoformat(),
        "groupId": group_id
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
