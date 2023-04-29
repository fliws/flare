import re

# Функция для преобразования эмодзи в unicode
def emoji_to_unicode(emoji_str):
    return '-'.join(['%04x' % ord(c) for c in emoji_str])

def extract_text_between_stars(text):
    ...
