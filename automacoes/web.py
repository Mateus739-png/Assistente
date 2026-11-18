import webbrowser
from urllib.parse import quote


def abrir_youtube():
    webbrowser.open("https://www.youtube.com")
    return "Abrindo o YouTube."


def abrir_google():
    webbrowser.open("https://www.google.com")
    return "Abrindo o Google."


def pesquisar_google(pesquisa):
    url = "https://www.google.com/search?q=" + quote(pesquisa)
    webbrowser.open(url)
    return f"Pesquisando {pesquisa} no Google."


def pesquisar_youtube(pesquisa):
    url = "https://www.youtube.com/results?search_query=" + quote(pesquisa)
    webbrowser.open(url)
    return f"Pesquisando {pesquisa} no YouTube."


def pesquisar_spotify(pesquisa):
    url = "https://open.spotify.com/search/" + quote(pesquisa)
    webbrowser.open(url)
    return f"Pesquisando {pesquisa} no Spotify."