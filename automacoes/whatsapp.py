import pyautogui
import subprocess
import time
import urllib.parse


def ligar_whatsapp(nome, telefone):
    print(f"📞 Ligando para {nome}...")

    url = f"https://wa.me/{telefone}"

    subprocess.Popen([
        "cmd", "/c",
        "start", "",
        url
    ])

    time.sleep(4)

    return f"Ligando para {nome}."


def mandar_mensagem(nome, telefone, mensagem):
    print(f"💬 Mandando mensagem para {nome}...")

    mensagem_codificada = urllib.parse.quote(mensagem)

    url = f"https://wa.me/{telefone}?text={mensagem_codificada}"

    subprocess.Popen([
        "cmd", "/c",
        "start", "",
        url
    ])

    time.sleep(4)

    pyautogui.press("enter")

    return f"Mensagem enviada para {nome}."


def desligar_ligacao():
    print("📴 Encerrando ligação...")

    pyautogui.press("esc")

    return "Ligação encerrada."