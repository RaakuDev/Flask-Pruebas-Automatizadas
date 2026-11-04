
import json
import time
import urllib.parse
import urllib.request

ZAP_URL = "http://172.17.0.5:8090"
TARGET = "http://host.docker.internal:5000/hello?name=TEST"


def zap_request(endpoint, params=None):
    query = urllib.parse.urlencode(params or {})
    url = f"{ZAP_URL}{endpoint}"
    if query:
        url += f"?{query}"

    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


print("Iniciando análisis OWASP ZAP...")

# Registrar la URL en ZAP.
zap_request("/JSON/core/action/accessUrl/", {
    "url": TARGET,
    "followRedirects": "true"
})

# Esperar a que termine el análisis pasivo.
for _ in range(60):
    remaining = zap_request("/JSON/pscan/view/recordsToScan/")
    if int(remaining["recordsToScan"]) == 0:
        break
    time.sleep(2)
else:
    raise RuntimeError("ZAP no terminó el análisis pasivo a tiempo.")

# Obtener las alertas detectadas.
result = zap_request("/JSON/core/view/alerts/", {
    "baseurl": TARGET,
    "start": 0,
    "count": 1000
})

alerts = result.get("alerts", [])

print(f"Análisis finalizado. Alertas detectadas: {len(alerts)}")

for alert in alerts:
    print(f"[{alert['risk']}] {alert['name']}")

# Guardar resultados para Jenkins.
with open("zap-results.json", "w", encoding="utf-8") as file:
    json.dump(alerts, file, indent=4, ensure_ascii=False)

print("Resultados guardados en zap-results.json")
