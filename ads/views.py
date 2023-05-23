import json

from django.forms import model_to_dict
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Categories, Ads


class AdsView(View):
    def get(self, request):
        return JsonResponse({"status": "ok"})


@method_decorator(csrf_exempt, name="dispatch")
class Cat(View):
    def get(self, request):
        ll = Ads.objects.all()
        result = []
        for i in ll:
            result.append(model_to_dict(i))
        return JsonResponse(result, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        print(data)
        ads = Ads.objects.create(**data)
        return JsonResponse(model_to_dict(ads), safe=False)


class CatOne(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        return JsonResponse(model_to_dict(self.get_object()))


class AdDetailView(DetailView):
    model = Categories

    def get(self, request, *args, **kwargs):
        return JsonResponse(model_to_dict(self.get_object()))


@method_decorator(csrf_exempt, name="dispatch")
class Ad(View):
    def get(self, request):
        ll = Categories.objects.all()
        result = []
        for i in ll:
            result.append(model_to_dict(i))
        return JsonResponse(result, safe=False)

    def post(self, request):
        print(123)
        data = json.loads(request.body)
        ads = Categories.objects.create(**data)
        return JsonResponse(model_to_dict(ads), safe=False)
