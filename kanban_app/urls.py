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
    path('work/<int:board_id>', views.home_sesh),
    path('new_board', views.create_board),
    path('new_column/<int:board_id>', views.create_column),
    path('new_card/<int:column_id>', views.create_card),
    path('edit_board/<int:board_id>', views.edit_board),
    path('edit_col/<int:column_id>', views.edit_column),
    path('edit_card/<int:card_id>', views.edit_card),
    path('profile/<int:user_id>', views.profile),
    path('profile/<int:user_id>/editabout', views.edit_about),
    path('profile/<int:user_id>/editinfo', views.edit_info),
]