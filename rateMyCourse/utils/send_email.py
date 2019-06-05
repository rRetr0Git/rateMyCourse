import random
from django.core.mail import send_mail
from rateMyCourse.models import *
from stupidSE.settings import EMAIL_FROM
import os
import time
from django.utils import timezone


def timeit(method):
    """装饰器，记录函数运行时间

    Args:
        method: method to be timed.

    Returns:
        timed: time of running the method.
    """
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('%r  %2.2f sec' % (method.__name__, te - ts))
        return result
    return timed

@timeit
def get_random_str(count):
    """生成激活密钥

    Args:
        count: length of code.

    Returns:
        random_str: code to activate user.
    """
    random_str = ''
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    str_len = len(chars) - 1
    for i in range(count):
        randindex = random.randint(0, str_len)
        randomchar = chars[randindex]
        random_str += randomchar
    return random_str


@timeit
def send_my_email(request, email, send_type):
    """发送邮件

    Args:
        email: email to receive code or reset password.
        send_type：'register' to register, 'resetPDW' to reset password.

    Returns:
        send_status: 1 if sending secceeds, else 0.
    """
    try:
        if send_type == 'register':
            email_record = EmailVerifyRecord()
            while(1):
                random_str = get_random_str(15)
                evrs = EmailVerifyRecord.objects.filter(code=random_str)
                if len(evrs) == 0:
                    break
            email_record.code = random_str
            email_record.email = email
            email_record.type = send_type
            email_record.time = timezone.now()
            email_record.valid = 0
            email_title = '公课网账户激活'
            email_body = '点击链接激活公课网账户。\r\n' + request.build_absolute_uri('/') +'active/{0}'.format(random_str)
            print('start sending email')
            send_status = send_mail(email_title, email_body, EMAIL_FROM, [email], html_message=email_body)
            print('sending email end')
            email_record.save()
            return send_status, email_record.id

        elif send_type == 'resetPWD':
            email_record = EmailVerifyRecord()
            while (1):
                random_str = get_random_str(15)
                evrs = EmailVerifyRecord.objects.filter(code=random_str)
                if len(evrs) == 0:
                    break
            email_record.code = random_str
            email_record.email = email
            email_record.type = send_type
            email_record.time = timezone.now()
            email_record.valid = 0
            email_title = '公课网账户重置密码'
            email_body = '点击链接重置公课网账户密码，10分钟内有效。\r\n' + request.build_absolute_uri('/') + 'toResetPWD/{0}'.format(random_str)
            print('start sending email')
            send_status = send_mail(email_title, email_body, EMAIL_FROM, [email], html_message=email_body)
            print('sending email end')
            email_record.save()
            return send_status, email_record.id
    except:
        print('email send error!')
        return -1, 'error'