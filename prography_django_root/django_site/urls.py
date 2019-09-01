from django.urls import path

from . import views

app_name='posting'
urlpatterns = [
    path('write/save/', views.save_view), #게시글 저장
    path('delete/<int:post_number>/', views.delete_view),
    path('read/<int:post_number>/', views.read_view, name='read'), #매개변수 추가
    path('write/<int:post_number>/', views.write_view), #구분할 수 있나?
    path('write/', views.write_view),
    path('page/<int:page_number>/', views.home_list),
    path('', views.home_list),#, name='index'),
]
# xs-폰 세로, sm-폰 가로, md, lg, xl
# {} 576 {} 768 {} 992 {} 1200 {}
# col-xs-12, col-sm-12, col-md-3, col-lg-3, col-xl-2,