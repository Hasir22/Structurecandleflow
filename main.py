from flask import Flask, request
import telegram
import os
import pandas as pd
from datetime import datetime
from io import BytesIO
from ai_analysis import analyze_data

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = None
bot = telegram.Bot(token=TOKEN)

def format_to_aurora_table(data):
    table = {
        "Symbol": [data.get("pair", "")],
        "TF": [data.get("timeframe", "")],
        "Internal": [data.get("internal", "")],
        "External": [data.get("external", "")],
        "INDEX%": [data.get("index", 0)],
        "RANGE%": [data.get("range", 0)],
        "Type": [data.get("candle_type", "")]
    }
    df = pd.DataFrame(table)
    return df

@app.route('/', methods=['GET'])
def home():
    return 'Aurora Bot is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    global CHAT_ID
    data = request.json

    if not data:
        return "No data received", 400

    df = format_to_aurora_table(data)
    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    analysis = analyze_data(df)

    message = f"**Structure Update**\\nPair: {data.get('pair')}\\nTF: {data.get('timeframe')}\\nInternal: {data.get('internal')}\\nExternal: {data.get('external')}\\nINDEX%: {data.get('index')}\\nRANGE%: {data.get('range')}\\nType: {data.get('candle_type')}\\n\\nAI Insight: {analysis}"
    try:
        bot.send_message(chat_id=CHAT_ID or data.get("chat_id"), text=message, parse_mode=telegram.ParseMode.MARKDOWN)
        bot.send_document(chat_id=CHAT_ID or data.get("chat_id"), document=output, filename="aurora_structure.xlsx")
    except Exception as e:
        print("Telegram send error:", e)

    return "Alert processed", 200

@app.route('/setchat', methods=['POST'])
def set_chat():
    global CHAT_ID
