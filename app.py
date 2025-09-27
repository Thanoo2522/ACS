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

@app.route("/get_token", methods=["POST"])
def get_token():
    try:
        data = request.json
        store_name = data.get("storeName")

        if not store_name:
            return jsonify({"error": "storeName is required"}), 400

        # สร้าง channel name จาก storeName
        channel_name = str(uuid.uuid5(uuid.NAMESPACE_DNS, str(store_name)))

        # สร้าง user ID (random หรือจาก client)
        uid = int(uuid.uuid4().int & 0xFFFFFFFF)

        # เวลา token หมดอายุ (เช่น 1 ชั่วโมง)
        expire_time_in_seconds = 3600
        current_timestamp = int(uuid.uuid1().time / 1e7)  # Timestamp ปัจจุบัน
        privilege_expire_time = current_timestamp + expire_time_in_seconds

        # สร้าง Agora RTC token
        token = RtcTokenBuilder.buildTokenWithUid(
            AGORA_APP_ID,
            AGORA_APP_CERTIFICATE,
            channel_name,
            uid,
            role=RtcTokenBuilder.Role_Attendee,
            privilege_expire_time=privilege_expire_time
        )

        print(f"[DEBUG] channel_name: {channel_name}")
        print(f"[DEBUG] uid: {uid}")
        print(f"[DEBUG] token: {token}")

        return jsonify({
            "channelName": channel_name,
            "uid": uid,
            "token": token,
            "expiresOn": privilege_expire_time
        })

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
