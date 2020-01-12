from logging import getLogger

from googletrans import Translator
from googletrans.models import Detected, Translated

log = getLogger('root')


def translate(value: str) -> str:
    """
    Translate a sentence to english.
    :param value: Sentence
    :return: English sentence.
    """
    log.info(f'[TRANSLATOR] Original: {value}')
    if value is None:
        return ''

    translator = Translator()
    curr_lang: Detected = translator.detect(value)
    if curr_lang.lang == 'en':
        return value

    result: Translated = translator.translate(value, dest='en', src=curr_lang.lang)
    log.info(f'[TRANSLATOR] Translated from "{curr_lang.lang}": "{result.text}"')
    return result.text
