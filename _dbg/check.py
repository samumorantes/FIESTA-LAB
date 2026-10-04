from playwright.sync_api import sync_playwright
import sys, os, json
os.makedirs('C:/Users/moran/FIESTA-LAB/_dbg', exist_ok=True)

VPS = [(1600, 1000), (1366, 768), (1920, 1080)]
out = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for vw, vh in VPS:
        ctx = browser.new_context(viewport={'width': vw, 'height': vh})
        page = ctx.new_page()
        page.goto('http://localhost:8899', wait_until='domcontentloaded')
        page.wait_for_timeout(3500)
        # inject some lyrics to make sure we see something rendered
        page.evaluate("""() => {
          const el = document.getElementById('lCur');
          if (el) { el.textContent = 'HOLA MUNDO'; window.setLyric('HOLA MUNDO', null); }
        }""")
        page.wait_for_timeout(800)
        page.screenshot(path=f'C:/Users/moran/FIESTA-LAB/_dbg/snap_{vw}x{vh}.png')
        bb = page.evaluate("""() => {
          const el = document.getElementById('lCur');
          if (!el) return null;
          const r = el.getBoundingClientRect();
          // medir los anchors hijos
          const anchors = Array.from(el.children);
          const positions = anchors.map(a => {
            const rr = a.getBoundingClientRect();
            return { x: rr.x, w: rr.width, cx: rr.x + rr.width/2 };
          });
          const lcd = document.getElementById('lensTarget') || document.getElementById('screen');
          const lr = lcd.getBoundingClientRect();
          return {
            line: { x:r.x, y:r.y, w:r.width, h:r.height, cx:r.x + r.width/2 },
            screen: { x:lr.x, y:lr.y, w:lr.width, h:lr.height, cx:lr.x + lr.width/2 },
            viewport_w: window.innerWidth,
            anchors: positions
          };
        }""")
        out.append({'vp': (vw, vh), 'bb': bb})
        ctx.close()
    browser.close()
print(json.dumps(out, indent=2))