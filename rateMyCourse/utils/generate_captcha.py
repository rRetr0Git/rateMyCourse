import random
from captcha.image import ImageCaptcha

captcha_picture_num = 0
max_captcha_picture_num = 30


def get_captcha():
    global captcha_picture_num
    captcha_picture_path = './rateMyCourse/static/captcha/' + str(captcha_picture_num) + '.jpg'
    url = '/static/captcha/' + str(captcha_picture_num) + '.jpg'
    captcha_picture_num = (captcha_picture_num + 1) % max_captcha_picture_num
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(0, 6):
        sa.append(random.choice(seed))
    captcha_string = ''.join(sa)
    a = [30 for i in range(0, 6)]
    img = ImageCaptcha(font_sizes=a, height=40)
    image = img.generate_image(captcha_string)
    image.save(captcha_picture_path)
    return url, captcha_string