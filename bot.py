from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import logging
from dotenv import load_dotenv
from os import getenv
from datetime import datetime

from db_funcs import query_present_day_data
from helpers import format_table_data_to_dict


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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_markdown(
    f"""
    **Hello!**
    I will provide a daily report of your chosen database table data.
    Otherwise use /fetch_now to get the latest results right now
    """)

async def fetch_now(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Fetch the current table data 
    when the user requests it
    """
    data = query_present_day_data(EVENTS_TABLE, "2023-05-05")
    data_dict = format_table_data_to_dict(data)
    print(data_dict)
    await update.message.reply_text(str(data_dict))

    

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("fetch_now", fetch_now))

    application.run_polling()


if __name__ == "__main__":
    main()