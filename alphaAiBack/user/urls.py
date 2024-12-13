# user/urls.py
from django.urls import path
from .views import login,create_new_user, get_all_clients_data,user1,user2

urlpatterns = [
    path('login/',login, name='login'),
    path('add/', create_new_user, name='create_new_user'),
    path('data/', get_all_clients_data, name='get_all_clients_data'),
    path('user1/', user1, name='user1'),
    path('user2/', user2, name='user2'),
]
