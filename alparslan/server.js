// Küçük statik sunucu (ES modülleri file:// ile yüklenemediği için)
const http = require('http'), fs = require('fs'), path = require('path');
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.wav': 'audio/wav', '.mp4': 'video/mp4' };
module.exports = (port = 0) => new Promise(res => {
  const root = __dirname;
  const s = http.createServer((q, r) => {
    const p = path.join(root, decodeURIComponent(q.url.split('?')[0]));
    if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); return r.end(); }
    r.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(r);
  });
  s.listen(port, '127.0.0.1', () => res(s));
});
if (require.main === module) module.exports(8080).then(() => console.log('http://127.0.0.1:8080/scene.html?play=1'));
