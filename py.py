from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DISCORD_TOKEN = "توكن البوت الخاص بك"
HEADERS = {"Authorization": f"Bot {DISCORD_TOKEN}", "Content-Type": "application/json"}

@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = request.json
    user_id = data.get("user_id")
    update_data = {}

    if data.get("username"):
        update_data["username"] = data["username"]
    if data.get("avatar"):
        update_data["avatar"] = data["avatar"]
    if data.get("banner"):
        update_data["banner"] = data["banner"]

    if not update_data:
        return jsonify({"error": "لا يوجد بيانات للتحديث"}), 400

    url = f"https://discord.com/api/v10/users/@me"
    response = requests.patch(url, json=update_data, headers=HEADERS)

    if response.status_code == 200:
        return jsonify({"message": "تم تحديث الحساب بنجاح"})
    else:
        return jsonify({"error": "فشل في التحديث", "details": response.json()}), response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
