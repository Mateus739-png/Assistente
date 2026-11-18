import subprocess

def desligar():
    subprocess.Popen(["shutdown", "/s", "/t", "10"])
    return "O computador será desligado em 10 segundos."

def reiniciar():
    subprocess.Popen(["shutdown", "/r", "/t", "10"])
    return "O computador será reiniciado em 10 segundos."