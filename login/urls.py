from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('signup',views.form,name='form'),
    path('signin',views.signin,name='signin'),
    path('<int:user_id>/User',views.userinfo,name='userinfo'),
    path('<int:user_id>/Home',views.home,name='home'),
    path('User',views.signin_user,name='signin_user'),
    path('<int:user_id>/search',views.search,name='search'),
    path('<int:user_id>/predict',views.predict,name='predict'),
    path('<int:user_id>/search/result',views.search_collect,name='search_collect'),
    path('<int:user_id>/predict/result',views.predict_result,name='predict_result'),
    path('<int:user_id>/search/addsearch',views.addsearch,name='addsearch')
]
