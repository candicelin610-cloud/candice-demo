"""
集章護照系統
使用 JSON 檔案（data/stamps.json）儲存每個 user_id 已完成的集章景點清單。
"""
import json
import os
import threading

# 集章護照可集章的 8 個景點（順序即顯示順序）
SPOTS = [
    "象山",
    "軍艦岩",
    "虎山",
    "大安森林公園",
    "淡水老街",
    "陽明山",
    "貓空",
    "八里左岸",
]

_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "stamps.json")
_lock = threading.Lock()  # 避免多個 request 同時讀寫 JSON 檔造成資料毀損


def load_stamps():
    """讀取所有使用者的集章資料，回傳 dict：{user_id: [spot1, spot2, ...]}"""
    if not os.path.exists(_DATA_PATH):
        return {}
    with open(_DATA_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return {}
        return json.loads(content)


def save_stamps(data):
    """將集章資料寫回 JSON 檔"""
    with open(_DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_user_stamps(user_id):
    """取得某位使用者已集章的景點清單"""
    data = load_stamps()
    return data.get(user_id, [])


def add_stamp(user_id, spot):
    """
    幫使用者蓋章。
    回傳 tuple: (success: bool, already_had: bool)
    - spot 不在 SPOTS 名單內 -> (False, False)
    - 已經蓋過章 -> (True, True)
    - 新蓋章成功 -> (True, False)
    """
    if spot not in SPOTS:
        return False, False

    with _lock:
        data = load_stamps()
        user_spots = data.get(user_id, [])
        if spot in user_spots:
            return True, True
        user_spots.append(spot)
        data[user_id] = user_spots
        save_stamps(data)
        return True, False


def get_progress(user_id):
    """回傳 (已完成數量, 總數量, 還差多少)"""
    user_spots = get_user_stamps(user_id)
    completed = len(user_spots)
    total = len(SPOTS)
    return completed, total, total - completed
