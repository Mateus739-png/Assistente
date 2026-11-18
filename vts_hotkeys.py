import json
import uuid
import websocket

VTS_URL = "ws://localhost:8001"

ws = websocket.create_connection(VTS_URL)


def enviar(tipo, dados):
    ws.send(json.dumps({
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": str(uuid.uuid4()),
        "messageType": tipo,
        "data": dados
    }))

    return json.loads(ws.recv())


# ==========================================================
# 1. PEDIR TOKEN
# ==========================================================

resposta = enviar(
    "AuthenticationTokenRequest",
    {
        "pluginName": "Jarvis",
        "pluginDeveloper": "Mateus"
    }
)

print("TOKEN:")
print(resposta)

token = resposta["data"]["authenticationToken"]


# ==========================================================
# 2. AUTENTICAR
# ==========================================================

resposta = enviar(
    "AuthenticationRequest",
    {
        "pluginName": "Jarvis",
        "pluginDeveloper": "Mateus",
        "authenticationToken": token
    }
)

print()
print("AUTENTICAÇÃO:")
print(resposta)


# ==========================================================
# 3. PEGAR HOTKEYS
# ==========================================================

resposta = enviar(
    "HotkeysInCurrentModelRequest",
    {}
)

print()
print("HOTKEYS DA PERSONAGEM:")
print(json.dumps(resposta, indent=4, ensure_ascii=False))


ws.close()