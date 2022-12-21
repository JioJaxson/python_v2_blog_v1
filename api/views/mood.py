from django.views import View
from django.http import JsonResponse
from api.views.login import clean_form
from django.db.models import F


class AddMoodsView(View):
    def post(self, request):
        data = request.data
        print(data)
        return JsonResponse(data)