import time
import threading

import numpy as np
import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16000
CHANNELS = 1
AUDIO_FILE = r"C:\Users\User\Downloads\Assistente\voz_temp.wav"
AULA_FILE = r"C:\Users\User\Downloads\Assistente\aula_teams.wav"

# Configurações
SILENCIO_SEGUNDOS = 0.8
TEMPO_MAXIMO = 8
TEMPO_MINIMO = 0.4

# Sensibilidade do microfone
LIMIAR_RMS = 0.015


def listar_dispositivos():
    try:
        return sd.query_devices()
    except Exception as erro:
        raise RuntimeError(f"Não foi possível listar os dispositivos de áudio: {erro}") from erro


def encontrar_dispositivo_vb_cable():
    try:
        dispositivos = listar_dispositivos()
    except Exception:
        return None

    # O áudio da aula do Teams precisa vir pelo OUTPUT do VB-Cable,
    # não pelo INPUT do virtual cable, que normalmente é um canal 16ch
    # e não aceita a configuração usada pela gravação da aula.
    for indice, dispositivo in enumerate(dispositivos):
        nome = str(dispositivo).lower()
        if isinstance(dispositivo, dict):
            nome = str(dispositivo.get("name", "")).lower()

        if "cable" in nome and "output" in nome:
            return indice

    # Fallback conservador para outros nomes do fabricante.
    for indice, dispositivo in enumerate(dispositivos):
        nome = str(dispositivo).lower()
        if isinstance(dispositivo, dict):
            nome = str(dispositivo.get("name", "")).lower()

        if "vb-audio" in nome or "virtual cable" in nome:
            return indice

    return None


def gravar_audio(device=None, tempo_maximo=TEMPO_MAXIMO, caminho=AUDIO_FILE, canais=None):
    if device is None:
        device = encontrar_dispositivo_vb_cable()

    if device is not None:
        print()
        print("🎧 Dispositivo de aula detectado via VB-Cable.")
        print("📼 Gravando áudio da aula do Teams.")
        if canais is None:
            canais = 2
    else:
        print()
        print("🔴 OUVINDO...")
        print("🗣️ Fale seu comando.")
        if canais is None:
            canais = CHANNELS

    blocos = []
    bloco_tamanho = 320

    inicio = time.time()
    inicio_fala = None
    ultimo_som = time.time()

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=canais,
        dtype="float32",
        blocksize=bloco_tamanho,
        device=device,
    ) as stream:

        while True:
            audio, _ = stream.read(bloco_tamanho)
            audio = np.squeeze(audio)

            if audio.size == 0:
                continue

            rms = np.sqrt(np.mean(audio ** 2))
            agora = time.time()

            if device is None:
                if rms >= LIMIAR_RMS:
                    if inicio_fala is None:
                        inicio_fala = agora
                        print("🎙️ Voz detectada...")
                    ultimo_som = agora

                if inicio_fala is not None:
                    silencio = agora - ultimo_som
                    if silencio >= SILENCIO_SEGUNDOS:
                        print("⏹️ Silêncio detectado.")
                        break
            else:
                if inicio_fala is None:
                    inicio_fala = agora
                    print("🎵 Capturando áudio da aula...")
                ultimo_som = agora

            if agora - inicio >= tempo_maximo:
                print("⏹️ Tempo máximo atingido.")
                break

            blocos.append(audio.copy())

    if not blocos:
        print("⚠️ Nenhum áudio capturado.")
        return caminho

    gravacao = np.concatenate(blocos)

    if len(gravacao) / SAMPLE_RATE < TEMPO_MINIMO:
        print("⚠️ Áudio muito curto.")

    sf.write(caminho, gravacao, SAMPLE_RATE)

    duracao = len(gravacao) / SAMPLE_RATE
    print(f"✅ Gravação finalizada ({duracao:.1f}s).")

    return caminho


def gravar_aula_teams(tempo_maximo=600, caminho=AULA_FILE):
    dispositivo = encontrar_dispositivo_vb_cable()

    if dispositivo is None:
        print("⚠️ VB-Cable não encontrado. Usando microfone como fallback.")
        return gravar_audio(device=None, tempo_maximo=tempo_maximo, caminho=caminho)

    print(f"🎧 Dispositivo VB-Cable encontrado no índice {dispositivo}.")
    print("📌 Usando o canal de saída do VB-Cable para capturar a aula do Teams.")
    return gravar_audio(device=dispositivo, tempo_maximo=tempo_maximo, caminho=caminho, canais=2)


def classificar_comando_aula(texto):
    if texto is None:
        return None

    texto = texto.lower().strip()
    frase = " ".join(texto.split())

    iniciar = (
        "iniciar" in frase or "começar" in frase or "inicie" in frase or "comece" in frase
    ) and (
        "grava" in frase or "gravar" in frase or "gravação" in frase or "aula" in frase
    )

    parar = (
        "parar" in frase or "encerrar" in frase or "terminar" in frase or "finalizar" in frase
    ) and (
        "grava" in frase or "gravar" in frase or "gravação" in frase or "aula" in frase
    )

    if iniciar:
        return "iniciar"
    if parar:
        return "parar"
    return None


def gravar_aula_continua(caminho=AULA_FILE, stop_event=None, max_segundos=3600):
    dispositivo = encontrar_dispositivo_vb_cable()

    if dispositivo is None:
        raise RuntimeError("VB-Cable não encontrado. Configure o dispositivo virtual antes de gravar a aula.")

    blocos = []
    bloco_tamanho = 320
    inicio = time.time()

    def parar_stream(stream):
        if stop_event is None:
            return

        stop_event.wait()
        try:
            stream.stop()
            print("⏹️ Parada manual solicitada.")
        except Exception:
            pass

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=2,
            dtype="float32",
            blocksize=bloco_tamanho,
            device=dispositivo,
        ) as stream:
            if stop_event is not None:
                monitor = threading.Thread(target=parar_stream, args=(stream,), daemon=True)
                monitor.start()

            while True:
                if stop_event is not None and stop_event.is_set():
                    break

                if time.time() - inicio >= max_segundos:
                    print("⏹️ Limite máximo de gravação atingido.")
                    break

                try:
                    audio, _ = stream.read(bloco_tamanho)
                except Exception:
                    if stop_event is not None and stop_event.is_set():
                        break
                    raise

                if audio.size == 0:
                    continue

                blocos.append(np.squeeze(audio).copy())
    except KeyboardInterrupt:
        print("⏹️ Parada manual via Ctrl+C detectada.")

    if not blocos:
        print("⚠️ Nenhum áudio da aula foi capturado.")
        return caminho

    gravacao = np.concatenate(blocos)
    sf.write(caminho, gravacao, SAMPLE_RATE)
    print(f"✅ Gravação da aula finalizada. Arquivo: {caminho}")
    return caminho


# Compatibilidade com o código antigo
# gravar_audio() continua funcionando para comandos por voz.