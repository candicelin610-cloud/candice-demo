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

  // 第1頁→第2頁（量表說明）
  await page.click('button:has-text("下一頁")');
  await page.waitForTimeout(2000);
  // 第2頁→第3頁（機會辨識說明）
  await page.click('button:has-text("下一頁")');
  await page.waitForTimeout(2000);
  // 第3頁→第4頁（發散思維量表題）
  await page.click('button:has-text("下一頁")');
  await page.waitForTimeout(2000);

  await page.screenshot({ path: 'scale_q4.png', fullPage: true });

  // 取得量表頁 HTML（找 matrix/subject 結構）
  const result = await page.evaluate(() => {
    // 找出第一個量表題的 HTML
    const subjects = document.querySelectorAll('[aria-label="subject"]');
    const firstSubjectHTML = subjects[0]?.outerHTML?.substring(0, 5000) || '找不到 subject';

    // 找出所有包含數字 1-5 的可點擊元素
    const allInputs = document.querySelectorAll('input[type="radio"], input[type="checkbox"]');
    const inputs = Array.from(allInputs).slice(0, 20).map(el => ({
      type: el.type,
      name: el.name,
      value: el.value,
      id: el.id,
      parentClass: el.parentElement?.className
    }));

    // 找出 td 或 li 元素（常見量表結構）
    const tds = document.querySelectorAll('td');
    const tdSamples = Array.from(tds).slice(0, 10).map(td => ({
      class: td.className,
      text: td.innerText?.trim(),
      html: td.outerHTML?.substring(0, 200)
    }));

    return {
      subjectCount: subjects.length,
      firstSubjectHTML,
      inputs,
      tdSamples,
      bodyText: document.body.innerText.substring(0, 1000)
    };
  });

  console.log('頁面文字:');
  console.log(result.bodyText);
  console.log('\nSubject 數量:', result.subjectCount);
  console.log('\nHTML of first subject (5000 chars):');
  console.log(result.firstSubjectHTML);
  console.log('\nInput elements:');
  console.log(JSON.stringify(result.inputs, null, 2));
  console.log('\nTD elements:');
  console.log(JSON.stringify(result.tdSamples, null, 2));

  await browser.close();
})();
