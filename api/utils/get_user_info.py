import requests
import re

# 乱码问题
# 1: charset="gb2312"时
# 先转二进制(.content) 再解码(decode('gbk'))
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}

# 获取ip地址
def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR') #判断是否用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0] #使用代理获取真实ip
        return ip
    ip = request.META.get('REMOTE_ADDR') # 未使用代理 获取ip
    return ip



# 获取浏览器地址信息
def get_address_info(ip):
    # 判断内网地址 国内三种内网开头
    if ip.startswith('10.') or ip.startswith('192') or ip.startswith('127'):
        return {'prov': '中国','city':'内网'}
    url = f'https://www.ip138.com/iplookup.asp?ip={ip}&action=2'
    res = requests.get(url=url, headers=headers).content.decode('gbk')
    result = re.findall(r'ip_result = (.*?);', res, re.S)[0] #正则获取数据为数组,将数组转为对象
    consequence = eval(result) #转成字典json格式
    addr:dict = consequence['ip_c_list'][0]
    addr.pop('begin')
    addr.pop('end')
    addr.pop('idc')
    addr.pop('net')
    area = addr.get('area')
    if not area:
        addr.pop('area')
    return addr

if __name__ == '__main__':
    get_address_info('117.61.90.38')

