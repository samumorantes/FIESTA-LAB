# FIESTA LAB — ESTADO DE TRABAJO (sesión 2026-08-24)

## Presets por música: FUNCIONANDO (probar errores simples restantes)
- Se evalúan en CADA tick (checkPresets en rama sameTrack del tick())
- Aplican TODO: tema, tamaño, CRT, modo fiesta/fluido, paleta
- Al cambiar a canción sin preset → restoreBaseConfig + "⚙ CONFIG HABITUAL"
- Reset de _presetAppliedFor al detectar cambio de track en sync
- globalLock = override global que bloquea presets

## Pendiente / conocido
- "Errores simples" en presets que el usuario quiere pulir (preguntarle cuáles mañana)
- Tilt 3D quedó DESACTIVADO (transform:none) durante el debug de la lente — decidir si se vuelve con ángulos suaves o se elimina
- Escala lente = 1.38 (body.lens-live #lensTarget)
- Palabras/frase: slider min=1, server acepta mw>=1, caches limpiadas con force=1
- Slider fs y wordSpacing repintan la línea actual al vuelo (setLyric(lastShown...))

## Infraestructura
- Repo LAB: github.com/samumorantes/FIESTA-LAB (tag beta-2.0, todo pusheado hasta 4c809e6+)
- Original estable intacta en :8888 / PARTY-VISUALIZER
