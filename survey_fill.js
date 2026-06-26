const { chromium } = require('playwright');

// 先只做「預覽」——把每一頁的題目全部印出來，不送出
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  // 輔助函式：用文字點選選項（span 或 div 包裝的文字）
  async function clickOption(text) {
    // 嘗試精確比對 span 文字
    const locator = page.locator(`span`).filter({ hasText: new RegExp(`^${text}$`) }).first();
    try {
      await locator.click({ timeout: 5000 });
      console.log(`  ✓ 點選: ${text}`);
    } catch {
      // 備用：用 div 文字
      const divLocator = page.locator(`div`).filter({ hasText: new RegExp(`^${text}$`) }).first();
      await divLocator.click({ timeout: 5000 });
      console.log(`  ✓ 點選(div): ${text}`);
    }
  }

  // 取得當前頁面所有題目文字
  async function getPageContent() {
    return await page.evaluate(() => document.body.innerText);
  }

  console.log('=== 開啟問卷 ===');
  await page.goto('https://www.surveycake.com/s/1qbm6', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);

  await page.click('button:has-text("開始")');
  await page.waitForTimeout(2000);

  // ── 第一頁：基本資料 ──
  console.log('\n=== 第一頁 ===');
  console.log(await getPageContent());

  await clickOption('女性');
  await clickOption('科技業（電子電機、通訊等）');
  await clickOption('策略：產品企劃、產品經理、策略分析師');
  await clickOption('4–6年');
  await clickOption('經常參與');
  // Q6 複選
  await clickOption('機會發掘/市場需求分析');
  await clickOption('產品構想發展');
  await clickOption('產品設計/研發');

  await page.screenshot({ path: 'p1_filled.png', fullPage: true });

  await page.click('button:has-text("下一頁")');
  await page.waitForTimeout(2000);

  // ── 第二頁 ──
  console.log('\n=== 第二頁 ===');
  const p2 = await getPageContent();
  console.log(p2);
  await page.screenshot({ path: 'p2.png', fullPage: true });

  // 確認是否還有更多頁
  const hasNext2 = await page.$('button:has-text("下一頁")');
  if (hasNext2) {
    // 先不填，只看內容
    console.log('\n（還有下一頁，先截圖記錄）');

    // 往後翻頁繼續看
    // 這裡先只截圖而不填，用來了解所有題目
  }

  await browser.close();
  console.log('\n=== 預覽完成 ===');
})();
