from django import template

"""FlashText - библиотека для замены слов в тексте
from flashtext import KeywordProcessor
keyword_processor = KeywordProcessor()
keyword_processor.add_keywords_from_dict(CURRENCY_WORDS)

CURRENCY_WORDS = {
     'р***': ['редиска'],
     'д***': ['директор'],
     'п***': ['пропускать'],
}"""


class CensorException(Exception):
    pass


register = template.Library()



CURRENCY_WORDS = {
    'редиска': 'редиска',
    'директор': 'директор',
    'пропускать': 'пропускать',
    'глубине': 'глубине',
    'поразили': 'поразили',
    'убитое': 'убитое',
    'напомним': 'напомним',
    'исполнительный' : 'исполнительный'
}



@register.filter()
def censor(value: str) -> str:
    try:
        if not isinstance(value, str):
            raise CensorException('Error')

        a = value
        for word in list(CURRENCY_WORDS.keys()):
            if word in a:
                a = a.replace(word, f'{word[:1]}*****{word[-1:-2:-1]}')
            if word.capitalize() in a:
                a = a.replace(word.capitalize(), f'{word[:1].capitalize()}*****{word[-1:-2:-1].capitalize()}')
                
        return a
        """Нашёл альтернативный способ как заменить слова в тексте.
        Использование этой библиотеки оправдано в случае если тексты огромные.
        За счёт заложенный алгоритмов не нужно на каждой итерации проходить по каждому слову теста.
        Вместо этого алгоритм по тексту пробегает всего 1 раз"""
        # new_value = keyword_processor.replace_keywords(value)
        # return new_value

    except CensorException as e:
        print(e)
