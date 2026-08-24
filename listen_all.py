# Escucha continua 60s por todos los loopbacks — dale PLAY a una canción durante esto
import soundcard as sc
import numpy as np
import time

print("DALE PLAY A UNA CANCION AHORA. Escuchando 45s...")
best = {}
deadline = time.time() + 45
loop = [m for m in sc.all_microphones(include_loopback=True) if m.isloopback]
while time.time() < deadline:
    for m in loop:
        try:
            with m.recorder(samplerate=48000, blocksize=2048) as rec:
                data = rec.record(numframes=4096)
            mono = data.mean(axis=1) if data.ndim > 1 else data.flatten()
            rms = float(np.sqrt((mono ** 2).mean()))
            if m.name not in best or rms > best[m.name]:
                best[m.name] = rms
            top = max(best.items(), key=lambda kv: kv[1])
            print("\r%-46s rms=%.5f | mejor: %s=%.5f" % (
                m.name[:44], rms, top[0][:30], top[1]), end="", flush=True)
        except Exception:
            pass
print("\n\nRESULTADO:")
for k, v in sorted(best.items(), key=lambda kv: -kv[1]):
    print("%-50s %.5f %s" % (k[:48], v, "<== ESTE" if v == max(best.values()) and v > 0.0002 else ""))
