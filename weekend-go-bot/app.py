"""
Weekend GO！雙北遊憩 Bot - Flask 主程式
負責接收 LINE Webhook，驗證簽章後分派給對應的事件處理函式。
"""
import os

from dotenv import load_dotenv
from flask import Flask, request, abort

from linebot.v3.webhook import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import ApiClient, MessagingApi, Configuration, ReplyMessageRequest
from linebot.v3.webhooks import MessageEvent, TextMessageContent, PostbackEvent, FollowEvent

import handlers
from puzzle.routes import puzzle_bp
from puzzle.models import init_db

load_dotenv()

LINE_CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

if not LINE_CHANNEL_SECRET or not LINE_CHANNEL_ACCESS_TOKEN:
    raise RuntimeError("請先在 .env 設定 LINE_CHANNEL_SECRET 與 LINE_CHANNEL_ACCESS_TOKEN")

app = Flask(__name__)
app.register_blueprint(puzzle_bp)
init_db()

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)
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
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(reply_token=event.reply_token, messages=reply_messages)
        )


@webhook_handler.add(MessageEvent, message=TextMessageContent)
def on_text_message(event):
    user_id = event.source.user_id
    reply_messages = handlers.handle_text_message(user_id, event.message.text)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(reply_token=event.reply_token, messages=reply_messages)
        )


@webhook_handler.add(PostbackEvent)
def on_postback(event):
    user_id = event.source.user_id
    reply_messages = handlers.handle_postback_event(user_id, event.postback.data)
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(reply_token=event.reply_token, messages=reply_messages)
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
