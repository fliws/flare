import discord
import re
from .telegram_bot import connect_to_telegram, send_image_to_telegram
from .utils import emoji_to_unicode, extract_text_between_stars

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

    pattern = r'\*\*.*\*\* - Image #\d+ <@\d+>'
    if re.match(pattern, message.content):
        await message.add_reaction('👉')


@client.event
async def on_raw_reaction_add(payload):
    # Получаем информацию о реакции
    emoji = payload.emoji
    channel_id = payload.channel_id
    user_id = payload.user_id

    # Проверяем, не является ли пользователь ботом
    if user_id == client.user.id:
        print ("own reaction - skip")
        return

    # Получаем объекты канала и сообщения
    channel = client.get_channel(channel_id)
    message = await channel.fetch_message(payload.message_id)
    print(f"reaction {emoji.name}")
    if emoji.name == '👉':
        print(message.content)
        if len(message.attachments) > 0:
            for attachment in message.attachments:
                if attachment.content_type.startswith('image'):
                    image_url = attachment.url
                    print(f"send {image_url}")
                    await message.add_reaction('👌')
                    await send_image_to_telegram(image_url, message.channel.name.split("-")[0] + ": " + f"`{extract_text_between_stars(message.content)}`", reply_to_msg_id=18515)
                    break