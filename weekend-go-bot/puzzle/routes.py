"""
拼圖集章 Flask Blueprint。
路由：
  GET  /puzzle              拼圖進度頁面（?uid=<LINE user_id>）
  GET  /puzzle/scan         自動掃碼頁面（?uid=<LINE user_id>）
  POST /api/puzzle/checkin  解鎖碎片 API（JSON body）
"""
from flask import Blueprint, jsonify, render_template, request

from puzzle.models import PIECES, add_piece, get_user_pieces

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

    collected = get_user_pieces(user_id)
    return jsonify({
        "ok": True,
        "already_had": already_had,
        "piece_id": piece_id,
        "collected": sorted(collected),
        "count": len(collected),
        "total": len(PIECES),
    })
