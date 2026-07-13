"""
拼圖集章資料層：SQLite 儲存使用者已解鎖的碎片。
每個碎片對應雙北一個景點，共 9 片（3×3）。
"""
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "puzzle.db")

# 9 個拼圖碎片，與景點對應
PIECES = [
    {"id": "1", "name": "象山步道",     "location": "台北市信義區", "emoji": "🐘",
     "fun_fact": "頂峰可俯瞰台北 101 全景，日落時分是最美的城市剪影"},
    {"id": "2", "name": "大安森林公園", "location": "台北市大安區", "emoji": "🌳",
     "fun_fact": "面積約 26 公頃，是台北市最大都市公園，有「城市之肺」美稱"},
    {"id": "3", "name": "陽明山",       "location": "台北市士林區", "emoji": "🌋",
     "fun_fact": "由大屯火山群組成，春天芒草如雪，七星山海拔 1,120 公尺"},
    {"id": "4", "name": "淡水老街",     "location": "新北市淡水區", "emoji": "🏮",
     "fun_fact": "清代北台灣最繁忙的貿易港口，西班牙、荷蘭都曾在此設砦"},
    {"id": "5", "name": "八里左岸",     "location": "新北市八里區", "emoji": "🌊",
     "fun_fact": "位於淡水河出海口，與淡水隔河相望，以文蛤養殖和自行車道著稱"},
    {"id": "6", "name": "平溪",         "location": "新北市平溪區", "emoji": "🏮",
     "fun_fact": "天燈節發源地，早年礦工以天燈傳遞平安訊號，沿用至今成節慶"},
    {"id": "7", "name": "烏來",         "location": "新北市烏來區", "emoji": "♨️",
     "fun_fact": "泰雅族傳統聚落，「烏來」在泰雅語意為「冒煙的水」，指天然溫泉"},
    {"id": "8", "name": "虎山步道",     "location": "台北市南港區", "emoji": "🐯",
     "fun_fact": "四獸山之一，視野媲美象山，與象山、獅山、豹山形成完整步道網"},
    {"id": "9", "name": "軍艦岩",       "location": "台北市北投區", "emoji": "⛰️",
     "fun_fact": "因花崗岩山形酷似軍艦而得名，是台北市區罕見的大面積裸露岩壁"},
]

VALID_PIECE_IDS = {p["id"] for p in PIECES}
PIECE_BY_ID = {p["id"]: p for p in PIECES}


def init_db():
    """建立 puzzle_checkins 資料表（若不存在）。"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS puzzle_checkins (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    TEXT NOT NULL,
            piece_id   TEXT NOT NULL,
            checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, piece_id)
        )
    """)
    conn.commit()
    conn.close()


def get_user_pieces(user_id: str) -> set:
    """回傳該使用者已解鎖的 piece_id 集合。"""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT piece_id FROM puzzle_checkins WHERE user_id = ?", (user_id,)
    ).fetchall()
    conn.close()
    return {row[0] for row in rows}


def add_piece(user_id: str, piece_id: str) -> tuple[bool, bool]:
    """
    解鎖一個碎片。
    回傳 (success, already_had)：
      - success=False 表示 piece_id 無效
      - already_had=True 表示之前就有了
    """
    if piece_id not in VALID_PIECE_IDS:
        return False, False
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            "INSERT INTO puzzle_checkins (user_id, piece_id) VALUES (?, ?)",
            (user_id, piece_id),
        )
        conn.commit()
        return True, False
    except sqlite3.IntegrityError:
        return True, True
    finally:
        conn.close()
