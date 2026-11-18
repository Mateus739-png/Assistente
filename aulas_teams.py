import os

from audio.gravacao import gravar_aula_teams
from ia.qwen import resumir_aula
from ia.whisper import transcrever


PASTA_ANOTACOES = os.path.join(os.path.dirname(__file__), "anotacoes")
os.makedirs(PASTA_ANOTACOES, exist_ok=True)


def anotar_aula_teams(tempo_segundos=600):
    audio = gravar_aula_teams(tempo_maximo=tempo_segundos)
    texto = transcrever(audio)

    if not texto:
        raise ValueError("Não consegui extrair o áudio da aula.")

    resumo = resumir_aula(texto)

    nome_arquivo = os.path.join(PASTA_ANOTACOES, "resumo_aula.txt")

    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write("TRANSCRIÇÃO\n")
        arquivo.write(texto + "\n\n")
        arquivo.write("RESUMO\n")
        arquivo.write(resumo)

    print("\n✅ Aula salva em:", nome_arquivo)
    print("\n📌 Resumo:\n")
    print(resumo)

    return texto, resumo, nome_arquivo


if __name__ == "__main__":
    print("\n=== ANOTAR AULA DO TEAMS ===")
    print("A gravação será feita pelo VB-Cable.")
    print("Para parar antes do tempo, pressione Ctrl+C.")
    print("Você pode ajustar o tempo em segundos no código.")
    try:
        anotar_aula_teams(tempo_segundos=600)
    except KeyboardInterrupt:
        print("\n⏹️ Gravação interrompida pelo usuário.")
        print("Se a gravação parcial foi salva, ela já está no arquivo aula_teams.wav.")
        print("O resumo só será gerado quando a gravação terminar normalmente ou quando você chamar a rotina de resumo manualmente.")
