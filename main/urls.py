from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('auth', views.auth),
    path('vk', views.vk),
    path('end_reg', views.end_reg),
    path('main', views.main_news),
    path('messages/<int:id>', views.messages),
    path('change_background', views.main_backraund),
    path('notification', views.notification),
    path('mention', views.mention),
    path('settings', views.settings),
    path('wallet', views.wallet),
    path('exchange', views.exchange),
    path('search', views.search),
    path('publications', views.publications),
    path('logout', views.log_out),
    #Принимает параметры
    path('profile/<str:username>', views.profile),
    path('post/<int:id>', views.publicate),
    #path('post/<str:id>', views.post),
    #API

    path('addPost', views.addPost),
    path('api_change_back_photo', views.api_change_back_photo),
    path('addComplain', views.addComplain),
    path('delPost', views.delPost),
    path('addLike', views.addLike),
    path('pin', views.pin),
    path('addhidepost', views.addHidePost),
    path('exchange_show_more', views.ex_show_more),
    path('search_show_more', views.search_show_more),
    path('buy_popup', views.fill_buy_popup),
    path('search_profile', views.search_profile),
    path('publications_show_more', views.publications_show_more),
    path('search_post', views.search_post),
    path('api_save_photo_profile', views.api_save_photo_profile),
    path('change_main_photo', views.change_main_photo),
]
