const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 512, height: 792 }, deviceScaleFactor: 4 });
  await p.goto('file://' + process.cwd() + '/card/card.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  console.log(await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight).join(', ')));
  await p.screenshot({ path: 'card/content.png', omitBackground: true });
  await b.close();
})();
