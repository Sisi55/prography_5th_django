from django.urls import path

from . import views

urlpatterns = [
    path('detail/', views.detail_view),
    path('', views.home_list),#, name='index'),
]