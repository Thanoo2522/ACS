import os
from flask import Flask, jsonify
from azure.communication.identity import CommunicationIdentityClient
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

ACS_CONNECTION_STRING = os.getenv("ACS_CONNECTION_STRING")
identity_client = CommunicationIdentityClient.from_connection_string(ACS_CONNECTION_STRING)

@app.route("/get_token")
def get_token():
    user = identity_client.create_user()
    token_response = identity_client.get_token(user, scopes=["voip","chat"])
    return jsonify({
        "userId": user.properties["id"],
        "token": token_response.token
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
