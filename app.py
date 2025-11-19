


    
from flask import Flask, request, jsonify, render_template # render_template را اضافه کنید
import requests
import os
import time

app = Flask(__name__)

# --- تنظیمات تلگرام (خوانده شده از متغیرهای محیطی Render) ---
TELEGRAM_BOT_TOKEN = os.environ.get("8230812940:AAElZIKFmg2ej0hB4Lbzg_AFJegMoYQq0CA") 
TELEGRAM_CHAT_ID = os.environ.get("-1003469151523")
# ---------------------------------------------

# *** افزودن مسیردهی برای نمایش فرم index.html ***
@app.route('/')
def index():
    # فرض بر این است که index.html در پوشه 'templates' قرار دارد
    return render_template('index.html')
# **********************************************


def send_telegram_notification(full_name, mobile, referrer_code):
    # ... (بقیه تابع ارسال نوتیفیکیشن بدون تغییر) ...
    # ... (کد API تلگرام) ...
    pass # جایگزین کد واقعی تلگرام

@app.route('/api/referral', methods=['POST'])
def handle_referral():
    # ... (بقیه تابع handle_referral بدون تغییر) ...
    pass # جایگزین کد واقعی Flask

if __name__ == '__main__':
    app.run(debug=True)