from telethon import TelegramClient, events
import re
import os

# تنظیمات ربات
api_id = int(os.environ.get("API_ID", 49360))
api_hash = os.environ.get("API_HASH", 'bffa5a33120b8473975d3deaee27cf97')
bot_token = os.environ.get("BOT_TOKEN", '8205194062:AAFJC24U0Dy7x7MiEk1f9EON26UN48EC49k')

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
async def handle_channel_post(event):
    message = event.message
    text = message.text or ''

    # بررسی تبلیغاتی بودن
    text_lower = text.lower()
    is_ad = any(keyword in text_lower for keyword in ad_keywords) or ad_pattern.search(text)

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
async def handle_private_message(event):
    if not event.is_private:
        return

    sender = await event.get_sender()
    if sender.username != allowed_user:
        return

    message = event.message
    text = message.text or ''
    new_text = f"{text}\n\n{channel_signature}" if text else channel_signature
    await client.send_message(
        destination_channel,
        message=new_text,
        file=message.media,
        parse_mode='html'
    )

# اجرای ربات
print("✅ ربات فعال شد و منتظر پیام‌هاست...")
client.run_until_disconnected()
