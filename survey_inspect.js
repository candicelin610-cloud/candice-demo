const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto('https://www.surveycake.com/s/1qbm6', { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);

  // 點擊開始
  await page.click('button:has-text("開始")');
  await page.waitForTimeout(2000);

  await page.screenshot({ path: 'survey_structure.png', fullPage: true });

  // 印出第一題的 HTML 結構
  const html = await page.evaluate(() => {
    // 找出所有選項相關元素
    const result = {};

    // 嘗試各種可能的選擇器
    const allClickable = document.querySelectorAll('div[class], span[class], li[class]');
    const samples = [];
    allClickable.forEach((el, i) => {
      if (i < 30 && el.innerText && el.innerText.trim().length > 0 && el.innerText.trim().length < 50) {
        samples.push({
          tag: el.tagName,
          class: el.className,
          text: el.innerText.trim()
        });
      }
    });
    result.samples = samples;

    // 印出整個第一個問題的 HTML
    const firstQ = document.querySelector('[class*="question"]') || document.querySelector('[class*="item"]');
    if (firstQ) {
      result.firstQHTML = firstQ.outerHTML.substring(0, 2000);
    }

    // 取得所有可見文字節點周圍的結構
    result.bodyHTML = document.body.innerHTML.substring(0, 5000);

    return result;
  });

  console.log('=== 可點擊元素樣本 ===');
  html.samples.forEach(s => console.log(`[${s.tag}] class="${s.class}" text="${s.text}"`));
  console.log('\n=== 第一題 HTML ===');
  console.log(html.firstQHTML);

  await browser.close();
})();
