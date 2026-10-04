from playwright.sync_api import sync_playwright
import json, time, os
os.makedirs('C:/Users/moran/FIESTA-LAB/_dbg', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={'width': 1600, 'height': 1000})
    page = ctx.new_page()

    # Capturar FPS real medido por la app (window.__fps)
    page.goto('http://localhost:8899', wait_until='domcontentloaded')
    page.wait_for_timeout(2000)

    # medir FPS durante 3 segundos en cada modo
    results = {}
    for mode in ['off', 'fish_on']:
        if mode == 'fish_on':
            page.evaluate("""() => {
              document.getElementById('fishChk').click();
            }""")
        else:
            page.evaluate("""() => {
              if (document.getElementById('fishChk').checked) document.getElementById('fishChk').click();
            }""")
        page.wait_for_timeout(500)
        # exponer el contador FPS interno
        fps = page.evaluate("""async () => {
          let frames = 0;
          let start = performance.now();
          return new Promise(res => {
            function loop(){
              frames++;
              if (performance.now() - start >= 3000) {
                res(Math.round(frames * 1000 / (performance.now() - start)));
              } else {
                requestAnimationFrame(loop);
              }
            }
            requestAnimationFrame(loop);
          });
        }""")
        results[mode] = fps
    print(json.dumps(results, indent=2))
    browser.close()