const { chromium } = require('playwright');

// ── 根據真實資料分析，設定每頁每題的分數 ──
// 資料來源：22筆真人填答，取3年以上受訪者(n=15)的平均
// 格式：[頁面標題關鍵字, [各題分數]]
const PAGE_SCORES = {
  '發散思維': [4, 4, 4, 4, 4, 4, 2],        // Q7反向 avg=2.0
  '創新警覺性': [5, 4, 4, 4, 3, 4, 4, 4, 5], // Q5競爭對手缺口 avg=3.87
  '市場感知能力': [4, 4, 4, 3, 4, 4],         // Q4準確預測 avg=3.80
  '吸收能力': [4, 5, 5, 4, 4, 5, 5, 5, 4],
  '知識吸收能力': [4, 5, 4, 4, 4, 3, 4, 3, 4, 4, 5, 4], // Q6,Q8整合 avg≈3.93
  '知識靈活性': [4, 4, 3, 4, 4, 4, 2],        // Q3思維轉換 avg=3.93, Q7反向 avg=1.93
  '創意思考能力': [4, 4, 4, 4, 4, 4, 4, 4],
};

// 根據頁面標題和題目索引取得分數
function getScore(pageTitle, questionIndex) {
  for (const [keyword, scores] of Object.entries(PAGE_SCORES)) {
    if (pageTitle.includes(keyword)) {
      return scores[questionIndex] || 4;
    }
  }
  return 4; // 預設
}

async function clickSimpleOption(page, text) {
  const locator = page.locator('span').filter({ hasText: new RegExp(`^${text}$`) }).first();
  try {
    await locator.click({ timeout: 5000 });
    return true;
  } catch {
    try {
      const divLocator = page.locator('div').filter({ hasText: new RegExp(`^${text}$`) }).first();
      await divLocator.click({ timeout: 5000 });
      return true;
    } catch {
      console.log(`  ✗ 無法點選: ${text}`);
      return false;
    }
  }
}

// 填寫當前頁面的 matrix 量表題
async function fillMatrixPage(page, pageTitle) {
  const result = await page.evaluate(() => {
    const rows = document.querySelectorAll('tr[data-subject-type="NESTCHILD"]');
    return Array.from(rows).map(row => {
      const textEl = row.querySelector('.css-m1kerg');
      return textEl ? textEl.innerText.trim() : '';
    });
  });

  if (result.length === 0) {
    console.log('  (此頁無量表題)');
    return false;
  }

  console.log(`  填寫 ${result.length} 道量表題:`);

  for (let i = 0; i < result.length; i++) {
    const text = result[i];
    const score = getScore(pageTitle, i);
    console.log(`  [${score}分] ${text.substring(0, 40)}...`);

    // 點擊對應分數的 td
    const success = await page.evaluate(({ rowIndex, scoreVal }) => {
      const rows = document.querySelectorAll('tr[data-subject-type="NESTCHILD"]');
      if (rowIndex >= rows.length) return false;
      const row = rows[rowIndex];
      const allTds = row.querySelectorAll('td');
      if (allTds.length < scoreVal + 1) return false;
      const targetTd = allTds[scoreVal]; // 1=非常不同意, 5=非常同意
      const optionDiv = targetTd.querySelector('[data-qa="option-"]');
      if (optionDiv) {
        optionDiv.click();
        return true;
      }
      return false;
    }, { rowIndex: i, scoreVal: score });

    if (!success) {
      console.log(`  ✗ 無法填寫第 ${i+1} 題`);
    }
    await page.waitForTimeout(150);
  }
  return true;
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  console.log('=== 開始填寫問卷 ===\n');
  await page.goto('https://www.surveycake.com/s/1qbm6', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(2000);

  await page.click('button:has-text("開始")');
  await page.waitForTimeout(2000);

  // ── 第1頁：基本資料 ──
  console.log('【第1頁】基本資料');
  await clickSimpleOption(page, '女性');
  await clickSimpleOption(page, '科技業（電子電機、通訊等）');
  await clickSimpleOption(page, '策略：產品企劃、產品經理、策略分析師');
  await clickSimpleOption(page, '4–6年');
  await clickSimpleOption(page, '經常參與');
  await clickSimpleOption(page, '機會發掘/市場需求分析');
  await clickSimpleOption(page, '產品構想發展');
  await clickSimpleOption(page, '產品設計/研發');
  console.log('  ✓ 完成');

  await page.click('button:has-text("下一頁")');
  await page.waitForTimeout(2000);

  // ── 第2頁：量表說明 ──
  console.log('\n【第2頁】量表說明 (直接下一頁)');
  await page.click('button:has-text("下一頁")');
  await page.waitForTimeout(2000);

  // ── 第3頁：機會辨識說明 ──
  console.log('\n【第3頁】機會辨識說明 (直接下一頁)');
  await page.click('button:has-text("下一頁")');
  await page.waitForTimeout(2000);

  // ── 後續各量表頁 ──
  let pageNum = 4;
  let maxPages = 30; // 安全上限

  while (pageNum <= maxPages) {
    // 取得頁面標題
    const pageTitle = await page.evaluate(() => {
      const titleEl = document.querySelector('[aria-label="subject"]');
      return titleEl ? titleEl.innerText.substring(0, 60).replace(/\n/g, ' ') : '';
    });

    const hasMatrix = await page.$('tr[data-subject-type="NESTCHILD"]');
    const hasNext = await page.$('button:has-text("下一頁")');
    const hasSubmit = await page.$('button:has-text("送出")') || await page.$('button:has-text("提交")');

    console.log(`\n【第${pageNum}頁】${pageTitle}`);

    if (hasMatrix) {
      await fillMatrixPage(page, pageTitle);
      await page.screenshot({ path: `filled_p${pageNum}.png`, fullPage: true });
    } else {
      console.log('  (說明頁或其他類型)');
      const bodyText = await page.evaluate(() => document.body.innerText.substring(0, 100));
      console.log('  ' + bodyText.replace(/\n/g, ' '));
    }

    if (hasSubmit) {
      console.log('\n=== 找到送出按鈕 ===');
      await page.screenshot({ path: 'before_submit.png', fullPage: true });
      console.log('截圖已儲存: before_submit.png');
      await page.click('button:has-text("送出")');
      await page.waitForTimeout(3000);
      await page.screenshot({ path: 'after_submit.png', fullPage: true });
      const finalText = await page.evaluate(() => document.body.innerText.substring(0, 200));
      console.log('送出後頁面:', finalText);
      break;
    }

    if (!hasNext) {
      console.log('  (沒有下一頁按鈕)');
      break;
    }

    await page.click('button:has-text("下一頁")');
    await page.waitForTimeout(2000);

    // 確認是否真的換頁了（避免卡在驗證錯誤）
    const errorVisible = await page.evaluate(() => {
      const body = document.body.innerText;
      return body.includes('此題必填');
    });

    if (errorVisible) {
      console.log('  ⚠ 驗證錯誤：有必填題目未填！截圖中...');
      await page.screenshot({ path: `error_p${pageNum}.png`, fullPage: true });
      break;
    }

    pageNum++;
  }

  console.log('\n=== 腳本執行完畢 ===');
  await browser.close();
})();
