import os
import uuid
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from agora_token_builder import RtcTokenBuilder

load_dotenv()

app = Flask(__name__)

AGORA_APP_ID = os.getenv("AGORA_APP_ID")
AGORA_APP_CERTIFICATE = os.getenv("AGORA_APP_CERTIFICATE")
if not AGORA_APP_ID or not AGORA_APP_CERTIFICATE:
    raise ValueError("❌ AGORA_APP_ID หรือ AGORA_APP_CERTIFICATE ไม่ถูกตั้งค่าใน .env")

app.route("/get_token", methods=["POST"])
def get_token():
    try:
        data = request.json
        channel_name = data.get("channelName")
        uid = data.get("uid", 0)

        if not channel_name:
            return jsonify({"error": "channelName is required"}), 400

        expiration_time_in_seconds = 3600  # token อายุ 1 ชม.
        current_timestamp = int(time.time())
        privilege_expired_ts = current_timestamp + expiration_time_in_seconds

        # สร้าง RTC token
        token = RtcTokenBuilder.buildTokenWithUid(
            AGORA_APP_ID, AGORA_APP_CERTIFICATE,
            channel_name, uid, 1, privilege_expired_ts
        )

        return jsonify({
            "appId": AGORA_APP_ID,
            "channelName": channel_name,
            "uid": uid,
            "token": token
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
