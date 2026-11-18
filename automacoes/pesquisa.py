from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from urllib.parse import quote
import time


def pesquisar_web(pergunta):
    print(f"🌐 Pesquisando: {pergunta}")

    opcoes = Options()
    opcoes.add_argument("--headless")
    opcoes.add_argument("--disable-gpu")
    opcoes.add_argument("--window-size=1920,1080")

    navegador = webdriver.Edge(options=opcoes)

    try:
        url = "https://www.bing.com/search?q=" + quote(pergunta)

        navegador.get(url)

        time.sleep(2)

        resultados = []

        blocos = navegador.find_elements(
            By.CSS_SELECTOR,
            "li.b_algo"
        )

        for bloco in blocos[:5]:

            try:
                titulo = bloco.find_element(
                    By.CSS_SELECTOR,
                    "h2"
                ).text
            except:
                continue

            try:
                link = bloco.find_element(
                    By.CSS_SELECTOR,
                    "h2 a"
                ).get_attribute("href")
            except:
                link = ""

            try:
                texto = bloco.find_element(
                    By.CSS_SELECTOR,
                    ".b_caption p"
                ).text
            except:
                texto = ""

            resultados.append({
                "titulo": titulo,
                "link": link,
                "texto": texto
            })

        return resultados

    finally:
        navegador.quit()