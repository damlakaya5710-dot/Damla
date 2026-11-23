// Kontrol amaçlı birkaç kareyi PNG olarak kaydeder: node stills.js outdir t1 t2 ...
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const [outDir, ...ts] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await p.goto('file://' + path.resolve(__dirname, 'scene.html'));
  await p.waitForFunction('window.READY===true');
  for (const t of ts) {
    const t0 = Date.now();
    const d = await p.evaluate(t => { renderFrame(Math.round(t * 30)); return document.getElementById('c').toDataURL('image/jpeg', 0.9); }, parseFloat(t));
    fs.writeFileSync(path.join(outDir, `t${t}.jpg`), Buffer.from(d.split(',')[1], 'base64'));
    console.log(t, Date.now() - t0, 'ms');
  }
  await b.close();
})();
