from django.urls import path
from . import views

app_name = 'talleres'  # Add this

urlpatterns = [
    path('', views.taller_list, name='taller_list'),  # This URL is mapped to the `show_list` view
    path('<int:taller_id>/', views.taller_details, name= 'taller_details'),
    path('<int:taller_id>/edit/', views.edit_taller, name='edit_taller'),
    path('<int:taller_id>/delete/', views.delete_taller, name='delete_taller'),
    path('add_taller/', views.add_taller, name='add_taller'),
]
