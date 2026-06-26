"""
所有 Flex Message / Carousel / Quick Reply 的內容建構函式。
統一回傳 line-bot-sdk 的訊息物件，handlers.py 只需呼叫並 reply_message。
"""
import random

from linebot.v3.messaging.models import (
    FlexMessage,
    TextMessage,
    QuickReply,
    QuickReplyItem,
    PostbackAction,
    FlexBubble,
    FlexCarousel,
)

import stamps

DETAIL_URL = "https://example.com"
VIDEO_URL = "https://www.youtube.com/watch?v=wCkerYMffMo"


# ---------------------------------------------------------------------------
# 1. 加入好友歡迎訊息
# ---------------------------------------------------------------------------
def welcome_flex_message():
    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "backgroundColor": "#FFF9C4",
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "text",
                    "text": "🎉 歡迎加入 Weekend GO！",
                    "weight": "bold",
                    "size": "xl",
                    "color": "#5D4037",
                    "wrap": True,
                },
                {
                    "type": "text",
                    "text": "放假不知道去哪？讓我幫你找到今天的目的地！",
                    "size": "sm",
                    "color": "#8D6E63",
                    "wrap": True,
                },
            ],
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "backgroundColor": "#FFF9C4",
            "paddingAll": "20px",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FBC02D",
                    "cornerRadius": "md",
                    "paddingAll": "12px",
                    "action": {
                        "type": "postback",
                        "label": "開始探索 →",
                        "data": "action=activities",
                    },
                    "contents": [
                        {
                            "type": "text",
                            "text": "開始探索 →",
                            "align": "center",
                            "weight": "bold",
                            "color": "#5D4037",
                        }
                    ],
                }
            ],
        },
    }
    return FlexMessage(
        alt_text="歡迎加入 Weekend GO！雙北遊憩 Bot",
        contents=FlexBubble.from_dict(bubble),
    )


def start_text_message():
    return TextMessage(
        text="太棒了！點選下方選單就能開始探索 🎉\n"
        "🚴 活動推薦 / 🗺 一日行程 / 🏅 集章護照\n"
        "都可以從選單直接點選喔！"
    )


# ---------------------------------------------------------------------------
# 3. 活動推薦
# ---------------------------------------------------------------------------
ACTIVITY_DATA = {
    "walk": {
        "title": "🚶 健走",
        "items": [
            {"name": "象山步道", "location": "台北市信義區", "level": "中等", "time": "約 1.5 小時"},
            {"name": "軍艦岩", "location": "台北市北投區", "level": "中等", "time": "約 2 小時"},
            {"name": "虎山步道", "location": "台北市南港區", "level": "簡單", "time": "約 1 小時"},
        ],
    },
    "bike": {
        "title": "🚴 自行車",
        "items": [
            {"name": "淡水河濱自行車道", "location": "新北市淡水區", "level": "簡單", "time": "約 2 小時"},
            {"name": "貓空騎旅", "location": "台北市文山區", "level": "困難", "time": "約 3 小時"},
            {"name": "八里左岸", "location": "新北市八里區", "level": "簡單", "time": "約 1.5 小時"},
        ],
    },
    "park": {
        "title": "🌳 公園散步",
        "items": [
            {"name": "大安森林公園", "location": "台北市大安區", "level": "簡單", "time": "約 1 小時"},
            {"name": "青年公園", "location": "台北市萬華區", "level": "簡單", "time": "約 1 小時"},
            {"name": "板橋435藝文特區", "location": "新北市板橋區", "level": "簡單", "time": "約 1.5 小時"},
        ],
    },
    "trail": {
        "title": "🏞 郊山步道",
        "items": [
            {"name": "陽明山", "location": "台北市士林區", "level": "中等", "time": "約 3 小時"},
            {"name": "烏來", "location": "新北市烏來區", "level": "中等", "time": "約 2.5 小時"},
            {"name": "平溪", "location": "新北市平溪區", "level": "簡單", "time": "約 2 小時"},
        ],
    },
}

