# Weekend GO！雙北遊憩 Bot

放假不知道去哪？這是一個 LINE Bot，幫你推薦雙北（台北市／新北市）的週末活動、一日行程，
還有集章護照可以收集踩點成就！

## 技術架構

- Python 3.9
- Flask（接收 LINE Webhook）
- line-bot-sdk（LINE 官方 Python SDK）
- 資料儲存：JSON 檔案（`data/stamps.json`），不使用資料庫

## 檔案結構

```
weekend-go-bot/
├── app.py              # Flask 主程式，接收 webhook 並分派事件
├── handlers.py          # 各功能 handler（解析 postback / 文字訊息）
├── messages.py           # 所有 Flex Message / Carousel / Quick Reply 內容
├── stamps.py             # 集章護照系統邏輯（讀寫 stamps.json）
├── setup_rich_menu.py     # 建立並上傳 Rich Menu 的獨立腳本
├── data/
│   └── stamps.json       # 集章資料（初始為空 {}）
├── requirements.txt
├── .env                  # LINE channel 密鑰設定
└── README.md
```

## 功能總覽

1. **加入好友歡迎訊息**：Flex Message 歡迎卡片 + 「開始探索」按鈕
2. **Rich Menu**（2 列 3 欄）：活動推薦 / 一日行程 / 集章護照 / 活動影片 / FAQ / 我的集章
3. **活動推薦**：依分類（健走／自行車／公園散步／郊山步道／不知道去哪）回傳活動卡片 Carousel
4. **一日行程**：4 套固定路線（台北市／新北市／親子同遊／拍照打卡），以時間軸 Flex Message 顯示
5. **集章護照**：JSON 記錄每位使用者的集章狀態，輸入「集章 景點名稱」即可蓋章
6. **活動影片**：精選影片 Carousel（YouTube 連結）
7. **FAQ**：常見問題 Carousel

## 啟動方式

### 1. 安裝套件

```bash
cd weekend-go-bot
pip install -r requirements.txt
```

### 2. 確認 `.env` 設定

`.env` 內已包含：

```
LINE_CHANNEL_SECRET=你的 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN=你的 Channel Access Token
```

請依實際的 LINE Developers Console 設定值確認是否需要更新。

### 3. 啟動 Flask 伺服器

```bash
python app.py
```

伺服器預設會在 `http://localhost:5001` 啟動，Webhook 路徑為 `/callback`。
（埠號選擇 5001 是因為 macOS 的 AirPlay Receiver 預設會佔用 5000 埠；若你已關閉該功能，也可以把 `app.py` 裡的 port 改回 5000。）

### 4. 另開一個終端機，啟動 ngrok 對外連線

```bash
ngrok http 5001
```

啟動後會得到一個類似 `https://xxxx-xx-xx-xx-xx.ngrok-free.app` 的網址。

### 5. 設定 LINE Webhook URL

到 [LINE Developers Console](https://developers.line.biz/console/) → 你的 Channel →
Messaging API → Webhook settings，將 Webhook URL 設定為：

```
https://你的ngrok網址/callback
```

並開啟「Use webhook」。

### 6. 建立 Rich Menu（首次設定執行一次即可）

```bash
python setup_rich_menu.py
```

此腳本會自動產生選單圖片、建立 6 格 Rich Menu，並設為所有使用者的預設選單。
若之後想更換 Rich Menu 內容，重新執行此腳本即可（會建立一個新的 Rich Menu 並覆蓋預設設定）。

### 7. 測試

用手機加入 LINE Bot 好友，應該會立即收到歡迎訊息，並看到下方的 Rich Menu。

- 點選 Rich Menu 上的「活動推薦」「一日行程」等功能即可體驗對應流程
- 直接在聊天室輸入「集章 象山」可以測試集章功能（合法景點清單見下方）

可集章景點（共 8 個）：
象山、軍艦岩、虎山、大安森林公園、淡水老街、陽明山、貓空、八里左岸

## 注意事項

- `data/stamps.json` 是唯一的資料儲存檔案，正式上線建議改用真正的資料庫（PostgreSQL / SQLite 等），
  目前以 JSON 檔案儲存僅適合小型專案或 Demo 使用。
- 所有活動詳情按鈕與影片連結目前皆使用範例網址（`https://example.com`、
  `https://www.youtube.com/watch?v=dQw4w9WgXcQ`），正式上線前請替換成真實連結。
