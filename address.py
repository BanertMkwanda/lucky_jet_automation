import requests
ip = requests.get("https://ifconfig.me").text.strip()
print(f"{i}")
