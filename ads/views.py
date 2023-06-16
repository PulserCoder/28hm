import json

from django.core.paginator import Paginator
from django.db.models import Count
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from OwnAvito import settings
from ads.models import Category, Ads, User, Location


@method_decorator(csrf_exempt, name="dispatch")
class AdsListView(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.select_related('author').order_by('-price')

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        response = []
        for i in page_obj:
            response.append(model_to_dict(i))

        response = {
            "items": response,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count,
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreate(CreateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category']

    def post(self, request, *args, **kwargs):
        ads_data = json.loads(request.body)
        ads_data['author'] = get_object_or_404(User, pk=ads_data['author'])
        ads_data['category'] = get_object_or_404(Category, pk=ads_data['category'])

        ads = Ads.objects.create(
            **ads_data
        )
        return JsonResponse(model_to_dict(ads), safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'is_published', 'category']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        ads_data = json.loads(request)
        if ads_data['name'] is not None:
            self.object.name = ads_data['name']
        if ads_data['price'] is not None:
            self.object.price = ads_data['price']
        if ads_data['description'] is not None:
            self.object.description = ads_data['description']
        if ads_data['is_published'] is not None:
            self.object.is_published = ads_data['is_published']

        self.object.author = get_object_or_404(User, pk=ads_data['author'])
        self.object.category = get_object_or_404(Category, pk=ads_data['category'])

        self.object.save()

        return JsonResponse(model_to_dict(self.object))


@method_decorator(csrf_exempt, name='dispatch')
class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        return JsonResponse(model_to_dict(self.get_object()))


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        return JsonResponse(model_to_dict(self.get_object()))


@method_decorator(csrf_exempt, name="dispatch")
class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('name')
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        response = []
        for i in page_obj:
            response.append(model_to_dict(i))

        response = {
            "items": response,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count,
        }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)
        ads = Category.objects.create(
            **category_data
        )
        return JsonResponse(model_to_dict(ads), safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "OK"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)

        if category_data['name'] is not None:
            self.object.name = category_data['name']

        self.object.save()

        return JsonResponse(model_to_dict(self.object))


class AdsDeleteView(DeleteView):
    model = Ads
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class UsersDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"}, status=200)


class UsersListView(ListView):
    model = User

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.annotate(total_ads=Count('ads'))
        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        response = []
        for i in page_obj:
            response.append(model_to_dict(i))

        response = {
            "items": response,
            "num_pages": page_obj.paginator.num_pages,
            "total": page_obj.paginator.count,
        }

        return JsonResponse(response, safe=False)


class UsersDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        return JsonResponse(model_to_dict(self.get_object()))


class UserCreateView(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'locations']

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            **user_data
        )
        for location_data in user_data['locations']:
            location, created = Location.objects.get_or_create(
                name=location_data
            )
            user.locations.add(location)
        user.save()

        return JsonResponse(model_to_dict(user), safe=False)


class UserUpdateView(UpdateView):
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)

        if user_data['first_name'] is not None:
            self.object.first_name = user_data['first_name']
        if user_data['last_name'] is not None:
            self.object.last_name = user_data['last_name']
        if user_data['username'] is not None:
            self.object.username = user_data['username']
        if user_data['password'] is not None:
            self.object.password = user_data['password']
        if user_data['role'] is not None:
            self.object.role = user_data['role']
        if user_data['age'] is not None:
            self.object.age = user_data['age']

        for location_data in user_data['locations']:
            location, created = Location.objects.update_or_create(name=location_data)
            self.object.locations.add(location)

        self.object.save()

        return JsonResponse(model_to_dict(self.object))


@method_decorator(csrf_exempt, name='dispatch')
class AdsUploadImageView(UpdateView):
    model = Ads
    fields = ["image"]

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.image = request.FILES.get("image", None)
        self.object.save()

        return JsonResponse(model_to_dict(self.object))
