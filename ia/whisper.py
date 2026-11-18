import subprocess
import re

WHISPER = r"C:\Users\User\Downloads\whisper-cli.exe"
WHISPER_MODEL = r"C:\Users\User\Downloads\ggml-medium.bin"


def transcrever(audio):
    comando = [
        WHISPER,
        "-m", WHISPER_MODEL,
        "-f", audio,

        "-l", "pt",
        "-nt",
        "-np",

        "--temperature", "0",
        "--temperature-inc", "0.2",

        "--max-context", "0",
        "--max-len", "0",

        "--print-progress", "false"
    ]

    resultado = subprocess.run(
        comando,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore"
    )

    texto = resultado.stdout.strip()

    texto = re.sub(
        r"\[\d\d:\d\d:\d\d\.\d\d\d --> \d\d:\d\d:\d\d\.\d\d\d\]",
        "",
        texto
    )

    texto = texto.replace("\n", " ")
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()