// Tüm kareleri üretir ve sesle birlikte MP4'e dönüştürür.
// Kullanım: node render.js <kare_klasörü> <ses.wav> <çıktı.mp4>
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const path = require('path'), fs = require('fs');
(async () => {
  const [framesDir, wav, outMp4] = process.argv.slice(2);
  fs.mkdirSync(framesDir, { recursive: true });
  const srv = await require('./server')(); const port = srv.address().port;
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
  const WORKERS = 3, pages = [];
  for (let w = 0; w < WORKERS; w++) {
    const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
    p.on('pageerror', e => console.error('PAGE ERROR', e.message));
    await p.goto(`http://127.0.0.1:${port}/scene.html`);
    await p.waitForFunction('window.READY===true', null, { timeout: 60000 });
    pages.push(p);
  }
  const NF = await pages[0].evaluate('NF');
  let next = 0, done = 0; const t0 = Date.now();
  await Promise.all(pages.map(async p => {
    while (next < NF) {
      const i = next++;
      const d = await p.evaluate(i => { renderFrame(i); return document.getElementById('out').toDataURL('image/jpeg', 0.95); }, i);
      fs.writeFileSync(path.join(framesDir, `f${String(i).padStart(4, '0')}.jpg`), Buffer.from(d.split(',')[1], 'base64'));
      if (++done % 60 === 0) console.log(`${done}/${NF} (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
    }
  }));
  await b.close(); srv.close();
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-framerate', '30', '-i', path.join(framesDir, 'f%04d.jpg'), '-i', wav,
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level', '4.2',
    '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-shortest', '-movflags', '+faststart', outMp4], { stdio: 'inherit' });
  console.log('Bitti:', outMp4);
})();
