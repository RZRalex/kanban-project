from django.urls import path
from . import views
urlpatterns = [
    path('', views.landing),
    path('info', views.signup),
    path('new_user', views.register),
    path('complete', views.home),
    path('login', views.reenter)
]