"""
各功能的事件 handler，負責解析事件內容並呼叫 messages.py 產生回覆訊息。
"""
from urllib.parse import parse_qs

from linebot.models import TextSendMessage

import messages
import stamps


def parse_postback_data(data):
    """將 'action=activities&category=walk' 轉成 {'action': 'activities', 'category': 'walk'}"""
    parsed = parse_qs(data)
    return {key: values[0] for key, values in parsed.items()}


def handle_follow_event():
    """加入好友時的歡迎訊息"""
    return [messages.welcome_flex_message()]


def handle_postback_event(user_id, data):
    """依照 postback data 的 action 分派到對應功能"""
    params = parse_postback_data(data)
    action = params.get("action")

    if action == "start":
        return [messages.start_text_message()]

    if action == "start_today":
        return [messages.start_today_text_message()]

    if action == "activities":
        category = params.get("category")
        if category:
            return [messages.activity_carousel_message(category)]
        return [messages.activity_category_quick_reply()]

    if action == "itinerary":
        pref = params.get("pref")
        if pref:
            return [messages.itinerary_timeline_flex(pref)]
        return [messages.itinerary_preference_quick_reply()]

    if action == "passport":
        return [messages.passport_flex(user_id)]

    if action == "my_stamps":
        return [messages.my_stamps_text(user_id)]

    if action == "videos":
        return [messages.videos_carousel_message()]

    if action == "faq":
        return [messages.faq_carousel_message()]

    return [TextSendMessage(text="收到囉！但這個指令我還不認識 🤔")]


def handle_text_message(user_id, text):
    """處理文字訊息，目前支援「集章 景點名稱」指令"""
    text = text.strip()

    if text.startswith("集章"):
        spot = text[2:].strip()
        if not spot:
            spots_text = "、".join(stamps.SPOTS)
            return [TextSendMessage(text=f"請輸入「集章 景點名稱」喔，例如「集章 象山」。\n可集章的景點有：\n{spots_text}")]

        success, already_had = stamps.add_stamp(user_id, spot)
        if not success:
            return [messages.stamp_invalid_text(spot)]
        return [messages.stamp_added_text(spot, already_had, user_id)]

    return [
        TextSendMessage(
            text="點選下方選單就能探索 Weekend GO 的功能喔 🎉\n"
            "🚴 活動推薦 / 🗺 一日行程 / 🏅 集章護照 / 🎥 活動影片 / ❓ FAQ / 👤 我的集章"
        )
    ]
