import os
import torch
import soundfile as sf

from audio.gravacao import gravar_audio
from audio.reconhecimento_voz import gerar_embedding


PASTA_VOZES = r"C:\Users\User\Downloads\Assistente\audio\vozes_mateus"

print("======================================")
print("   TESTE DE RECONHECIMENTO - 5 VOZES")
print("======================================")
print()

arquivos = [
    os.path.join(PASTA_VOZES, "voz_1.wav"),
    os.path.join(PASTA_VOZES, "voz_2.wav"),
    os.path.join(PASTA_VOZES, "voz_3.wav"),
    os.path.join(PASTA_VOZES, "voz_4.wav"),
    os.path.join(PASTA_VOZES, "voz_5.wav"),
]

print("🔎 Gerando referência das 5 amostras...")

embeddings_referencia = []

for arquivo in arquivos:

    if not os.path.exists(arquivo):
        print(f"⚠️ Não encontrado: {arquivo}")
        continue

    print(f"   → {os.path.basename(arquivo)}")

    embedding = gerar_embedding(arquivo)

    embeddings_referencia.append(
        (os.path.basename(arquivo), embedding)
    )

print()
print("✅ Referências carregadas.")
print()

input("Pressione ENTER e fale uma frase nova...")

audio = gravar_audio()

print()
print("🔎 Comparando sua nova fala com as 5 amostras...")
print()

embedding_novo = gerar_embedding(audio)

resultados = []

for nome, referencia in embeddings_referencia:

    similaridade = torch.nn.functional.cosine_similarity(
        referencia.unsqueeze(0),
        embedding_novo.unsqueeze(0)
    ).item()

    resultados.append(
        (nome, similaridade)
    )

resultados.sort(
    key=lambda x: x[1],
    reverse=True
)

print("======================================")
print("           RESULTADOS")
print("======================================")

for nome, score in resultados:

    print(
        f"{nome}: {score:.3f}"
    )

print()

media = sum(
    score for nome, score in resultados
) / len(resultados)

print(f"📊 Média: {media:.3f}")
print(f"📈 Maior similaridade: {resultados[0][1]:.3f}")
print(f"📉 Menor similaridade: {resultados[-1][1]:.3f}")

print("======================================")