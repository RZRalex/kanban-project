from django.urls import path
from . import views
urlpatterns = [
    path('', views.landing),
    path('info', views.signup),
    path('new_user', views.register),
    path('complete', views.home),
    path('login', views.reenter),
    path('logout', views.logout),
    path('select', views.select),
    path('work/<int:board_id>', views.home_sesh)
]