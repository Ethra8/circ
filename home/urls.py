from django.contrib import admin
from django.urls import path
from . import views, utils

app_name = 'home'

urlpatterns = [
    path('', views.index, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('search_results/', views.search_results, name='search_results'),  # Search bar view
    path('about/', views.about, name='about'),
    # path('subscribe/', views.subscribe, name='subscribe'),
    # path('companies/', views.companies, name='companies'),
]