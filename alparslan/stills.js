// Seçilen anlardan PNG kareleri üretir: node stills.js <klasör> 1 4.5 7 ...
const { chromium } = require('playwright'); const path = require('path'), fs = require('fs');
(async () => {
  const [dir, ...ts] = process.argv.slice(2); fs.mkdirSync(dir, { recursive: true });
  const srv = await require('./server')(); const port = srv.address().port;
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.error('PAGE ERROR', e.message)); p.on('console', m => m.type() === 'error' && console.error(m.text()));
  await p.goto(`http://127.0.0.1:${port}/scene.html`); await p.waitForFunction('window.READY===true', null, { timeout: 60000 });
  for (const t of ts) {
    const d = await p.evaluate(t => { renderAt(t); return document.getElementById('out').toDataURL('image/jpeg', .9); }, +t);
    fs.writeFileSync(path.join(dir, `t${(+t).toFixed(1)}.jpg`), Buffer.from(d.split(',')[1], 'base64'));
  }
  await b.close(); srv.close();
})();
