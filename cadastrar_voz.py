import os
import shutil

from audio.gravacao import gravar_audio
from audio.reconhecimento_voz import cadastrar_voz


PASTA_VOZES = r"C:\Users\User\Downloads\Assistente\audio\vozes_mateus"

os.makedirs(
    PASTA_VOZES,
    exist_ok=True
)

arquivos = []


print("======================================")
print("       CADASTRO DE VOZ - JARVIS")
print("======================================")
print()
print("Vamos gravar 3 amostras da sua voz.")
print("Fale naturalmente em cada uma.")
print()


for numero in range(1, 6):

    input(
        f"Pressione ENTER para gravar a amostra {numero}..."
    )

    audio = gravar_audio()

    destino = os.path.join(
        PASTA_VOZES,
        f"voz_{numero}.wav"
    )

    shutil.copyfile(
        audio,
        destino
    )

    arquivos.append(
        destino
    )

    print(
        f"✅ Amostra {numero} salva."
    )

    print()


cadastrar_voz(
    arquivos
)