from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from .config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from .responses import intro_text, help_text

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def send_image_to_telegram(image_url, caption, reply_to_msg_id=None):
    print(f"Send image {image_url, caption}")

    try:
        await bot.send_photo(
            chat_id=TELEGRAM_CHAT_ID,
            photo=image_url,
            caption=caption,
            reply_to_message_id=reply_to_msg_id,
            parse_mode=types.ParseMode.MARKDOWN,
        )
        return True
    except Exception as e:
        print(f"Failed to send message: {e}")
        return False


@dp.message_handler(commands=["start"])
async def on_start(message: types.Message):
    await message.reply(intro_text)


@dp.message_handler(commands=["intro"])
async def on_intro(message: types.Message):
    await message.reply(intro_text)


@dp.message_handler(commands=["help"])
async def on_help(message: types.Message):
    await message.reply(help_text)
