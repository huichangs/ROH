from django.urls import path
from . import views

urlpatterns = [
    path("", views.user, name="user_join"),
    path("<str:room_name>/", views.room, name="room"),
]