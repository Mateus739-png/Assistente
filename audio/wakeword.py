import sounddevice as sd
import numpy as np
import time
from openwakeword.model import Model

SAMPLE_RATE = 16000
CHUNK = 1280

THRESHOLD = 0.60
CONSECUTIVE_HITS = 2

model = Model(
    wakeword_models=["hey_jarvis"],
    inference_framework="onnx"
)


def limpar_microfone(stream, segundos=1.5):

    blocos = int((SAMPLE_RATE * segundos) / CHUNK)

    for _ in range(blocos):
        stream.read(CHUNK)


def detectar_wakeword():

    acertos = 0

    print("👂 Aguardando: Hey Jarvis...")

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        blocksize=CHUNK
    ) as stream:

        # Descarta o áudio que ficou no buffer
        limpar_microfone(stream, 1.5)

        # Reinicia o estado do modelo
        model.reset()

        while True:

            audio, _ = stream.read(CHUNK)

            audio = np.squeeze(audio)

            resultado = model.predict(audio)

            if not resultado:
                continue

            confianca = max(resultado.values())

            if confianca >= THRESHOLD:

                acertos += 1

                print(
                    f"\r🎯 {confianca:.2f} "
                    f"({acertos}/{CONSECUTIVE_HITS})",
                    end="",
                    flush=True
                )

                if acertos >= CONSECUTIVE_HITS:

                    print()
                    print("🚀 WAKE WORD DETECTADA!")
                    print()

                    return True

            else:

                acertos = 0