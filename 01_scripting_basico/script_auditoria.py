import json
import os
import requests
import urllib3
urllib3.disable_warnings()

url = "https://10.10.20.66/restconf/data/ietf-interfaces:interfaces"
headers = {"Accept": "application/yang-data+json"}
auth = ("admin", "CiscoPassword123!")

try:
    response = requests.get(url, auth=auth, headers=headers, verify=False, timeout=5)
    response.raise_for_status()
    datos = response.json()
    print("Tas conecto al router, todo salio joya")
except Exception as e:
    print("El router no responde, solo esta leyendo el response.json local")
    with open("response.json", "r") as f:
        datos = json.load(f)

interfaces = datos["ietf-interfaces:interfaces"]["interface"]
activas = []

for i in interfaces:
    ip_info = i.get("ietf-ip:ipv4", {})
    if i.get("enabled") == True and "address" in ip_info:
        activas.append({
            "nombre": i["name"],
            "ip": ip_info["address"][0]["ip"],
            "mascara": ip_info["address"][0]["netmask"],
            "activa": i["enabled"]
        })
with open("inventario_interfaces.json", "w") as archivo:
    json.dump(activas. archivo, indent=4)
print("Ya quedo, se creo el inventario_interfaces.json")