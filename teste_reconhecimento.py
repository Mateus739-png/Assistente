from audio.gravacao import gravar_audio
from audio.reconhecimento_voz import identificar_voz


print("======================================")
print("      TESTE DE RECONHECIMENTO")
print("======================================")
print()

input("Pressione ENTER e fale normalmente...")

audio = gravar_audio()

nome, confianca = identificar_voz(audio)

print()
print("======================================")
print(f"👤 Pessoa: {nome}")
print(f"📊 Similaridade: {confianca:.3f}")
print("======================================")