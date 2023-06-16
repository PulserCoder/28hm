from django.urls import path

from ads import views

urlpatterns = [
    path('', views.AdsListView.as_view()),
    path('<int:pk>/', views.AdsDetailView.as_view()),
    path('create/', views.AdsCreate.as_view()),
    path('<int:pk>/update/', views.AdsUpdateView.as_view()),
    path('<int:pk>/delete/', views.AdsDeleteView.as_view()),
    path('<int:pk>/upload_image/', views.AdsUploadImageView.as_view()),
]