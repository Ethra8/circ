from django.urls import path
from . import views

app_name = 'shows'  # Add this

urlpatterns = [
    path('', views.show_list, name='show_list'),  # This URL is mapped to the `show_list` view
    path('<int:show_id>/', views.show_details, name= 'show_details'),
    path('<int:show_id>/edit/', views.edit_show, name='edit_show'), 
]
