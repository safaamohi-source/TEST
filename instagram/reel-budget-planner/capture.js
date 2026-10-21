const { chromium } = require('playwright');
const HIDE = '.wa-float, .fbtn.wab { display: none !important; }';
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 390, height: 604 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true });

  // 1) Home page with the "صمم بيتك حسب ميزانيتك" slide showing
  await p.goto('https://megafurnitures.com/ar/', { waitUntil: 'networkidle', timeout: 60000 }).catch(e => console.log('goto:', e.message));
  await p.addStyleTag({ content: HIDE });
  for (let i = 0; i < 80; i++) {
    const ok = await p.evaluate(() => {
      const c = document.querySelector('#heroSlider').getBoundingClientRect();
      const s = document.querySelectorAll('#heroSlider .hs-slide')[2].getBoundingClientRect();
      return Math.abs(s.left - c.left) < 1 && Math.abs(s.right - c.right) < 1;
    });
    if (ok) break;
    await p.waitForTimeout(250);
  }
  await p.waitForTimeout(400);
  await p.screenshot({ path: 'raw/1_home.png' });

  // 2) Planner page landing
  await p.goto('https://megafurnitures.com/ar/planner', { waitUntil: 'networkidle' });
  await p.addStyleTag({ content: HIDE });
  await p.waitForTimeout(800);
  await p.screenshot({ path: 'raw/2_planner.png' });

  // 3) Pick rooms (same picks as the reference screenshot)
  for (const slug of ['bedroom', 'lcorner', 'living-room', 'tv-unit'])
    await p.click(`#pl-rooms [data-slug="${slug}"]`);
  await p.evaluate(() => { const r = document.querySelector('#pl-rooms').closest('section').getBoundingClientRect(); window.scrollBy(0, r.top - 12); });
  await p.waitForTimeout(600);
  await p.screenshot({ path: 'raw/3_rooms.png' });

  // 4) Budget step + generate button
  await p.evaluate(() => { const r = document.querySelector('#pl-slider').closest('section').getBoundingClientRect(); window.scrollBy(0, r.top - 60); });
  await p.waitForTimeout(600);
  await p.screenshot({ path: 'raw/4_budget.png' });

  // 5) Generated package — wider viewport so all 4 products + total fit in one frame
  const q = await b.newPage({ viewport: { width: 768, height: 1189 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  await q.goto('https://megafurnitures.com/ar/planner', { waitUntil: 'networkidle' });
  await q.addStyleTag({ content: HIDE });
  for (const slug of ['bedroom', 'lcorner', 'living-room', 'tv-unit'])
    await q.click(`#pl-rooms [data-slug="${slug}"]`);
  await q.click('#pl-generate');
  await q.waitForSelector('#pl-result:not([hidden])', { timeout: 30000 });
  await q.waitForLoadState('networkidle');
  await q.waitForTimeout(2500);
  await q.evaluate(() => { const r = document.querySelector('#pl-result').getBoundingClientRect(); window.scrollBy(0, r.top - 12); });
  await q.waitForTimeout(1500);
  await q.screenshot({ path: 'raw/5_result.png' });
  await b.close();
})();
