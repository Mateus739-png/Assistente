from audio.gravacao import gravar_audio
from audio.wakeword import detectar_wakeword
from audio.reconhecimento_voz import identificar_voz

from ia.whisper import transcrever
from ia.qwen import perguntar
from ia.tts import falar

from automacoes import executar_comando
from automacoes.agenda import iniciar_monitor_agenda

import time


print("======================================")
print("          JARVIS LOCAL 🇧🇷")
print("======================================")
print()
print("🧠 Qwen: ONLINE")
print("🎤 Whisper: ONLINE")
print("🔊 TTS: ONLINE")
print("⚙️ Automações: ONLINE")
print("👂 Wake Word: ONLINE")

iniciar_monitor_agenda(falar)

print("📅 Agenda: ONLINE")
print()
print("Diga: Hey Jarvis")
print("Pressione CTRL+C para sair.")
print()


while True:

    try:

        # ==========================================
        # ESPERA PELO WAKE WORD
        # ==========================================

        detectar_wakeword()

        print()
        print("🚀 Jarvis ativado!")

        # ==========================================
        # GRAVA O COMANDO
        # ==========================================

        audio = gravar_audio()

        # ==========================================
        # RECONHECIMENTO DE VOZ
        # ==========================================

        nome, confianca = identificar_voz(audio)

        print()
        print("👤 Voz:", nome)
        print(f"📊 Similaridade: {confianca:.3f}")

        if nome != "Mateus":
            print("⚠️ Voz não reconhecida. Comando ignorado.")
            print()
            continue

        # ==========================================
        # WHISPER
        # ==========================================

        print("⚡ Transcrevendo...")

        texto = transcrever(audio)

        if not texto:
            print("⚠️ Não entendi.")
            print()
            continue

        print()
        print("👤 Você:")
        print(texto)
        print()

        # ==========================================
        # AUTOMAÇÕES
        # ==========================================

        resultado = executar_comando(texto)

        if resultado:

            print("🤖 Jarvis:")
            print(resultado)
            print()

            # 🔊 Jarvis fala
            falar(resultado)

            # Evita que o próprio áudio residual
            # seja interpretado como "Hey Jarvis"
            print("⏳ Limpando áudio...")
            time.sleep(4)

            print()
            print("👂 Pronto. Aguardando Hey Jarvis...")
            print()

            continue

        # ==========================================
        # QWEN
        # ==========================================

        print("🧠 Qwen pensando...")

        resposta = perguntar(texto)

        print()
        print("🤖 Jarvis:")
        print(resposta)
        print()

        # 🔊 Jarvis fala a resposta
        falar(resposta)

        # Evita nova ativação logo após a fala
        print("⏳ Limpando áudio...")
        time.sleep(4)

        print()
        print("👂 Pronto. Aguardando Hey Jarvis...")
        print()

    except KeyboardInterrupt:

        print()
        print("👋 Encerrando Jarvis...")
        break

    except Exception as erro:

        print()
        print("❌ ERRO:")
        print(erro)
        print()