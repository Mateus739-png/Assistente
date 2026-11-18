from ia.qwen import perguntar


def traduzir(texto, idioma):

    idiomas = {
        "ingles": "inglês",
        "english": "inglês",

        "espanhol": "espanhol",
        "español": "espanhol",
        "spanish": "espanhol",

        "frances": "francês",
        "francês": "francês",
        "french": "francês",

        "alemao": "alemão",
        "alemão": "alemão",
        "german": "alemão",

        "italiano": "italiano",
        "italian": "italiano",

        "japones": "japonês",
        "japonês": "japonês",
        "japanese": "japonês",

        "coreano": "coreano",
        "korean": "coreano",

        "chines": "chinês",
        "chinês": "chinês",
        "chinese": "chinês",
    }

    idioma = idioma.strip().lower()

    idioma = idiomas.get(idioma, idioma)

    prompt = f"""
Você é um tradutor profissional.

Traduza o texto abaixo do português brasileiro para {idioma}.

Texto:
{texto}

Regras:
- Retorne somente a tradução.
- Não explique nada.
- Não coloque aspas.
- Preserve o significado original.
- Mantenha o tom do texto original.
"""

    return perguntar(prompt).strip()