from flask import Flask, request, jsonify
import requests
import json
import time # برای درج زمان ثبت

app = Flask(__name__)

# --- تنظیمات تلگرام (برای ارسال نوتیفیکیشن) ---
TELEGRAM_BOT_TOKEN = "8230812940:AAElZIKFmg2ej0hB4Lbzg_AFJegMoYQq0CA" 
TELEGRAM_CHAT_ID = "-1003469151523" 
# ---------------------------------------------
# ---------------------------------------------

def send_telegram_notification(full_name, mobile, referrer_code):
    """ ارسال نوتیفیکیشن به گروه یا کانال تلگرام آزمایشگاه """
    
    # ساخت متن پیام به صورت Markdown
    message_text = (
        f"🚨 *ارجاع بیمار جدید* 🚨\n"
        f"--------------------------\n"
        f"👤 *نام بیمار:* {full_name}\n"
        f"📞 *شماره تماس:* {mobile}\n"
        f"🏥 *ارجاع دهنده:* {referrer_code}\n"
        f"⏱ *زمان ثبت:* {time.strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message_text,
        'parse_mode': 'Markdown' 
    }
    
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status() # در صورت عدم موفقیت، خطا ایجاد می‌کند
        print(f"Telegram Notification Sent: {response.json()}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending Telegram notification: {e}")
        return False

@app.route('/api/referral', methods=['POST'])
def handle_referral():
    """ دریافت داده‌های ارسالی از فرم و انجام عملیات """
    try:
        data = request.json
        full_name = data.get('fullName')
        mobile = data.get('mobile')
        referrer_code = data.get('referrerCode')

        if not all([full_name, mobile, referrer_code]):
            return jsonify({"success": False, "message": "اطلاعات ناقص است."}), 400

        # --- ۱. ذخیره سازی در دیتابیس (اختیاری، اما توصیه می‌شود) ---
        # در اینجا می‌توانید کد ذخیره سازی در SQLite یا PostgreSQL را اضافه کنید.
        # db.session.add(NewReferral(name=full_name, mobile=mobile, ...))
        # db.session.commit()
        print(f"Data Received: {full_name}, {mobile}, {referrer_code}")
        # --------------------------------------------------------

        # --- ۲. ارسال نوتیفیکیشن به آزمایشگاه ---
        notification_successful = send_telegram_notification(full_name, mobile, referrer_code)

        if notification_successful:
            return jsonify({"success": True, "message": "ارجاع با موفقیت ثبت شد."}), 200
        else:
            # حتی اگر نوتیفیکیشن با خطا مواجه شود، ممکن است بخواهید 200 برگردانید 
            # (چون داده ذخیره شده)، یا 500 اگر ارسال نوتیفیکیشن حیاتی است.
            return jsonify({"success": False, "message": "ثبت انجام شد اما نوتیفیکیشن ارسال نشد."}), 500
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"success": False, "message": f"خطای سرور: {str(e)}"}), 500

if __name__ == '__main__':
    # این فقط برای تست محلی است. برای محیط عملیاتی از Gunicorn یا مشابه استفاده کنید.
    app.run(debug=True, host='0.0.0.0', port=5000)