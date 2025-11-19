from flask import Flask, request, jsonify, render_template
import requests
import os
import time

app = Flask(__name__)

# --- تنظیمات تلگرام (خوانده شده از متغیرهای محیطی Render) ---
# توجه: os.environ.get باید نام متغیر را بخواند، نه مقدار آن را!
# مطمئن شوید که Keyها در Render دقیقا همین نام‌ها هستند.
TELEGRAM_BOT_TOKEN = os.environ.get("8230812940:AAElZIKFmg2ej0hB4Lbzg_AFJegMoYQq0CA") 
TELEGRAM_CHAT_ID = os.environ.get("-1003469151523")
# ---------------------------------------------


# --- ۱. تابع ارسال نوتیفیکیشن تلگرام ---
def send_telegram_notification(full_name, mobile, referrer_code):
    """ ارسال نوتیفیکیشن به گروه یا کانال تلگرام آزمایشگاه """
    
    # 1. ساخت متن پیام به صورت Markdown
    message_text = (
        f"🚨 *ارجاع بیمار جدید* 🚨\n"
        f"--------------------------\n"
        f"👤 *نام بیمار:* {full_name}\n"
        f"📞 *شماره تماس:* {mobile}\n"
        f"🏥 *ارجاع دهنده:* {referrer_code}\n"
        f"⏱ *زمان ثبت:* {time.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    # 2. تعریف URL API تلگرام
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # 3. تعریف متغیر payload
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message_text,
        'parse_mode': 'Markdown' 
    }
    
    # 4. ارسال درخواست و مدیریت خطا
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status() # در صورت خطاهای HTTP (مثل 400)، استثنا ایجاد می‌کند
        print(f"Telegram Notification Sent Successfully.")
        return True
    except requests.exceptions.RequestException as e:
        # اگر ارتباط با تلگرام یا پاسخ تلگرام خطا داد، False برمی‌گرداند
        print(f"Error sending Telegram notification: {e}")
        return False


# --- ۲. مسیردهی برای نمایش فرم (Frontend) ---
@app.route('/')
def index():
    """ نمایش صفحه اصلی index.html """
    return render_template('index.html')


# --- ۳. مسیردهی برای پردازش ارجاع (Backend API) ---
@app.route('/api/referral', methods=['POST'])
def handle_referral():
    """ دریافت داده‌های ارسالی از فرم و انجام عملیات """
    try:
        data = request.json
        full_name = data.get('fullName', 'ناشناس') # مقدار پیش‌فرض در صورت نبود داده
        mobile = data.get('mobile', 'ناشناس')
        referrer_code = data.get('referrerCode', 'ناشناس')

        if not all([full_name, mobile, referrer_code]):
            return jsonify({"success": False, "message": "اطلاعات ناقص است."}), 400

        # --- فراخوانی تابع ارسال نوتیفیکیشن ---
        notification_successful = send_telegram_notification(full_name, mobile, referrer_code)

        if notification_successful:
            return jsonify({"success": True, "message": "✅ ارجاع با موفقیت ثبت و نوتیفیکیشن ارسال شد!"}), 200
        else:
            # اگر نوتیفیکیشن موفق نبود (مثلا توکن اشتباه بود)، خطا برمی‌گرداند
            return jsonify({"success": False, "message": "❌ ثبت انجام شد، اما نوتیفیکیشن ارسال نشد. (خطای API تلگرام)"}), 500
            
    except Exception as e:
        # مدیریت خطاهای پیش بینی نشده (مثلا مشکل در دریافت JSON)
        print(f"FATAL SERVER ERROR: {e}")
        return jsonify({"success": False, "message": "❌ خطای داخلی سرور. (تلاش مجدد لازم است)"}), 500


if __name__ == '__main__':
    # این فقط برای تست محلی است
    app.run(debug=True, host='0.0.0.0', port=5000)