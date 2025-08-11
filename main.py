from telethon import TelegramClient, events
import re

# تنظیمات مستقیم (برای تست)
api_id = 49360
api_hash = 'bffa5a33120b8473975d3deaee27cf97'
bot_token = '8205194062:AAFJC24U0Dy7x7MiEk1f9EON26UN48EC49k'
source_channels = ['@nim_beyt', '@tk_khati', '@biotextve', '@janierami']  # کانال‌های منبع
destination_channel = '@sher_khoub'  # کانال مقصد
channel_signature = 'منبع: @sher_khoub (شعر خوب نوش جان کن)'  # امضای زیر هر پست
allowed_user = 'janierami'  # نام کاربری مجاز برای ارسال پیام به ربات (بدون @)

# کلمات کلیدی تبلیغاتی برای فیلتر
ad_keywords = [
    'تبلیغ', 'خرید', 'فروش', 'لینک', 'پروموشن', 'تخفیف', 'اشتراک',
    'شرگ', 'شرطبندی', 'بت', 'بونوس', 'پیش بینی', 'کازینو', 'شرطبندی',
    'شرط', 'پیشبینی', 'کازینوی', 'بونس', 'بتینگ', 'گیمبلینگ',
    'دعانویسی', 'جادو', 'رمل', 'فال', 'اینجا کلیک کن', 'کلیک', 'ثبت نام',
    'فالگیری', 'طلسم', 'دعا', 'سحر', 'جن', 'پیشگویی', 'قرعه کشی', 'جایزه'
]
ad_pattern = re.compile(r'http[s]?://|t\.me/.*\?start|\.ir|\.com|\.org|\.net')  # الگو برای لینک‌ها

# ایجاد کلاینت ربات
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# هندلر برای پست‌های کانال‌های منبع (کپی با فیلتر و امضا)
@client.on(events.NewMessage(chats=source_channels))
async def handler(event):
    message = event.message
    text = message.text if message.text else ''

    # چک کردن اینکه پیام تبلیغاتی هست یا نه
    is_ad = False
    if text:
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in ad_keywords):
            is_ad = True
        if ad_pattern.search(text):
            is_ad = True

    # اگه تبلیغ نبود، محتوا رو کپی کن و با امضای کانال پست کن
    if not is_ad:
        new_text = f"{text}\n\n{channel_signature}" if text else channel_signature
        await client.send_message(
            destination_channel,
            message=new_text,
            file=message.media,
            parse_mode='html'
        )

# هندلر برای پیام‌های خصوصی به ربات (فقط از کاربر مجاز)
@client.on(events.NewMessage(incoming=True))
async def user_message_handler(event):
    if not event.is_private:
        return  # فقط پیام‌های خصوصی را پردازش کن

    sender = await event.get_sender()
    if sender.username != allowed_user:
        return  # اگر کاربر مجاز نبود، نادیده بگیر

    message = event.message
    text = message.text if message.text else ''
    new_text = f"{text}\n\n{channel_signature}" if text else channel_signature
    await client.send_message(
        destination_channel,
        message=new_text,
        file=message.media,
        parse_mode='html'
    )

# شروع ربات
print("ربات شروع شد...")
client.run_until_disconnected()
