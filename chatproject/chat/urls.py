from django.urls import path
from . import views


urlpatterns = [
    path('rooms/', views.Rooms.as_view()),
    path('room/<str:room_name>/', views.Room.as_view()),
]
