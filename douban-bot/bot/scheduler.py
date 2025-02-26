from apscheduler.schedulers.background import BackgroundScheduler
from bot.reply_logic import process_messages

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(process_messages, "interval", minutes=5)  # 每 5 分钟检查一次消息
    scheduler.start()
