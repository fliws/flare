import discord
from .config import DISCORD_TOKEN
from .telegram_bot import connect_to_telegram
from .utils import emoji_to_unicode, extract_text_between_stars, send_image_to_telegram

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    # Авторизация с использованием токена бота
    await connect_to_telegram()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f"full: {message}")
    print(f"content: {message.content}")

    keywords = ['flare', 'flar', 'fler', 'flaer', 'phoenix', 'феникс', 'флер', 'флэр']
    if any(keyword in message.content.lower() for keyword in keywords):
        # если сообщение содержит обращение к flare, проверяем, является ли это приветствием
        if re.search(r'(прив|здоров|дарова|здрав|hi |hello|добр|салют).*', message.content.lower()):
            await message.reply(f'Привет {message.channel.name.split("-")[0]}')
        elif re.search(r'(как\s+дела|как\s+жизнь|как\s+ты).*', message.content.lower()):
            await message.reply("У меня все отлично, готов помочь вам")
        elif re.search(r'(помоги|помощь|как.*пользоваться|справка|help).*', message.content.lower()):
            await message.reply("Сейчас у меня только одна функция - если вы реагируете на картинку с помощью эмодзи :knot:, я ретранслирую эту картинку в телеграм OpenLongevity/Modjourney")
        else:
            await message.reply("Вы меня упомянули, но я не смог разобрать вашу команду. Напишите Флэр помоги, чтобы получить справку по моим функциям")


@client.event
async def on_raw_reaction_add(payload):
    # Получаем информацию о реакции
    emoji = payload.emoji
    channel_id = payload.channel_id
    user_id = payload.user_id

    # Проверяем, не является ли пользователь ботом
    if user_id == client.user.id:
        return

    # Получаем объекты канала и сообщения
    channel = client.get_channel(channel_id)
    message = await channel.fetch_message(payload.message_id)
    reaction = emoji_to_unicode(emoji.name)
    print(f"reaction {reaction}")
    if reaction == '1faa2':
        print("ITS KNOT")
        print(message.content)
        if len(message.attachments) > 0:
            print(f"SHOME:{message.attachments}")
            for attachment in message.attachments:
                if attachment.content_type.startswith('image'):
                    image_url = attachment.url
                    await message.reply('Перенаправляю изображение в чат')
                    await send_image_to_telegram(image_url, message.channel.name.split("-")[0] + ": " + extract_text_between_stars(message.content), reply_to_msg_id=18515)
                    break