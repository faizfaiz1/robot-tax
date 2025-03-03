from flask import Flask, request, redirect, jsonify
import requests

app = Flask(__name__)

# بيانات تطبيقك في ديسكورد
CLIENT_ID = "1344091056601301063"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "https://faizfaiz1.github.io/robot-tax/callback"

# رابط طلب التوكن
TOKEN_URL = "https://discord.com/api/oauth2/token"
# رابط تعديل البروفايل
USER_URL = "https://discord.com/api/v10/users/@me"

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "لم يتم استقبال الكود", 400

    # طلب الحصول على التوكن
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    token_info = response.json()

    if "access_token" not in token_info:
        return f"فشل في المصادقة: {token_info}", 400

    access_token = token_info["access_token"]

    # استدعاء صفحة التحكم في الحساب مع التوكن
    return redirect(f"/profile?token={access_token}")

@app.route('/update-profile', methods=['POST'])
def update_profile():
    data = request.json
    token = data.get("token")
    username = data.get("username")
    avatar_url = data.get("avatar_url")
    banner_url = data.get("banner_url")

    if not token:
        return jsonify({"error": "Token مفقود"}), 400

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {}

    if username:
        payload["username"] = username
    if avatar_url:
        payload["avatar"] = avatar_url  # هنا تحتاج رفع الصورة إلى Base64
    if banner_url:
        payload["banner"] = banner_url  # نفس الأمر للبنر

    response = requests.patch(USER_URL, json=payload, headers=headers)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True, port=5000)
