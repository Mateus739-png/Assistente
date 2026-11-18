import sounddevice as sd
import numpy as np

DISPOSITIVO = 21
DURACAO = 5
SAMPLE_RATE = 48000

print("🎧 Testando CABLE Output WASAPI...")
print("Reproduza um vídeo/música AGORA.")

audio = sd.rec(
    int(SAMPLE_RATE * DURACAO),
    samplerate=SAMPLE_RATE,
    channels=2,
    dtype="float32",
    device=DISPOSITIVO
)

sd.wait()

rms = np.sqrt(np.mean(audio ** 2))
pico = np.max(np.abs(audio))

print()
print(f"RMS: {rms:.6f}")
print(f"Pico: {pico:.6f}")

if rms > 0.001:
    print("✅ ÁUDIO CHEGOU!")
else:
    print("❌ Ainda não chegou áudio.")