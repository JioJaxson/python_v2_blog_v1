# PIL 库 安装指令  pip install pillow
from PIL import Image, ImageDraw, ImageFont
import string
import random

# 所有字符 数字+大小写字母
str_all = string.digits + string.ascii_letters

# Image.new(颜色模式, 尺寸, 背景颜色)
img = Image.new('RGB', (200, 40), color=(255, 255, 255))
# 创建画布  以生成的img为背景和大小 生成 画布
draw = ImageDraw.Draw(img)
# 生成字体
font = ImageFont.truetype(font='./font/MexicanTequila.ttf', size=32)
# 书写文字
vaild_code = ''
for i in range(4):
    random_char = random.choice(str_all)
    draw.text((40 * i + 20, 10), random_char, (0, 0, 0), font=font)
    vaild_code += random_char
print(vaild_code)

# 保存img
img.save('new_img.png', 'PNG')
