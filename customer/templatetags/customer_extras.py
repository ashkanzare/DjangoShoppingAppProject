from django import template
import jdatetime
from datetime import datetime

register = template.Library()


@register.filter(name='en_to_fa')
def en_to_fa(text):
    """convert english number to persian"""
    fa_numbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
    text_list = list(str(text))
    for i in range(len(text_list)):
        if text_list[i].isnumeric():
            text_list[i] = fa_numbers[int(text_list[i])]
    return ''.join(text_list)


@register.filter(name='date_delta')
def date_delta(date_time):
    """ compute delta time between now and post date """
    now = datetime.now()
    delta = now - date_time
    if delta.days != 0:
        days = delta.days, 'روز'
        if days[0] >= 30:
            days = int(days[0] / 30), 'ماه'
        return f"{en_to_fa(days[0])} {days[1]}"

    elif delta.seconds != 0:
        seconds = delta.seconds, 'ثانیه'
        if seconds[0] >= 3600:
            seconds = int(seconds[0] / 3600), 'ساعت'
        elif seconds[0] >= 60:
            seconds = int(seconds[0] / 60), 'دقیقه'
        return f"{en_to_fa(seconds[0])} {seconds[1]}"


@register.filter(name='convert_date')
def convert_date(date):
    """ get christian year and convert to jalali date """
    j_date = jdatetime.date.fromgregorian(day=date.day, month=date.month, year=date.year)
    month = j_date.j_months_fa[j_date.month - 1]
    return f"{en_to_fa(j_date.day)} {month} {en_to_fa(j_date.year)}"

