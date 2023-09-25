from django.shortcuts import render
from django.core.mail import send_mail

from R4C.settings import EMAIL_HOST_USER


def send_mail_to_customers(serial: str, list_customer: tuple):
    model, version = tuple(serial.split('-'))
    subject = f'{model}-{version} есть в наличии!'
    message = (
        'Добрый день!'
        f'Недавно вы интересовались нашим роботом модели {model}, версии {version}.'
        'Этот робот теперь в наличии. Если вам подходит этот вариант - '
        'пожалуйста, свяжитесь с нами'
    )
    from_email = EMAIL_HOST_USER

    # TODO следующую строку закоммитить чтобы началась рассылка
    list_customer = 'можно вписать свою почту для проверки'

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=list_customer
    )

