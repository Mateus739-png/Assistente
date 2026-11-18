import json
import uuid
import websocket

VTS_URL = "ws://localhost:8001"

ws = websocket.create_connection(VTS_URL)

pedido = {
    "apiName": "VTubeStudioPublicAPI",
    "apiVersion": "1.0",
    "requestID": str(uuid.uuid4()),
    "messageType": "AuthenticationTokenRequest",
    "data": {
        "pluginName": "Jarvis",
        "pluginDeveloper": "Mateus"
    }
}

ws.send(json.dumps(pedido))

resposta = json.loads(ws.recv())

print("Resposta do VTube Studio:")
print(json.dumps(resposta, indent=4, ensure_ascii=False))

ws.close()