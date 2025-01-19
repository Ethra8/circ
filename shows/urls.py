from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_list, name='show_list'),  # This URL is mapped to the `show_list` view
    path('<int:show_id>/', views.show_details, name= 'show_details'),
]
