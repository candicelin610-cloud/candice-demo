"""
拼圖集章 Flask Blueprint。
路由：
  GET  /puzzle              拼圖進度頁面（?uid=<LINE user_id>）
  GET  /puzzle/scan         自動掃碼頁面（?uid=<LINE user_id>）
  POST /api/puzzle/checkin  解鎖碎片 API（JSON body）
"""
import os

from flask import Blueprint, jsonify, render_template, request

from puzzle.models import PIECES, PIECE_BY_ID, add_piece, get_user_pieces


def _push_unlock_flex(user_id, piece, count, total):
    """解鎖新碎片後推播 Flex Message 到 LINE 聊天室（失敗時靜默記錄）。"""
    try:
        import messages
        from linebot.v3.messaging import ApiClient, Configuration, MessagingApi, PushMessageRequest
        token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
        if not token:
            return
        with ApiClient(Configuration(access_token=token)) as api_client:
            MessagingApi(api_client).push_message(
                PushMessageRequest(to=user_id, messages=[messages.puzzle_unlock_flex(piece, count, total)])
            )
    except Exception as exc:
        print(f"[puzzle] push unlock flex failed: {exc}")

puzzle_bp = Blueprint("puzzle", __name__)


@puzzle_bp.route("/puzzle")
def puzzle_page():
    user_id = request.args.get("uid", "guest")
    collected = get_user_pieces(user_id)
    pieces_with_status = [
        {**p, "collected": p["id"] in collected}
        for p in PIECES
    ]
    return render_template(
        "puzzle.html",
        pieces=pieces_with_status,
        count=len(collected),
        total=len(PIECES),
        user_id=user_id,
    )


@puzzle_bp.route("/puzzle/scan")
def puzzle_scan():
    user_id = request.args.get("uid", "guest")
    return render_template("puzzle_scan.html", user_id=user_id)


@puzzle_bp.route("/api/puzzle/checkin", methods=["POST"])
def puzzle_checkin():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"ok": False, "error": "missing JSON body"}), 400

    user_id = str(data.get("user_id", "")).strip()
    piece_id = str(data.get("piece_id", "")).strip()

    if not user_id or not piece_id:
        return jsonify({"ok": False, "error": "user_id and piece_id are required"}), 400

    success, already_had = add_piece(user_id, piece_id)
    if not success:
        return jsonify({"ok": False, "error": f"invalid piece_id: {piece_id}"}), 400

    piece = PIECE_BY_ID[piece_id]
    collected = get_user_pieces(user_id)
    count = len(collected)
    total = len(PIECES)

    # 首次解鎖才推播（重複掃碼不推）
    if not already_had:
        _push_unlock_flex(user_id, piece, count, total)

    return jsonify({
        "ok": True,
        "already_had": already_had,
        "piece_id": piece_id,
        "piece_name": piece["name"],
        "piece_emoji": piece["emoji"],
        "piece_fun_fact": piece["fun_fact"],
        "collected": sorted(collected),
        "count": count,
        "total": total,
    })
