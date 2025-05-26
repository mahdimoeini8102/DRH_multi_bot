import datetime
import jdatetime
from hijri_converter import convert
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# توکن ربات را جایگزین کنید
TOKEN = "7283056652:AAFCH1vFup361bahbkO-HdxEp8i--2Y2fVU"

# لیست مناسبت‌های شمسی
calendar_events_shamsi = [
    {"date": jdatetime.date(1403, 11, 15), "name": "ولادت ابوالفضل العباس علیه السلام و روز جانباز [4 شعبان]"},
    {"date": jdatetime.date(1403, 11, 16), "name": "ولادت امام زین العابدین علیه السلام [5 شعبان]"},
    {"date": jdatetime.date(1403, 11, 19), "name": "روز نیروی هوایی"},
    {"date": jdatetime.date(1403, 11, 22), "name": "پیروزی انقلاب اسلامی"},
    {"date": jdatetime.date(1403, 11, 22), "name": "ولادت علی اکبر علیه السلام و روز جوان [11 شعبان]"},
    {"date": jdatetime.date(1403, 11, 23), "name": "حمله به سفارت روسیه و قتل گریبایدوف سفیر روسیه تزاری در ایران [11 February]"},
    {"date": jdatetime.date(1403, 11, 26), "name": "ولادت حضرت قائم عجل الله تعالی فرجه و جشن نیمه شعبان [15 شعبان]"},
    {"date": jdatetime.date(1403, 11, 26), "name": "جشن ولنتاین [14 February]"},
    {"date": jdatetime.date(1403, 11, 29), "name": "جشن سپندارمذگان و روز عشق"},
    {"date": jdatetime.date(1403, 11, 29), "name": "فاجعه انفجار قطار نیشابور [1382 خورشیدی]"},
    {"date": jdatetime.date(1403, 12, 5), "name": "روز بزرگداشت زن و زمین"},
    {"date": jdatetime.date(1403, 12, 5), "name": "روز بزرگداشت خواجه نصیر الدین طوسی و روز مهندس"},
    {"date": jdatetime.date(1403, 12, 7), "name": "سالروز استقلال کانون وکلای دادگستری و روز وکیل مدافع"},
    {"date": jdatetime.date(1403, 12, 15), "name": "روز درختکاری"},
    {"date": jdatetime.date(1403, 12, 18), "name": "روز جهانی زنان [8 March]"},
    {"date": jdatetime.date(1403, 12, 24), "name": "روز جهانی عدد پی π [14 March]"},
    {"date": jdatetime.date(1403, 12, 25), "name": "پایان سرایش شاهنامه"},
    {"date": jdatetime.date(1403, 12, 25), "name": "روز بزرگداشت اختر چرخ ادب، پروین اعتصامی"},
    {"date": jdatetime.date(1403, 12, 26), "name": "ولادت امام حسن مجتبی علیه السلام [15 رمضان]"},
    {"date": jdatetime.date(1403, 12, 28), "name": "جشن چهارشنبه سوری"},
    {"date": jdatetime.date(1403, 12, 29), "name": "روز ملی شدن صنعت نفت ایران"},
    {"date": jdatetime.date(1403, 12, 29), "name": "شب قدر [18 رمضان]"},
    {"date": jdatetime.date(1403, 12, 30), "name": "ضربت خوردن حضرت علی علیه السلام [19 رمضان]"},
    {"date": jdatetime.date(1403, 12, 30), "name": "آخرین روز سال"},
    {"date": jdatetime.date(1403, 12, 30), "name": "روز جهانی شادی [20 March]"},
    {"date": jdatetime.date(1404, 1, 1), "name": "جشن نوروز/جشن سال نو"},
    {"date": jdatetime.date(1404, 1, 1), "name": "روز جهانی نوروز [21 March]"},
    {"date": jdatetime.date(1404, 1, 2), "name": "عیدنوروز"},
    {"date": jdatetime.date(1404, 1, 2), "name": "شهادت حضرت علی علیه السلام [٢١ رمضان]"},
    {"date": jdatetime.date(1404, 1, 3), "name": "عیدنوروز"},
    {"date": jdatetime.date(1404, 1, 3), "name": "شب قدر [٢٢ رمضان]"},
    {"date": jdatetime.date(1404, 1, 3), "name": "روز جهانی هواشناسی [23 March]"},
    {"date": jdatetime.date(1404, 1, 4), "name": "عیدنوروز"},
    {"date": jdatetime.date(1404, 1, 6), "name": "روز امید، روز شادباش نویسی"},
    {"date": jdatetime.date(1404, 1, 6), "name": "زادروز اَشو زرتشت، اَبَراِنسان بزرگ تاریخ"},
    {"date": jdatetime.date(1404, 1, 7), "name": "روز جهانی تئاتر [27 March]"},
    {"date": jdatetime.date(1404, 1, 10), "name": "جشن آبانگاه"},
    {"date": jdatetime.date(1404, 1, 11), "name": "عید سعید فطر [١ شوال]"},
    {"date": jdatetime.date(1404, 1, 12), "name": "روز جمهوری اسلامی"},
    {"date": jdatetime.date(1404, 1, 12), "name": "تعطیل به مناسبت عید سعید فطر [٢ شوال]"},
    {"date": jdatetime.date(1404, 1, 13), "name": "جشن سیزده به در"},
    {"date": jdatetime.date(1404, 1, 17), "name": "سروش روز، جشن سروشگان"},
    {"date": jdatetime.date(1404, 1, 18), "name": "روز جهانی بهداشت [7 April]"},
    {"date": jdatetime.date(1404, 1, 19), "name": "فروردین روز، جشن فروردینگان"},
    {"date": jdatetime.date(1404, 1, 23), "name": "روز دندانپزشک"},
    {"date": jdatetime.date(1404, 1, 25), "name": "روز بزرگداشت عطار نیشابوری"},
    {"date": jdatetime.date(1404, 1, 29), "name": "روز ارتش جمهوری اسلامی ایران"},
    {"date": jdatetime.date(1404, 1, 30), "name": "روز علوم آزمایشگاهی، زادروز حکیم سید اسماعیل جرجانی"},
    {"date": jdatetime.date(1404, 2, 1), "name": "روز بزرگداشت سعدی"},
    {"date": jdatetime.date(1404, 2, 2), "name": "جشن گیاه آوری؛ روز زمین [22 April]"},
    {"date": jdatetime.date(1404, 2, 3), "name": "روز بزرگداشت شیخ بهایی؛ روز ملی کارآفرینی؛ روز معماری"},
    {"date": jdatetime.date(1404, 2, 4), "name": "شهادت امام جعفر صادق علیه السلام [٢٥ شوال]"},
    {"date": jdatetime.date(1404, 2, 7), "name": "روز جهانی طراحی و گرافیک [27 April]"},
    {"date": jdatetime.date(1404, 2, 9), "name": "ولادت حضرت معصومه سلام الله علیها و روز دختران [١ ذوالقعده]"},
    {"date": jdatetime.date(1404, 2, 9), "name": "روز ملی روانشناس و مشاور"},
    {"date": jdatetime.date(1404, 2, 10), "name": "جشن چهلم نوروز؛ روز ملی خلیج فارس"},
    {"date": jdatetime.date(1404, 2, 11), "name": "روز جهانی کارگر [1 May]"},
    {"date": jdatetime.date(1404, 2, 12), "name": "روز معلم"},
    {"date": jdatetime.date(1404, 2, 15), "name": "جشن میانه بهار/جشن بهاربد؛ روز شیراز"},
    {"date": jdatetime.date(1404, 2, 15), "name": "روز جهانی ماما [5 May]"},
    {"date": jdatetime.date(1404, 2, 18), "name": "روز جهانی صلیب سرخ و هلال احمر [8 May]"},
    {"date": jdatetime.date(1404, 2, 19), "name": "ولادت امام رضا علیه السلام [١١ ذوالقعده]"},
    {"date": jdatetime.date(1404, 2, 22), "name": "زادروز مریم میرزاخانی ریاضیدان ایرانی، روز جهانی زن در ریاضیات"},
    {"date": jdatetime.date(1404, 2, 22), "name": "روز جهانی پرستار [12 May]"},
    {"date": jdatetime.date(1404, 2, 25), "name": "روز بزرگداشت فردوسی"},
    {"date": jdatetime.date(1404, 2, 27), "name": "روز ارتباطات و روابط عمومی"},
    {"date": jdatetime.date(1404, 2, 28), "name": "روز بزرگداشت حکیم عمر خیام"},
    {"date": jdatetime.date(1404, 2, 28), "name": "روز جهانی موزه و میراث فرهنگی [18 May]"},
    {"date": jdatetime.date(1404, 3, 1), "name": "روز بهره وری و بهینه سازی مصرف"},
    {"date": jdatetime.date(1404, 3, 1), "name": "روز بزرگداشت ملاصدرا"},
    {"date": jdatetime.date(1404, 3, 2), "name": "فروریختن ساختمان متروپل در آبادان"},
    {"date": jdatetime.date(1404, 3, 3), "name": "فتح خرمشهر در عملیات بیت المقدس و روز مقاومت، ایثار و پیروزی"},
    {"date": jdatetime.date(1404, 3, 4), "name": "روز دزفول، روز مقاومت و پایداری"},
    {"date": jdatetime.date(1404, 3, 6), "name": "خرداد روز، جشن خردادگان"},
    {"date": jdatetime.date(1404, 3, 6), "name": "شهادت امام محمد تقی علیه السلام [٢٩ ذوالقعده]"},
    {"date": jdatetime.date(1404, 3, 10), "name": "روز جهانی بدون دخانیات [31 May]"},
    {"date": jdatetime.date(1404, 3, 13), "name": "شهادت امام محمد باقر علیه السلام [٧ ذوالحجه]"},
    {"date": jdatetime.date(1404, 3, 14), "name": "رحلت حضرت امام خمینی"},
    {"date": jdatetime.date(1404, 3, 15), "name": "قیام 15 خرداد"},
    {"date": jdatetime.date(1404, 3, 15), "name": "روز جهانی محیط زیست [5 June]"},
    {"date": jdatetime.date(1404, 3, 15), "name": "روز عرفه [٩ ذوالحجه]"},
    {"date": jdatetime.date(1404, 3, 16), "name": "عید سعید قربان [١٠ ذوالحجه]"},
    {"date": jdatetime.date(1404, 3, 20), "name": "روز جهانی صنایع دستی [10 June]"},
    {"date": jdatetime.date(1404, 3, 21), "name": "ولادت امام علی النقی الهادی علیه السلام [١٥ ذوالحجه]"},
    {"date": jdatetime.date(1404, 3, 22), "name": "روز جهانی مبارزه با کار کودکان [12 June]"},
    {"date": jdatetime.date(1404, 3, 24), "name": "عید سعید غدیر خم [١٨ ذوالحجه]"},
    {"date": jdatetime.date(1404, 3, 24), "name": "روز جهانی اهدای خون [14 June]"},
    {"date": jdatetime.date(1404, 3, 25), "name": "روز ملی گل و گیاه"},
    {"date": jdatetime.date(1404, 3, 26), "name": "ولادت امام موسی کاظم علیه السلام [٢٠ ذوالحجه]"},
    {"date": jdatetime.date(1404, 3, 26), "name": "روز جهانی پدر [16 June]"},
    {"date": jdatetime.date(1404, 3, 27), "name": "روز جهانی بیابان زدایی [17 June]"},
    {"date": jdatetime.date(1404, 3, 31), "name": "سالروز زلزله رودبار و منجیل [1369 خورشیدی]"}
]

