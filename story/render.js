// Story şablonunu 1080×1920 PNG olarak dışa aktarır.
// Kullanım: node story/render.js            -> output/cumartesi_story.png (+ kılavuzlu önizleme)
const { chromium } = require('playwright');
const path = require('path'), fs = require('fs');
(async () => {
  const out = path.join(__dirname, 'output');
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  const url = 'file://' + path.join(__dirname, 'story.html');
  for (const [q, name] of [['', 'cumartesi_story.png'], ['?guides', 'cumartesi_story_guvenli_alan.png']]) {
    await p.goto(url + q);
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: path.join(out, name), clip: { x: 0, y: 0, width: 1080, height: 1920 } });
    console.log('yazıldı:', name);
  }
  await b.close();
})();
