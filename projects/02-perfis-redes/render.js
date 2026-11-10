const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const dir = path.join(__dirname, 'html'); const out = path.join(__dirname, 'out');
  fs.mkdirSync(out, { recursive: true });
  const pecas = JSON.parse(fs.readFileSync(path.join(dir, 'pecas.json')));
  const b = await chromium.launch();
  for (const p of pecas) for (const s of p.escalas) {
    const pg = await b.newPage({ viewport: { width: p.w, height: p.h }, deviceScaleFactor: s });
    await pg.goto('file://' + path.join(dir, p.nome + '.html'));
    await pg.evaluate(() => document.fonts.ready);
    await pg.waitForTimeout(150);
    const nome = s === 1 ? p.nome : `${p.nome}@${s}x`;
    await pg.screenshot({ path: path.join(out, nome + '.png') });
    await pg.close();
  }
  await b.close();
})();
