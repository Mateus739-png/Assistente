import ctypes
import subprocess


HWND_BROADCAST = 0xFFFF
WM_SYSCOMMAND = 0x0112
SC_MONITORPOWER = 0xF170


def apagar_tela():
    ctypes.windll.user32.SendMessageW(
        HWND_BROADCAST,
        WM_SYSCOMMAND,
        SC_MONITORPOWER,
        2
    )

    return "Tela desligada."


def ligar_tela():
    ctypes.windll.user32.SendMessageW(
        HWND_BROADCAST,
        WM_SYSCOMMAND,
        SC_MONITORPOWER,
        -1
    )

    return "Tela ligada."


def bloquear_tela():
    ctypes.windll.user32.LockWorkStation()

    return "Tela bloqueada."


def estender_telas():
    subprocess.run(
        [
            r"C:\Windows\System32\DisplaySwitch.exe",
            "/extend"
        ],
        check=True
    )

    return "Telas estendidas."


def duplicar_telas():
    subprocess.run(
        [
            r"C:\Windows\System32\DisplaySwitch.exe",
            "/clone"
        ],
        check=True
    )

    return "Telas duplicadas."

# ==========================================================
# PRINT / CAPTURA DE TELA
# ==========================================================

from PIL import ImageGrab
import os
from datetime import datetime


PASTA_PRINTS = r"C:\Users\User\Downloads\Assistente\prints"


def tirar_print():
    os.makedirs(
        PASTA_PRINTS,
        exist_ok=True
    )

    agora = datetime.now()

    nome_arquivo = agora.strftime(
        "print_%Y-%m-%d_%H-%M-%S.png"
    )

    caminho = os.path.join(
        PASTA_PRINTS,
        nome_arquivo
    )

    try:
        imagem = ImageGrab.grab(
            all_screens=True
        )

        imagem.save(
            caminho
        )

        print(f"📸 Print salvo em: {caminho}")

        return "Print tirado e salvo com sucesso."

    except Exception as erro:

        print(
            f"⚠️ Erro ao tirar print: {erro}"
        )

        return "Não consegui tirar o print."
    
    # ==========================================================
    # PEGAR O ÚLTIMO PRINT
    # ==========================================================

def obter_ultimo_print():
    if not os.path.exists(PASTA_PRINTS):
        return None

    arquivos = [
        os.path.join(PASTA_PRINTS, arquivo)
        for arquivo in os.listdir(PASTA_PRINTS)
        if arquivo.lower().endswith(".png")
        and arquivo.lower().startswith("print_")
    ]

    if not arquivos:
        return None

    return max(
        arquivos,
        key=os.path.getmtime
    )