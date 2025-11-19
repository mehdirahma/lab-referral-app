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
# app.py - نمونه اصلاح شده برای مدیریت خطا

# ... (بقیه کد، شامل وارد کردن کتابخانه ها و تنظیم متغیرها)

def send_telegram_notification(full_name, mobile, referrer_code):
    """ ارسال نوتیفیکیشن به گروه یا کانال تلگرام آزمایشگاه """
    # توکن و آیدی از متغیرهای محیطی خوانده شده‌اند
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # ... (ساخت message_text) ...
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status() # **اگر خطا (مثل 400 یا 500) رخ دهد، یک استثنا ایجاد می‌کند**
        return True
    except requests.exceptions.RequestException as e:
        # اگر ارتباط با تلگرام یا پاسخ تلگرام (400 Bad Request) خطا داد، اینجا آن را می‌گیریم
        print(f"Error sending Telegram notification: {e}")
        return False # تابع با موفقیت به پایان می رسد و False برمی گرداند

# ... (بقیه کد) ...

# --------------------
# مطمئن شوید که این تابع نیز یک return در انتهای بخش except خود دارد:
# @app.route('/api/referral', methods=['POST'])
# def handle_referral():
    # ...
    # except Exception as e:
    #     print(f"An error occurred during referral handling: {e}")
    #     return jsonify({"success": False, "message": f"خطای داخلی سرور: {str(e)}"}), 500