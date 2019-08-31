from django.urls import path

from . import views

urlpatterns = [
    path('read/', views.read_view), #매개변수 추가
    path('write/', views.write_view),
    path('', views.home_list),#, name='index'),
]
# xs-폰 세로, sm-폰 가로, md, lg, xl
# {} 576 {} 768 {} 992 {} 1200 {}
# col-xs-12, col-sm-12, col-md-3, col-lg-3, col-xl-2,