"""
Weekend GO！雙北遊憩 Bot - Flask 主程式
負責接收 LINE Webhook，驗證簽章後分派給對應的事件處理函式。
"""
import os

from dotenv import load_dotenv
from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, PostbackEvent, FollowEvent

import handlers

load_dotenv()

LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

if not LINE_CHANNEL_SECRET or not LINE_CHANNEL_ACCESS_TOKEN:
    raise RuntimeError("請先在 .env 設定 LINE_CHANNEL_SECRET 與 LINE_CHANNEL_ACCESS_TOKEN")

app = Flask(__name__)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
webhook_handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        webhook_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@app.route("/", methods=["GET"])
def index():
    return "Weekend GO！雙北遊憩 Bot is running."


@webhook_handler.add(FollowEvent)
def on_follow(event):
    reply_messages = handlers.handle_follow_event()
    line_bot_api.reply_message(event.reply_token, reply_messages)


@webhook_handler.add(MessageEvent, message=TextMessage)
def on_text_message(event):
    user_id = event.source.user_id
    reply_messages = handlers.handle_text_message(user_id, event.message.text)
    line_bot_api.reply_message(event.reply_token, reply_messages)


@webhook_handler.add(PostbackEvent)
def on_postback(event):
    user_id = event.source.user_id
    reply_messages = handlers.handle_postback_event(user_id, event.postback.data)
    line_bot_api.reply_message(event.reply_token, reply_messages)


if __name__ == "__main__":
    # 5000 埠在 macOS 上常被 AirPlay Receiver 佔用，因此改用 5001
    app.run(host="0.0.0.0", port=5001, debug=True)
