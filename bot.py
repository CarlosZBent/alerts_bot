from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, JobQueue

import logging
from dotenv import load_dotenv
from os import getenv
from datetime import datetime
from dateutil import tz

from standalone_funcs import fetch_data_from_table


load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


CZ_USERID = getenv("CZ_USERID")
BOT_TOKEN = getenv("BOT_TOKEN")
EVENTS_TABLE = getenv("EVENTS_TABLE")
today = datetime.now().date()


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(
    f"""
    Hello!
I will provide a daily report of your chosen database table data.
Otherwise use /fetch_now to get the latest results right now
    """)


def fetch_now(update: Update, context: CallbackContext) -> None:
    """
    Fetch the current table data 
    when the user requests it
    """
    message_content = fetch_data_from_table(EVENTS_TABLE, "2023-05-05")
    update.message.reply_markdown(
        f"""{ today }\n\n{ message_content }"""
    )


def main() -> None:
    """Start the bot."""
    
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("fetch_now", fetch_now))

    def daily_alert(*args, **kwargs):
        ThisBot = Bot(BOT_TOKEN)
        print(ThisBot)
        message_content = fetch_data_from_table(EVENTS_TABLE, "2023-05-05")
        print(message_content)
        ThisBot.send_message(CZ_USERID, message_content, parse_mode="markdown")


    CustomJobQueue = JobQueue()
    CustomJobQueue.set_dispatcher(dispatcher=dispatcher)
    # CustomJobQueue.run_once(daily_alert, 25, name="25_seconds")
    tz_info = tz.gettz("America/Havana")
    print("TZ: ", tz_info)
    trigger_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 11, 57, 00, 0o40153, tz_info).time()
    print("TRIGGER_TIME: ", trigger_time)
    CustomJobQueue.run_daily(daily_alert, trigger_time, name="daily_alert")
    CustomJobQueue.scheduler.start()

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()