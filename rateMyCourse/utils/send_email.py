import random
from django.core.mail import send_mail
from rateMyCourse.models import *
from stupidSE.settings import EMAIL_FROM
import os


def get_random_str(count):
    random_str = ''
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    str_len = len(chars) - 1
    for i in range(count):
        randindex = random.randint(0, str_len)
        randomchar = chars[randindex]
        random_str += randomchar
    return random_str


def send_register_email(request, email, send_type='register'):
    email_record = EmailVerifyRecord()
    while(1):
        random_str = get_random_str(15)
        evrs = EmailVerifyRecord.objects.filter(code=random_str)
        if len(evrs) == 0:
            break
    email_record.code = random_str  # how to ensure unique
    email_record.email = email  # how to ensure unique
    email_record.type = send_type
    email_record.save()
    email_title = '点击验证公课网账户'
    email_body = '请点击下边的链接激活 ' + request.build_absolute_uri('/') +'active/{0}'.format(random_str)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email], html_message=email_body)
    return send_status