"""
建立並設定 Rich Menu（6 格：2 列 3 欄）。

LINE 的 Rich Menu 圖片與設定必須透過 Messaging API 上傳，無法只靠 webhook 完成，
因此用這支獨立腳本：
1. 用 Pillow 產生一張 2500x1686 的 Rich Menu 圖片（6 格 + 文字標籤）
2. 呼叫 LINE API 建立 Rich Menu 並設定 6 個區域的 message action
3. 上傳圖片、並將此 Rich Menu 設為全部使用者的預設選單

執行方式：
    python setup_rich_menu.py
"""
import math
import os

from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

from linebot.v3.messaging import (
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    Configuration,
)
from linebot.v3.messaging.models import (
    RichMenuRequest,
    RichMenuArea,
    RichMenuBounds,
    RichMenuSize,
    MessageAction,
)

load_dotenv()

LINE_CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
if not LINE_CHANNEL_ACCESS_TOKEN:
    raise RuntimeError("請先在 .env 設定 LINE_CHANNEL_ACCESS_TOKEN")

configuration = Configuration(access_token=LINE_CHANNEL_ACCESS_TOKEN)

# Rich Menu 圖片尺寸（LINE 建議的標準尺寸，2 列 3 欄）
MENU_WIDTH = 2500
MENU_HEIGHT = 1686
COL_WIDTH = MENU_WIDTH // 3
ROW_HEIGHT = MENU_HEIGHT // 2

IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "rich_menu.png")

# 6 個格子：(label, icon_key, message_text)，依「第一列 3 格、第二列 3 格」排列
# 點擊按鈕會在對話框自動送出 message_text
MENU_ITEMS = [
    ("活動推薦", "bike",     "🗺️ 活動推薦"),
    ("一日行程", "map",      "🚶 一日行程"),
    ("集章護照", "medal",    "📖 集章護照"),
    ("活動影片", "video",    "🎬 活動影片"),
    ("FAQ",     "question", "❓ FAQ"),
    ("我的集章", "person",   "🏅 我的集章"),
]

# 鵝黃色系配色：依格子位置給不同深淺的黃，圖示與文字統一用深咖啡色
ICON_TEXT_COLOR = "#5D4037"
COLORS = ["#FFF9C4", "#FFF176", "#FFEE58", "#FFD54F", "#FFCA28", "#FFB300"]

# 中文字型：macOS 上 PingFang.ttc 實際路徑因系統版本而異且常無法被 Pillow 直接讀取，
# STHeiti Medium.ttc 是穩定存在於 /System/Library/Fonts 且能正確渲染中文的字型。
FONT_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]


def _load_font(size):
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _draw_bike_icon(draw, cx, cy, r, color, width):
    """簡易自行車線稿：兩個輪子 + 車架"""
    wheel_r = r * 0.42
    left = (cx - r * 0.55, cy + r * 0.3)
    right = (cx + r * 0.55, cy + r * 0.3)
    seat = (cx - r * 0.05, cy - r * 0.5)
    handle = (cx + r * 0.55, cy - r * 0.15)
    pedal = (cx - r * 0.05, cy + r * 0.3)

    draw.ellipse(
        [left[0] - wheel_r, left[1] - wheel_r, left[0] + wheel_r, left[1] + wheel_r],
        outline=color, width=width,
    )
    draw.ellipse(
        [right[0] - wheel_r, right[1] - wheel_r, right[0] + wheel_r, right[1] + wheel_r],
        outline=color, width=width,
    )
    draw.line([left, seat], fill=color, width=width)
    draw.line([seat, pedal], fill=color, width=width)
    draw.line([pedal, right], fill=color, width=width)
    draw.line([seat, handle], fill=color, width=width)
    draw.line([handle, right], fill=color, width=width)


