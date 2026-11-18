from pycaw.pycaw import AudioUtilities


def obter_dispositivo():
    dispositivos = AudioUtilities.GetSpeakers()
    return dispositivos.EndpointVolume


def obter_volume():
    volume = obter_dispositivo()
    nivel = volume.GetMasterVolumeLevelScalar()
    return round(nivel * 100)


def definir_volume(valor):
    valor = max(0, min(100, valor))

    volume = obter_dispositivo()
    volume.SetMasterVolumeLevelScalar(valor / 100, None)

    return f"Volume definido para {valor}%."


def aumentar_volume():
    atual = obter_volume()
    return definir_volume(min(100, atual + 10))


def diminuir_volume():
    atual = obter_volume()
    return definir_volume(max(0, atual - 10))


def falar_volume():
    return f"O volume está em {obter_volume()}%."


def mutar_volume():
    volume = obter_dispositivo()
    volume.SetMute(1, None)
    return "Volume mutado."


def desmutar_volume():
    volume = obter_dispositivo()
    volume.SetMute(0, None)
    return "Volume desmutado."


# ==========================================================
# VOLUME POR APLICATIVO
# ==========================================================

def encontrar_aplicativo(nome):
    sessoes = AudioUtilities.GetAllSessions()

    for sessao in sessoes:
        processo = sessao.Process

        if processo is None:
            continue

        if processo.name().lower() == nome.lower():
            return sessao.SimpleAudioVolume

    return None


def mutar_aplicativo(nome):
    volume = encontrar_aplicativo(nome)

    if volume is None:
        return f"{nome} não está aberto ou não possui áudio."

    volume.SetMute(1, None)

    return f"{nome} mutado."


def desmutar_aplicativo(nome):
    volume = encontrar_aplicativo(nome)

    if volume is None:
        return f"{nome} não está aberto ou não possui áudio."

    volume.SetMute(0, None)

    return f"{nome} desmutado."


def mutar_spotify():
    return mutar_aplicativo("Spotify.exe")


def desmutar_spotify():
    return desmutar_aplicativo("Spotify.exe")


def mutar_discord():
    return mutar_aplicativo("Discord.exe")


def desmutar_discord():
    return desmutar_aplicativo("Discord.exe")