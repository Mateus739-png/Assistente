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
# 1. PEGAR TOKEN
# ==========================================================

resposta = enviar(
    "AuthenticationTokenRequest",
    {
        "pluginName": "Jarvis",
        "pluginDeveloper": "Mateus"
    }
)

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

if not resposta["data"]["authenticated"]:
    print("❌ Falha na autenticação.")
    ws.close()
    exit()


print("✅ Jarvis conectado ao VTube Studio.")


# ==========================================================
# 3. ATIVAR ANIMAÇÃO
# ==========================================================

resposta = enviar(
    "HotkeyTriggerRequest",
    {
        "hotkeyID": "87ae0e4011f147a6954fac47317bf04c"
    }
)

print()
print("🎭 Animação acionada!")
print(resposta)

ws.close()