def _draw_map_icon(draw, cx, cy, r, color, width, bg_color):
    """簡易地圖定位點：水滴形（圓頭 + 尖底）中間挖一個圓孔，露出背景色"""
    head_r = r * 0.55
    head_cy = cy - r * 0.2
    tip = (cx, cy + r * 0.65)

    draw.polygon(
        [
            (cx - head_r * 0.95, head_cy + head_r * 0.35),
            (cx + head_r * 0.95, head_cy + head_r * 0.35),
            tip,
        ],
        fill=color,
    )
    draw.ellipse(
        [cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
        fill=color,
    )
    hole_r = head_r * 0.42
    draw.ellipse(
        [cx - hole_r, head_cy - hole_r, cx + hole_r, head_cy + hole_r],
        fill=bg_color,
    )


def _star_points(cx, cy, outer_r, inner_r, n=5, rotation=-90):
    """產生 n 角星形的頂點座標（用於繪製獎章中心的星星）"""
    points = []
    angle = math.radians(rotation)
    step = math.pi / n
    for i in range(n * 2):
        radius = outer_r if i % 2 == 0 else inner_r
        a = angle + i * step
        points.append((cx + radius * math.cos(a), cy + radius * math.sin(a)))
    return points


def _draw_medal_icon(draw, cx, cy, r, color, width, bg_color):
    """簡易獎章：圓形勳章（中心鏤空星形） + 兩條緞帶"""
    medal_cy = cy - r * 0.15
    medal_r = r * 0.5

    # 緞帶尾端固定在圓形邊緣（角度 250° / 290°），往下延伸，避免與圓形重疊出怪異形狀
    for angle_deg, tip_dx in ((250, -0.32), (290, 0.32)):
        a = math.radians(angle_deg)
        anchor_outer = (cx + medal_r * 1.05 * math.cos(a), medal_cy + medal_r * 1.05 * math.sin(a))
        anchor_inner = (cx + medal_r * 0.55 * math.cos(a), medal_cy + medal_r * 0.55 * math.sin(a))
        tip = (cx + r * tip_dx, cy + r * 0.85)
        draw.polygon([anchor_outer, anchor_inner, tip], fill=color)

    # 勳章圓形實心，蓋住緞帶與圓形交接處
    draw.ellipse(
        [cx - medal_r, medal_cy - medal_r, cx + medal_r, medal_cy + medal_r],
        fill=color,
    )

    # 中心鏤空一個星形，露出背景色，呈現勳章紋路
    star = _star_points(cx, medal_cy, medal_r * 0.6, medal_r * 0.26)
    draw.polygon(star, fill=bg_color)


def _draw_video_icon(draw, cx, cy, r, color, width):
    """簡易播放鍵：圓形外框 + 三角形播放符號"""
    draw.ellipse([cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7], outline=color, width=width)
    tri_r = r * 0.38
    draw.polygon(
        [
            (cx - tri_r * 0.6, cy - tri_r),
            (cx - tri_r * 0.6, cy + tri_r),
            (cx + tri_r * 1.1, cy),
        ],
        fill=color,
    )


def _draw_question_icon(draw, cx, cy, r, color, width, font_path_size):
    """簡易問號圖示：圓形外框 + 置中問號文字"""
    draw.ellipse([cx - r * 0.7, cy - r * 0.7, cx + r * 0.7, cy + r * 0.7], outline=color, width=width)
    font = _load_font(font_path_size)
    bbox = draw.textbbox((0, 0), "?", font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - w / 2 - bbox[0], cy - h / 2 - bbox[1]), "?", font=font, fill=color)


