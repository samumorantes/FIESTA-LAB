# FIESTA LAB — BUILD BETA OFICIAL (v2.0-beta)

Copia experimental promocionada a **beta oficial** por el usuario (2026-08-24).
La original (fiesta-visualizer, :8888) NO se toca. LAB corre en **:8899**.

## Funciones exclusivas del LAB
- **Mueble de TV vintage real**: imagen PNG superpuesta, pantalla empotrada en el hueco,
  lente de deformación centrada en el cristal. Toggle: checkbox "Mueble de TV" o `?tv=0`
- **Temas completos**: Clásico / Vaporwave / Matrix / Super Nintendo (paleta+CRT+fuente)
- **Regla especial**: "Die For You" de Joji → fluido + vaporwave + paleta oscura automático
- **Presets por música**: guarda la config para canción/artista/álbum; se aplica sola al sonar
- **Paleta manual del fluido**: 5 color pickers + aleatorio; ignora la portada
- **Estelas de nebulosa**, **espectro CRT**, **rebote al beat**, **explosión de drops**,
  **QR de votación (tecla Q)**, **traducción EN→ES**, **contraste por zonas**
- **Tecla F** alterna fiesta/fluido con toast (selector visual eliminado)

## Fixes recientes
- Lente SVG centrada en #screen (antes deformaba desde el viewport → esquina negra)
- Fluido cubre todo el hueco: estelas con fade del color base (nunca negro)
- "Palabras por frase": invalida caché de frases + sync (recarga end-to-end real)

## Reglas
- NO tocar C:\Users\moran\fiesta-visualizer sin permiso explícito.
- Túnel público disponible vía cloudflared (ver memory).
