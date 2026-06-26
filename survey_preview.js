const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  console.log('開啟問卷頁面...');
  await page.goto('https://www.surveycake.com/s/1qbm6', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);

  // 點擊「開始」
  await page.click('button:has-text("開始")');
  await page.waitForTimeout(2000);

  console.log('=== 第一頁 ===');
  console.log(await page.evaluate(() => document.body.innerText));

  // 填第一頁基本資料
  // Q1: 性別 → 女性
  await page.click('label:has-text("女性")');
  // Q2: 產業 → 科技業
  await page.click('label:has-text("科技業")');
  // Q3: 職務 → 策略：產品企劃
  await page.click('label:has-text("策略")');
  // Q4: 年資 → 4-6年
  await page.click('label:has-text("4–6年")');
  // Q5: 參與程度 → 經常參與
  await page.click('label:has-text("經常參與")');
  // Q6: 參與階段（複選）
  await page.click('label:has-text("機會發掘")');
  await page.click('label:has-text("產品構想發展")');
  await page.click('label:has-text("產品設計")');

  await page.screenshot({ path: 'survey_q1_filled.png', fullPage: true });

  // 點下一頁
  await page.click('button:has-text("下一頁")');
  await page.waitForTimeout(2000);

  console.log('\n=== 第二頁 ===');
  console.log(await page.evaluate(() => document.body.innerText));
  await page.screenshot({ path: 'survey_q2.png', fullPage: true });

  await browser.close();
})();