RANDOM_COMBOS = [
    {"icon1": "🌿", "name1": "大安森林公園", "icon2": "☕", "name2": "永康街午餐",
     "icon3": "🚶", "name3": "象山步道", "duration": "5 小時", "suitable": "適合輕鬆出遊"},
    {"icon1": "🌳", "name1": "青年公園", "icon2": "🍜", "name2": "萬華小吃",
     "icon3": "🚴", "name3": "淡水河濱自行車道", "duration": "6 小時", "suitable": "適合運動愛好者"},
    {"icon1": "🏞", "name1": "陽明山", "icon2": "🍱", "name2": "士林夜市午餐",
     "icon3": "🚶", "name3": "虎山步道", "duration": "7 小時", "suitable": "適合喜愛大自然的你"},
    {"icon1": "🌉", "name1": "八里左岸", "icon2": "🦐", "name2": "淡水老街美食",
     "icon3": "🚴", "name3": "貓空騎旅", "duration": "6 小時", "suitable": "適合親友出遊"},
]


def activity_category_quick_reply():
    categories = [
        ("🚶 健走", "action=activities&category=walk"),
        ("🚴 自行車", "action=activities&category=bike"),
        ("🌳 公園散步", "action=activities&category=park"),
        ("🏞 郊山步道", "action=activities&category=trail"),
        ("🎯 不知道去哪", "action=activities&category=random"),
    ]
    items = [
        QuickReplyItem(action=PostbackAction(label=label, data=data))
        for label, data in categories
    ]
    return TextMessage(
        text="想做什麼類型的活動呢？選一個分類給你推薦 👇",
        quick_reply=QuickReply(items=items),
    )


def _activity_bubble(item):
    return {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
                {"type": "text", "text": item["name"], "weight": "bold", "size": "lg", "wrap": True},
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {"type": "text", "text": "📍 地點", "size": "sm", "color": "#999999", "flex": 2},
                        {"type": "text", "text": item["location"], "size": "sm", "color": "#666666", "flex": 5, "wrap": True},
                    ],
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {"type": "text", "text": "💪 難度", "size": "sm", "color": "#999999", "flex": 2},
                        {"type": "text", "text": item["level"], "size": "sm", "color": "#666666", "flex": 5},
                    ],
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {"type": "text", "text": "⏰ 時間", "size": "sm", "color": "#999999", "flex": 2},
                        {"type": "text", "text": item["time"], "size": "sm", "color": "#666666", "flex": 5},
                    ],
                },
            ],
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FBC02D",
                    "cornerRadius": "md",
                    "paddingAll": "12px",
                    "action": {"type": "uri", "label": "查看詳情", "uri": DETAIL_URL},
                    "contents": [
                        {
                            "type": "text",
                            "text": "查看詳情",
                            "align": "center",
                            "weight": "bold",
                            "color": "#5D4037",
                        }
                    ],
                }
            ],
        },
    }


def activity_carousel_message(category):
    if category == "random":
        return random_recommendation_message()

    info = ACTIVITY_DATA.get(category)
    if not info:
        return TextMessage(text="找不到這個分類，請重新選擇喔！")

    carousel = {
        "type": "carousel",
        "contents": [_activity_bubble(item) for item in info["items"]],
    }
    return FlexMessage(
        alt_text=f"{info['title']} 活動推薦",
        contents=FlexCarousel.from_dict(carousel),
    )


def random_recommendation_message():
    combo = random.choice(RANDOM_COMBOS)
    text = (
        "今天推薦你這條路線 🎲\n"
        f"{combo['icon1']} {combo['name1']} → {combo['icon2']} {combo['name2']} → "
        f"{combo['icon3']} {combo['name3']}\n"
        f"共約 {combo['duration']}｜{combo['suitable']}"
    )
    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {"type": "text", "text": text, "wrap": True, "size": "md"},
            ],
        },
        "footer": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "backgroundColor": "#FBC02D",
                    "cornerRadius": "md",
                    "paddingAll": "12px",
                    "action": {"type": "postback", "label": "開始今天行程", "data": "action=start_today"},
                    "contents": [
                        {
                            "type": "text",
                            "text": "開始今天行程",
                            "align": "center",
                            "weight": "bold",
                            "color": "#5D4037",
                        }
                    ],
                }
            ],
        },
    }
    return FlexMessage(
        alt_text="今天推薦你這條路線",
        contents=FlexBubble.from_dict(bubble),
    )


