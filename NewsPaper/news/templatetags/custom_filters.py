from django import template

register = template.Library()

BAD_WORDS = ['коза', 'редиска', 'редиске', 'осел']


@register.filter(name='censor')
def censor(value):
    if not isinstance(value, str):
        raise ValueError('Нельзя цензурировать не строку')

    for word in BAD_WORDS:
        value = value.replace(word[1:], '*' * (len(word) - 1))

    return value