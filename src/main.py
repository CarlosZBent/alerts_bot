from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, CallbackContext, JobQueue

import logging
from dotenv import load_dotenv
from os import getenv
from datetime import datetime, timedelta
import pytz

from db_funcs.db_funcs import query_events_data
from helpers.helpers import format_data_for_text_message


load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


USERID = getenv("USERID")
BOT_TOKEN = getenv("BOT_TOKEN")
EVENTS_TABLE = getenv("EVENTS_TABLE")
user_timezone = pytz.timezone("US/Eastern")
today = datetime.now(tz=user_timezone).date()
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
    if update.effective_user.id == int(USERID):
        events_data = query_events_data(EVENTS_TABLE, today)
        message_content = format_data_for_text_message(events_data)

        update.message.reply_markdown(
            f"""Events for { today }\n\n{ message_content }"""
        )
        print(f">>> Events data requested for {today}. Sent successfully.")
    else:
        update.message.reply_text("You are not authorized to use this bot. To know more contact @cezbent. Thanks!")
        context.bot.send_message(USERID, f"""
    Unauthorized user attempted access:
    - user_id: {update.effective_message.from_user.id}
    - username: {update.effective_message.from_user.username}
    - full_name: {update.effective_message.from_user.first_name}  {update.effective_message.from_user.last_name}
    """)


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
        events_data = query_events_data(EVENTS_TABLE, yesterday)
        message_content = format_data_for_text_message(events_data)
        ThisBot.send_message(USERID, f"""Events for { yesterday }\n\n{ message_content }""", parse_mode="markdown")
        print(f">>> Daily alert sent successfully. Corresponding date={yesterday}")


    CustomJobQueue = JobQueue()
    CustomJobQueue.set_dispatcher(dispatcher=dp)
    trigger_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 10, 00, 00, 0, user_timezone).timetz()
    print("TZ: ", user_timezone)
    print("TRIGGER_TIME: ", trigger_time)
    CustomJobQueue.run_daily(daily_alert, trigger_time, name="daily_alert")
    CustomJobQueue.scheduler.start()

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()