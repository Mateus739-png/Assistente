import os
import torch
import soundfile as sf

from speechbrain.inference.speaker import SpeakerRecognition


PASTA_MODELO = r"C:\Users\User\Downloads\Assistente\modelos\spkrec-ecapa-voxceleb"
ARQUIVO_PERFIL = r"C:\Users\User\Downloads\Assistente\audio\perfil_mateus.pt"

SAMPLE_RATE = 16000


print("🔎 Carregando reconhecimento de voz...")

modelo = SpeakerRecognition.from_hparams(
    source="speechbrain/spkrec-ecapa-voxceleb",
    savedir=PASTA_MODELO
)

print("✅ Reconhecimento de voz carregado.")


def carregar_audio(caminho):

    audio, taxa = sf.read(
        caminho,
        dtype="float32"
    )

    audio = torch.from_numpy(audio)

    if audio.ndim > 1:
        audio = audio.mean(dim=1)

    audio = audio.unsqueeze(0)

    if taxa != SAMPLE_RATE:
        raise ValueError(
            f"Áudio precisa estar em {SAMPLE_RATE} Hz, "
            f"mas está em {taxa} Hz."
        )

    return audio


def gerar_embedding(caminho):

    audio = carregar_audio(caminho)

    with torch.no_grad():
        embedding = modelo.encode_batch(audio)

    embedding = embedding.squeeze()

    # Normaliza
    embedding = torch.nn.functional.normalize(
        embedding,
        p=2,
        dim=0
    )

    return embedding


def cadastrar_voz(arquivos):

    embeddings = []

    for arquivo in arquivos:

        if not os.path.exists(arquivo):
            continue

        print(f"🔎 Analisando: {arquivo}")

        embedding = gerar_embedding(
            arquivo
        )

        embeddings.append(
            embedding
        )

    if not embeddings:
        print("❌ Nenhuma gravação encontrada.")
        return False

    perfil = torch.stack(
        embeddings
    ).mean(dim=0)

    perfil = torch.nn.functional.normalize(
        perfil,
        p=2,
        dim=0
    )

    os.makedirs(
        os.path.dirname(ARQUIVO_PERFIL),
        exist_ok=True
    )

    torch.save(
        perfil,
        ARQUIVO_PERFIL
    )

    print()
    print("✅ Voz cadastrada com sucesso.")
    print(f"📁 Perfil: {ARQUIVO_PERFIL}")

    return True

def identificar_voz(arquivo):

    if not os.path.exists(arquivo):
        return "desconhecido", 0.0

    pasta_vozes = os.path.join(
        os.path.dirname(ARQUIVO_PERFIL),
        "vozes_mateus"
    )

    arquivos_referencia = [
        os.path.join(pasta_vozes, "voz_1.wav"),
        os.path.join(pasta_vozes, "voz_2.wav"),
        os.path.join(pasta_vozes, "voz_3.wav"),
        os.path.join(pasta_vozes, "voz_4.wav"),
        os.path.join(pasta_vozes, "voz_5.wav"),
    ]

    embedding_novo = gerar_embedding(arquivo)

    resultados = []

    for referencia in arquivos_referencia:

        if not os.path.exists(referencia):
            continue

        embedding_referencia = gerar_embedding(
            referencia
        )

        similaridade = torch.nn.functional.cosine_similarity(
            embedding_referencia.unsqueeze(0),
            embedding_novo.unsqueeze(0)
        ).item()

        resultados.append(
            similaridade
        )

    if not resultados:
        return "desconhecido", 0.0

    # Ordena da maior para a menor
    resultados.sort(reverse=True)

    # Usa as 3 melhores comparações
    melhores = resultados[:3]

    media_melhores = sum(melhores) / len(melhores)

    # Limite provisório baseado nos seus testes
    LIMIAR = 0.45

    if media_melhores >= LIMIAR:
        return "Mateus", media_melhores

    return "desconhecido", media_melhores