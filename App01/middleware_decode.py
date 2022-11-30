from django.utils.deprecation import MiddlewareMixin
import json


# 解析post请求的数据
class Md1(MiddlewareMixin):
    # 请求中间件
    def process_request(self, request):
        if request.method == 'POST' and request.META.get('CONTENT_TYPE') == 'application/json':
            data = json.loads(request.body)
            request.data = data

    def process_response(self, request, response):
        # print('响应接收之前')
        return response
