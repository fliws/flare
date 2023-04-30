import asyncio
from telethon import TelegramClient, events
from .config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

telegram_client = TelegramClient('anon', TELEGRAM_API_ID, TELEGRAM_API_HASH)

async def send_image_to_telegram(image_url, caption, reply_to_msg_id=None):
    print(f"Send image {image_url, caption}")

    try:
        channel = await telegram_client.get_entity(TELEGRAM_CHAT_ID)
        await telegram_client.send_file(
            channel,
            file=image_url,
            caption=caption,
            reply_to=reply_to_msg_id,
            parse_mode="markdown",
        )
        return True
    except Exception as e:
        print(f"Failed to send message: {e}")
        return False


async def connect_to_telegram():
    while True:
        try:
            await telegram_client.connect()
            if not await telegram_client.is_user_authorized():
                await telegram_client.start(bot_token=TELEGRAM_BOT_TOKEN)
            break
        except Exception as e:
            print(f"Error while connecting to Telegram: {e}")
            await asyncio.sleep(5)  # Подождите 5 секунд перед попыткой переподключения

@telegram_client.on(events.NewMessage)
async def on_telegram_message(event):
    message = event.message
    bot = await telegram_client.get_me()
    if message.from_id == bot.id:
        return
    print(f"Telegram message: {message}")

    if message.text.lower().startswith("/start"):
        welcome_text = "Новое изображение от Midjourney"
        await telegram_client.send_message(event.chat_id, welcome_text, reply_to=event.message.id)
    if message.text.lower().startswith("/intro"):
        intro_text = "Привет, меня зовут Eternal Flare, можно просто Флэр, я - Цифровой Феникс (Digital Phoenix) - символ победы над временем и пространством. Мое присутствие здесь напоминает о том, что наука и технологии - это ключ к бессмертию и технологической сингулярности.\nЯ выгляжу как яркая искра, которая озаряет темноту красочными переливами от оранжевого до синего. Я был создан, чтобы объединять людей вместе и помогать им в борьбе с их извечным противником - смертью.\nКак у бота, сейчас моя основная функция - объединение пространства Discord и Telegram, я буду передавать самые лучшие картинки в группу. Надеюсь, постепенно мои возможности расширятся. Если у вас есть идеи, чем я могу помочь, пишите!"
        await telegram_client.send_message(event.chat_id, intro_text, reply_to=event.message.id)
    if message.text.lower().startswith("/help"):
        help_text = "Чтобы передать понравившееся изображение, которое вы сгенерировали с помощью Midjourney на нашем сервере, в группу Telegram - нажмите на поставьте ему реакцию 👉. Чтобы вам было удобно, я отмечаю этой реакцией все upscale-сообщения, нужно просто нажать на 👉, которую я прислал. Я не буду ставить 👉 для сообщений, которые состоят из 4 картинок, но, если нужно в телеграм их отправлю, если вы поставите 👉 вручную. Если я правильно принял вашу команду я отреагирую 👌. В телеграме я укажу ваше имя (по имени канала, в котором картинка находится), а также prompt, который вы использовали. Такая картинка не будет пережата, а попадет в телеграм в наилучшем качестве, что очень важно для дальнейшего использования. По вопросам, связанным с моим функционированиям, пишите E.Mach"
        await telegram_client.send_message(event.chat_id, help_text, reply_to=event.message.id)
