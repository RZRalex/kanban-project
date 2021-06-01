from django.urls import path
from . import views
urlpatterns = [
    path('', views.bouncer_login)
]