// ============================================================
// 德文每日學習 LINE Bot — Google Apps Script
// 設定完成後，每天自動發送 A1 德文學習內容到你的 LINE
// ============================================================

// 【必填】你的 LINE 金鑰
const LINE_ACCESS_TOKEN = 's6g6kSsWJY8dTyL0IBoM/CLi7CFiICPSvlYXp8WgtfY/Ozy/PKaCWYVYCLTUJQXTLyL4x9KFZYKg4YJA7Q4UeM7KkKSyFLP5Ggzcuzk/sGMCb+Fz09trYiN8mSZhUX/Ytq8pryuBLJAj4rRsGFO4WAdB04t89/1O/w1cDnyilFU=';
const USER_ID = 'U98c99130bd7938f74c900dab4bd1132f';

// ============================================================
// A1 德文課程內容（30 天，涵蓋日常生活各主題）
// ============================================================
const LESSONS = [
  {
    topic: "打招呼 Greetings",
    words: [
      { de: "Hallo", zh: "你好", pron: "哈囉" },
      { de: "Guten Morgen", zh: "早安", pron: "顧騰 摩根" },
      { de: "Guten Tag", zh: "午安", pron: "顧騰 塔克" },
    ],
    phrase: "Wie heißen Sie? — Ich heiße Candice.",
    phrase_zh: "您叫什麼名字？— 我叫 Candice。",
    grammar: "正式場合用 \"Sie\"（您），朋友間用 \"du\"（你）",
    challenge: "用德文介紹自己：Ich heiße ___.",
    culture: "德國人打招呼時通常握手，眼神接觸很重要！"
  },
  {
    topic: "數字 1-10 Numbers",
    words: [
      { de: "eins / zwei / drei", zh: "一 / 二 / 三", pron: "愛因斯 / 茨威 / 揣" },
      { de: "vier / fünf / sechs", zh: "四 / 五 / 六", pron: "費爾 / 分福 / 澤克斯" },
      { de: "sieben / acht / neun / zehn", zh: "七 / 八 / 九 / 十", pron: "吉本 / 阿赫特 / 諾因 / 澤恩" },
    ],
    phrase: "Ich hätte gerne zwei Kaffee, bitte.",
    phrase_zh: "我想要兩杯咖啡，謝謝。",
    grammar: "記住 1-10，之後 11-19 只要在後面加 \"-zehn\"",
    challenge: "用德文從 1 數到 10！",
    culture: "在德國餐廳比「一個」時要豎大拇指，不是食指！"
  },
  {
    topic: "星期 Days of the Week",
    words: [
      { de: "Montag / Dienstag", zh: "星期一 / 星期二", pron: "蒙塔克 / 丁斯塔克" },
      { de: "Mittwoch / Donnerstag", zh: "星期三 / 星期四", pron: "米特沃赫 / 唐納斯塔克" },
      { de: "Freitag / Samstag / Sonntag", zh: "星期五 / 六 / 日", pron: "弗萊塔克 / 薩姆斯塔克 / 尊塔克" },
    ],
    phrase: "Was machst du am Montag?",
    phrase_zh: "你星期一做什麼？",
    grammar: "星期幾前面用 \"am\"：am Montag（在星期一）",
    challenge: "說出今天是星期幾！",
    culture: "德國大多數商店星期日不開（Sonntag），要特別注意！"
  },
  {
    topic: "顏色 Colors",
    words: [
      { de: "rot / blau / gelb", zh: "紅 / 藍 / 黃", pron: "肉特 / 布勞 / 椰普" },
      { de: "grün / schwarz / weiß", zh: "綠 / 黑 / 白", pron: "格律恩 / 虛瓦茨 / 懷斯" },
      { de: "grau / braun / orange", zh: "灰 / 棕 / 橘", pron: "格勞 / 布勞恩 / 歐杭日" },
    ],
    phrase: "Das T-Shirt ist blau.",
    phrase_zh: "這件 T 恤是藍色的。",
    grammar: "形容詞放名詞前面，結尾會隨名詞性別變化",
    challenge: "說出你今天穿的衣服顏色！",
    culture: "德國國旗是黑、紅、金（schwarz, rot, gold）"
  },
  {
    topic: "食物與飲料 Food & Drinks",
    words: [
      { de: "das Brot / die Wurst", zh: "麵包 / 香腸", pron: "布羅特 / 烏斯特" },
      { de: "der Käse / das Ei", zh: "起司 / 雞蛋", pron: "凱澤 / 艾" },
      { de: "das Wasser / der Saft", zh: "水 / 果汁", pron: "瓦瑟 / 扎夫特" },
    ],
    phrase: "Ich möchte ein Bier, bitte.",
    phrase_zh: "我想要一杯啤酒，謝謝。",
    grammar: "名詞有三種性：der（陽）、die（陰）、das（中），要一起記！",
    challenge: "說出你早餐吃了什麼！",
    culture: "德國有超過 300 種麵包，麵包文化是國家驕傲！"
  },
  {
    topic: "在咖啡廳 At the Café",
    words: [
      { de: "der Kaffee / der Tee", zh: "咖啡 / 茶", pron: "卡費 / 泰" },
      { de: "die Torte / der Kuchen", zh: "蛋糕 / 糕點", pron: "托爾特 / 庫亨" },
      { de: "die Rechnung", zh: "帳單", pron: "瑞希農" },
    ],
    phrase: "Die Rechnung, bitte!",
    phrase_zh: "買單，謝謝！",
    grammar: "\"bitte\" 可以表示「請」或「不客氣」，非常萬用！",
    challenge: "練習點餐：Einen Kaffee und ein Stück Kuchen, bitte.",
    culture: "在德國咖啡廳服務生不會主動送帳單，要自己說 \"Zahlen, bitte!\""
  },
  {
    topic: "家庭成員 Family",
    words: [
      { de: "die Mutter / der Vater", zh: "媽媽 / 爸爸", pron: "姆特 / 法特" },
      { de: "die Schwester / der Bruder", zh: "姊妹 / 兄弟", pron: "虛維斯特 / 布魯德" },
      { de: "die Großmutter / der Großvater", zh: "奶奶外婆 / 爺爺外公", pron: "格羅斯姆特 / 格羅斯法特" },
    ],
    phrase: "Ich habe eine Schwester.",
    phrase_zh: "我有一個姊妹。",
    grammar: "\"haben\"（有）的變化：ich habe / du hast / er hat",
    challenge: "介紹你的家人：Meine Familie hat ___ Personen.",
    culture: "Oma（奶奶）和 Opa（爺爺）是常用的親切口語說法"
  },
  {
    topic: "問路 Asking Directions",
    words: [
      { de: "links / rechts / geradeaus", zh: "左 / 右 / 直走", pron: "林克斯 / 瑞赫茨 / 格拉德奧斯" },
      { de: "die Straße / der Platz", zh: "街道 / 廣場", pron: "虛特拉瑟 / 普拉茨" },
      { de: "nah / weit", zh: "近 / 遠", pron: "那 / 懷特" },
    ],
    phrase: "Entschuldigung, wo ist der Bahnhof?",
    phrase_zh: "不好意思，請問車站在哪裡？",
    grammar: "\"Entschuldigung\"（不好意思）是問路必備開場白",
    challenge: "練習說：Gehen Sie geradeaus, dann links.",
    culture: "德國人問路通常給很詳細的指示，可以放心問！"
  },
  {
    topic: "天氣 Weather",
    words: [
      { de: "die Sonne / der Regen", zh: "太陽 / 雨", pron: "尊內 / 雷根" },
      { de: "der Schnee / der Wind", zh: "雪 / 風", pron: "虛內 / 文特" },
      { de: "warm / kalt / heiß", zh: "暖 / 冷 / 熱", pron: "瓦爾姆 / 卡爾特 / 海斯" },
    ],
    phrase: "Wie ist das Wetter heute?",
    phrase_zh: "今天天氣怎麼樣？",
    grammar: "天氣用 \"Es ist...\"：Es ist sonnig.（天氣晴朗）",
    challenge: "描述今天的天氣：Es ist ___ heute.",
    culture: "德國人非常愛聊天氣，這是開啟對話的好話題！"
  },
  {
    topic: "時間 Time",
    words: [
      { de: "die Uhr", zh: "時鐘 / 點鐘", pron: "烏爾" },
      { de: "jetzt / heute / morgen", zh: "現在 / 今天 / 明天", pron: "耶茨特 / 侯伊特 / 摩根" },
      { de: "früh / spät", zh: "早 / 晚", pron: "弗呂 / 虛佩特" },
    ],
    phrase: "Wie viel Uhr ist es?",
    phrase_zh: "現在幾點了？",
    grammar: "Es ist drei Uhr.（三點）/ Es ist halb vier.（三點半，字面是「四點的一半」）",
    challenge: "說出現在的時間！",
    culture: "德國人非常重視守時，遲到超過 15 分鐘要事先通知"
  },
  {
    topic: "交通 Transportation",
    words: [
      { de: "der Zug / die U-Bahn", zh: "火車 / 地鐵", pron: "楚克 / 烏班" },
      { de: "der Bus / das Taxi", zh: "公車 / 計程車", pron: "布斯 / 塔克西" },
      { de: "der Bahnhof / die Haltestelle", zh: "車站 / 公車站", pron: "班霍夫 / 哈爾特虛特勒" },
    ],
    phrase: "Wann fährt der nächste Zug?",
    phrase_zh: "下一班火車幾點開？",
    grammar: "\"wann\"（什麼時候）用來問時間",
    challenge: "練習問：Wo ist die nächste U-Bahn-Station?",
    culture: "德國大眾交通很發達，但逃票（schwarzfahren）罰款很重！"
  },
  {
    topic: "購物 Shopping",
    words: [
      { de: "der Preis / teuer / billig", zh: "價格 / 貴 / 便宜", pron: "普萊斯 / 托伊爾 / 比利希" },
      { de: "das Geschäft / der Markt", zh: "商店 / 市場", pron: "格謝夫特 / 馬爾克特" },
      { de: "kaufen / bezahlen", zh: "買 / 付款", pron: "考芬 / 貝扎倫" },
    ],
    phrase: "Was kostet das?",
    phrase_zh: "這個多少錢？",
    grammar: "\"Wie viel kostet...?\" 也是問價格的常用說法",
    challenge: "練習回答：Das kostet fünf Euro.",
    culture: "德國有很多週六早市（Wochenmarkt），賣新鮮蔬果與在地特產"
  },
  {
    topic: "在餐廳 At the Restaurant",
    words: [
      { de: "die Speisekarte", zh: "菜單", pron: "虛派瑟卡爾特" },
      { de: "bestellen / empfehlen", zh: "點餐 / 推薦", pron: "貝虛特勒 / 恩普費倫" },
      { de: "lecker / nicht schlecht", zh: "好吃 / 不錯", pron: "勒克爾 / 尼赫特 虛勒赫特" },
    ],
    phrase: "Ich würde gerne bestellen.",
    phrase_zh: "我想點餐了。",
    grammar: "\"würde + 動詞\" 是有禮貌的請求方式",
    challenge: "對服務生說：Die Speisekarte, bitte!",
    culture: "德國餐廳通常要等服務生來帶位，不能自己隨便坐"
  },
  {
    topic: "身體部位 Body Parts",
    words: [
      { de: "der Kopf / der Bauch", zh: "頭 / 肚子", pron: "科普夫 / 包赫" },
      { de: "die Hand / der Fuß", zh: "手 / 腳", pron: "漢特 / 富斯" },
      { de: "der Rücken / das Bein", zh: "背 / 腿", pron: "呂克恩 / 拜因" },
    ],
    phrase: "Mir tut der Kopf weh.",
    phrase_zh: "我頭痛。",
    grammar: "\"Mir tut ___ weh.\" 是表示身體某部位痛的固定說法",
    challenge: "練習說：Mir tut der Bauch weh.",
    culture: "德國有完善的醫療保險制度，看診前通常要預約"
  },
  {
    topic: "數字 11-100 Numbers",
    words: [
      { de: "elf / zwölf / dreizehn", zh: "十一 / 十二 / 十三", pron: "艾夫 / 茨沃夫 / 揣澤恩" },
      { de: "zwanzig / dreißig / vierzig", zh: "二十 / 三十 / 四十", pron: "茨萬齊克 / 揣西克 / 費爾齊克" },
      { de: "hundert / tausend", zh: "一百 / 一千", pron: "洪德爾特 / 陶森特" },
    ],
    phrase: "Das kostet neunzehn Euro fünfzig.",
    phrase_zh: "這個要十九歐元五十分。",
    grammar: "21-99 的說法：個位在前、十位在後，中間加 und：einundzwanzig（21）",
    challenge: "用德文說出你的年齡！",
    culture: "歐元（Euro）是德國貨幣，1 Euro = 100 Cent"
  },
  {
    topic: "月份 Months",
    words: [
      { de: "Januar / Februar / März", zh: "一月 / 二月 / 三月", pron: "亞努阿爾 / 費布魯阿爾 / 梅爾茨" },
      { de: "April / Mai / Juni", zh: "四月 / 五月 / 六月", pron: "阿普里爾 / 麥 / 尤尼" },
      { de: "Juli / August / September", zh: "七月 / 八月 / 九月", pron: "尤利 / 奧古斯特 / 澤普騰伯" },
    ],
    phrase: "Ich habe im März Geburtstag.",
    phrase_zh: "我的生日在三月。",
    grammar: "月份前面用 \"im\"：im Januar（在一月）",
    challenge: "說出你的生日月份：Ich habe im ___ Geburtstag.",
    culture: "德國人很重視生日，但不能在生日前提前祝賀，這被認為不吉利！"
  },
  {
    topic: "日常動詞 Common Verbs",
    words: [
      { de: "essen / trinken / schlafen", zh: "吃 / 喝 / 睡", pron: "艾森 / 欽肯 / 虛拉芬" },
      { de: "gehen / fahren / kommen", zh: "走 / 搭車 / 來", pron: "給恩 / 法倫 / 科門" },
      { de: "arbeiten / lernen / spielen", zh: "工作 / 學習 / 玩", pron: "阿爾拜騰 / 勒爾南 / 虛皮倫" },
    ],
    phrase: "Ich lerne jeden Tag Deutsch.",
    phrase_zh: "我每天學德文。",
    grammar: "規則動詞變化：ich lerne / du lernst / er lernt",
    challenge: "說說你今天做了什麼：Ich habe heute ___.",
    culture: "德國人工作與生活分明，下班後通常不回工作訊息"
  },
  {
    topic: "形容詞 Adjectives",
    words: [
      { de: "groß / klein / lang", zh: "大 / 小 / 長", pron: "格羅斯 / 克萊因 / 朗" },
      { de: "schnell / langsam / laut", zh: "快 / 慢 / 吵", pron: "虛內爾 / 朗薩姆 / 勞特" },
      { de: "schön / interessant / langweilig", zh: "美麗 / 有趣 / 無聊", pron: "虛恩 / 因特瑞桑特 / 朗懷利希" },
    ],
    phrase: "Berlin ist eine schöne Stadt.",
    phrase_zh: "柏林是一個美麗的城市。",
    grammar: "形容詞放在名詞前面要加詞尾，放後面不用變化",
    challenge: "描述你今天的心情：Ich bin heute ___.",
    culture: "德國人評價事物很直接，說 \"nicht schlecht\"（不錯）其實是很高的評價！"
  },
  {
    topic: "住宅 Home & Rooms",
    words: [
      { de: "die Wohnung / das Haus", zh: "公寓 / 房子", pron: "沃農 / 浩斯" },
      { de: "das Zimmer / die Küche", zh: "房間 / 廚房", pron: "奇默 / 克依赫" },
      { de: "das Badezimmer / der Garten", zh: "浴室 / 花園", pron: "巴德奇默 / 加爾騰" },
    ],
    phrase: "Ich wohne in einer kleinen Wohnung.",
    phrase_zh: "我住在一個小公寓裡。",
    grammar: "\"wohnen\"（住）是描述居住的動詞：ich wohne in ___",
    challenge: "描述你住的地方：Ich wohne in ___.",
    culture: "德國租房率很高，很多人一輩子租房，擁有自己的房子並不是主流目標"
  },
  {
    topic: "興趣嗜好 Hobbies",
    words: [
      { de: "Musik hören / lesen", zh: "聽音樂 / 閱讀", pron: "穆齊克 侯倫 / 勒澤恩" },
      { de: "Sport treiben / reisen", zh: "運動 / 旅行", pron: "虛波爾特 崔本 / 萊澤恩" },
      { de: "kochen / tanzen / singen", zh: "煮飯 / 跳舞 / 唱歌", pron: "科亨 / 騰森 / 辛根" },
    ],
    phrase: "Was machst du in deiner Freizeit?",
    phrase_zh: "你空閒時間做什麼？",
    grammar: "\"gern\" 放在動詞後表示喜歡：Ich lese gern.（我喜歡閱讀）",
    challenge: "說出你的興趣：Ich ___ gern.",
    culture: "德國人非常重視休閒時間（Freizeit），這是工作與生活平衡的重要部分"
  },
  {
    topic: "在超市 At the Supermarket",
    words: [
      { de: "das Obst / das Gemüse", zh: "水果 / 蔬菜", pron: "歐布斯特 / 格繆澤" },
      { de: "die Milch / die Butter", zh: "牛奶 / 奶油", pron: "米爾赫 / 布特爾" },
      { de: "die Kasse / der Einkaufswagen", zh: "收銀台 / 購物車", pron: "卡瑟 / 艾因考夫斯瓦根" },
    ],
    phrase: "Wo finde ich die Milch?",
    phrase_zh: "請問牛奶在哪裡？",
    grammar: "\"finden\"（找到）的問句：Wo finde ich ___?",
    challenge: "列出你今天要買的三樣東西的德文！",
    culture: "德國超市結帳很快，要自己快速打包，動作慢會引來不耐煩的目光"
  },
  {
    topic: "緊急狀況 Emergency Phrases",
    words: [
      { de: "Hilfe! / Vorsicht!", zh: "救命！/ 小心！", pron: "希爾費 / 佛爾錫赫特" },
      { de: "die Polizei / der Arzt", zh: "警察 / 醫生", pron: "波利柴 / 阿爾茨特" },
      { de: "das Krankenhaus / die Apotheke", zh: "醫院 / 藥局", pron: "克朗肯浩斯 / 阿波泰克" },
    ],
    phrase: "Rufen Sie bitte die Polizei!",
    phrase_zh: "請打電話叫警察！",
    grammar: "緊急情況下用「命令句」，動詞放句首",
    challenge: "記住德國緊急電話：警察 110，消防救護 112",
    culture: "德國緊急救援電話免費且24小時服務，旅遊時務必記下來！"
  },
  {
    topic: "在旅館 At the Hotel",
    words: [
      { de: "das Zimmer / das Einzelzimmer", zh: "房間 / 單人房", pron: "奇默 / 艾因策爾奇默" },
      { de: "das Doppelzimmer / der Schlüssel", zh: "雙人房 / 鑰匙", pron: "多佩爾奇默 / 虛呂塞爾" },
      { de: "das Frühstück / die Reservierung", zh: "早餐 / 預訂", pron: "弗呂虛圖克 / 瑞澤爾維隆" },
    ],
    phrase: "Ich habe eine Reservierung auf den Namen Candice.",
    phrase_zh: "我有一個以 Candice 名義的訂房。",
    grammar: "\"auf den Namen ___\" 用來說「以某人名義」",
    challenge: "練習問：Ist das Frühstück inbegriffen?（早餐含在內嗎？）",
    culture: "德國旅館早餐通常非常豐盛，有麵包、起司、香腸、水煮蛋等"
  },
  {
    topic: "在機場 At the Airport",
    words: [
      { de: "der Flug / der Flughafen", zh: "航班 / 機場", pron: "弗魯克 / 弗魯克哈芬" },
      { de: "das Gepäck / der Pass", zh: "行李 / 護照", pron: "格佩克 / 帕斯" },
      { de: "der Abflug / die Ankunft", zh: "出發 / 抵達", pron: "阿布弗魯克 / 安孔夫特" },
    ],
    phrase: "Wo ist der Gate für Flug LH123?",
    phrase_zh: "LH123 航班的登機門在哪裡？",
    grammar: "\"Wo ist...?\" 是問地點最基本的句型",
    challenge: "練習說：Mein Flug geht um ___ Uhr ab.",
    culture: "德國最大機場是法蘭克福機場（Flughafen Frankfurt），是歐洲最繁忙的機場之一"
  },
  {
    topic: "禮貌用語 Polite Expressions",
    words: [
      { de: "Danke schön / Bitte schön", zh: "非常感謝 / 不客氣", pron: "當克 虛恩 / 比特 虛恩" },
      { de: "Entschuldigung / Es tut mir leid", zh: "不好意思 / 對不起", pron: "恩虛爾迪崗 / 艾斯 圖特 米爾 萊特" },
      { de: "Natürlich / Selbstverständlich", zh: "當然 / 理所當然", pron: "那圖爾利赫 / 澤爾普斯特費爾虛坦特利赫" },
    ],
    phrase: "Könnten Sie das bitte wiederholen?",
    phrase_zh: "可以請您重複一遍嗎？",
    grammar: "\"Könnten Sie...?\" 是非常有禮貌的請求方式",
    challenge: "當別人說 Danke，你要回答：Bitte schön!",
    culture: "德國人直接但有禮，說話直接不代表不禮貌"
  },
  {
    topic: "食物過敏 Food Allergies",
    words: [
      { de: "die Allergie / allergisch", zh: "過敏 / 過敏的", pron: "阿勒爾吉 / 阿勒爾吉虛" },
      { de: "vegetarisch / vegan", zh: "素食的 / 純素的", pron: "費格塔里虛 / 費根" },
      { de: "die Nuss / das Gluten", zh: "堅果 / 麩質", pron: "努斯 / 格魯騰" },
    ],
    phrase: "Ich bin allergisch gegen Nüsse.",
    phrase_zh: "我對堅果過敏。",
    grammar: "\"allergisch gegen ___\" 表示對某物過敏",
    challenge: "練習說出你的飲食限制！",
    culture: "德國餐廳對食物過敏標示越來越完善，可以放心詢問"
  },
  {
    topic: "在藥局 At the Pharmacy",
    words: [
      { de: "die Tablette / die Salbe", zh: "藥錠 / 藥膏", pron: "塔布勒特 / 扎爾貝" },
      { de: "das Pflaster / das Fieber", zh: "OK繃 / 發燒", pron: "普拉斯特 / 費伯" },
      { de: "der Husten / der Schnupfen", zh: "咳嗽 / 流鼻水", pron: "虛斯騰 / 虛努芬" },
    ],
    phrase: "Ich brauche etwas gegen Kopfschmerzen.",
    phrase_zh: "我需要一些治頭痛的藥。",
    grammar: "\"gegen ___\" 在這裡表示「對抗、治療」",
    challenge: "練習說你的症狀：Ich habe ___ seit ___ Tagen.",
    culture: "在德國，一般藥品必須在藥局（Apotheke）購買，超市不賣藥"
  },
  {
    topic: "談論天氣進階 Weather (Advanced)",
    words: [
      { de: "der Nebel / das Gewitter", zh: "霧 / 雷雨", pron: "內伯爾 / 格維特爾" },
      { de: "bewölkt / sonnig / regnerisch", zh: "多雲 / 晴天 / 下雨", pron: "貝沃爾克特 / 尊尼希 / 雷格內里虛" },
      { de: "die Temperatur / der Grad", zh: "溫度 / 度", pron: "騰佩拉圖爾 / 格拉特" },
    ],
    phrase: "Es sind heute 15 Grad.",
    phrase_zh: "今天氣溫是 15 度。",
    grammar: "溫度說法：Es sind ___ Grad.（是幾度）",
    challenge: "查一下德國今天的天氣，用德文描述！",
    culture: "德國夏天舒適宜人，但冬天日照很少，很多人會有「冬季憂鬱」"
  },
  {
    topic: "德國文化 German Culture",
    words: [
      { de: "das Oktoberfest", zh: "十月啤酒節", pron: "歐克托伯費斯特" },
      { de: "die Bratwurst / das Sauerkraut", zh: "烤香腸 / 酸菜", pron: "布拉特烏斯特 / 蘇爾克勞特" },
      { de: "das Schloss / der Dom", zh: "城堡 / 大教堂", pron: "虛洛斯 / 多姆" },
    ],
    phrase: "Deutschland ist wunderschön!",
    phrase_zh: "德國真的很美！",
    grammar: "\"wunderschön\" = wunder（奇蹟）+ schön（美麗）= 超級美麗",
    challenge: "說出一個你想去的德國城市！",
    culture: "德國有超過 20,000 座城堡，是世界上城堡密度最高的國家之一！"
  },
  {
    topic: "綜合複習 Review Day",
    words: [
      { de: "Ich spreche ein bisschen Deutsch.", zh: "我會說一點德文。", pron: "依赫 虛普瑞赫 艾因 比斯亨 多伊奇" },
      { de: "Können Sie langsamer sprechen?", zh: "您可以說慢一點嗎？", pron: "科能 吉 朗薩姆爾 虛普瑞亨" },
      { de: "Ich verstehe nicht.", zh: "我不懂。", pron: "依赫 費爾虛提 尼赫特" },
    ],
    phrase: "Ich lerne Deutsch. Es macht Spaß!",
    phrase_zh: "我在學德文，很好玩！",
    grammar: "\"Es macht Spaß\"（很有趣/很好玩）是日常常用表達",
    challenge: "回顧一下這一個月學了什麼，選一個最喜歡的單字！",
    culture: "德文是全球約 1 億人的母語，學德文為你打開歐洲的大門！"
  }
];

