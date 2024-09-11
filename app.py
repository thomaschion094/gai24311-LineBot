import json
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
app = Flask(__name__)

# 讀取 config.json，取得 secret 和 token
CONFIG = json.load(open("/home/24311/config.json", "r"))
LINE_SECRET = CONFIG["line"]["line_secret"]
LINE_TOKEN = CONFIG["line"]["line_token"]
LINE_BOT = LineBotApi(LINE_TOKEN)
HANDLER = WebhookHandler(LINE_SECRET)


@app.route("/callback", methods=["POST"])
def callback():
    # X-Line-Signature: 數位簽章
    signature = request.headers["X-Line-Signature"]
    print(signature)
    body = request.get_data(as_text=True)
    print(body)
    try:
        HANDLER.handle(body, signature)
    except InvalidSignatureError:
        print("Check the channel secret/access token.")
        abort(400)
    return "OK"