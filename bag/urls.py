 # Namespace for the bag app
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'bag'  # Namespace for the bag app

urlpatterns = [
    path('', views.view_bag, name='bag'),
    path('add-to-bag/<str:item_type>/<int:item_id>/', views.add_to_bag, name='add_to_bag'),
    path('adjust/<str:item_key>/', views.adjust_bag, name='adjust_bag'),
    path('remove-item/<str:item_type>/<int:item_id>/', views.remove_bag_item, name='remove_bag_item'),
]
