# PIL 库 安装指令  pip install pillow
from PIL import Image, ImageDraw, ImageFont
import string
import random
from io import BytesIO


# 随机颜色
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


# 所有字符 数字+大小写字母
str_all = string.digits + string.ascii_letters


# 随机验证码
def random_code(size=(200, 40), length=4, print_num=100, line_num=10):
    # Image.new(颜色模式, 尺寸, 背景颜色)
    width, height = size

    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    # 创建画布  以生成的img为背景和大小 生成 画布
    draw = ImageDraw.Draw(img)
    # 生成字体
    font = ImageFont.truetype(font='static/my/font/MexicanTequila.ttf', size=32)
    # 书写文字
    vaild_code = ''
    for i in range(length):
        random_char = random.choice(str_all)
        draw.text((40 * i + 20, 10), random_char, (0, 0, 0), font=font)
        vaild_code += random_char
    print(vaild_code)
    # 随机生成点
    for i in range(print_num):
        x, y = random.randint(0, width), random.randint(0, height)
        draw.point((x, y), random_color())

    # 随机生成线条
    for i in range(line_num):
        x1, y1 = random.randint(0, width), random.randint(0, height)
        x2, y2 = random.randint(0, width), random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=random_color())

    # 创建一个内存句柄
    f = BytesIO()

    # 将图片保存到内存句柄中
    img.save(f, 'PNG')
    # 读取内存句柄
    data = f.getvalue()
    print(data)
    return (data, vaild_code)


if __name__ == '__main__':
    random_code()
