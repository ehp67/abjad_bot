import telebot

API_KEY = "7628143947:AAHswbUKYmz49eV_MfuyJC_q4PqhYhX1Tv4"

bot = telebot.TeleBot(API_KEY)

abjad_values = {
    "ا": 1, "آ": 1, "ئ": 10,
    "ب": 2, "پ": 2, "ج": 3, "چ": 3, "د": 4,
    "ه": 5, "و": 6, "ز": 7, "ژ": 7, "ح": 8,
    "ط": 9, "ی": 10, "ک": 20, "گ": 20, "ل": 30,
    "م": 40, "ن": 50, "س": 60, "ع": 70,
    "ف": 80, "ص": 90, "ق": 100, "ر": 200,
    "ش": 300, "ت": 400, "ث": 500, "خ": 600,
    "ذ": 700, "ض": 800, "ظ": 900, "غ": 1000
}

def normalize_name(name):
    replacements = {
        "ي": "ی",
        "ك": "ک",
        "ى": "ی",
        "ة": "ه",
        "ﻻ": "لا",
        "آ": "آ",
        "أ": "آ",
        "آ": "آ"
    }
    for old, new in replacements.items():
        name = name.replace(old, new)
    # حذف فاصله و کاراکترهای غیرابجدی
    name = "".join(ch for ch in name if ch in abjad_values or ch in ["آ", "ئ"])
    return name

def calc_abjad(name):
    total = 0
    for ch in name:
        if ch in abjad_values:
            total += abjad_values[ch]
    return total

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message,
        "نام خود را بدون هیچ کاراکتر اضافی وارد کنید\nمثلاً: مریم"
    )

@bot.message_handler(func=lambda m: True)
def handle_name(message):
    user_name = message.text.strip()
    name = normalize_name(user_name)
    filtered_name = "".join([ch for ch in name if ch in abjad_values])
    wealth_code = calc_abjad(filtered_name) + 27735

    bot.reply_to(
        message,
        f"💰 کد ثروت {user_name}: {wealth_code}\n\n"
        "📜 طریقه استفاده: این کد را روی کاغذ از سمت چپ به راست بنویسید و تک تک بخوانید."
    )

try:
    bot.infinity_polling()
except telebot.apihelper.ApiTelegramException as e:
    print("⚠️ خطا:", e)
    print("لطفاً مطمئن شوید که هیچ نسخه دیگری از ربات در حال اجرا نیست.")
