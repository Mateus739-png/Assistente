import os
import subprocess


def abrir_programa(nome, mensagem):
    try:
        # Primeiro tenta abrir normalmente
        subprocess.Popen([nome])
        return mensagem

    except FileNotFoundError:
        # Caminhos comuns dos programas
        caminhos = {
            "steam": [
                r"C:\Program Files (x86)\Steam\steam.exe",
                r"C:\Program Files\Steam\steam.exe"
            ],

            "code": [
                r"C:\Program Files\Microsoft VS Code\Code.exe",
                os.path.expandvars(
                    r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
                )
            ],

            "edge": [
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
            ],

            "chrome": [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ]
        }

        if nome in caminhos:
            for caminho in caminhos[nome]:
                if os.path.exists(caminho):
                    subprocess.Popen([caminho])
                    return mensagem

        print(f"⚠️ Programa não encontrado: {nome}")
        return f"Não consegui abrir {nome}."

    except Exception as erro:
        print(f"⚠️ Erro ao abrir {nome}: {erro}")
        return f"Não consegui abrir {nome}."


def abrir_link(link, mensagem):
    try:
        os.startfile(link)
        return mensagem
    except Exception as erro:
        print(f"⚠️ Erro ao abrir {link}: {erro}")
        return mensagem


# ==========================================================
# PROGRAMAS
# ==========================================================

def abrir_edge():
    return abrir_programa(
        "edge",
        "Abrindo o Edge."
    )


def abrir_chrome():
    return abrir_programa(
        "chrome",
        "Abrindo o Google Chrome."
    )


def abrir_calculadora():
    return abrir_programa(
        "calc.exe",
        "Abrindo a calculadora."
    )


def abrir_steam():
    try:
        caminho = r"C:\Program Files (x86)\Steam\steam.exe"
        subprocess.Popen([caminho])
        return "Abrindo a Steam."
    except Exception as erro:
        print(f"⚠️ Erro ao abrir Steam: {erro}")
        return "Não consegui abrir a Steam."


def abrir_vscode():
    try:
        caminhos = [
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe")
        ]

        for caminho in caminhos:
            if os.path.exists(caminho):
                subprocess.Popen([caminho])
                return "Abrindo o VS Code."

        return "Não encontrei o VS Code instalado."

    except Exception as erro:
        print(f"⚠️ Erro ao abrir VS Code: {erro}")
        return "Não consegui abrir o VS Code."


# ==========================================================
# SITES / APLICATIVOS
# ==========================================================

def abrir_whatsapp():
    return abrir_link(
        "https://web.whatsapp.com",
        "Abrindo o WhatsApp."
    )

def abrir_spotify():
    try:
        os.startfile("spotify:")
        return "Abrindo o Spotify."
    except Exception as erro:
        print(f"⚠️ Erro ao abrir Spotify: {erro}")
        return "Não consegui abrir o Spotify."

    except Exception as erro:
        print(f"⚠️ Erro ao abrir Spotify: {erro}")
        return "Não consegui abrir o Spotify."



def abrir_discord():
    return abrir_link(
        "discord://",
        "Abrindo o Discord."
    )


# ==========================================================
# JOGOS STEAM
# ==========================================================

def abrir_rocket_league():
    return abrir_link(
        "steam://rungameid/252950",
        "Abrindo o Rocket League."
    )


def abrir_breakpoint():
    return abrir_link(
        "steam://rungameid/2231380",
        "Abrindo o Ghost Recon Breakpoint."
    )


def abrir_stormworks():
    return abrir_link(
        "steam://rungameid/573090",
        "Abrindo o Stormworks."
    )


def abrir_motorfest():
    return abrir_link(
        "steam://rungameid/2698940",
        "Abrindo o The Crew Motorfest."
    )


def abrir_carx_street():
    return abrir_link(
        "steam://rungameid/1119730",
        "Abrindo o CarX Street."
    )


def abrir_pubg():
    return abrir_link(
        "steam://rungameid/578080",
        "Abrindo o PUBG."
    )


def abrir_watch_dogs_2():
    return abrir_link(
        "steam://rungameid/447040",
        "Abrindo o Watch Dogs 2."
    )


# ==========================================================
# TLAUNCHER
# ==========================================================

def abrir_tlauncher():
    try:
        os.startfile("TLauncher")
        return "Abrindo o TLauncher."
    except Exception as erro:
        print(f"⚠️ Erro ao abrir TLauncher: {erro}")
        return "Não consegui abrir o TLauncher."


# ==========================================================
# PROJETO SEXTA-FEIRA
# ==========================================================

def abrir_projeto_sexta_feira():
    pasta = r"C:\SextaFeira"

    arquivos = [
        r"C:\SextaFeira\main.py",
        r"C:\SextaFeira\teste_wake.py",
        r"C:\SextaFeira\vts.py",
        r"C:\SextaFeira\ia\tts.py",
    ]

    try:
        subprocess.Popen([
            "code",
            pasta,
            *arquivos
        ])

        os.startfile("https://chatgpt.com")

        return (
            "Projeto Sexta-feira iniciado. "
            "VS Code e ChatGPT estão abrindo."
        )

    except Exception as erro:
        print(f"⚠️ Erro ao abrir Projeto Sexta-feira: {erro}")
        return "Tive um problema ao abrir o Projeto Sexta-feira."
    return "Projeto Sexta-feira iniciado. VS Code e ChatGPT estão abrindo."

