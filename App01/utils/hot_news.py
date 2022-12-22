import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
}

def grt_news():
    url = 'http://www.fengfengzhidao.com/api/news/'
    res = requests.get(url=url,headers=headers,)
    print(res)