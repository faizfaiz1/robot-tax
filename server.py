from flask import Flask, request, redirect, jsonify
import requests
import os

app = Flask(__name__)

CLIENT_ID = "1344091056601301063"
CLIENT_SECRET = "wy2bDpKOCm-Vx2N2YXL-XmTEULplsJ2W"
REDIRECT_URI = "https://robot-taxa.vercel.app/callback"
DISCORD_API_URL = "https://discord.com/api"

@app.route("/")
def home():
    return "Discord API Server is Running!"

@app.route("/login")
def login():
    return redirect(f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=identify guilds.members.read")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "Authorization failed!", 400

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_response = requests.post(f"{DISCORD_API_URL}/oauth2/token", data=data, headers=headers).json()

    if "access_token" not in token_response:
        return "Failed to obtain access token", 400

    access_token = token_response["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    user_data = requests.get(f"{DISCORD_API_URL}/users/@me", headers=headers).json()

    return jsonify(user_data)

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    access_token = data.get("access_token")
    if not access_token:
        return jsonify({"error": "Unauthorized"}), 403

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    payload = {}
    if "username" in data:
        payload["username"] = data["username"]
    if "avatar" in data:
        payload["avatar"] = data["avatar"]
    if "banner" in data:
        payload["banner"] = data["banner"]

    response = requests.patch(f"{DISCORD_API_URL}/users/@me", json=payload, headers=headers)

    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
