import json
import os

ARQUIVO_MEMORIA = r"C:\Users\User\Downloads\Assistente\memoria\memoria.json"


def carregar_memoria():
    if not os.path.exists(ARQUIVO_MEMORIA):
        return []

    try:
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if isinstance(dados, list):
            return dados

    except (json.JSONDecodeError, OSError):
        return []

    return []


def salvar_memoria(memoria):
    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as arquivo:
        json.dump(memoria, arquivo, ensure_ascii=False, indent=4)


def adicionar_memoria(texto):
    memoria = carregar_memoria()

    if texto.strip() == "":
        return

    if texto not in memoria:
        memoria.append(texto)

    salvar_memoria(memoria)


def remover_memoria(texto):
    memoria = carregar_memoria()
    nova_memoria = []

    for item in memoria:
        if texto.lower() not in item.lower():
            nova_memoria.append(item)

    salvar_memoria(nova_memoria)


def obter_memorias():
    return carregar_memoria()


def limpar_memoria():
    salvar_memoria([])
    
def pesquisar_memoria(pergunta):
    memoria = carregar_memoria()

    if not memoria:
        return []

    palavras = pergunta.lower().split()

    resultados = []

    for item in memoria:
        item_lower = item.lower()

        pontos = 0

        for palavra in palavras:
            if len(palavra) >= 3 and palavra in item_lower:
                pontos += 1

        if pontos > 0:
            resultados.append((pontos, item))

    resultados.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [item for pontos, item in resultados[:5]]

PALAVRAS_IGNORAR = {
    "qual",
    "quais",
    "meu",
    "minha",
    "meus",
    "minhas",
    "você",
    "voce",
    "sobre",
    "mim",
    "isso",
    "mesmo",
    "mesma",
    "o",
    "a",
    "os",
    "as",
    "de",
    "do",
    "da",
    "dos",
    "das",
    "que",
    "é",
    "e",
    "um",
    "uma",
}


def pesquisar_memoria(pergunta):
    memoria = carregar_memoria()

    if not memoria:
        return []

    palavras = [
        palavra
        for palavra in pergunta.lower().split()
        if len(palavra) >= 3
        and palavra not in PALAVRAS_IGNORAR
    ]

    resultados = []

    for item in memoria:
        item_lower = item.lower()
        pontos = 0

        for palavra in palavras:
            if palavra in item_lower:
                pontos += 1

        if pontos > 0:
            resultados.append((pontos, item))

    resultados.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        item
        for pontos, item in resultados[:5]
    ]