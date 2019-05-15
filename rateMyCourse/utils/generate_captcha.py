import random
from captcha.image import ImageCaptcha

import os
import random
from PIL import Image
from PIL import ImageFilter
from PIL.ImageDraw import Draw
from PIL.ImageFont import truetype
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
try:
    from wheezy.captcha import image as wheezy_captcha
except ImportError:
    wheezy_captcha = None

DATA_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')
DEFAULT_FONTS = [os.path.join(DATA_DIR, 'DroidSansMono.ttf')]

if wheezy_captcha:
    __all__ = ['ImageCaptcha', 'WheezyCaptcha']
else:
    __all__ = ['ImageCaptcha']


table = []
for i in range(256):
    table.append(i * 1.97)

captcha_picture_num = 0
max_captcha_picture_num = 300


# rewrite the method to generate captcha
class MyImageCaptcha(ImageCaptcha):
    def create_captcha_image(self, chars, color, background):
        """Create the CAPTCHA image itself.

        :param chars: text to be generated.
        :param color: color of the text.
        :param background: color of the background.

        The color should be a tuple of 3 numbers, such as (0, 255, 255).
        """
        image = Image.new('RGB', (self._width, self._height), background)
        draw = Draw(image)

        def _draw_character(c):
            font = random.choice(self.truefonts)
            w, h = draw.textsize(c, font=font)

            dx = random.randint(0, 4)
            dy = random.randint(0, 6)
            im = Image.new('RGBA', (w + dx, h + dy))
            Draw(im).text((dx, dy), c, font=font, fill=color)

            # rotate
            im = im.crop(im.getbbox())
            im = im.rotate(random.uniform(-10, 10), Image.BILINEAR, expand=1)

            # warp
            dx = w * random.uniform(0.1, 0.3)
            dy = h * random.uniform(0.2, 0.3)
            x1 = int(random.uniform(-dx, dx))
            y1 = int(random.uniform(-dy, dy))
            x2 = int(random.uniform(-dx, dx))
            y2 = int(random.uniform(-dy, dy))
            w2 = w + abs(x1) + abs(x2)
            h2 = h + abs(y1) + abs(y2)
            data = (
                x1, y1,
                -x1, h2 - y2,
                w2 + x2, h2 + y2,
                w2 - x2, -y1,
            )
            im = im.resize((w2, h2))
            im = im.transform((w, h), Image.QUAD, data)
            return im

        images = []
        for c in chars:
            if random.random() > 0.5:
                images.append(_draw_character(" "))
            images.append(_draw_character(c))

        text_width = sum([im.size[0] for im in images])

        width = max(text_width, self._width)
        image = image.resize((width, self._height))

        average = int(text_width / len(chars))
        rand = int(0.25 * average)
        offset = int(average * 0.1)

        for im in images:
            w, h = im.size
            mask = im.convert('L').point(table)
            image.paste(im, (offset, int((self._height - h) / 2)), mask)
            offset = offset + w

        if width > self._width:
            image = image.resize((self._width, self._height))

        return image


def get_captcha():
    """生成验证码

    Returns:
        url: path of captcha.
        captcha_string: value of captcha.
    """
    global captcha_picture_num
    captcha_picture_path = './rateMyCourse/static/captcha/' + str(captcha_picture_num) + '.jpg'
    url = '/static/captcha/' + str(captcha_picture_num) + '.jpg'
    captcha_picture_num = (captcha_picture_num + 1) % max_captcha_picture_num
    seed = "34abcdefhjkmnpqruvwxyACDEFGHJKMNPRUVWXY"
    sa = []
    for i in range(0, 6):
        sa.append(random.choice(seed))
    captcha_string = ''.join(sa)
    a = [30 for i in range(0, 6)]
    img = MyImageCaptcha(font_sizes=a, height=40)
    image = img.generate_image(captcha_string)
    image.save(captcha_picture_path)
    return url, captcha_string
