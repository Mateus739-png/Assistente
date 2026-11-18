

import threading
import time
from ia.tts import falar


def iniciar_cronometro(tempo, unidade="minutos"):
    try:
        tempo = float(tempo)

        if tempo <= 0:
            return "O tempo precisa ser maior que zero."

        if unidade.lower().startswith("h"):
            segundos = int(tempo * 3600)
        elif unidade.lower().startswith("s"):
            segundos = int(tempo)
        else:
            segundos = int(tempo * 60)

        if segundos <= 0:
            return "O tempo precisa ser de pelo menos um segundo."

        def finalizar():
            for restante in range(segundos, 0, -1):
                print(f"⏱️ {restante} segundo(s)")
                time.sleep(1)

            print("⏰ TEMPO ESGOTADO!")
            falar("Seu temporizador acabou.")

        threading.Thread(target=finalizar, daemon=True).start()

        return f"Temporizador iniciado por {segundos} segundos."

    except (ValueError, TypeError):
        return "Não consegui entender o tempo."


def reconhecer_temporizador(texto):
    import re

    texto = texto.lower().strip()

    gatilhos = [
        "temporizador",
        "timer",
        "cronômetro",
        "cronometro",
        "contagem regressiva",
    ]

    if not any(gatilho in texto for gatilho in gatilhos):
        return None

    # Aceita números como 5, 5.5 ou 5,5.
    correspondencia = re.search(
        r"(\d+(?:[.,]\d+)?)\s*"
        r"(segundos?|secs?|s|minutos?|mins?|min|horas?|hrs?|h)\b",
        texto,
    )

    if not correspondencia:
        return "Diga a duração, por exemplo: temporizador de 5 segundos."

    valor = float(correspondencia.group(1).replace(",", "."))
    unidade = correspondencia.group(2)

    if unidade.startswith("s"):
        unidade = "segundos"
    elif unidade.startswith("h"):
        unidade = "horas"
    else:
        unidade = "minutos"

    return iniciar_cronometro(valor, unidade)
