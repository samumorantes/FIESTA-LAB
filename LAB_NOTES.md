# FIESTA LAB — registro de experimentos

Copia experimental. La original (fiesta-visualizer, :8888) NO se toca.
LAB corre en **:8899**.

## Experimentos en curso

### 1. Audio reactivo REAL (audio_engine.py)
- Captura WASAPI loopback del altavoz (soundcard lib, venv propio).
- FFT por bloque 2048 → energía bass/mid/treble + onsets → BPM real.
- Estado actual: el motor detecta y calcula, PERO todos los loopbacks
  devuelven silencio mientras suena música (`listen_all.py` en background
  buscando qué dispositivo lleva la señal). Sospecha: el audio sale por un
  dispositivo no listado como loopback o Windows lo mezcla distinto.
- Plan B si loopback falla: usar el micrófono (capta el audio ambiente del
  Echo Dot) con supresión de ruido off — menos preciso pero funciona.

### 2. Modo karaoke (frontend)
- Barrido de color palabra por palabra dentro de la línea activa,
  repartiendo el tiempo de la línea entre sus palabras.
- Pendiente implementar en index.html del LAB.

### 3. Fluido chill v2
- Vórtices/estelas en vez de blobs simples.

## Reglas
- NO tocar C:\Users\moran\fiesta-visualizer (producción, puerto 8888).
- Commits locales en este repo; push solo si el usuario aprueba.
