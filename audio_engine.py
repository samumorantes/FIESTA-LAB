# -*- coding: utf-8 -*-
"""FIESTA LAB — captura de audio del sistema (loopback) + detección de beats por FFT.
Sirve /api/audio con: energía por bandas (bass/mid/treble), beat flag, BPM estimado.
El frontend lo consulta cada ~100ms y sincroniza colores/fluido al audio REAL."""
import json
import time
import numpy as np
import soundcard as sc

SR = 48000
CHUNK = 2048            # muestras por bloque FFT (~43ms)
HISTORY = 43            # ~2s de historial de energía para BPM

_state = {
    "bass": 0.0, "mid": 0.0, "treble": 0.0,
    "beat": False, "energy": 0.0, "bpm": 120.0,
    "onsets": [],          # timestamps de onsets para BPM
    "last_update": 0.0, "error": None, "device": None,
}

def _find_loopback():
    """Altavoz preferido: Echo Dot (el default del usuario) o el primero con señal."""
    loop = [m for m in sc.all_microphones(include_loopback=True) if m.isloopback]
    for m in loop:
        if "Echo" in m.name:
            return m
    return loop[0] if loop else None

def _band_energy(spec, freqs, lo, hi):
    mask = (freqs >= lo) & (freqs < hi)
    return float(np.sqrt((spec[mask] ** 2).mean())) if mask.any() else 0.0

def capture_worker():
    import threading
    def run():
        try:
            mic = _find_loopback()
            if mic is None:
                _state["error"] = "no loopback device"
                return
            _state["device"] = mic.name
            prev_e = 0.0
            with mic.recorder(samplerate=SR, blocksize=CHUNK) as rec:
                while True:
                    data = rec.record(numframes=CHUNK)
                    mono = data.mean(axis=1) if data.ndim > 1 else data
                    # ventana Hann + FFT
                    win = mono * np.hanning(len(mono))
                    spec = np.abs(np.fft.rfft(win))
                    freqs = np.fft.rfftfreq(len(mono), 1.0 / SR)

                    bass = _band_energy(spec, freqs, 20, 160)
                    mid = _band_energy(spec, freqs, 160, 2000)
                    treble = _band_energy(spec, freqs, 2000, 8000)
                    energy = float(np.abs(mono).mean())

                    # onset: salto brusco de bajos respecto al promedio reciente
                    now = time.time()
                    beat = bass > prev_e * 1.35 and bass > 0.02
                    if beat:
                        _state["onsets"].append(now)
                        _state["onsets"] = [t for t in _state["onsets"] if now - t < 4]
                        # BPM de intervalos entre onsets
                        if len(_state["onsets"]) >= 4:
                            iv = np.diff(_state["onsets"][-9:])
                            iv = iv[(iv > 0.25) & (iv < 1.5)]   # 40-240 BPM
                            if len(iv):
                                _state["bpm"] = round(60.0 / float(np.median(iv)))
                    prev_e = bass * 0.6 + prev_e * 0.4

                    _state.update(bass=round(min(bass * 12, 1), 3),
                                  mid=round(min(mid * 8, 1), 3),
                                  treble=round(min(treble * 10, 1), 3),
                                  energy=round(min(energy * 15, 1), 3),
                                  beat=beat, last_update=now)
        except Exception as e:
            _state["error"] = str(e)

    t = threading.Thread(target=run, daemon=True)
    t.start()

def get_audio_state():
    age = time.time() - _state["last_update"]
    out = dict(_state)
    out.pop("onsets", None)
    out["stale"] = age > 1.0
    return out

if __name__ == "__main__":
    capture_worker()
    time.sleep(36000)