def generate_calendar(offset=0):
    """تولید تقویم برای آفست مشخص‌شده"""
    target_gregorian = datetime.date.today() + datetime.timedelta(days=offset)
    target_jalali = jdatetime.date.fromgregorian(date=target_gregorian)
    hijri_date = convert.Gregorian(target_gregorian.year, target_gregorian.month, target_gregorian.day).to_hijri()

    # نام روزهای هفته
    days_fa = ["شنبه", "یک‌شنبه", "دوشنبه", "سه‌شنبه", "چهارشنبه", "پنج‌شنبه", "جمعه"]
    days_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    days_ar = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]

    # نام ماه‌های شمسی و قمری
    jalali_months = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
                     "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"]
    hijri_months = ["محرم", "صفر", "ربیع‌الاول", "ربیع‌الثانی", "جمادی‌الاول", "جمادی‌الثانی",
                    "رجب", "شعبان", "رمضان", "شوال", "ذی‌القعده", "ذی‌الحجه"]

    # استخراج نام روزها و ماه‌ها
    day_fa = days_fa[target_jalali.weekday()]
    day_en = days_en[target_gregorian.weekday()]
    day_ar = days_ar[target_gregorian.weekday()]
    month_fa = jalali_months[target_jalali.month - 1]
    month_ar = hijri_months[hijri_date.month - 1]

    # ---- بررسی مناسبت‌ها ----
    events_today = "🌟 مناسبت‌های مهم:\n"
    future_events = []

    for event in calendar_events_shamsi:
        if event['date'] >= target_jalali:
            days_remaining = (event['date'] - target_jalali).days
            future_events.append((days_remaining, event['name']))
            if target_jalali == event['date']:
                events_today += f"🔹 {event['name']}\n"

    if events_today == "🌟 مناسبت‌های مهم:\n":
        events_today = ''
    else:
        events_today += '\n'

    # روزشمار مناسبت‌های آینده
    remaining_days_output = "📆 روزشمار:\n"
    if future_events:
        future_events.sort()  # مرتب‌سازی بر اساس روز باقی‌مانده
        for days_remaining, event_name in future_events:
            if 0 < days_remaining < 16:
                remaining_days_output += f"▪️ {days_remaining} روز تا {event_name}\n"

    if remaining_days_output == "📆 روزشمار:\n":
        remaining_days_output = ''
    else:
        remaining_days_output += '\n'

    # ساخت پیام تقویم
    calendar_text = f"""🗓 ﺗﻘﻮﯾﻢ ﺗﺎﺭﯾﺦ
☀️ ﺍﻣﺮﻭﺯ:
ﺧﻮﺭﺷﯿﺪﯼ: {day_fa} - {target_jalali.day} {month_fa} {target_jalali.year}
ﻣﯿﻼﺩﯼ: {day_en} - {target_gregorian.year} {target_gregorian.strftime('%d %B')}
ﻗﻤﺮﯼ: {day_ar} - {hijri_date.day} {month_ar} {hijri_date.year}

{events_today}{remaining_days_output}
"""
    return calendar_text

def start(update: Update, context: CallbackContext) -> None:
    """دستور /start برای نمایش پیام خوش‌آمدگویی"""
    update.message.reply_text("سلام! 👋\nیک عدد به من بفرست تا تاریخ آن روز را بهت بگویم! (مثلاً 0 برای امروز، 2 برای پس‌فردا)")

def handle_message(update: Update, context: CallbackContext) -> None:
    """پردازش پیام کاربر و ارسال تاریخ مربوطه"""
    text = update.message.text.strip()

    try:
        offset = int(text)  # تبدیل ورودی به عدد
        calendar_text = generate_calendar(offset)  # تولید تقویم برای آفست
        update.message.reply_text(calendar_text)  # ارسال پیام به کاربر
    except ValueError:
        update.message.reply_text("❌ لطفاً یک عدد صحیح بفرستید! (مثلاً 0، 1، -2)")

def main():
    """راه‌اندازی ربات"""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # تنظیمات فرمان‌ها
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # شروع دریافت پیام‌ها
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