def _draw_person_icon(draw, cx, cy, r, color, width):
    """簡易人形圖示：頭（圓形） + 身體（扇形肩膀）"""
    head_r = r * 0.32
    head_cy = cy - r * 0.35
    draw.ellipse(
        [cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
        fill=color,
    )
    body_w = r * 1.1
    body_h = r * 0.85
    draw.pieslice(
        [cx - body_w / 2, cy - body_h * 0.1, cx + body_w / 2, cy + body_h * 1.5],
        180, 360,
        fill=color,
    )


ICON_DRAWERS = {
    "bike": _draw_bike_icon,
    "map": _draw_map_icon,
    "medal": _draw_medal_icon,
    "video": _draw_video_icon,
    "person": _draw_person_icon,
}


def generate_image():
    image = Image.new("RGB", (MENU_WIDTH, MENU_HEIGHT), "#FFFFFF")
    draw = ImageDraw.Draw(image)

    font_label = _load_font(95)
    icon_radius = min(COL_WIDTH, ROW_HEIGHT) * 0.22
    icon_line_width = max(int(icon_radius * 0.12), 8)

    for index, (label, icon_key, _message_text) in enumerate(MENU_ITEMS):
        row = index // 3
        col = index % 3
        x0 = col * COL_WIDTH
        y0 = row * ROW_HEIGHT
        x1 = x0 + COL_WIDTH
        y1 = y0 + ROW_HEIGHT
        cx = x0 + COL_WIDTH / 2
        icon_cy = y0 + ROW_HEIGHT * 0.4

        draw.rectangle([x0, y0, x1, y1], fill=COLORS[index], outline="#FFFFFF", width=8)

        if icon_key == "question":
            _draw_question_icon(draw, cx, icon_cy, icon_radius, ICON_TEXT_COLOR, icon_line_width, int(icon_radius * 1.3))
        elif icon_key == "medal":
            _draw_medal_icon(draw, cx, icon_cy, icon_radius, ICON_TEXT_COLOR, icon_line_width, COLORS[index])
        elif icon_key == "map":
            _draw_map_icon(draw, cx, icon_cy, icon_radius, ICON_TEXT_COLOR, icon_line_width, COLORS[index])
        else:
            ICON_DRAWERS[icon_key](draw, cx, icon_cy, icon_radius, ICON_TEXT_COLOR, icon_line_width)

        label_bbox = draw.textbbox((0, 0), label, font=font_label)
        label_w = label_bbox[2] - label_bbox[0]
        label_h = label_bbox[3] - label_bbox[1]
        label_y = y0 + ROW_HEIGHT * 0.72
        draw.text(
            (cx - label_w / 2 - label_bbox[0], label_y - label_h / 2 - label_bbox[1]),
            label,
            font=font_label,
            fill=ICON_TEXT_COLOR,
        )

    os.makedirs(os.path.dirname(IMAGE_PATH), exist_ok=True)
    image.save(IMAGE_PATH, "PNG")
    return IMAGE_PATH


def build_rich_menu_areas():
    areas = []
    for index, (label, _icon, message_text) in enumerate(MENU_ITEMS):
        row = index // 3
        col = index % 3
        areas.append(
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=col * COL_WIDTH,
                    y=row * ROW_HEIGHT,
                    width=COL_WIDTH,
                    height=ROW_HEIGHT,
                ),
                action=MessageAction(label=label, text=message_text),
            )
        )
    return areas


def main():
    image_path = generate_image()
    print(f"已產生 Rich Menu 圖片：{image_path}")

    rich_menu = RichMenuRequest(
        size=RichMenuSize(width=MENU_WIDTH, height=MENU_HEIGHT),
        selected=True,
        name="Weekend GO Main Menu",
        chat_bar_text="開啟選單",
        areas=build_rich_menu_areas(),
    )

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api_blob = MessagingApiBlob(api_client)

        response = line_bot_api.create_rich_menu(rich_menu_request=rich_menu)
        rich_menu_id = response.rich_menu_id
        print(f"已建立 Rich Menu，ID：{rich_menu_id}")

        with open(image_path, "rb") as f:
            line_bot_api_blob.set_rich_menu_image(rich_menu_id, body=f.read())
        print("已上傳 Rich Menu 圖片")

        line_bot_api.set_default_rich_menu(rich_menu_id)
        print("已將此 Rich Menu 設為所有使用者的預設選單 ✅")


if __name__ == "__main__":
    main()
