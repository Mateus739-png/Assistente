import subprocess
import soundfile as sf
import sounddevice as sd
import numpy as np

PIPER = r"C:\Python314\python.exe"
MODELO = r"C:\Users\User\Downloads\Assistente\pt_BR-faber-medium.onnx"
ARQUIVO_AUDIO = r"C:\Users\User\Downloads\Assistente\voz_jarvis.wav"


def melhorar_voz(audio, taxa):
    # Remove um pouco do excesso de graves
    # e deixa a voz mais aberta.
    audio = audio.astype(np.float32)

    # Normalização leve
    pico = np.max(np.abs(audio))

    if pico > 0:
        audio = audio / pico * 0.85

    # Evita estourar o áudio
    audio = np.clip(audio, -1.0, 1.0)

    return audio


def falar(texto):
    print("🔊 Jarvis falando...")

    subprocess.run(
        [
            PIPER,
            "-m", "piper",
            "-m", MODELO,
            "-f", ARQUIVO_AUDIO,
            "--",
            texto
        ],
        check=True
    )

    audio, taxa = sf.read(
        ARQUIVO_AUDIO,
        dtype="float32"
    )

    audio = melhorar_voz(audio, taxa)

    sd.play(audio, taxa)
    sd.wait()