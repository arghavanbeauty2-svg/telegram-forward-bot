from telethon import TelegramClient, events
import re

# تنظیمات
api_id = 49360
api_hash = 'bffa5a33120b8473975d3deaee27cf97'
bot_token = '8205194062:AAFJC24U0Dy7x7MiEk1f9EON26UN48EC49k'

source_channels = ['@nim_beyt', '@tk_khati', '@biotextve', '@janierami']
destination_channel = '@sher_khoub'
channel_signature = 'منبع: @sher_khoub (شعر خوب نوش جان کن)'
allowed_user = 'janierami'

ad_keywords = [
    'تبلیغ', 'خرید', 'فروش', 'لینک', 'پروموشن', 'تخفیف', 'اشتراک',
    'شرگ', 'شرطبندی', 'بت', 'بونوس', 'پیش بینی', 'کازینو',
    'شرط', 'پیشبینی', 'کازینوی', 'بونس', 'بتینگ', 'گیمبلینگ',
    'دعانویسی', 'جادو', 'رمل', 'فال', 'اینجا کلیک کن', 'کلیک', 'ثبت نام',
    'فالگیری', 'طلسم', 'دعا', 'سحر', 'جن', 'پیشگویی', 'قرعه کشی', 'جایزه'
]
ad_pattern = re.compile(r'http[s]?://|t\.me/.*\?start|\.ir|\.com|\.org|\.net')

# ایجاد کلاینت
client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# هندلر برای پست‌های کانال‌های منبع
@client.on(events.NewMessage(chats=source_channels))
async def forward_filtered_message(event):
    msg = event.message
    text = msg.message or ''
    is_ad = False

    if text:
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in ad_keywords) or ad_pattern.search(text):
            is_ad = True

    if not is_ad:
        new_text = f"{text}\n\n{channel_signature}" if text else channel_signature
        try:
            await client.send_message(
                destination_channel,
                message=new_text,
                file=msg.media if msg.media else None,
                parse_mode='html'
            )
        except Exception as e:
            print(f"خطا در ارسال پیام: {e}")

# هندلر برای پیام‌های خصوصی از کاربر مجاز
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def private_message_handler(event):
    sender = await event.get_sender()
    username = getattr(sender, "username", None)

    if username != allowed_user:
        return

    msg = event.message
    text = msg.message or ''
    new_text = f"{text}\n\n{channel_signature}" if text else channel_signature

    try:
        await client.send_message(
            destination_channel,
            message=new_text,
            file=msg.media if msg.media else None,
            parse_mode='html'
        )
    except Exception as e:
        print(f"خطا در ارسال پیام خصوصی: {e}")

# اجرای ربات
print("ربات شروع شد...")
client.run_until_disconnected()
