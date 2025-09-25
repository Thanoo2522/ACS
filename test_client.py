import requests

url = "https://acs-e9lu.onrender.com/get_token" 
payload = {"storeName": "TA"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)

print("Status Code:", response.status_code)
print("Response Text:", response.text)   # 👈 ดูว่ามี error อะไร