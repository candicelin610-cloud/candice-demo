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
    """建立所有資料表（若不存在）。"""
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
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id    TEXT PRIMARY KEY,
            nickname   TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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


def set_nickname(user_id: str, nickname: str) -> None:
    """儲存或更新使用者自訂代號。"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO user_profiles (user_id, nickname, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id) DO UPDATE SET
            nickname = excluded.nickname,
            updated_at = excluded.updated_at
    """, (user_id, nickname))
    conn.commit()
    conn.close()


def get_nickname(user_id: str):
    """取得使用者自訂代號，未設定則回傳 None。"""
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT nickname FROM user_profiles WHERE user_id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return row[0] if row else None


def _format_duration(seconds) -> str:
    """將秒數轉換為易讀的中文時間格式。"""
    if seconds is None or seconds < 1:
        return "< 1 秒"
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds} 秒"
    minutes, secs = divmod(seconds, 60)
    if minutes < 60:
        return f"{minutes} 分 {secs} 秒" if secs else f"{minutes} 分"
    hours, mins = divmod(minutes, 60)
    if hours < 24:
        return f"{hours} 小時 {mins} 分" if mins else f"{hours} 小時"
    days, hrs = divmod(hours, 24)
    return f"{days} 天 {hrs} 小時" if hrs else f"{days} 天"


def get_leaderboard(limit: int = 10) -> list[dict]:
    """
    回傳已集滿 9/9 拼圖的前 N 名玩家，依完成時間（最後一塊 - 第一塊）升冪排列。
    每筆資料：rank, nickname, seconds, duration_str, finished_at
    """
    total = len(PIECES)
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("""
        SELECT
            pc.user_id,
            COALESCE(up.nickname, '神秘玩家') AS nickname,
            (JULIANDAY(MAX(pc.checked_at)) - JULIANDAY(MIN(pc.checked_at))) * 86400 AS seconds_taken,
            MAX(pc.checked_at) AS finished_at
        FROM puzzle_checkins pc
        LEFT JOIN user_profiles up ON pc.user_id = up.user_id
        GROUP BY pc.user_id
        HAVING COUNT(DISTINCT pc.piece_id) = ?
        ORDER BY seconds_taken ASC
        LIMIT ?
    """, (total, limit)).fetchall()
    conn.close()

    result = []
    for rank, (user_id, nickname, seconds, finished_at) in enumerate(rows, start=1):
        result.append({
            "rank": rank,
            "nickname": nickname,
            "seconds": seconds or 0,
            "duration_str": _format_duration(seconds),
            "finished_at": finished_at,
        })
    return result


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
