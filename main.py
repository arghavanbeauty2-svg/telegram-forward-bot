from telethon import TelegramClient, events
from flask import Flask
import threading
import re
import os

# تنظیمات ربات
api_id = 49360
api_hash = 'bffa5a33120b8473975d3deaee27cf97'
bot_token = '8205194062:AAFJC24U0Dy7x7MiEk1f9EON26UN48EC49k'
source_channels = ['@nim_beyt', '@tk_khati', '@biotextve', '@janierami']
destination_channel = '@sher_khoub'
channel_signature = 'منبع: @sher_khoub (شعر خوب نوش جان کن)'
allowed_user = 'janierami'  # بدون @

# کلمات کلیدی تبلیغاتی
ad_keywords = [
    'تبلیغ', 'خرید', 'فروش', 'لینک', 'پروموشن', 'تخفیف', 'اشتراک',
    'شرگ', 'شرطبندی', 'بت', 'بونوس', 'پیش بینی', 'کازینو', 'شرطبندی',
    'شرط', 'پیشبینی', 'کازینوی', 'بونس', 'بتینگ', 'گیمبلینگ',
    'دعانویسی', 'جادو', 'رمل', 'فال', 'اینجا کلیک کن', 'کلیک', 'ثبت نام',
    'فالگیری', 'طلسم', 'دعا', 'سحر', 'جن', 'پیشگویی', 'قرعه کشی', 'جایزه'
]
ad_pattern = re.compile(r'http[s]?://|t\.me/.*\?start|\.ir|\.com|\.org|\.net')

# ایجاد کلاینت تلگرام
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# هندلر برای کانال‌های منبع
@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    message = event.message
    text = message.text if message.text else ''

    is_ad = False
    if text:
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in ad_keywords):
            is_ad = True
        if ad_pattern.search(text):
            is_ad = True

    if not is_ad:
        new_text = f"{text}\n\n{channel_signature}" if text else channel_signature
        await client.send_message(
            destination_channel,
            message=new_text,
            file=message.media,
            parse_mode='html'
        )

# هندلر برای پیام‌های خصوصی از کاربر مجاز
@client.on(events.NewMessage(incoming=True))
async def user_message_handler(event):
    if not event.is_private:
        return

    sender = await event.get_sender()
    if sender.username != allowed_user:
        return

    message = event.message
    text = message.text if message.text else ''
    new_text = f"{text}\n\n{channel_signature}" if text else channel_signature
    await client.send_message(
        destination_channel,
        message=new_text,
        file=message.media,
        parse_mode='html'
    )

# اجرای ربات در یک Thread جداگانه
def run_bot():
    print("ربات شروع شد...")
    client.run_until_disconnected()

bot_thread = threading.Thread(target=run_bot)
bot_thread.start()

# راه‌اندازی وب‌سرور ساده با Flask برای Render
app = Flask(__name__)

@app.route('/')
def home():
    return "ربات تلگرام فعال است ✅"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
