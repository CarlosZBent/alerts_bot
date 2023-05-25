from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, JobQueue

import logging
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, timedelta
import pytz

from db_funcs import query_events_data
from helpers import format_data_for_text_message


load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


USERID = getenv("USERID")
BOT_TOKEN = getenv("BOT_TOKEN")
EVENTS_TABLE = getenv("EVENTS_TABLE")
today = datetime.now().date()
yesterday = today - timedelta(1)


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
    events_data = query_events_data(EVENTS_TABLE, today)
    message_content = format_data_for_text_message(events_data)

    update.message.reply_markdown(
        f"""Events for { today }\n\n{ message_content }"""
    )


def main() -> None:
    """Start the bot."""
    
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("fetch_now", fetch_now))

    def daily_alert(*args, **kwargs):
        """
        Send a daily alert message
        """
        ThisBot = Bot(BOT_TOKEN)
        events_data = query_events_data(EVENTS_TABLE, today)
        message_content = format_data_for_text_message(events_data)
        ThisBot.send_message(USERID, f"""Events for { yesterday }\n\n{ message_content }""", parse_mode="markdown")


    CustomJobQueue = JobQueue()
    CustomJobQueue.set_dispatcher(dispatcher=dp)
    timez = pytz.timezone("US/Eastern")
    trigger_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 9, 00, 00, 0, timez).timetz()
    print("TZ: ", timez)
    print("TRIGGER_TIME: ", trigger_time)
    CustomJobQueue.run_daily(daily_alert, trigger_time, name="daily_alert")
    CustomJobQueue.scheduler.start()

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()