import requests
# 乱码问题
# 1: charset="gb2312"时
# 先转二进制(.content) 再解码(decode('gbk'))
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
}
def get_address_info(ip):
    url = f'https://www.ip138.com/iplookup.asp?ip={ip}&action=2'
    res = requests.get(url=url, headers=headers).content
    print(res.decode('gbk'))


if __name__ == '__main__':
    get_address_info('117.61.90.38')

