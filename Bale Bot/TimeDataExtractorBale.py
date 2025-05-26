import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import arabic_reshaper
import jdatetime
from datetime import datetime
import time
import schedule
import requests
from datetime import datetime
import json
from hijri_converter import Gregorian


def fetch_time_ir_data():
    url = 'https://www.time.ir/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        return response.text
    else:
        print(f"Error: Unable to fetch data from {url}")
        return None

def parse_time_ir_data(html_content, offset_days):
    soup = BeautifulSoup(html_content, 'html.parser')

    date_boxes = soup.find_all('div', class_='DateBox_root__K4S8K')

    today_shamsi = None
    today_miladi = None
    today_ghamari = None

    for box in date_boxes:
        label = box.find('p', class_='DateBox_root__label__V4tlc')
        if not label:
            continue
        label_text = label.text.strip()

        if label_text == 'تاریخ خورشیدی':
            date_texts = box.find_all('p', class_='MuiTypography-root MuiTypography-button1 muirtl-1vbhkcf')
            today_shamsi = date_texts[1].text.strip()
        elif label_text == 'تاریخ میلادی':
            date_texts = box.find_all('p', class_='MuiTypography-root MuiTypography-button1 en muirtl-1vbhkcf')
            today_miladi = date_texts[1].text.strip()
        elif label_text == 'تاریخ قمری':
            date_texts = box.find_all('p', class_='MuiTypography-root MuiTypography-button1 muirtl-1vbhkcf')
            today_ghamari = date_texts[1].text.strip()

    parts_today_shamsi = [part.strip() for part in today_shamsi.split('\n') if part.strip()]
    parts_today_miladi = [part.strip() for part in today_miladi.split('\n') if part.strip()]
    parts_today_ghamari = [part.strip() for part in today_ghamari.split('\n') if part.strip()]



    if offset_days != 0:
        # تغییر تاریخ با توجه به offset_days
        today_miladi = f"میلادی: {parts_today_miladi[-1]}"
        today_date_str = today_miladi.split('-')[-1].strip()
        today_date_gregorian = datetime.strptime(today_date_str, '%Y %B %d').date()
        today_date_gregorian += timedelta(days=offset_days)
        today_date_shamsi = jdatetime.date.fromgregorian(date=today_date_gregorian)

        # بازسازی today_shamsi
        today_date_shamsi = jdatetime.date.fromgregorian(date=today_date_gregorian)

        # Persian names for weekdays
        persian_weekdays = [ 'شنبه', 'یک‌شنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه']

        # Get the Persian weekday name
        weekday_shamsi = persian_weekdays[today_date_shamsi.weekday()]  # e.g., 'یکشنبه'

        # Persian months (for Shamsi date)
        months_shamsi = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
                        'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']

        month_name_shamsi = months_shamsi[today_date_shamsi.month - 1]

        # Format the Shamsi (Solar Hijri) date string
        today_shamsi = f"خورشیدی: {weekday_shamsi} - {today_date_shamsi.day} {month_name_shamsi} {today_date_shamsi.year}"

        # بازسازی today_miladi
        weekday_miladi = today_date_gregorian.strftime('%A')  # like 'Sunday'
        month_name_miladi = today_date_gregorian.strftime('%B')  # like 'April'
        today_miladi = f"میلادی: {weekday_miladi} - {today_date_gregorian.year} {today_date_gregorian.day} {month_name_miladi}"

        # Convert Gregorian to Hijri
        hijri_date = Gregorian(today_date_gregorian.year, today_date_gregorian.month, today_date_gregorian.day).to_hijri()

        # Arabic names for weekdays and months
        arabic_weekdays = ['السبت', 'الأحد', 'الإثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة']
        arabic_months = ['محرم', 'صفر', 'ربيع‌الاول', 'ربيع الثاني', 'جمادي‌الاولي', 'جمادي‌الثانيه',
                        'رجب', 'شعبان', 'رمضان', 'شوال', 'ذوالقعدة', 'ذوالحجة']

        # Find correct weekday (important: weekday of Gregorian date!)
        weekday_ghamari = arabic_weekdays[today_date_gregorian.weekday()]
        month_name_ghamari = arabic_months[hijri_date.month - 1]
        # Final string
        today_ghamari = f"قمری: {weekday_ghamari} - {hijri_date.day} {month_name_ghamari} {hijri_date.year}"
    


    # Find dates by site:
    else:
        today_shamsi = f"خورشیدی: {parts_today_shamsi[-1]}"
        today_miladi = f"میلادی: {parts_today_miladi[-1]}"
        today_ghamari = f"قمری: {parts_today_ghamari[-1]}"
        today_date_str = today_miladi.split('-')[-1].strip()
        today_date_gregorian = datetime.strptime(today_date_str, '%Y %B %d').date()
        today_date_gregorian += timedelta(days=offset_days)
        today_date_shamsi = jdatetime.date.fromgregorian(date=today_date_gregorian)




    calendar_events_shamsi = [
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

    events_today = "🌟 مناسبت‌های مهم:\n"
    future_events = []

    for event in calendar_events_shamsi:
        if event['date'] >= today_date_shamsi:
            days_remaining = (event['date'] - today_date_shamsi).days
            future_events.append((days_remaining, event['name']))
            if today_date_shamsi == event['date']:
                events_today += f"🔹 {event['name']}\n"

    if events_today == "🌟 مناسبت‌های مهم:\n":
        events_today = ''
    else:
        events_today += '\n'

    remaining_days_output = "📆 روزشمار:\n"
    if future_events:
        future_events.sort()
        for days_remaining, event_name in future_events:
            if days_remaining > 0 and days_remaining < 16:
                remaining_days_output += f"▪️ {days_remaining} روز تا {event_name}\n"
    if remaining_days_output == "📆 روزشمار:\n":
        remaining_days_output = ''
    else:
        remaining_days_output += '\n'
    
    return today_shamsi, today_miladi, today_ghamari, events_today, remaining_days_output

def generate_daily_message_for_offset(offset_days):
    html_content = fetch_time_ir_data()
    if not html_content:
        return "Error: Unable to fetch data from time.ir"

    today_shamsi, today_miladi, today_ghamari, events_today, remaining_days_output = parse_time_ir_data(html_content, offset_days)
    
    message = "🗓 تقویم تاریخ\n"
    message += f"☀️ روز انتخابی:\n{today_shamsi}\n{today_miladi}\n{today_ghamari}\n\n"
    message += events_today
    message += remaining_days_output
    message += f"✅ برای اطلاعات بیشتر و همراهی با ما به کانال بپیوندید!"
    message += "\n@DailyReminderHub"
    return message





# Replace with your own Bale bot token
TOKEN = '786452027:6tTiofvREnPUuldQtluEDcNJvNAKta7Mss7IvekW'
BASE_URL = f'https://tapi.bale.ai/bot{TOKEN}'
sent_time = "16:30"

# File to save subscribers
SUBSCRIBERS_FILE = "subscribers.json"

# Users who are entering a number
waiting_for_day_number = {}

def load_subscribers():
    """Load the list of subscribers from a file."""
    try:
        with open(SUBSCRIBERS_FILE, "r") as file:
            return set(json.load(file))
    except FileNotFoundError:
        return set()  # Return an empty set if the file doesn't exist

def save_subscribers():
    """Save the list of subscribers to a file."""
    with open(SUBSCRIBERS_FILE, "w") as file:
        json.dump(list(subscribers), file)

# Load subscribers at startup
subscribers = load_subscribers()

def send_message(chat_id, text):
    """Send a message to a chat."""
    url = f"{BASE_URL}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=payload)
    return response.json()

def send_daily_message():
    """Send the daily message to all subscribers at 00:00."""
    daily_message = generate_daily_message_for_offset()
    reshaped_text = arabic_reshaper.reshape(daily_message)
    
    for chat_id in subscribers:
        send_message(chat_id, reshaped_text)
    print(f"Daily message sent to all subscribers at {datetime.now()}")

def handle_update(update):
    """Process incoming updates."""
    if 'message' in update:
        message = update['message']
        chat_id = message['from']['id']
        text = message.get('text', '')

        if waiting_for_day_number.get(chat_id, False):
            # User is expected to send a number
            try:
                day_offset = int(text)
                if day_offset < 0:
                    send_message(chat_id, "❌ Please enter 0 or a positive number.")
                    return
                message_to_send = generate_daily_message_for_offset(day_offset)
                reshaped_text = arabic_reshaper.reshape(message_to_send)
                send_message(chat_id, reshaped_text)
                waiting_for_day_number.pop(chat_id)  # Reset the state
            except ValueError:
                send_message(chat_id, "❌ Please send a valid number.")
            return

        if text == '/start':
            daily_message = generate_daily_message_for_offset(0)
            reshaped_text = arabic_reshaper.reshape(daily_message)
            send_message_with_button(chat_id, reshaped_text)
            if chat_id not in subscribers:
                subscribers.add(chat_id)
                save_subscribers()
                send_message(chat_id, "You have subscribed to daily reminders! 🎉")
            else:
                send_message(chat_id, "You are already subscribed to daily reminders.")
        
        elif text == '/stop':
            if chat_id in subscribers:
                subscribers.remove(chat_id)
                save_subscribers()
                send_message(chat_id, "You have unsubscribed from daily reminders.")
            else:
                send_message(chat_id, "You are not subscribed.")

        elif text == '📅 انتخاب روز':
            send_message(chat_id, "🔢 لطفاً یک عدد وارد کنید:\n(0 = امروز، 1 = فردا و...)")
            waiting_for_day_number[chat_id] = True


def get_updates(offset=None):
    """Fetch updates from Bale with error handling."""
    url = f"{BASE_URL}/getUpdates"
    params = {'offset': offset} if offset else {}
    
    try:
        response = requests.get(url, params=params, timeout=10)  # Add a timeout
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching updates: {e}")
        time.sleep(5)  # Wait before retrying
        return {"result": []}  # Return an empty result to prevent crashes

def schedule_tasks():
    """Schedule the daily message."""
    schedule.every().day.at(sent_time).do(send_daily_message)

    while True:
        schedule.run_pending()
        time.sleep(1)



def send_message_with_button(chat_id, text):
    """Send a message with a custom keyboard."""
    url = f"{BASE_URL}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
        'reply_markup': {
            'keyboard': [['📅 انتخاب روز']],
            'resize_keyboard': True,
            'one_time_keyboard': False
        }
    }
    response = requests.post(url, json=payload)
    return response.json()



def main():

    # Start the bot
    offset = None

    # Schedule daily messages
    import threading
    threading.Thread(target=schedule_tasks, daemon=True).start()

    # Process updates continuously
    while True:
        updates = get_updates(offset)
        for update in updates.get('result', []):
            handle_update(update)
            offset = update['update_id'] + 1

if __name__ == '__main__':
    main()
