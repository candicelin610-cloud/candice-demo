const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  async function clickOption(text) {
    const locator = page.locator(`span`).filter({ hasText: new RegExp(`^${text}$`) }).first();
    try {
      await locator.click({ timeout: 5000 });
    } catch {
      const divLocator = page.locator(`div`).filter({ hasText: new RegExp(`^${text}$`) }).first();
      await divLocator.click({ timeout: 5000 });
    }
  }

  await page.goto('https://www.surveycake.com/s/1qbm6', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);

  await page.click('button:has-text("開始")');
  await page.waitForTimeout(2000);

  // 填第一頁基本資料
  await clickOption('女性');
  await clickOption('科技業（電子電機、通訊等）');
  await clickOption('策略：產品企劃、產品經理、策略分析師');
  await clickOption('4–6年');
  await clickOption('經常參與');
  await clickOption('機會發掘/市場需求分析');
  await clickOption('產品構想發展');
  await clickOption('產品設計/研發');

  // 翻到第二頁（說明頁）
  await page.click('button:has-text("下一頁")');
  await page.waitForTimeout(2000);

  // 翻到第三頁（開始量表題）
  await page.click('button:has-text("下一頁")');
  await page.waitForTimeout(2000);

  let pageNum = 3;
  while (true) {
    const content = await page.evaluate(() => document.body.innerText);
    console.log(`\n=== 第 ${pageNum} 頁 ===`);
    console.log(content);
    await page.screenshot({ path: `page_${pageNum}.png`, fullPage: true });

    const hasNext = await page.$('button:has-text("下一頁")');
    if (!hasNext) {
      console.log('\n（沒有下一頁按鈕，這是最後一頁）');
      break;
    }

    // 不填答，直接翻頁（先看完所有題目）
    // 但如果有必填驗證，可能需要先填
    try {
      await page.click('button:has-text("下一頁")');
      await page.waitForTimeout(2000);

      // 檢查是否出現驗證錯誤
      const errorMsg = await page.$('[class*="error"], [class*="warning"], [class*="alert"]');
      if (errorMsg) {
        console.log('（有驗證錯誤，需要先填答）');
        break;
      }
      pageNum++;
    } catch {
      break;
    }
  }

  await browser.close();
})();