// ============================================================
// 主要執行函式 — 每天由定時觸發器自動呼叫
// ============================================================
function sendDailyLesson() {
  // 用 PropertiesService 記錄目前進度到第幾天
  const props = PropertiesService.getScriptProperties();
  let dayIndex = parseInt(props.getProperty('dayIndex') || '0');

  // 取得今日課程，超過30天後自動循環
  const lesson = LESSONS[dayIndex % LESSONS.length];

  // 組合並發送訊息
  const message = formatLesson(lesson, dayIndex + 1);
  sendLineMessage(message);

  // 更新天數計數
  props.setProperty('dayIndex', String(dayIndex + 1));
  Logger.log('已發送第 ' + (dayIndex + 1) + ' 天的課程：' + lesson.topic);
}

// ============================================================
// 格式化訊息內容
// ============================================================
function formatLesson(lesson, day) {
  const words = lesson.words
    .map(w => `• ${w.de}（${w.pron}）= ${w.zh}`)
    .join('\n');

  return `🇩🇪 第${day}天德文練習

━━━━━━━━━━━━
📚 今日主題：${lesson.topic}

🔤 單字
${words}

💬 實用句子
「${lesson.phrase}」
→ ${lesson.phrase_zh}

🧠 文法小提示
${lesson.grammar}

🎯 今日挑戰
${lesson.challenge}

🌍 文化小知識
${lesson.culture}
━━━━━━━━━━━━
Viel Erfolg! 加油！🎉`;
}

// ============================================================
// 呼叫 LINE Messaging API 發送 Push Message
// ============================================================
function sendLineMessage(text) {
  const url = 'https://api.line.me/v2/bot/message/push';

  const payload = {
    to: USER_ID,
    messages: [{ type: 'text', text: text }]
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    headers: { 'Authorization': 'Bearer ' + LINE_ACCESS_TOKEN },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  };

  const response = UrlFetchApp.fetch(url, options);
  Logger.log('LINE API 回應：' + response.getContentText());
}

// ============================================================
// 測試用函式 — 手動執行確認訊息是否正常發送
// ============================================================
function testSend() {
  sendLineMessage('🇩🇪 Hallo! 測試成功！\nSprechen Sie Bitte Bot 已準備好，每天德文練習即將開始！\nViel Erfolg! 加油！');
}
