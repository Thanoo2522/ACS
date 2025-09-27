import requests

# 👉 เปลี่ยนให้เป็น endpoint ที่ Flask (Render) คุณทำสำหรับ Agora
url = "https://acs-e9lu.onrender.com//get_token"

payload = {
    "channelName": "TA",   # ใช้ channelName แทน storeName
    "uid": 123             # สามารถ fix หรือสุ่ม uid ก็ได้
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())  # ใช้ json() จะอ่านง่ายกว่า
