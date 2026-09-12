const { chromium } = require('playwright');
const path = require('path');

async function main() {
  const sceneFile = process.argv[2];      // e.g. scenes/merger.html
  const outDir = process.argv[3];         // e.g. frames/merger
  const totalFrames = parseInt(process.argv[4] || '150', 10);

  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--use-gl=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist']
  });
  const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
  page.on('console', msg => console.log('PAGE:', msg.text()));
  page.on('pageerror', err => console.log('PAGEERROR:', err.message));

  const baseName = path.basename(sceneFile);
  const url = `http://127.0.0.1:8931/${baseName}`;
  await page.goto(url);
  await page.waitForFunction('window.__ready === true', { timeout: 30000 });

  const fs = require('fs');
  fs.mkdirSync(outDir, { recursive: true });

  for (let i = 0; i < totalFrames; i++) {
    await page.evaluate(([i, total]) => window.__renderFrame(i, total), [i, totalFrames]);
    const frameName = String(i).padStart(5, '0');
    await page.screenshot({ path: `${outDir}/frame_${frameName}.png` });
    if (i % 20 === 0) console.log(`frame ${i}/${totalFrames}`);
  }

  await browser.close();
  console.log('done');
}

main().catch(e => { console.error(e); process.exit(1); });
