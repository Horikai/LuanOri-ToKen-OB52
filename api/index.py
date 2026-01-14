# api/index.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

ORIGINAL_API = "https://arafatjwtapiv1.vercel.app/api/token"
CUSTOM_CREDIT = "Developed by t.me/ShiinaTenju & @LuanOri04"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Accept": "application/json",
}

@app.route("/get_token", methods=["GET"])
def get_token():
    uid = request.args.get("uid")
    password = request.args.get("password")

    if not uid or not password:
        return jsonify({
            "success": False,
            "error": "Thiếu uid hoặc password",
            "credit": CUSTOM_CREDIT
        }), 400

    try:
        # Gọi API gốc
        params = {"uid": uid, "password": password}
        r = requests.get(ORIGINAL_API, params=params, headers=HEADERS, timeout=15)

        try:
            data = r.json()  # Thử parse JSON
        except ValueError:
            data = {"raw_response": r.text.strip()}

        # Chuẩn hóa response
        response_data = {
            "success": r.status_code == 200 and data.get("success", False) or "token" in data or "access_token" in data,
            "status_code": r.status_code,
            "original_data": data,
            "credit": CUSTOM_CREDIT,
            "note": "Token Free Fire OB52"
        }

        # Nếu có token rõ ràng, đưa lên top level cho tiện dùng
        if "token" in data:
            response_data["token"] = data["token"]
        if "access_token" in data:
            response_data["access_token"] = data["access_token"]
        if "jwt" in data:
            response_data["jwt"] = data["jwt"]

        return jsonify(response_data), r.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": f"Lỗi kết nối API gốc: {str(e)}",
            "credit": CUSTOM_CREDIT
        }), 500


@app.route("/")
def home():
    return jsonify({
        "message": "API Get Token OB52",
        "usage": "/get_token?uid=YOUR_UID&password=YOUR_PASSWORD",
        "credit": CUSTOM_CREDIT,
        "Tele": "https://t.me/ShiinaTenju & @LuanOri04"
    })


if __name__ == "__main__":
    app.run()