import ctypes


# ==========================================================
# CONTROLE DE MÍDIA
# ==========================================================

VK_MEDIA_NEXT_TRACK = 0xB0
VK_MEDIA_PREV_TRACK = 0xB1
VK_MEDIA_PLAY_PAUSE = 0xB3


def _pressionar_tecla_midia(tecla):
    ctypes.windll.user32.keybd_event(
        tecla,
        0,
        0,
        0
    )

    ctypes.windll.user32.keybd_event(
        tecla,
        0,
        2,
        0
    )


def pausar_musica():
    _pressionar_tecla_midia(
        VK_MEDIA_PLAY_PAUSE
    )

    return "Música pausada."


def continuar_musica():
    _pressionar_tecla_midia(
        VK_MEDIA_PLAY_PAUSE
    )

    return "Música continuada."


def proxima_musica():
    _pressionar_tecla_midia(
        VK_MEDIA_NEXT_TRACK
    )

    return "Pulando para a próxima música."


import time


def musica_anterior():
    _pressionar_tecla_midia(
        VK_MEDIA_PREV_TRACK
    )

    time.sleep(0.3)

    _pressionar_tecla_midia(
        VK_MEDIA_PREV_TRACK
    )

    return "Voltando para a música anterior."

# ==========================================================
# ABRIR ARQUIVO / PASTA GENERICAMENTE
# ==========================================================

import os


PASTAS_BUSCA = [
    r"C:\Users\User\Downloads\Assistente",
    r"C:\Users\User\Downloads",
]


def encontrar_caminho(nome):

    nome = nome.lower().strip()

    encontrados = []

    for pasta in PASTAS_BUSCA:

        if not os.path.exists(pasta):
            continue

        for raiz, diretorios, arquivos in os.walk(pasta):

            for arquivo in arquivos:

                if arquivo.lower() == nome:
                    encontrados.append(
                        os.path.join(raiz, arquivo)
                    )

            for diretorio in diretorios:

                if diretorio.lower() == nome:
                    encontrados.append(
                        os.path.join(raiz, diretorio)
                    )

    # Remove duplicados
    encontrados = list(
        dict.fromkeys(encontrados)
    )

    return encontrados


def abrir_caminho_generico(nome):

    encontrados = encontrar_caminho(nome)

    if not encontrados:
        return f"Não encontrei {nome}."

    if len(encontrados) > 1:

        return (
            f"Encontrei {len(encontrados)} itens chamados "
            f"{nome}. Seja mais específico."
        )

    caminho = encontrados[0]

    try:
        os.startfile(caminho)

        return f"Abrindo {nome}."

    except Exception as erro:

        print(
            f"❌ Erro ao abrir {caminho}: {erro}"
        )

        return "Não consegui abrir esse arquivo."
    
    # ==========================================================
# ABRIR PASTAS E ARQUIVOS
# ==========================================================

import os


PASTA_ASSISTENTE = r"C:\Users\User\Downloads\Assistente"
PASTA_DOWNLOADS = r"C:\Users\User\Downloads"


def abrir_downloads():
    os.startfile(PASTA_DOWNLOADS)
    return "Abrindo a pasta Downloads."


def abrir_assistente():
    os.startfile(PASTA_ASSISTENTE)
    return "Abrindo a pasta do Assistente."


def abrir_main():
    caminho = os.path.join(
        PASTA_ASSISTENTE,
        "main.py"
    )

    os.startfile(caminho)
    return "Abrindo o main.py."


def abrir_interface():
    caminho = os.path.join(
        PASTA_ASSISTENTE,
        "interface.py"
    )

    os.startfile(caminho)
    return "Abrindo a interface."


def encontrar_caminho(nome):

    nome = nome.lower().strip()

    encontrados = []

    pastas_busca = [
        PASTA_ASSISTENTE,
        PASTA_DOWNLOADS
    ]

    for pasta in pastas_busca:

        if not os.path.exists(pasta):
            continue

        for raiz, diretorios, arquivos in os.walk(pasta):

            for arquivo in arquivos:

                if arquivo.lower() == nome:
                    encontrados.append(
                        os.path.join(raiz, arquivo)
                    )

            for diretorio in diretorios:

                if diretorio.lower() == nome:
                    encontrados.append(
                        os.path.join(raiz, diretorio)
                    )

    return list(
        dict.fromkeys(encontrados)
    )


def abrir_caminho_generico(nome):

    encontrados = encontrar_caminho(nome)

    if not encontrados:
        return f"Não encontrei {nome}."

    if len(encontrados) > 1:
        return (
            f"Encontrei {len(encontrados)} itens chamados "
            f"{nome}. Seja mais específico."
        )

    caminho = encontrados[0]

    try:

        os.startfile(caminho)

        return f"Abrindo {nome}."

    except Exception as erro:

        print(
            f"❌ Erro ao abrir {caminho}: {erro}"
        )

        return "Não consegui abrir esse arquivo."
    
    