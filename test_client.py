import requests

url = "https://acs-e9lu.onrender.com/get_token"  # ✅ แก้ / ให้ถูก
payload = {
    "channelName": "TA",
    "uid": 123
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)

try:
    print("Response JSON:", response.json())
except requests.exceptions.JSONDecodeError:
    print("Response Text:", response.text)  # ถ้าไม่ใช่ JSON จะแสดงข้อความดิบ
