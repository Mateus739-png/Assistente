import json
import os

ARQUIVO_CONTATOS = r"C:\Users\User\Downloads\Assistente\memoria\contatos.json"


def carregar_contatos():
    if not os.path.exists(ARQUIVO_CONTATOS):
        return {}

    try:
        with open(ARQUIVO_CONTATOS, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        if isinstance(dados, dict):
            return dados

    except (json.JSONDecodeError, OSError):
        pass

    return {}


def salvar_contatos(contatos):
    os.makedirs(os.path.dirname(ARQUIVO_CONTATOS), exist_ok=True)

    with open(ARQUIVO_CONTATOS, "w", encoding="utf-8") as arquivo:
        json.dump(
            contatos,
            arquivo,
            ensure_ascii=False,
            indent=4
        )


def adicionar_contato(nome, telefone):
    contatos = carregar_contatos()

    nome = nome.strip().lower()
    telefone = telefone.strip()

    contatos[nome] = {
        "nome": nome,
        "telefone": telefone
    }

    salvar_contatos(contatos)

    return f"Contato {nome} salvo."


def buscar_contato(nome):
    contatos = carregar_contatos()

    nome = nome.strip().lower()

    return contatos.get(nome)


def remover_contato(nome):
    contatos = carregar_contatos()

    nome = nome.strip().lower()

    if nome not in contatos:
        return f"Não encontrei o contato {nome}."

    del contatos[nome]

    salvar_contatos(contatos)

    return f"Contato {nome} removido."


def listar_contatos():
    return carregar_contatos()