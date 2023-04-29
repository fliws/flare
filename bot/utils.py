import re

# Функция для преобразования эмодзи в unicode
def emoji_to_unicode(emoji_str):
    return '-'.join(['%04x' % ord(c) for c in emoji_str])

# Функция для извлечения промта
def extract_text_between_stars(text):
    pattern = r'\*\*(.*?)\*\*'
    matches = re.findall(pattern, text)
    return matches[0]