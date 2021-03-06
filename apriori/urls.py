from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:data_set_id>/', views.show, name='show'),
    path('delete/<int:data_set_id>/', views.delete, name='delete')
]