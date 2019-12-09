import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message


load_dotenv()


machine = TocMachine(
    states=["user", "start", "default_search_keyword", "do_default_search", "custom_search_keyword", "custom_search_nPush", "custom_search_count", "do_custom_search", "done"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "start",
            "conditions": "is_going_to_start",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "default_search_keyword",
            "conditions": "is_going_to_default_search",
        },
        {
            "trigger": "advance",
            "source": "default_search_keyword",
            "dest": "do_default_search",
            "conditions": "get_keyword",
        },
        {
            "trigger": "go_back",
            "source": "done",
            "dest": "start",
        },
        {
            "trigger": "advance",
            "source": ["default_search_keyword", "custom_search_keyword", "custom_search_nPush", "custom_search_count"],
            "dest": "start",
            "conditions": "is_goingback"
        },
        {
            "trigger": "advance",
            "source": ["user", "start", "default_search_keyword", "custom_search_keyword", "custom_search_nPush", "custom_search_count"],
            "dest": "user",
            "conditions": "reset"
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "custom_search_keyword",
            "conditions": "is_going_to_custom_search",
        },
        {
            "trigger": "advance",
            "source": "custom_search_keyword", 
            "dest": "custom_search_nPush",
            "conditions": "get_keyword"
        },
        {
            "trigger": "advance",
            "source": "custom_search_nPush", 
            "dest": "custom_search_count",
            "conditions": "isValidnPush"
        },
        {
            "trigger": "advance",
            "source": "custom_search_count",
            "dest": "do_custom_search",
            "conditions": "isValidCount"
        },
        {
            "trigger": "advance",
            "source": ["do_default_search" ,"do_custom_search"],
            "dest": "done",
            "conditions": "anykey"
        }
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)
'''
print("start drawing")
machine.get_graph().draw("fsm.png", prog="dot", format="png")
print("drawing done")
'''
app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", "d8557c823e748cd1f9c3a73890c06f2e")
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "RGnfDCRGLy9hqZxWvMQ34bGdSSFVw1tM74Dto4Bmko0Gu8vIZAcChpVtprCgH2nOSwBblABZn/q1LkfJ5xw7EMyybQ8l7ndtWOqJvej/Bda2erNu/8wAM5uy5++pevybOeEUDaius0pAfheWkJFTCQdB04t89/1O/w1cDnyilFU=")
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")

        response = machine.advance(event)
        
        if response == False:
            send_text_message(event.reply_token, "不合法輸入 請輸入正確內容")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
