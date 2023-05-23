"""
URL configuration for OwnAvito project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ads.views import AdsView, Ad, CatOne, AdDetailView
from ads.views import Cat
urlpatterns = [
    path('admin/', admin.site.urls),
    path('ads/', AdsView.as_view()),
    path('ad/', Cat.as_view()),
    path('cat/', Ad.as_view()),
    path('cat/<int:pk>', CatOne.as_view()),
    path('ad/<int:pk>', AdDetailView.as_view())
]