def start_today_text_message():
    return TextMessage(text="祝你有美好的一天 🌞 出發前記得帶水跟防曬，玩得愉快！")


# ---------------------------------------------------------------------------
# 4. 一日行程
# ---------------------------------------------------------------------------
ITINERARY_DATA = {
    "taipei": {
        "title": "台北市一日遊",
        "steps": [
            ("10:00", "大安森林公園"),
            ("12:00", "永康街午餐"),
            ("14:00", "華山文創"),
            ("16:00", "松菸市集"),
        ],
    },
    "newtaipei": {
        "title": "新北市一日遊",
        "steps": [
            ("09:00", "淡水老街"),
            ("11:00", "漁人碼頭"),
            ("13:00", "八里左岸午餐"),
            ("15:00", "十三行博物館"),
        ],
    },
    "family": {
        "title": "親子同遊一日遊",
        "steps": [
            ("09:30", "兒童新樂園"),
            ("12:00", "士林夜市午餐"),
            ("14:00", "科學教育館"),
            ("16:00", "天母公園"),
        ],
    },
    "photo": {
        "title": "拍照打卡一日遊",
        "steps": [
            ("10:00", "象山步道"),
            ("12:30", "信義區午餐"),
            ("14:00", "中山站老屋"),
            ("16:00", "北投溫泉博物館"),
        ],
    },
}


def itinerary_preference_quick_reply():
    prefs = [
        ("台北市", "action=itinerary&pref=taipei"),
        ("新北市", "action=itinerary&pref=newtaipei"),
        ("親子同遊", "action=itinerary&pref=family"),
        ("拍照打卡", "action=itinerary&pref=photo"),
    ]
    items = [
        QuickReplyItem(action=PostbackAction(label=label, data=data))
        for label, data in prefs
    ]
    return TextMessage(
        text="想規劃哪一種一日行程呢？",
        quick_reply=QuickReply(items=items),
    )


def itinerary_timeline_flex(pref):
    info = ITINERARY_DATA.get(pref)
    if not info:
        return TextMessage(text="找不到這個行程偏好，請重新選擇喔！")

    timeline_contents = []
    for i, (time, place) in enumerate(info["steps"]):
        timeline_contents.append(
            {
                "type": "box",
                "layout": "horizontal",
                "spacing": "md",
                "contents": [
                    {"type": "text", "text": time, "size": "sm", "color": "#06C755", "weight": "bold", "flex": 2},
                    {"type": "text", "text": "●", "size": "sm", "color": "#06C755", "flex": 0},
                    {"type": "text", "text": place, "size": "md", "wrap": True, "flex": 6},
                ],
            }
        )
        if i != len(info["steps"]) - 1:
            timeline_contents.append({"type": "separator", "margin": "sm"})

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": f"🗺 {info['title']}", "weight": "bold", "size": "lg"},
                {"type": "separator", "margin": "md"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "margin": "md",
                    "contents": timeline_contents,
                },
            ],
        },
    }
    return FlexMessage(
        alt_text=info["title"],
        contents=FlexBubble.from_dict(bubble),
    )


# ---------------------------------------------------------------------------
# 5. 集章護照系統
# ---------------------------------------------------------------------------
def passport_flex(user_id):
    user_spots = stamps.get_user_stamps(user_id)
    rows = []
    for spot in stamps.SPOTS:
        mark = "✅" if spot in user_spots else "⬜"
        rows.append(
            {
                "type": "box",
                "layout": "baseline",
                "spacing": "sm",
                "contents": [
                    {"type": "text", "text": mark, "size": "md", "flex": 0},
                    {"type": "text", "text": spot, "size": "md", "wrap": True, "flex": 5},
                ],
            }
        )

    bubble = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {"type": "text", "text": "🏅 集章護照", "weight": "bold", "size": "lg"},
                {"type": "separator", "margin": "md"},
                {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "margin": "md",
                    "contents": rows,
                },
                {
                    "type": "text",
                    "text": "完成活動後輸入「集章 景點名稱」即可蓋章！",
                    "size": "xs",
                    "color": "#999999",
                    "wrap": True,
                    "margin": "md",
                },
            ],
        },
    }
    return FlexMessage(
        alt_text="集章護照",
        contents=FlexBubble.from_dict(bubble),
    )


