from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('set_language/', views.set_language, name='set_language'),
    path('home/', views.home, name='home'), 
    path('index/', views.index, name='index'), 
    path('room/', views.room, name='room'),
    path('register/', views.register, name='register'), 
    path('login/', views.login, name='login'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('get_token/', views.getToken), 
    path('create_member/', views.createUser), 
    path('get_member/', views.get_member),
    path('delete_member/', views.deleteMember), 
    path('discussion/', views.discussion, name='discussion'), 
    path('add_post/', views.add_post, name='add_post'), 
    path('notifications/', views.notifications, name="notifications"), 
    path('create_notification/', views.create_notification, name='create_notification')
]