def my_stamps_text(user_id):
    completed, total, remaining = stamps.get_progress(user_id)
    if remaining == 0:
        return TextMessage(
            text=f"🎉 太厲害了！你已經完成全部 {total} 個景點集章，恭喜達成 Weekend GO 雙北遊憩成就！"
        )
    return TextMessage(
        text=f"目前已完成 {completed}/{total} 個景點集章 🏅\n"
        f"距離完成護照還差 {remaining} 個，繼續加油！"
    )


def stamp_added_text(spot, already_had, user_id):
    completed, total, remaining = stamps.get_progress(user_id)
    if already_had:
        return TextMessage(text=f"「{spot}」之前就蓋過章囉！目前已完成 {completed}/{total} 個 🏅")
    return TextMessage(
        text=f"✅ 已幫你蓋上「{spot}」的章！\n"
        f"目前進度：{completed}/{total}，還差 {remaining} 個就完成護照了！"
    )


def stamp_invalid_text(spot):
    spots_text = "、".join(stamps.SPOTS)
    return TextMessage(
        text=f"找不到「{spot}」這個景點喔，可集章的景點有：\n{spots_text}"
    )


# ---------------------------------------------------------------------------
# 6. 活動影片
# ---------------------------------------------------------------------------
VIDEO_DATA = [
    {"title": "象山步道介紹影片", "desc": "輕鬆走完象山步道，看夜景必去！"},
    {"title": "淡水河濱騎車", "desc": "沿著河岸吹風騎車，超療癒路線"},
    {"title": "陽明山一日遊", "desc": "賞花、泡湯、看夜景一次滿足"},
    {"title": "大安森林公園散步", "desc": "市區綠地小旅行，適合悠閒散步"},
]


def videos_carousel_message():
    bubbles = []
    for video in VIDEO_DATA:
        bubbles.append(
            {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "sm",
                    "contents": [
                        {"type": "text", "text": "🎥 " + video["title"], "weight": "bold", "size": "md", "wrap": True},
                        {"type": "text", "text": video["desc"], "size": "sm", "color": "#666666", "wrap": True},
                    ],
                },
                "footer": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "box",
                            "layout": "vertical",
                            "backgroundColor": "#FBC02D",
                            "cornerRadius": "md",
                            "paddingAll": "12px",
                            "action": {"type": "uri", "label": "觀看影片", "uri": VIDEO_URL},
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "觀看影片",
                                    "align": "center",
                                    "weight": "bold",
                                    "color": "#5D4037",
                                }
                            ],
                        }
                    ],
                },
            }
        )
    carousel = {"type": "carousel", "contents": bubbles}
    return FlexMessage(
        alt_text="活動影片",
        contents=FlexCarousel.from_dict(carousel),
    )


# ---------------------------------------------------------------------------
# 7. FAQ
# ---------------------------------------------------------------------------
FAQ_DATA = [
    {"q": "如何集章？", "a": "完成活動後輸入「集章 景點名稱」即可蓋章"},
    {"q": "活動需要報名嗎？", "a": "本 Bot 推薦的皆為免費自由行活動，不需報名"},
    {"q": "需要付費嗎？", "a": "完全免費！"},
    {"q": "交通方式？", "a": "每個活動頁面都有詳細交通資訊"},
    {"q": "適合帶小孩嗎？", "a": "可選擇「親子同遊」行程，適合全家出遊"},
]


def faq_carousel_message():
    bubbles = []
    for faq in FAQ_DATA:
        bubbles.append(
            {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "spacing": "md",
                    "contents": [
                        {"type": "text", "text": "❓ " + faq["q"], "weight": "bold", "size": "md", "wrap": True},
                        {"type": "separator", "margin": "sm"},
                        {"type": "text", "text": faq["a"], "size": "sm", "color": "#666666", "wrap": True, "margin": "md"},
                    ],
                },
            }
        )
    carousel = {"type": "carousel", "contents": bubbles}
    return FlexMessage(
        alt_text="常見問題 FAQ",
        contents=FlexCarousel.from_dict(carousel),
    )
